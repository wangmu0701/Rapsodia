##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
include ../../MakeDefs.mk
include ../../MakeRules.mk

default: driver
	./$^

GEN_DIR=RALib

RA_EXTRAS=../../hotF90
IPATH+=-I$(GEN_DIR) $(MODSEARCHFLAG) $(GEN_DIR) $(MODSEARCHFLAG) $(RA_EXTRAS)

unexport IPATH

OBJS= \
$(addprefix $(RA_EXTRAS)/, $(addsuffix .o,$(HOTF90NAMES))) \
simple.o \
driver.o

driver: $(OBJS) $(GEN_DIR)/libRapsodia.a
	$(F90C) $(FFLAGS) $(IPATH) -o $@ $^

$(GEN_DIR)/libRapsodia.a : FORCE
	../../Generator/generate.py -d 10 -o 3 -f $(GEN_DIR)
	cd $(GEN_DIR) && $(MAKE)

FORCE:

clean: 
	rm -rf $(GEN_DIR) *.o *.mod driver

.PHONY: default clean

driver.f90:$(GEN_DIR)/libRapsodia.a
simple.f90:$(GEN_DIR)/libRapsodia.a
