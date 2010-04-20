# __BEGIN_LICENSE__
# Copyright (C) 2009 Michael J. Broxton
# All Rights Reserved.
# __END_LICENSE__

########################################################################
# sources
########################################################################

if MAKE_MODULE_VIDEO
video_subdirs = Video
video_headers = Video.h
endif

include_HEADERS = $(video_headers) pe.h config.h

SUBDIRS = $(video_subdirs) .

CLEANFILES = config.h.pre.in~

########################################################################
# general
########################################################################

includedir = $(prefix)/include/pe

include $(top_srcdir)/config/rules.mak
