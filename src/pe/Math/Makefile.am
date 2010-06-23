# __BEGIN_LICENSE__
# Copyright (C) 2006-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__


########################################################################
# sources
########################################################################

if MAKE_MODULE_MATH

include_HEADERS = Functors.h Vector.h Matrix.h BBox.h

libpeMath_la_SOURCES = 
libpeMath_la_LIBADD = @MODULE_MATH_LIBS@

lib_LTLIBRARIES = libpeMath.la

endif

########################################################################
# general
########################################################################

AM_CPPFLAGS = @MODULE_MATH_CPPFLAGS@ @PKG_BOOST_CPPFLAGS@ -I../../
AM_LDFLAGS = @PE_LDFLAGS@ -version-info @LIBTOOL_VERSION@

SUBDIRS = .

includedir = $(prefix)/include/pe/Math

include $(top_srcdir)/config/rules.mak
