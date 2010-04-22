// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__


/// \file Core/Debugging.cc
/// 
/// Types and functions to assist in debugging code.
///
#include <pe/Core/Debugging.h>

#include <iostream>

#ifdef WIN32
#include <Windows.h>
#endif

pe::Timer::Timer( std::string const& desc, MessageLevel level, std::string const& log_namespace )
  : m_desc(desc), m_level(level), m_log_namespace(log_namespace) {
#ifdef WIN32
  LARGE_INTEGER begin;
  QueryPerformanceCounter( &begin );
  m_begin= begin.QuadPart;
#else
  gettimeofday( &m_begin, 0 );
#endif
}

pe::Timer::~Timer() {
#ifdef WIN32
  LARGE_INTEGER end, freq;
  QueryPerformanceCounter( &end );
  QueryPerformanceFrequency( &freq );
  double duration = (end.QuadPart - m_begin)/(double)freq.QuadPart;
#else
  timeval end;
  gettimeofday( &end, 0 );
  double duration = end.tv_sec - m_begin.tv_sec;
  duration += (end.tv_usec - m_begin.tv_usec)/1.0e6;
#endif
  pe_out(m_level, m_log_namespace) << m_desc << ": " << duration << std::endl;
}
