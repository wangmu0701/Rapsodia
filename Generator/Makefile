##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
include ../MakeDefs.mk

GENFLAGS=-d 3 -o 10

ifdef RA_USE_QUEUE
GENFLAGS+=-s 2 -q
endif	

check: generate
	cd TestLib && $(MAKE) check

generate: 
	./generate.py $(GENFLAGS) -c TestLib/Cpp 
ifndef RA_USE_QUEUE
	./generate.py $(GENFLAGS) -f TestLib/F90 
endif
	./generate.py --reverse -c TestLib/revCpp 
	./generate.py --reverse -f TestLib/revF90 


clean:
	cd TestLib && $(MAKE) clean
	rm -rf *.pyc *~  doc  */*.pyc 

.PHONY:  check generate clean
