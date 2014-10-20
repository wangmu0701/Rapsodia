#!/bin/bash
##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
compilers="g95 gfortran ifort nagfor pgf95 af95"
for i in `echo $compilers`
do 
  which $i > /dev/null 2>&1
  if [ $? -ne 0 ] 
  then 
    echo compiler $i is not available
  else
    set -e
    make clean > /dev/null
    echo "running with $i"
    ./configure.py -f $i
    make > $i.out
    make check >> $i.out
    set +e
  fi
done
