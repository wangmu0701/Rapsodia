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

RA_EXTRAS=../../hotCpp
IPATH+=-I$(GEN_DIR) -I$(RA_EXTRAS)

OBJS= \
$(addprefix $(RA_EXTRAS)/, $(addsuffix .o, $(HOTCPPNAMES))) \
simple.o \
driver.o

driver:  $(OBJS) $(GEN_DIR)/libRapsodia.a
	$(CXX) $(CXXFLAGS) $(IPATH) -o $@ $^

$(GEN_DIR)/libRapsodia.a: FORCE
	../../Generator/generate.py -d 10 -o 3 -c $(GEN_DIR)
	cd $(GEN_DIR) && $(MAKE)

FORCE:

clean: 
	rm -rf $(GEN_DIR) *.o driver

.PHONY: default clean

simple.cpp:$(GEN_DIR)/libRapsodia.a
driver.cpp:$(GEN_DIR)/libRapsodia.a
