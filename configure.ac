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



##################################################
# package checks
##################################################

AX_PKG_PTHREADS

AX_PKG_BOOST
AX_PKG_BOOST_CHECK_VERSION([PE_])

AC_MSG_NOTICE([Stereo will be built using Boost version $BOOST_VERSION])
AX_PKG_BOOST_LIB(PROGRAM_OPTIONS, [-lboost_program_options], [boost/program_options.hpp])

AX_PKG_ONE_OF(BOOST_FILESYSTEM,
    BOOST_FILESYSTEM_PRE_1_35,  [AX_PKG_BOOST_LIB(FILESYSTEM_PRE_1_35,  [-lboost_filesystem], [boost/filesystem/path.hpp])],
    BOOST_FILESYSTEM_POST_1_35, [AX_PKG_BOOST_LIB(FILESYSTEM_POST_1_35, [-lboost_filesystem -lboost_system], [boost/filesystem/path.hpp])])

AX_PKG_BOOST_LIB(THREAD, [-lboost_thread], [boost/thread/thread.hpp])

# This provides an easy way for users to override the threads options
# if they are replacing Boost threads with something else for their platform.
AX_PKG(THREADS, [BOOST_THREAD], [], [])

AX_PKG_ONE_OF(LAPACK,
  APPLE_LAPACK,
    [AX_PKG_APPLE(LAPACK, [], [-framework vecLib])],
  CLAPACK,
    [AX_PKG(CLAPACK, [], [-lclapack -lblas -lf2c], [])],
  SLAPACK,
    [AX_PKG(SLAPACK, [], [-llapack -lblas], [])],
  FLAPACK,
    [AX_PKG(FLAPACK, [], [-llapack -lblas -lgfortran], [])],
  STANDALONE_LAPACK_BLAS,
    [AX_PKG(STANDALONE_BLAS, [], [-lblas], [])
     AX_PKG(STANDALONE_LAPACK, [], [-llapack], [])
     AX_GROUP_PKG(STANDALONE_LAPACK_AND_BLAS, [STANDALONE_LAPACK STANDALONE_BLAS])],
  STANDALONE_FLAPACK_FBLAS,
    [AX_PKG(STANDALONE_F2C, [], [-lf2c], [])
     AX_PKG(STANDALONE_FBLAS, [STANDALONE_F2C], [-lblas], [])
     AX_PKG(STANDALONE_FLAPACK, [STANDALONE_F2C], [-llapack], [])
     AX_GROUP_PKG(STANDALONE_FLAPACK_FBLAS, [STANDALONE_FLAPACK STANDALONE_FBLAS STANDALONE_F2C])])

AX_PKG(VW,                [BOOST], [-lvw],            [vw/Image/ImageView.h vw/Math/LinearAlgebra.h])
AX_PKG(VW_CORE,           [BOOST], [-lvwCore],        [vw/Core/Thread.h])
AX_PKG(VW_IMAGE,          [BOOST], [-lvwImage],       [vw/Image/ImageView.h])
AX_PKG(VW_STEREO,         [BOOST], [-lvwStereo],      [vw/Stereo/OptimizedCorrelator.h])
AX_PKG(VW_CAMERA,         [BOOST], [-lvwCamera],      [vw/Camera/CAHVModel.h])
AX_PKG(VW_CARTOGRAPHY,    [BOOST], [-lvwCartography], [vw/Cartography/GeoReference.h])
AX_PKG(VW_INTEREST_POINT, [BOOST], [-lvwInterestPoint])

AX_PKG(CUDA,              [],      [-lcuda -lcudart], [cuda.h])
AX_PKG(PORTAUDIO,         [],      [-lportaudio], [portaudio.h])
AX_PKG_APPLE(COREMIDI,    [],      [-framework CoreMidi])
AX_PKG(LO,         [],      [-llo], [lo/lo.h])
AX_PKG(V8,         [],      [-lv8], [v8.h])
AX_PKG(SDL,        [],      [-lSDL], [SDL.h])

AX_PKG_ONE_OF(CG,
  APPLE_CG,
    [AX_PKG_APPLE(CG, [], [-framework Cg])],
  LINUX_CG,
    [AX_PKG(LINUX_CG,       [],      [-lCg -lCgGL],     [Cg/cg.h])])

AX_PKG_ONE_OF(GL,
  APPLE_GL,
    [AX_PKG_APPLE([GL], [], [-framework OpenGL -framework GLUT -Wl,-dylib_file,/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib])],
  LINUX_GL,
    [AX_PKG(X11, [], [-lXext -lX11 -lXmu -lXi -lXt], [])
     AX_PKG(LINUX_GL, [X11], [-lGL -lGLU -lglut], [GL/gl.h GL/glu.h GL/glut.h], [])])

# AX_PKG(OPENSCENEGRAPH, [GL], [-losg -losgDB -lOpenThreads -losgViewer -losgText -losgGA -losgFX -losgTerrain -losgUtil], [osg/ref_ptr])
# AX_PKG(SPICE, [], [-lcspice], [SpiceUsr.h SpiceZfc.h])

# Qt with AutoTroll.
AT_WITH_QT([+gui +sql +opengl], [], [], [], [HAVE_PKG_QT_INCLUDE=no])

if test x"$HAVE_PKG_QT_INCLUDE" != x"no"; then
    AT_REQUIRE_QT_VERSION([4.0], [], [HAVE_PKG_QT_INCLUDE=no])
fi

# We seed QT_INCLUDE's cppflags with the ones qmake figured out
PKG_QT_INCLUDE_CPPFLAGS="$PKG_QT_INCLUDE_CPPFLAGS $QT_CPPFLAGS"
AX_PKG(QT_INCLUDE, [], [], [QVector])

AX_PKG_ONE_OF(QT,
    APPLE_QT, [AX_PKG_APPLE(QT, [GL QT_INCLUDE], [$QT_LIBS])],
    LINUX_QT,
     [AX_PKG(QT_LIBS,    [],              [$QT_LIBS], [])
      AX_PKG(QT_OPENGL,  [GL QT_INCLUDE], [],         [QtOpenGL])
      AX_PKG(QT_GUI,     [QT_INCLUDE],    [],         [QLabel])
      AX_PKG(QT_SQL,     [QT_INCLUDE],    [],         [QtSql])
      AX_GROUP_PKG(LINUX_QT, [QT_INCLUDE QT_GUI QT_OPENGL QT_SQL QT_LIBS])])

##################################################
# module definitions
##################################################

AX_GROUP_PKG(BOOST_COMMON, [BOOST BOOST_PROGRAM_OPTIONS])
AX_GROUP_PKG(BOOST_ALL,    [BOOST_COMMON BOOST_FILESYSTEM])
AX_GROUP_PKG(VW_ALL,       [VW VW_CAMERA VW_CARTOGRAPHY VW_STEREO VW_INTEREST_POINT])

AX_APP(PHOSPHORESSENCE,        [src], yes,  [BOOST_THREAD VW_CORE VW_IMAGE QT PORTAUDIO APPLE_COREMIDI LO V8])

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
