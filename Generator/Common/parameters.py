##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
## @var o
# derivative order
o = None
## @var d
# number of directions
d = None
## @var slices
# number of slices
slices = None
## @var sliceSize
# the size (= number of directions) of each slice
sliceSize = None
## @var useQueue
# true if queue is enabled, false otherwise
useQueue = None
# true if temporariesBug workaround is enabled, false otherwise
temporariesBug = None

useOPA = None
rootdir = None

## @var useOpenmp
# true is using openmp, false otherwise
useOpenmp = None

## @var openmpChunkSize
# the size of each chunk for loop scheduling
openmpChunkSize = None

## @var openmpUseOrphaning
# true if orphaning is enabled, false otherwise
openmpUseOrphaning = None

## @var disableInit
# true if we want to ommit default initialization to 0
disableInit = None

#Reverse mode

reverse=False
doubleOnly=False
accOnLoc=False
tapeLen=1000
locationLen=1000
blockSize=4096

Cpp=False
F90=False
