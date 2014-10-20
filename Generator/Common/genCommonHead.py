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

def genCommonHead(sourceList, helper):
    if isinstance(helper.p, cpp.CppPrinter):
      # create defines header file
      src = ast.SimpleSource('common', '.h')
      src.appendChild(ast.Special(
      '''
#ifndef __RA_COMMOM_H__
#define __RA_COMMOM_H__

#define ADDRESS_LOC   
typedef void* location;
      '''))

      if (params.doubleOnly):
        src.appendChild(ast.Special('#define FAST_MODE_D'))

      src.appendChild(ast.Special('#define MAX_LOCAL_TAPE '+str(params.tapeLen)))
      src.appendChild(ast.Special('#define INITIAL_LOCATION_LEN '+str(params.locationLen)))
      src.appendChild(ast.Special('#define RA_PAGE_SIZE '+str(params.blockSize)))

      src.appendChild(ast.Special(
      '''
#define NULLLOC (location)-1
#define NULLType -1
      '''))

      src.appendChild(ast.Special(
      '''
//architecture specific parameters
#define RA_SIZE_INT sizeof(int)
#define RA_SIZE_VOIDP sizeof(void*)
#define RA_SIZE_DOUBLE sizeof(double)
#define RA_SIZE_LOCATION sizeof(location)
#endif
      '''))

      sourceList.append(src)
    else:
      # create defines header file
      src = ast.SimpleSource('common', '.h')
      src.appendChild(ast.Special(
      '''
#ifndef __RA_COMMOM_H__
#define __RA_COMMOM_H__


#define INTEGER_LOC   
typedef int location;
      '''))

      if (params.doubleOnly):
        src.appendChild(ast.Special('#define FAST_MODE_D'))
      if (params.accOnLoc):
        src.appendChild(ast.Special('#define RA_ACC_ON_LOC'))
      src.appendChild(ast.Special('#define MAX_LOCAL_TAPE '+str(params.tapeLen)))
      src.appendChild(ast.Special('#define INITIAL_LOCATION_LEN '+str(params.locationLen)))
      src.appendChild(ast.Special('#define RA_PAGE_SIZE '+str(params.blockSize)))

      src.appendChild(ast.Special(
      '''
#define NULLLOC (location)-1
#define NULLType -1
      '''))


      src.appendChild(ast.Special(
      '''
#define RA_SIZE_INT sizeof(int)
#define RA_SIZE_VOIDP sizeof(void*)
      '''))
      src.appendChild(ast.Special(
      '''
#define RA_SIZE_DOUBLE sizeof(double)
#define RA_SIZE_LOCATION sizeof(location)
#endif
      '''))

      sourceList.append(src)

    return
