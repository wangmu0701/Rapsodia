##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

# For FORTRAN only

def genSum(sourceList,helper): 
    # the generic bits for sum
    sourceList.append(generateSumBody(helper))
    # the sum intrinsic
    aSourceNode=helper.generateUnaryArrayOpAll('sum',
                                               None,
                                               names.Fixed.pN+'sum',
                                               False,
                                               'r',
                                               'matchKindReturn',
                                               None,
                                               [],[])
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)

import Common.ast as ast
import Common.slice as slice

def generateSumBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'sum',
                                 helper.p.iE)
    aSourceNode.fortranOnly=True
    # compute Sum
    aSourceNode.appendChild(ast.Assignment(util.vOf('r'),ast.FuncCall('sum',[util.vOf('a')])))

    s = slice.Slice(aSourceNode)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
#       s.appendChild(ast.Assignment(util.dOf('r',direct,deg),
        s.appendChild(ast.Assignment(util.dOf(util.getVarGlobalName('r'),direct,deg),
                                     ast.FuncCall('sum',[util.dOf('a',direct,deg)])))
#   s.endSlice()
    s.endSliceAndSave()

    return aSourceNode
