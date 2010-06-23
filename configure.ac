# __BEGIN_LICENSE__
# Copyright (C) 2009 Michael J. Broxton
# All Rights Reserved.
# __END_LICENSE__

m4_pattern_forbid([^AX_])
m4_pattern_allow([^AX_CFLAGS$])
m4_pattern_allow([^AX_INCLUDE_DIR$])
m4_pattern_allow([^AX_LIBDIR$])
m4_pattern_allow([^AX_OTHER_LIBDIR$])
m4_pattern_allow([^PKG_[A-Z_]+_CPPFLAGS$])
m4_pattern_allow([^PKG_[A-Z_]+_LDFLAGS$])
m4_pattern_allow([^PKG_[A-Z_]+_LIBS$])
m4_pattern_allow([^PKG_PATHS$])
m4_pattern_allow([^PKG_PATHS_[A-Z_]+$])
m4_pattern_allow([^PKG_BOOST_INCDIR$])
m4_pattern_allow([^PKG_BOOST_LIBDIR$])
m4_pattern_allow([^PKG_PE_LIBS_TEMP$])
m4_pattern_allow([^PKG_ARBITRARY_QT_NEEDED_HEADERS$])

##################################################
# A few starting bits
##################################################

AC_PREREQ([2.59])
dnl TODO BEFORE RELEASE: update package version
AC_INIT([PhosphorEssence], [0.3], [], [PhosphorEssence])
AC_CONFIG_AUX_DIR(config)
AC_CONFIG_MACRO_DIR([m4])
AC_CANONICAL_HOST
AM_INIT_AUTOMAKE([nostdinc 1.8.5])
AX_CONFIG_HEADER_PREFIX([src/pe/config.h], [PE_])

dnl Fix for early autoconf that doesn't export these
AC_SUBST([abs_top_srcdir])
AC_SUBST([abs_top_builddir])

m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])

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

m4_divert_text([INIT_PREPARE], [dnl
# load the config.options
if test -f ./config.options; then
  AX_LOG([using config.options << EOF])
  AX_LOG([`cat ./config.options`])
  AX_LOG([EOF])
  . ./config.options
fi
])


##################################################
# Find the necessary programs
##################################################

# Make sure these are set so AC_PROG_CC doesn't initialize them with
# its defaults, since we take care of setting debug and optimization
# levels ourselves.
CFLAGS="$CFLAGS"
CXXFLAGS="$CXXFLAGS"

# Disable static libraries by default
AM_DISABLE_STATIC

# Find the tools
AC_PROG_CC
AC_PROG_CXX
AC_PROG_OBJC
AC_PROG_INSTALL
AX_PROG_AR
AC_PROG_LIBTOOL
AC_PROG_MAKE_SET
AC_LANG(C++)
AX_COMMON_OPTIONS

# Looking for posix headers
AC_CHECK_HEADERS([unistd.h pwd.h])
AC_CHECK_FUNCS([getpwuid getpid])

# Look for the python stuff
AM_PATH_PYTHON([2.4], [HAVE_PYTHON=yes], [HAVE_PYTHON=no])
AC_PYTHON_DEVEL([HAVE_PYTHON=yes], [HAVE_PYTHON=no])
AC_SUBST(HAVE_PYTHON)

# For the moment this is just a manual switch, defaulting to off.
# Someday this should be sensibly autodetected.
AX_ARG_ENABLE(sse,           no,  [am-yes cpp-bool], [enable SSE optimizations in some places (development)])
AX_ARG_ENABLE(qt-qmake,      yes, [none],            [Allow qmake detection of QT])

##################################################
# package checks
##################################################

AX_PKG_PTHREADS

AX_PKG_BOOST([BOOST_PROGRAM_OPTIONS BOOST_FILESYSTEM BOOST_THREAD BOOST_GRAPH],
  BOOST_PROGRAM_OPTIONS,
    [AX_PKG_BOOST_LIB(PROGRAM_OPTIONS, [-lboost_program_options], [boost/program_options.hpp], [boost::program_options::options_description("Rawr");])],
  BOOST_SYSTEM,
    [AX_PKG_BOOST_LIB(SYSTEM,          [-lboost_system],          [boost/system/error_code.hpp], [boost::system::error_code();])],
  BOOST_FILESYSTEM,
    [AX_PKG_BOOST_LIB(FILESYSTEM,      [-lboost_filesystem],      [boost/filesystem/path.hpp], [boost::filesystem::path();], [$PKG_BOOST_SYSTEM_LIBS])],
  BOOST_REGEX,
    [AX_PKG_BOOST_LIB(REGEX,           [-lboost_regex],           [boost/regex.hpp], [boost::regex(".*");])],
  BOOST_DATETIME,
    [AX_PKG_BOOST_LIB(DATETIME,        [-lboost_date_time],       [boost/date_time/gregorian/gregorian_types.hpp])],
  BOOST_THREAD,
    [AX_PKG_BOOST_LIB(THREAD,          [-lboost_thread],          [boost/thread/thread.hpp], [boost::mutex();], [$PKG_BOOST_DATETIME_LIBS], [boost/thread/condition.hpp])],
  BOOST_IOSTREAMS,
    [AX_PKG_BOOST_LIB(IOSTREAMS,       [-lboost_iostreams],       [boost/iostreams/device/mapped_file.hpp], [boost::iostreams::mapped_file_source();])],
  BOOST_GRAPH,
    [AX_PKG_BOOST_LIB(GRAPH,           [],                        [boost/graph/adjacency_list.hpp])]
)

