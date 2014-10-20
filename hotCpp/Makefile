##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
include ../MakeDefs.mk
include ../MakeRules.mk

all : $(addsuffix .o,$(HOTCPPNAMES))

IPATH+=-I./

clean: 
	rm -rf *.o *.mod *.a doc

.PHONY: clean all

HigherOrderTensor.hpp:MultiIndex.hpp
HigherOrderTensor.cpp:HigherOrderTensor.hpp
MultiIndex.cpp:MultiIndex.hpp
MultiIndex.hpp:Matrix.hpp
