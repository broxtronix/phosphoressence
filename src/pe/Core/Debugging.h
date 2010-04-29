// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


/// \file Core/Debugging.h
/// 
/// Types and functions to assist in debugging code.
///
#ifndef __PE_CORE_DEBUGGING_H__
#define __PE_CORE_DEBUGGING_H__

#include <pe/Core/Log.h>
#include <pe/Core/Features.h>

#ifndef WIN32
#include <sys/time.h>
#endif

#include <ostream>
#include <string>

namespace pe {


  // *******************************************************************
  // Timing types and functions
  // *******************************************************************

  class Timer {
    std::string m_desc;
    MessageLevel m_level;
    std::string m_log_namespace;
#ifdef WIN32
    __int64 m_begin;
#else
    timeval m_begin;
#endif
  public:
    Timer( std::string const& desc, MessageLevel level=InfoMessage, std::string const& log_namespace = "console" );

    ~Timer();
  };


} // namespace pe

#endif  // __PE_CORE_DEBUGGING_H__
