# __BEGIN_LICENSE__
# Copyright (C) 2009 Michael J. Broxton
# All Rights Reserved.
# __END_LICENSE__

##################################################
# A few starting bits
##################################################

dnl TODO BEFORE RELEASE: update package version
AC_INIT([PhosphorEssence], [0.2], [], [PhosphorEssence])
AC_CONFIG_AUX_DIR(config)
AC_CONFIG_MACRO_DIR([m4])
AC_CANONICAL_HOST
AM_INIT_AUTOMAKE([nostdinc])
AX_CONFIG_HEADER_PREFIX([src/pe_config.h], [PE_])

dnl TODO BEFORE RELEASE: update libtool version
dnl if abi changes in any way:
dnl     current++
dnl     revision=0
dnl     if new abi is backward-compatible:
dnl         age += 1
dnl     else:
dnl         age = 0
dnl else:
dnl     revision++
dnl (see http://sources.redhat.com/autobook/autobook/autobook_91.html)
dnl
dnl LIBTOOL_VERSION=current:revision:age
LIBTOOL_VERSION=1:0:0
AC_SUBST(LIBTOOL_VERSION)

# This should be first, so everything else can use it
AX_ARG_ENABLE(verbose, no, [none], [verbose configuration output])

# load the config.options
if test -f config.options; then
  if test "yes" = "$ENABLE_VERBOSE" ; then
    AC_MSG_NOTICE([sourcing config.options])
    cat config.options
  fi
  source config.options
fi



##################################################
# Find the necessary programs
##################################################

# Make sure these are set so AC_PROG_CC doesn't initialize them with
# its defaults, since we take care of setting debug and optimization
# levels ourselves.
CFLAGS="$CFLAGS"
CXXFLAGS="$CXXFLAGS"

# Find the tools
AC_PROG_CC
AC_PROG_CXX
AC_PROG_INSTALL
AX_PROG_AR
AC_PROG_LIBTOOL
AC_PROG_MAKE_SET
AC_LANG(C++)
AX_COMMON_OPTIONS

# Look for the python stuff
AM_PATH_PYTHON([2.4], [HAVE_PYTHON=yes], [HAVE_PYTHON=no])
AC_PYTHON_DEVEL([HAVE_PYTHON=yes], [HAVE_PYTHON=no])
AC_SUBST(HAVE_PYTHON)

##################################################
# package checks
##################################################

AX_PKG_PTHREADS

AX_PKG_BOOST
if test x"$HAVE_PKG_BOOST" == "xyes"; then
  AX_PKG_BOOST_CHECK_VERSION([PE_])
  AC_MSG_NOTICE([PE will be built using Boost version $BOOST_VERSION])

  AX_PKG_BOOST_LIB(PROGRAM_OPTIONS, [-lboost_program_options], [boost/program_options.hpp])
  AX_PKG_BOOST_LIB(SYSTEM,          [-lboost_system],          [boost/system/error_code.hpp])
  AX_PKG_BOOST_LIB(FILESYSTEM,      [-lboost_filesystem],      [boost/filesystem/path.hpp], [$PKG_BOOST_SYSTEM_LIBS])
  AX_PKG_BOOST_LIB(THREAD,          [-lboost_thread],          [boost/thread/thread.hpp])
  AX_PKG_BOOST_LIB(IOSTREAMS,       [-lboost_iostreams],       [boost/iostreams/stream_buffer.hpp])
fi

# This provides an easy way for users to override the threads options
# if they are replacing Boost threads with something else for their platform.
AX_PKG(THREADS,           [BOOST_THREAD], [], [])
AX_PKG(VW_CORE,           [BOOST], [-lvwCore],        [vw/Core/Thread.h])

AX_PKG(CUDA,              [],      [-lcuda -lcudart], [cuda.h])
AX_PKG(PORTAUDIO,         [],      [-lportaudio], [portaudio.h])
AX_PKG_APPLE(COREMIDI,    [],      [-framework CoreMidi])
AX_PKG_APPLE(COREAUDIO,   [],      [-framework CoreAudio])
AX_PKG(RTAUDIO,           [APPLE_COREAUDIO],      [-lrtaudio], [RtAudio.h])
AX_PKG(LO,                [],      [-llo], [lo/lo.h])
AX_PKG(SDL,               [],      [-lSDL], [SDL.h])

AX_PKG_ONE_OF(GL,
  APPLE_GL,
    [AX_PKG_APPLE([GL], [], [-framework OpenGL -framework GLUT -Wl,-dylib_file,/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib])],
  LINUX_GL,
    [AX_PKG(X11, [], [-lXext -lX11 -lXmu -lXi -lXt], [])
     AX_PKG(LINUX_GL, [X11], [-lGL -lGLU -lglut], [GL/gl.h GL/glu.h GL/glut.h], [])])

AX_PKG(OPENVG,        [GL],      [-lOpenVG], [vg/openvg.h])

# Qt with AutoTroll.
AT_WITH_QT([+gui +sql +opengl], [], [], [HAVE_PKG_QT_BASE="no:missing QT"], [])

if test x"$HAVE_PKG_QT_BASE" != x"no:missing QT"; then
    AT_REQUIRE_QT_VERSION([4.0], [HAVE_PKG_QT_BASE="no:wrong QT version"], [])
fi

# We seed QT_BASE's cppflags and libs with the ones qmake figured out
PKG_QT_BASE_CPPFLAGS="$PKG_QT_BASE_CPPFLAGS $QT_CPPFLAGS"
AX_PKG(QT_BASE, [], [$QT_LIBS], [QVector])

AX_PKG_ONE_OF(QT,
    APPLE_QT, [AX_PKG_APPLE(QT, [GL QT_BASE], [])],
    LINUX_QT,
     [AX_PKG(QT_OPENGL,  [QT_BASE], [], [QtOpenGL])
      AX_PKG(QT_GUI,     [QT_BASE], [], [QLabel])
      AX_PKG(QT_SQL,     [QT_BASE], [], [QtSql])
      AX_GROUP_PKG(LINUX_QT, [QT_BASE QT_GUI QT_OPENGL QT_SQL])])

##################################################
# module definitions
##################################################

AX_GROUP_PKG(BOOST_COMMON, [BOOST BOOST_PROGRAM_OPTIONS])
AX_GROUP_PKG(BOOST_ALL,    [BOOST_COMMON BOOST_FILESYSTEM])

AX_APP(PHOSPHORESSENCE,        [src], yes,  [BOOST_THREAD VW_CORE QT RTAUDIO LO OPENVG])

# These are here (instead of inside the APP macro where they belong)
# for backwards compatability with older versions of automake.
AM_CONDITIONAL(MAKE_APP_PHOSPHORESSENCE, [test "$MAKE_APP_PHOSPHORESSENCE" = "yes"])

##################################################
# final processing
##################################################

PE_CPPFLAGS="-I\${top_srcdir}/src $OTHER_CPPFLAGS"
PE_LDFLAGS="$OTHER_LDFLAGS"

if test "yes" = "$ENABLE_VERBOSE" ; then
  AC_MSG_NOTICE([using CPPFLAGS=$CPPFLAGS])
  AC_MSG_NOTICE([using PE_CPPFLAGS=$PE_CPPFLAGS])
  AC_MSG_NOTICE([using CFLAGS=$CFLAGS])
  AC_MSG_NOTICE([using CXXFLAGS=$CXXFLAGS])
  AC_MSG_NOTICE([using LDFLAGS=$LDFLAGS])
  AC_MSG_NOTICE([using PE_LDFLAGS=$PE_LDFLAGS])
  AC_MSG_NOTICE([using PE_ENABLE_EXCEPTIONS=$ENABLE_EXCEPTIONS])
fi

AC_SUBST(PE_CPPFLAGS)
AC_SUBST(PE_LDFLAGS)



##################################################
# makefiles to process
##################################################

AC_CONFIG_FILES([                       \
  Makefile                              \
  src/Makefile                          \
])

AC_OUTPUT
