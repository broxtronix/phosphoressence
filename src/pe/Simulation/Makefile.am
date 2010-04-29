# __BEGIN_LICENSE__
# Copyright (C) 2006-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__


########################################################################
# sources
########################################################################

if MAKE_MODULE_SIMULATION

include_HEADERS = FluidDynamics.h

libpeSimulation_la_SOURCES = FluidDynamics.cc
libpeSimulation_la_LIBADD = @MODULE_SIMULATION_LIBS@

lib_LTLIBRARIES = libpeSimulation.la

endif

########################################################################
# general
########################################################################

AM_CPPFLAGS = @PE_CPPFLAGS@ @PKG_BOOST_CPPFLAGS@ -I../../
AM_LDFLAGS = @PE_LDFLAGS@ -version-info @LIBTOOL_VERSION@

SUBDIRS = .

includedir = $(prefix)/include/pe/Simulation

include $(top_srcdir)/config/rules.mak