if test x"$HAVE_PKG_BOOST" = "xyes"; then
  AX_PKG_BOOST_CHECK_VERSION([PE_])
  AC_MSG_NOTICE([Using Boost header version $BOOST_VERSION, library suffix $PKG_BOOST_SAME_SUFFIX])
fi

# This provides an easy way for users to override the threads options
# if they are replacing Boost threads with something else for their platform.
AX_PKG(THREADS,           [BOOST_THREAD], [], [])

AX_PKG(M, [], [-lm], [math.h])

# Assorted other dependencies
AX_PKG_APPLE(COREMIDI,    [],      [-framework CoreMidi])
AX_PKG_APPLE(COREAUDIO,   [],      [-framework CoreAudio])
AX_PKG(RTAUDIO,           [],      [-lrtaudio], [RtAudio.h])
AX_PKG(LO,                [],      [-llo], [lo/lo.h])
AX_PKG(SDL,               [],      [-lSDL], [SDL.h], [SDL])

# Dependencies for OpenFrameworks
AX_PKG(FREEIMAGE,               [],      [-lfreeimage], [FreeImage.h])
AX_PKG(GLEE,                    [],      [-lGLee], [GL/GLee.h])
AX_PKG(FREETYPE,                [],      [-lfreetype], [ft2build.h freetype/freetype.h], [freetype2])

# OpenGL
AX_PKG_ONE_OF(GL,
  APPLE_GL,
    [AX_PKG_APPLE([GL], [], [-framework OpenGL -framework GLUT -Wl,-dylib_file,/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib])],
  LINUX_GL,
    [AX_PKG(X11, [], [-lXext -lX11 -lXmu -lXi -lXt], [])
     AX_PKG(LINUX_GL, [X11], [-lglut -lGLU -lGL], [GL/gl.h GL/glu.h GL/glut.h], [], [], [glCreateShader])])

AX_PKG(OPENVG,        [GL],      [-lOpenVG], [vg/openvg.h])
AX_PKG(OPENCV,        [],        [-lcv -lcvaux -lcxcore -lml -lhighgui], [cv.h], [opencv])

if test "$ENABLE_QT_QMAKE" = no; then
  AX_GROUP_PKG([QT_QMAKE])
else
  # Qt with AutoTroll.
  AT_WITH_QT([+gui +sql +opengl +network], [], [], [HAVE_PKG_QT_QMAKE="no:missing QT"], [])

  if test x"$HAVE_PKG_QT_QMAKE" != x"no:missing QT"; then
      AT_REQUIRE_QT_VERSION([4.0], [HAVE_PKG_QT_QMAKE="no:wrong QT version"], [])
  fi

  # We seed QT_QMAKE's cppflags and libs with the ones qmake figured out
  PKG_QT_QMAKE_CPPFLAGS="$PKG_QT_QMAKE_CPPFLAGS $QT_CPPFLAGS"
  AX_PKG(QT_QMAKE, [], [$QT_LIBS], [QVector])
fi

AX_PKG_ONE_OF(QT,
    ARBITRARY_QT,
     [if test -z "$QT_ARBITRARY_MODULES" -a -z "$HAVE_PKG_ARBITRARY_MODULES"; then
        HAVE_PKG_ARBITRARY_QT="no:Set \$QT_ARBITRARY_MODULES"
      else
        for module in $QT_ARBITRARY_MODULES; do
          PKG_ARBITRARY_QT_NEEDED_HEADERS="$PKG_ARBITRARY_QT_NEEDED_HEADERS Qt${module}"
          PKG_ARBITRARY_QT_LIBS="-lQt${module} $PKG_ARBITRARY_QT_LIBS"
        done
      fi
      PKG_ARBITRARY_QT_CPPFLAGS="$PKG_ARBITRARY_QT_CPPFLAGS -DQT_SHARED"
      AX_PKG(ARBITRARY_QT, [], [-lQtCore], [$PKG_ARBITRARY_QT_NEEDED_HEADERS])],
    APPLE_QMAKE_QT, [AX_PKG_APPLE(QMAKE_QT, [GL QT_QMAKE], [])],
    LINUX_QMAKE_QT,
     [AX_PKG(QT_QMAKE_OPENGL, [QT_QMAKE], [], [QtOpenGL])
      AX_PKG(QT_QMAKE_GUI,    [QT_QMAKE], [], [QLabel])
      AX_PKG(QT_QMAKE_SQL,    [QT_QMAKE], [], [QtSql])
      AX_PKG(QT_QMAKE_NETWORK,    [QT_QMAKE], [], [QtNetwork])
      AX_GROUP_PKG(LINUX_QMAKE_QT, [QT_QMAKE QT_QMAKE_GUI QT_QMAKE_OPENGL QT_QMAKE_SQL QT_QMAKE_NETWORK])],
    GUESS_QT,
     [PKG_QT_GUESS_BASE_CPPFLAGS="$PKG_QT_GUESS_BASE_CPPFLAGS -DQT_SHARED"
      AX_PKG(QT_GUESS_BASE,   [],                           [],           [QtCore/qstring.h])
      AX_PKG(QT_GUESS_CORE,   [QT_GUESS_BASE],              [-lQtCore],   [QtCore],   [QtCore])
      AX_PKG(QT_GUESS_GUI,    [QT_GUESS_CORE],              [-lQtGui],    [QtGui],    [QtGui])
      AX_PKG(QT_GUESS_SQL,    [QT_GUESS_CORE],              [-lQtSql],    [QtSql],    [QtSql])
      AX_PKG(QT_GUESS_NETWORK,[QT_GUESS_CORE],              [-lQtNetwork],[QtNetwork],[QtNetwork])
      AX_PKG(QT_GUESS_OPENGL, [QT_GUESS_CORE QT_GUESS_GUI], [-lQtOpenGL], [QtOpenGL], [QtOpenGL])
      AX_GROUP_PKG(GUESS_QT,  [QT_GUESS_BASE QT_GUESS_CORE QT_GUESS_GUI QT_GUESS_SQL QT_GUESS_NETWORK QT_GUESS_OPENGL])])


