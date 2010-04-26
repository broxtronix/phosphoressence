# __BEGIN_LICENSE__
# Copyright (C) 2009 Michael J. Broxton
# All Rights Reserved.
# __END_LICENSE__

########################################################################
# sources
########################################################################

if MAKE_MODULE_CORE
core_subdirs = Core
core_headers = Core.h
endif

if MAKE_MODULE_MATH
math_subdirs = Math
math_headers = Math.h
endif

if MAKE_MODULE_GRAPHICS
graphics_subdirs = Graphics
graphics_headers = Graphics.h
endif

if MAKE_MODULE_VIDEO
video_subdirs = Video
video_headers = Video.h
endif

if MAKE_MODULE_SIMULATION
simulation_subdirs = Simulation
simulation_headers = Simulation.h
endif

if MAKE_MODULE_VISION
vision_subdirs = Vision
vision_headers = Vision.h
endif

include_HEADERS = $(core_headers) $(math_headers) $(video_headers)	\
		  $(graphics_headers) $(simulation_headers) $(vision_headers)

SUBDIRS = $(core_subdirs) $(math_subdirs) $(graphics_subdirs)	\
          $(video_subdirs) $(simulation_subdirs) $(vision_subdirs) .

CLEANFILES = config.h.pre.in~

########################################################################
# general
########################################################################

includedir = $(prefix)/include/pe

include $(top_srcdir)/config/rules.mak
