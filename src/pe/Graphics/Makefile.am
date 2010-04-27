# __BEGIN_LICENSE__
# Copyright (C) 2006-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__


########################################################################
# sources
########################################################################

if MAKE_MODULE_GRAPHICS

StandardShaders.cc:
	perl StandardShaders.pl
CLEANFILES = StandardShaders.cc

include_HEADERS = Texture.h GpuProgram.h StandardShaders.h Utilities.h BitmapFont.h

libpeGraphics_la_SOURCES = Texture.cc GpuProgram.cc StandardShaders.cc Utilities.cc BitmapFont.cc
libpeGraphics_la_LIBADD = @MODULE_GRAPHICS_LIBS@

lib_LTLIBRARIES = libpeGraphics.la

endif

########################################################################
# general
########################################################################

AM_CPPFLAGS = @PE_CPPFLAGS@ 
AM_LDFLAGS = @PE_LDFLAGS@ -version-info @LIBTOOL_VERSION@

SUBDIRS = .

includedir = $(prefix)/include/pe/Graphics

include $(top_srcdir)/config/rules.mak
