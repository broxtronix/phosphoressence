# __BEGIN_LICENSE__
#
# Copyright (C) 2006 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration
# (NASA).  All Rights Reserved.
# 
# This software is distributed under the NASA Open Source Agreement
# (NOSA), version 1.3.  The NOSA has been approved by the Open Source
# Initiative.  See the file COPYING at the top of the distribution
# directory tree for the complete NOSA document.
# 
# THE SUBJECT SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY WARRANTY OF ANY
# KIND, EITHER EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT
# LIMITED TO, ANY WARRANTY THAT THE SUBJECT SOFTWARE WILL CONFORM TO
# SPECIFICATIONS, ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE, OR FREEDOM FROM INFRINGEMENT, ANY WARRANTY THAT
# THE SUBJECT SOFTWARE WILL BE ERROR FREE, OR ANY WARRANTY THAT
# DOCUMENTATION, IF PROVIDED, WILL CONFORM TO THE SUBJECT SOFTWARE.
#
# __END_LICENSE__

########################################################################
# tests (using cxxtest)
########################################################################

SUFFIXES = .cxx

CXXTEST_DIR =   $(top_srcdir)/thirdparty/cxxtest
CXXTEST_GEN =   $(CXXTEST_DIR)/cxxtestgen.pl
CXXTEST_ARGS =  --error-printer

.h.cxx:
	$(CXXTEST_GEN) $(CXXTEST_ARGS) -o $@ $<

include $(top_srcdir)/thirdparty/autotroll.mak
include $(top_srcdir)/thirdparty/cuda.mak