##################################################
# module definitions
##################################################

AX_GROUP_PKG(BOOST_COMMON, [BOOST BOOST_PROGRAM_OPTIONS])
AX_GROUP_PKG(BOOST_ALL,    [BOOST_COMMON BOOST_FILESYSTEM])

AX_MODULE(CORE,         [src/pe/Core],       [libpeCore.la],        yes, [BOOST BOOST_PROGRAM_OPTIONS THREADS M], [PTHREADS])
AX_MODULE(MATH,         [src/pe/Math],       [libpeMath.la],        yes, [CORE],    [])
AX_MODULE(GRAPHICS,     [src/pe/Graphics],   [libpeGraphics.la],    yes, [CORE],    [GL])
AX_MODULE(VIDEO,        [src/pe/Video],      [libpeVideo.la],       yes, [CORE GRAPHICS OPENCV],    [])
AX_MODULE(VISION,       [src/pe/Vision],     [libpeVision.la],      yes, [CORE OPENCV],   [])
AX_MODULE(SIMULATION,   [src/pe/Simulation], [libpeSimulation.la],  yes, [CORE MATH],  [])
#AX_APP(PHOSPHORESSENCE, [src], yes,  [CORE GRAPHICS MATH VIDEO SIMULATION VISION BOOST_THREAD BOOST_PROGRAM_OPTIONS QT RTAUDIO LO FREEIMAGE GLEE FREETYPE OPENVG OPENCV])

# These are here (instead of inside the APP macro where they belong)
# for backwards compatability with older versions of automake.
AM_CONDITIONAL(MAKE_MODULE_CORE,              [test "$MAKE_MODULE_CORE" = "yes"])
AM_CONDITIONAL(MAKE_MODULE_MATH,              [test "$MAKE_MODULE_MATH" = "yes"])
AM_CONDITIONAL(MAKE_MODULE_VIDEO,             [test "$MAKE_MODULE_VIDEO" = "yes"])
AM_CONDITIONAL(MAKE_MODULE_VISION,            [test "$MAKE_MODULE_VISION" = "yes"])
AM_CONDITIONAL(MAKE_MODULE_GRAPHICS,          [test "$MAKE_MODULE_GRAPHICS" = "yes"])
AM_CONDITIONAL(MAKE_MODULE_SIMULATION,        [test "$MAKE_MODULE_SIMULATION" = "yes"])
AM_CONDITIONAL(MAKE_APP_PHOSPHORESSENCE,      [test "$MAKE_APP_PHOSPHORESSENCE" = "yes"])

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

AX_LOG([using CPPFLAGS=$CPPFLAGS])
AX_LOG([using PE_CPPFLAGS=$PE_CPPFLAGS])
AX_LOG([using CFLAGS=$CFLAGS])
AX_LOG([using CXXFLAGS=$CXXFLAGS])
AX_LOG([using LDFLAGS=$LDFLAGS])
AX_LOG([using PE_LDFLAGS=$PE_LDFLAGS])

AC_SUBST(PE_CPPFLAGS)
AC_SUBST(PE_LDFLAGS)

##################################################
# makefiles to process
##################################################

AC_CONFIG_FILES([                       \
  Makefile                              \
  src/Makefile                          \
  src/pe/Makefile                       \
  src/pe/Core/Makefile                  \
  src/pe/Math/Makefile                  \
  src/pe/Graphics/Makefile              \
  src/pe/Vision/Makefile                \
  src/pe/Video/Makefile                 \
  src/pe/Simulation/Makefile            \
  src/OpenFrameworks/Makefile           \
])

AC_OUTPUT
