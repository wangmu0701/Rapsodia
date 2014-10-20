##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################

import Common.ast as ast
import Common.names as names
import Common.parameters as params
import Common.util as util
import Cpp.Printer as cpp
import F90.Printer as f90

def genDefines(sourceList, helper):
    if isinstance(helper.p, cpp.CppPrinter) and params.useQueue:
      # create defines header file
      src = ast.SimpleSource('defines', helper.p.hE)
      src.appendChild(ast.Special(
      '''
#define locint unsigned int
#define queue_int unsigned short
#define slice_bits unsigned int // max 32 slices
#define UNUSED ~((locint) 0)
#define MAX_QUEUE_SIZE 65536
      '''))
      sourceList.append(src)
    return
