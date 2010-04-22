// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

#ifndef __PE_CORE_TIME__
#define __PE_CORE_TIME__

#include <pe/Core/Thread.h>

namespace pe {

  // ---------------------------------------------------------------------
  // PeTime
  // ---------------------------------------------------------------------

  class PeTime {
    float m_time;
    long long m_last_time;
    pe::Mutex m_mutex;

  public:
    PeTime();
    double operator()();
  };

  /// Return the singleton instance of the PhosphorEssence time
  /// structure.  The time struct is created the first time this method
  /// is invoked and initialized to time = 0.  You should *always* access
  /// the time using this function.
  double pe_time();

} // namespace pe

#endif
