##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
include ../../MakeDefs.mk
include ../../MakeRules.mk

GEN_DIR=RALib

ifeq ($(ENABLEREVERSEF90),1)

default: driver
	./$^


IPATH+=-I$(GEN_DIR) $(MODSEARCHFLAG) $(GEN_DIR)

OBJS= driver.o

driver: $(OBJS) $(GEN_DIR)/libRapsodia.a
	$(MIXLANG_LD_TOPF90) $(MIXLANG_LDFLAGS_TOPF90_LIBSF90) -o $@ $^

$(GEN_DIR)/libRapsodia.a : FORCE
	../../Generator/generate.py --reverse -f $(GEN_DIR)
	cd $(GEN_DIR) && $(MAKE)
else

endif

FORCE:

clean: 
	rm -rf $(GEN_DIR) *.o *.mod driver

.PHONY: default clean

driver.f90: $(GEN_DIR)/libRapsodia.a
