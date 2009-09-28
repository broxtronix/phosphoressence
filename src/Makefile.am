# __BEGIN_LICENSE__
# Copyright (C) 2009 Michael J. Broxton
# All Rights Reserved.
# __END_LICENSE__

########################################################################
# sources
########################################################################

StandardShaders.cc:
	perl StandardShaders.pl

CLEANFILES = StandardShaders.cc *.moc.cc

bin_PROGRAMS=

header_sources = MainWindow.h GraphicsEngine.h AudioEngine.h		\
		 ScriptEngine.h PeParameters.h OScopeShape.h		\
		 SpectrographShape.h Controller.h OscController.h	\
		 JoystickController.h FFT.h

gpu_module_sources = GpuProgram.h GpuProgram.cc Utilities.cc		\
		     Utilities.h StandardShaders.h StandardShaders.h	\
		     StandardShaders.cc

if MAKE_APP_PHOSPHORESSENCE
  bin_PROGRAMS += pe
  pe_SOURCES = pe.cc MainWindow.cc MainWindow.moc.cc GraphicsEngine.cc	\
	            GraphicsEngine.moc.cc GraphicsElements.cc		\
	            AudioEngine.cc AudioEngine.moc.cc			\
	            SpectrographShape.moc.cc ScriptEngine.cc		\
	            PeParameters.cc Controller.cc OscController.cc	\
	            JoystickController.cc FFT.cc $(gpu_module_sources)	\
	            $(header_sources)

  pe_LDADD = $(APP_PHOSPHORESSENCE_LIBS) $(PYTHON_EXTRA_LIBS)
endif

AM_CPPFLAGS = @PE_CPPFLAGS@ $(PYTHON_CPPFLAGS) -I/Users/mbroxton/local/include -I/Users/mbroxton/local/include/SDL
AM_LDFLAGS  = @PE_LDFLAGS@ $(PYTHON_LDFLAGS) $(PYTHON_EXTRA_LDFLAGS) -L/opt/local/lib -lSDL -lboost_system-mt -framework CoreFoundation

##############################################################################
#                             Tests					     #
##############################################################################

include $(top_srcdir)/config/rules.mak
