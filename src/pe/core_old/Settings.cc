// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


#include <fstream>

#include <pe/config.h>
#include <pe/core/Thread.h>
#include <pe/core/Cache.h>
#include <pe/core/Settings.h>
#include <pe/core/ConfigParser.h>

// Boost headers
#include <boost/bind.hpp>
#include <boost/thread/xtime.hpp>

// C Standard Library headers ( for stat(2) and getpwuid() )
#include <sys/types.h>
#include <sys/stat.h>
#include <ctime>

#include <pe/config.h>

#ifdef PE_HAVE_UNISTD_H
#include <unistd.h>
#endif

#ifdef PE_HAVE_PWD_H
#include <pwd.h>
#endif

#ifdef WIN32
#define stat _stat
typedef struct _stat struct_stat;
#else
typedef struct stat struct_stat;
#endif

namespace {

  // ---------------------------------------------------
  // Create a single instance of the Settings class
  // ---------------------------------------------------
  pe::RunOnce settings_once = PE_RUNONCE_INIT;
  boost::shared_ptr<pe::Settings> system_settings_ptr;
  void init_system_settings() {
    system_settings_ptr = boost::shared_ptr<pe::Settings>(new pe::Settings());
  }
}

// ---------------------------------------------------
// Settings Methods
// ---------------------------------------------------

// Every m_rc_poll_period seconds, this method polls the
// m_rc_filename to see if it exists and to see if it has been
// recently modified.  If so, we reload the log ruleset from the file.
void pe::Settings::reload_config() {

#if PE_ENABLE_CONFIG_FILE

  // We CANNOT use the pe log infrastructure here, because it will
  // call reload_config and deadlock!

  boost::xtime xt;
  boost::xtime_get(&xt, boost::TIME_UTC);
  bool needs_reloading = false;

  // Every five seconds, we attempt to open the log config file to see
  // if there have been any changes.  The mutex locking for querying
  // the time is handled separately from reading the file so that only
  // one thread takes the performance hit of reading the rc file
  // during any given reload.
  {
    Mutex::Lock time_lock(m_rc_time_mutex);
    if (xt.sec - m_rc_last_polltime > m_rc_poll_period) {
      m_rc_last_polltime = xt.sec;
      needs_reloading = true;
    }
  }

  if (needs_reloading) {
    Mutex::Lock lock(m_rc_file_mutex);

    // Check to see if the file has changed.  If so, re-read the settings.
    struct_stat statbuf;
    if (stat(m_rc_filename.c_str(), &statbuf) != 0)
      return;
#ifdef __APPLE__
    time_t mtime = statbuf.st_mtimespec.tv_sec;
#else // Linux / Windows
    time_t mtime = statbuf.st_mtime;
#endif
    if (mtime > m_rc_last_modification) {
      m_rc_last_modification = mtime;

      // if it throws, let it bubble up.
      parse_config_file(m_rc_filename.c_str(), *this);
    }
  }
#endif
}

void pe::Settings::set_rc_filename(std::string filename) {

  // limit the scope of the lock
  {
    // we grab both locks in the same order that reload_config does.
    Mutex::Lock time_lock(m_rc_time_mutex);
    Mutex::Lock file_lock(m_rc_file_mutex);

    if (filename != m_rc_filename) {
      if (filename.empty()) {
        // Set the last poll time and the last modification time to the death
        // of the universe.  This is a little bit of a hack, but it lets us
        // disable the config file without making the locking in
        // reload_config() even more complex.
        m_rc_last_polltime     = std::numeric_limits<long>::max();
        m_rc_last_modification = std::numeric_limits<long>::max();
      } else {
        m_rc_last_polltime = 0;
        m_rc_last_modification = 0;
      }
      m_rc_filename = filename;
    }
  }

  // Okay, we might have changed the filename. Call reload_config() in order to
  // re-read it. It will grab time_lock and file_lock, so we need to make sure
  // we've released them before we re-read it (or we deadlock).

  reload_config();
}

void pe::Settings::set_rc_poll_period(double period) {

  // limit the scope of the lock
  {
    // we only need the time lock here
    Mutex::Lock time_lock(m_rc_time_mutex);
    m_rc_poll_period = period;
    m_rc_last_polltime = 0;
  }
  reload_config();
}

pe::Settings::Settings() : m_rc_last_polltime(0),
                           m_rc_last_modification(0),
                           m_rc_poll_period(5.0) {
  std::string homedir;
#ifdef PE_HAVE_GETPWUID
  struct passwd *pw;
  pw = getpwuid( getuid() );
  homedir = pw->pw_dir;
#endif
  if (homedir.empty())
      homedir = getenv("HOME");
  m_rc_filename = homedir + "/.perc";

  // Set defaults
  m_default_num_threads = PE_NUM_THREADS;
  m_system_cache_size = 1024 * 1024 * 1024;   // Default cache size is 1024-MB
  m_default_tile_size = 1024;
  m_tmp_directory = "/tmp";

  // By default, the .perc file has precedence, but the user can
  // override these settings by explicitly changing them using the
  // system_settings() API.
  m_default_num_threads_override = false;
  m_system_cache_size_override = false;
  m_default_tile_size_override = false;
  m_tmp_directory_override = false;
}

pe::Settings& pe::pe_settings() {
  settings_once.run( init_system_settings );
  return *system_settings_ptr;
}


// -----------------------------------------------------------------
//                        Settings API
// -----------------------------------------------------------------

int pe::Settings::default_num_threads() {
  if (!m_default_num_threads_override)
    reload_config();
  Mutex::Lock lock(m_settings_mutex);
  return m_default_num_threads;
}

void pe::Settings::set_default_num_threads(unsigned num) {

  { // Used to contain the lock from reload_config()
    Mutex::Lock lock(m_settings_mutex);
    if ( num == 0 ) {
      // Reset state
      m_default_num_threads_override = false;
    } else {
      m_default_num_threads_override = true;
      m_default_num_threads = num;
    }
  } 

  if ( num == 0 )
    reload_config();
}

size_t pe::Settings::system_cache_size() {
  if (!m_system_cache_size_override)
    reload_config();
  Mutex::Lock lock(m_settings_mutex);
  return m_system_cache_size;
}

void pe::Settings::set_system_cache_size(size_t size) {
  {
    Mutex::Lock lock(m_settings_mutex);
    m_system_cache_size_override = true;
    m_system_cache_size = size;
  }
  pe_system_cache().resize(size);
}

int pe::Settings::default_tile_size() { 
  if (!m_default_tile_size_override)
    reload_config();
  Mutex::Lock lock(m_settings_mutex);
  return m_default_tile_size;
}

void pe::Settings::set_default_tile_size(int num) {
  Mutex::Lock lock(m_settings_mutex);
  m_default_tile_size_override = true;
  m_default_tile_size = num;
}

std::string pe::Settings::tmp_directory() { 
  if (!m_tmp_directory_override)
    reload_config();
  Mutex::Lock lock(m_settings_mutex);
  return m_tmp_directory;
}

void pe::Settings::set_tmp_directory(std::string const& path) {
  Mutex::Lock lock(m_settings_mutex);
  m_tmp_directory_override = true;
  m_tmp_directory = path;
}
