##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
include ../../MakeDefs.mk

MODDIR=./

check: 
	cd Cpp && $(MAKE)
ifndef RA_USE_QUEUE
	cd F90 && $(MAKE)
endif
# 	cd revCpp && $(MAKE)
# ifeq ($(ENABLEREVERSEF90),1)
# 	cd revF90 && $(MAKE)
# endif
clean: 
	rm -rf Cpp/*.o Cpp/*.?pp Cpp/*.a Cpp/Makefile Cpp/*.*
	rm -rf F90/*.o F90/*.mod F90/*.?90 F90/*.a F90/Makefile F90/*.*
	rm -rf revCpp/*.o revCpp/*.?pp revCpp/*.a revCpp/Makefile revCpp/*.*
	rm -rf revF90/*.o revF90/*.mod revF90/*.?90 revF90/*.a revF90/Makefile revF90/*.*

.PHONY: check clean
