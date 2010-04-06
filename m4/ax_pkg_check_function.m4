dnl __BEGIN_LICENSE__
dnl Copyright (C) 2006-2010 United States Government as represented by
dnl the Administrator of the National Aeronautics and Space Administration.
dnl All Rights Reserved.
dnl __END_LICENSE__


m4_ifdef([_AX_FIXUPS], [], [m4_include([m4/fixups.m4])])

dnl usage: PKG_CHECK_FUNCTION(pkg, function, alias, define-in-c)
dnl check a pkg for an optional function, and call it by a different name
AC_DEFUN([PKG_CHECK_FUNCTION],
[m4_pushdef([var], my_tolower([$1])[_has_]m4_tolower(m4_default([$3],[$2])))
  var=0
  if test x"$HAVE_PKG_[]my_toupper([$1])" = x"yes"; then
    AX_CHECK_FUNCTIONS([$2], [$PKG_[]my_toupper([$1])[]_LIBS], [var=1], [], [for $3 in $1])
  fi
  if test x"$var" = "x1"; then
    m4_toupper(var)=yes
  else
    m4_toupper(var)=no
  fi
  m4_if([$4], [yes], [AC_DEFINE_UNQUOTED(AS_TR_CPP(m4_toupper(var)), [$var], [Define to 1 if $1 has $3 support])])
  m4_popdef([var])
])
