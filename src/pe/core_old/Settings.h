// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


/// \file Core/Settings.h
///
/// This file provides a singleton object that provides access to
/// Vision Workbench system-wide settings.  These can be twiddled
/// programmatically by interacting with this object, or they can be
/// set using the ~/.perc file in the user's home directory.  That
/// file is reloaded on every call to access settings, so the user can
/// modify the contents of that file in real time as the program is
/// running.

#ifndef __PE_CORE_SETTINGS_H__
#define __PE_CORE_SETTINGS_H__

#include <vector>

#include <pe/Core/Thread.h>

namespace pe {

  // -------------------------------------------------------
  //                    Settings
  // -------------------------------------------------------

  /// The system settings class manages runtime configuration for the
  /// Vision Workbench.
  ///
  /// Important Note: You should access the system settings using the
  /// static pe_settings() function below, which returns a singleton
  /// instance of the system settings class.  You should _not_ need to
  /// create a settings object yourself!!!!
  class Settings {

    // Vision Workbench Global Settings
    int m_default_num_threads;
    bool m_default_num_threads_override;
    size_t m_system_cache_size;
    bool m_system_cache_size_override;
    int m_default_tile_size;
    bool m_default_tile_size_override;
    std::string m_tmp_directory;
    bool m_tmp_directory_override;

    // Member variables assoc. with periodically polling the log
    // configuration (logconf) file.
    long m_rc_last_polltime;
    long m_rc_last_modification;
    std::string m_rc_filename;
    double m_rc_poll_period;
    Mutex m_rc_time_mutex;
    Mutex m_rc_file_mutex;
    Mutex m_settings_mutex;

    // Ensure non-copyable semantics
    Settings( Settings const& );
    Settings& operator=( Settings const& );

  public:

    /// You should not create an instance of Settings on your own
    /// using this constructor.  Instead, you can access a global
    /// instance of the settings class using the static
    /// pe_settings() method below.
    Settings();

    /// Change the rc filename (default: ~/.perc)
    void set_rc_filename(std::string filename);

    /// Change the rc file poll period.  (default: 5 seconds)
    /// Note -- this sets the *minimum* poll time for the file.  The
    /// actual file is only polled when a setting is requested.
    void set_rc_poll_period(double period);

    // -----------------------------------------------------------------
    //                        Settings API
    // -----------------------------------------------------------------

    // Reload the config. When this returns, the config will be reloaded.
    // It may happen in a different thread than requested, however.
    void reload_config();

    /// Query for the default number of threads used in block
    /// processing operations.
    int default_num_threads();

    /// Set the default number of threads used in block processing
    /// operations.
    void set_default_num_threads(unsigned num = 0);

    /// Query for the current system cache size.  Result is given in
    /// units of bytes.
    size_t system_cache_size();

    /// Set the current system cache size.  'size' should be in units
    /// of bytes.  The system cache is shared by all
    /// BlockRasterizeView<>'s, including DiskImageView<>'s.
    void set_system_cache_size(size_t size);

    /// Query for the default tile size used for block processing ops.
    int default_tile_size();
    
    /// Set the default tile size to be used for block processing.
    void set_default_tile_size(int num);

    /// Query for the directory being used to store temporary files.
    std::string tmp_directory();
    
    /// Set the directory to be used for storing temporary files.
    void set_tmp_directory(std::string const& path);
  };

  /// Static method to access the singleton instance of the system
  /// settings.  You should *always* use this method if you want to
  /// access Vision Workbench system log, where all Vision Workbench
  /// log messages go.
  ///
  /// For example:
  ///
  ///     pe_settings().set_system_cache_size(2048)
  ///
  Settings& pe_settings();

} // namespace pe

#endif // __PE_CORE_SETTINGS_H__
