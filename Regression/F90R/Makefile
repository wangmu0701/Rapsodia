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

IPATH+=-I$(GEN_DIR) $(MODSEARCHFLAG) $(GEN_DIR)

OBJS= driver.o

driver: $(OBJS) $(GEN_DIR)/libRapsodia.a
	$(F90C) $(FFLAGS) $(IPATH) -o $@ $^

$(GEN_DIR)/libRapsodia.a : FORCE
	@echo $(IPATH)
	../../Generator/generate.py -d 2 -o 10 -f $(GEN_DIR)
	cd $(GEN_DIR) && $(MAKE)

FORCE:

clean: 
	rm -rf $(GEN_DIR) *.o *.mod driver

.PHONY: default clean

driver.f90: $(OBJS) $(GEN_DIR)/libRapsodia.a
