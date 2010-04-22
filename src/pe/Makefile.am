# __BEGIN_LICENSE__
# Copyright (C) 2009 Michael J. Broxton
# All Rights Reserved.
# __END_LICENSE__

########################################################################
# sources
########################################################################

if MAKE_MODULE_CORE
core_subdirs = core
core_headers = Core.h
endif

if MAKE_MODULE_GRAPHICS
graphics_subdirs = graphics
graphics_headers = Graphics.h
endif

if MAKE_MODULE_VIDEO
video_subdirs = video
video_headers = Video.h
endif

if MAKE_MODULE_SIMULATION
simulation_subdirs = simulation
simulation_headers = Simulation.h
endif

include_HEADERS = $(core_headers) $(video_headers) $(graphics_headers) $(simulation_headers)

SUBDIRS = $(core_subdirs) $(graphics_subdirs) $(video_subdirs) $(simulation_subdirs) .

CLEANFILES = config.h.pre.in~

########################################################################
# general
########################################################################

includedir = $(prefix)/include/pe

include $(top_srcdir)/config/rules.mak
