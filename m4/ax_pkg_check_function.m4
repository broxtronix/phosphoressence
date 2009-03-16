dnl __BEGIN_LICENSE__
dnl Copyright (C) 2006, 2007 United States Government as represented by
dnl the Administrator of the National Aeronautics and Space Administration.
dnl All Rights Reserved.
dnl __END_LICENSE__


dnl usage: PKG_CHECK_FUNCTION(pkg, function [, alias])
dnl check a pkg for an optional function, and perhaps call it by a different name
AC_DEFUN([PKG_CHECK_FUNCTION],
[AS_VAR_PUSHDEF([var], [m4_tolower([[$1]])[_has_]m4_tolower(m4_default([$3],[$2]))])
  var=0
  if test x"$HAVE_PKG_[]m4_toupper([[$1]])" = x"yes"; then
    AX_CHECK_FUNCTIONS([$2], [$PKG_[]m4_toupper([[$1]])[]_LIBS], [var=1], [], [for $3 in $1])
  fi
  if test x"$var" = "x1"; then
    m4_toupper(var)=yes
  else
    m4_toupper(var)=no
  fi
  AC_DEFINE_UNQUOTED(AS_TR_CPP(m4_toupper(var)), [$var], [Define to 1 if $1 has $3 support])
  AS_VAR_POPDEF([var])
])
