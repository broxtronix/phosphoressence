# __BEGIN_LICENSE__
# Copyright (C) 2006-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__


########################################################################
# sources
########################################################################

if MAKE_MODULE_VIDEO

include_HEADERS = QtKitVideoGrabber.h

libpeVideo_la_SOURCES = QtKitVideoGrabber.m
libpeVideo_la_LIBADD = @MODULE_VIDEO_LIBS@

lib_LTLIBRARIES = libpeVideo.la

endif

# Hack to get objective C code to compile as Objective C++
AM_OBJCFLAGS = -x objective-c++

########################################################################
# general
########################################################################

AM_CPPFLAGS = @PE_CPPFLAGS@ 
AM_LDFLAGS = @PE_LDFLAGS@ -version-info @LIBTOOL_VERSION@

SUBDIRS = .

includedir = $(prefix)/include/pe/video

include $(top_srcdir)/config/rules.mak
