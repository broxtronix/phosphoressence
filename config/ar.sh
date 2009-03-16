#!/bin/sh
if test -z "${3}" ; then
  echo '!<arch>' > ${2}
else
  ar ${*}
fi
