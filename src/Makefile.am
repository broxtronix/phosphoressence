# __BEGIN_LICENSE__
# Copyright (C) 2009 Michael J. Broxton
# All Rights Reserved.
# __END_LICENSE__

########################################################################
# sources
########################################################################

bin_PROGRAMS=

header_sources = MainWindow.h GraphicsEngine.h AudioEngine.h	\
		 VideoEngine.h ScriptEngine.h PeParameters.h	\
		 OScopeShape.h SpectrographShape.h Controller.h	\
		 OscController.h JoystickController.h FFT.h

if MAKE_APP_PHOSPHORESSENCE
  bin_PROGRAMS += phosphoressence
  phosphoressence_SOURCES = pe.cc MainWindow.cc MainWindow.moc.cc	\
	            GraphicsEngine.cc GraphicsEngine.moc.cc		\
	            GraphicsElements.cc AudioEngine.cc VideoEngine.cc	\
	            SpectrographShape.moc.cc ScriptEngine.cc		\
	            PeParameters.cc Controller.cc OscController.cc	\
	            JoystickController.cc FFT.cc $(header_sources)
  phosphoressence_LDADD = $(APP_PHOSPHORESSENCE_LIBS) $(PYTHON_EXTRA_LIBS)
endif

AM_CPPFLAGS = @PE_CPPFLAGS@ $(PYTHON_CPPFLAGS) -I/usr/include/SDL -I/usr/local/include/SDL -I./OpenFrameworks/utils
AM_LDFLAGS  = @PE_LDFLAGS@ $(PYTHON_LDFLAGS) $(PYTHON_EXTRA_LDFLAGS) -L/opt/local/lib -lSDL -lboost_system-mt -framework CoreFoundation -framework CoreAudio -framework Cocoa -framework QTKit -framework CoreVideo

SUBDIRS = pe OpenFrameworks

##############################################################################
#                             Tests					     #
##############################################################################

include $(top_srcdir)/config/rules.mak
