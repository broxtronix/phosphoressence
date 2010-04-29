# __BEGIN_LICENSE__
# Copyright (C) 2006-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__


########################################################################
# sources
########################################################################

if MAKE_MODULE_VISION

include_HEADERS = Blob.h ContourFinder.h BlobTracker.h

libpeVision_la_SOURCES = ContourFinder.cc Blob.cc BlobTracker.cc
libpeVision_la_LIBADD = @MODULE_VISION_LIBS@

lib_LTLIBRARIES = libpeVision.la

endif

########################################################################
# general
########################################################################

AM_CPPFLAGS = @PE_CPPFLAGS@ 
AM_LDFLAGS = @PE_LDFLAGS@ -version-info @LIBTOOL_VERSION@

SUBDIRS = .

includedir = $(prefix)/include/pe/Vision

include $(top_srcdir)/config/rules.mak
