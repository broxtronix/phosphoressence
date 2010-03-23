# __BEGIN_LICENSE__
# Copyright (C) 2009 Michael J. Broxton
# All Rights Reserved.
# __END_LICENSE__

########################################################################
# sources
########################################################################

libOpenFrameworks_la_SOURCES = utils/ofUtils.cpp utils/ofMath.cpp
libOpenFrameworks_la_LIBADD = $(APP_PHOSPHORESSENCE_LIBS)

lib_LTLIBRARIES = libOpenFrameworks.la

AM_CPPFLAGS = @PE_CPPFLAGS@ -I./utils -I./image
AM_LDFLAGS  = @PE_LDFLAGS@ $(PYTHON_EXTRA_LDFLAGS)

EXTRA_DIST = Doxyfile test/Helpers.h

########################################################################
# general
########################################################################

include $(top_srcdir)/config/rules.mak
