# __BEGIN_LICENSE__
# Copyright (C) 2006-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__


########################################################################
# sources
########################################################################

if MAKE_MODULE_CORE

include_HEADERS = Exception.h Debugging.h Thread.h Stopwatch.h Log.h	\
		  Time.h Features.h Settings.h ConfigParser.h Cache.h	\
		  VarArray.h Functors.h TypeDeduction.h			\
		  FundamentalTypes.h CompoundTypes.h Random.h

libpeCore_la_SOURCES = Debugging.cc Exception.cc Thread.cc Time.cc	\
		       Stopwatch.cc Log.cc Settings.cc ConfigParser.cc	\
		       Cache.cc Random.cc
libpeCore_la_LIBADD = @MODULE_CORE_LIBS@

lib_LTLIBRARIES = libpeCore.la

endif

########################################################################
# general
########################################################################

AM_CPPFLAGS = @MODULE_CORE_CPPFLAGS@ @PKG_BOOST_CPPFLAGS@ -I../../
AM_LDFLAGS = @PE_LDFLAGS@ -version-info @LIBTOOL_VERSION@

SUBDIRS = .

includedir = $(prefix)/include/pe/Core

include $(top_srcdir)/config/rules.mak
