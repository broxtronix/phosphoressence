# __BEGIN_LICENSE__
# Copyright (C) 2006-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__


########################################################################
# sources
########################################################################

if MAKE_MODULE_GRAPHICS

include_HEADERS = Texture.h

libpeGraphics_la_SOURCES = Texture.cc
libpeGraphics_la_LIBADD = @MODULE_GRAPHICS_LIBS@

lib_LTLIBRARIES = libpeGraphics.la

endif

########################################################################
# general
########################################################################

AM_CPPFLAGS = @PE_CPPFLAGS@ 
AM_LDFLAGS = @PE_LDFLAGS@ -version-info @LIBTOOL_VERSION@

SUBDIRS = .

includedir = $(prefix)/include/pe/graphics

include $(top_srcdir)/config/rules.mak
