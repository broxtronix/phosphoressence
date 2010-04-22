// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#include <pe/Core/Time.h>
#include <pe/Core/Stopwatch.h>
#include <boost/shared_ptr.hpp>

// -----------------------------------------------------------
// Create a single instance of the Time Struct
// -----------------------------------------------------------

namespace {
  pe::RunOnce pe_time_once = PE_RUNONCE_INIT;
  boost::shared_ptr<pe::PeTime> pe_time_ptr;
  void init_pe_time() {
    pe_time_ptr = boost::shared_ptr<pe::PeTime>(new pe::PeTime());
  }
}

double pe::pe_time() {
  pe_time_once.run( init_pe_time );
  return (*pe_time_ptr)();
}

// ---------------------------------------------------------------------
// PeTime
// ---------------------------------------------------------------------

pe::PeTime::PeTime() {
  m_time = 0;    
  m_last_time = pe::Stopwatch::microtime();
}

double pe::PeTime::operator()() {
  pe::Mutex::Lock lock(m_mutex);
  long long new_time = pe::Stopwatch::microtime();
  m_time += double(new_time - m_last_time) / 1e6;
  m_last_time = new_time;
  return m_time;
}
