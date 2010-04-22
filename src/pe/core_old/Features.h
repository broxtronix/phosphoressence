// __BEGIN_LICENSE__
// Copyright (C) 2006-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__

// This file contains some useful macros and definitions so they don't get
// scattered everywhere.

#ifndef __PE_CORE_MACRO_H__
#define __PE_CORE_MACRO_H__

#include <pe/config.h>

#if defined(PE_COMPILER_HAS_ATTRIBUTE_DEPRECATED) && (PE_COMPILER_HAS_ATTRIBUTE_DEPRECATED==1)
#define PE_DEPRECATED __attribute__((deprecated))
#else
#define PE_DEPRECATED
#endif

#if defined(PE_COMPILER_HAS_ATTRIBUTE_NORETURN) && (PE_COMPILER_HAS_ATTRIBUTE_NORETURN==1)
#define PE_NORETURN __attribute__((noreturn))
#else
#define PE_NORETURN
#endif

/// The master compile-time debugging level flag.  The default value
/// for PE_DEBUG_LEVEL is guessed based on whether or not NDEBUG
/// is defined if the user has not specified it explicitly.
#ifndef PE_DEBUG_LEVEL
#ifdef NDEBUG
#define PE_DEBUG_LEVEL 0
#else
#define PE_DEBUG_LEVEL 1
#endif
#endif

/// A quick macro for selectively disabling code in non-debug builds.
#if PE_DEBUG_LEVEL == 0
#define PE_DEBUG(x)
#else
#define PE_DEBUG(x) x
#endif

#endif
