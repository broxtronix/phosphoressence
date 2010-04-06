dnl __BEGIN_LICENSE__
dnl Copyright (C) 2006-2010 United States Government as represented by
dnl the Administrator of the National Aeronautics and Space Administration.
dnl All Rights Reserved.
dnl __END_LICENSE__


dnl Usage: AX_PKG_PTHREADS
AC_DEFUN([AX_PKG_PTHREADS],
[
  AC_MSG_CHECKING(for package PTHREADS)

  AC_LANG_PUSH(C)
  HAVE_PKG_PTHREADS=no

  ax_pkg_pthreads_cppflags_options="none -pthread"
  ax_pkg_pthreads_ldflags_options="-lpthread none"

  for ax_pkg_pthreads_ldflags in $ax_pkg_pthreads_ldflags_options; do
    if test "$ax_pkg_pthreads_ldflags" = "none" ; then
      PKG_PTHREADS_LDFLAGS=""
    else
      PKG_PTHREADS_LDFLAGS=$ax_pkg_pthreads_ldflags
    fi
    for ax_pkg_pthreads_cppflags in $ax_pkg_pthreads_cppflags_options; do
      if test "$ax_pkg_pthreads_cppflags" = "none" ; then
        PKG_PTHREADS_CPPFLAGS=""
      else
        PKG_PTHREADS_CPPFLAGS=$ax_pkg_pthreads_cppflags
      fi

      ax_pkg_pthreads_save_CFLAGS="$CFLAGS"
      ax_pkg_pthreads_save_LDFLAGS="$LDFLAGS"
      CFLAGS="$CFLAGS $PKG_PTHREADS_CPPFLAGS"
      LDFLAGS="$PKG_PTHREADS_LDFLAGS $LDFLAGS"

      AC_TRY_LINK([#include <pthread.h>],
                  [pthread_t th; pthread_create(0,0,0,0);],
                  [HAVE_PKG_PTHREADS=yes])

      CFLAGS="$ax_pkg_pthreads_save_CFLAGS"
      LDFLAGS="$ax_pkg_pthreads_save_LDFLAGS"

      if test "$HAVE_PKG_PTHREADS" = "yes"; then
        break 2;
      fi
    done
  done

  AC_LANG_POP(C)

  if test "$HAVE_PKG_PTHREADS" = "yes" ; then
    CFLAGS="$CFLAGS $PKG_PTHREADS_CPPFLAGS"
    CXXFLAGS="$CXXFLAGS $PKG_PTHREADS_CPPFLAGS"
    PKG_PTHREADS_LIBS="$PKG_PTHREADS_LDFLAGS"
  fi

  AC_MSG_RESULT([${HAVE_PKG_PTHREADS}])

  if test "${HAVE_PKG_PTHREADS}" = "yes" ; then
    ax_have_pkg_bool=1
  else
    ax_have_pkg_bool=0
  fi
  AC_DEFINE_UNQUOTED([HAVE_PKG_PTHREADS],
                     [$ax_have_pkg_bool],
                     [Define to 1 if the PTHREADS package is available.])

  AC_SUBST(HAVE_PKG_PTHREADS)
  AC_SUBST(PKG_PTHREADS_CPPFLAGS)
  AC_SUBST(PKG_PTHREADS_LIBS)

  AX_LOG([HAVE_PKG_PTHREADS=${HAVE_PKG_PTHREADS}])
  AX_LOG([PKG_PTHREADS_CPPFLAGS=${PKG_PTHREADS_CPPFLAGS}])
  AX_LOG([PKG_PTHREADS_LIBS=${PKG_PTHREADS_LIBS}])
  AX_LOG([CFLAGS=$CFLAGS])
  AX_LOG([CXXFLAGS=$CXXFLAGS])
  AX_LOG([CPPFLAGS=$CPPFLAGS])
  AX_LOG([LDFLAGS=$LDFLAGS])

])
