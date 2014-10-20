##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
MODDIR=./

include ../MakeDefs.mk
include ../MakeRules.mk

all : $(addsuffix .o,$(HOTF90NAMES))

clean: 
	rm -rf *.o *.mod *.a doc

.PHONY: clean all

higherOrderTensorUtil.f90:multiIndexUtil.o
