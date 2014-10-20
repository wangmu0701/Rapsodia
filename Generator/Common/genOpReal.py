##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

# For FORTRAN only

def genReal(sourceList,helper): 
    # the generic bits for cast to real
    sourceList.append(generateRealBody(helper))
    # the real intrinsic
    aSourceNode=helper.generateUnaryOpAll('real',
                                          None,
                                          names.Fixed.pN+'real',
                                          None,
                                          'r',
                                          'matchKindReturn',
                                          [],
                                          [],
                                          [],
                                          [])
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)


import Common.ast as ast
import Common.slice as slice

def generateRealBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'real', helper.p.iE)
    aSourceNode.fortranOnly=True
    # this is to get the real part from an active complex
    aSourceNode.appendChild(ast.Assignment(util.vOf('r'),
                                           ast.FuncCall('real',
                                                        [util.vOf('a')])))

    s = slice.Slice(aSourceNode)
    for direct in range(1,parameters.sliceSize+1,1):
        for deg in range(1,parameters.o+1,1):
#           s.appendChild(ast.Assignment(util.dOf('r',direct,deg),
            s.appendChild(ast.Assignment(util.dOf(util.getVarGlobalName('r'),direct,deg),
                                         ast.FuncCall('real',[util.dOf('a',direct,deg)])))
#   s.endSlice()
    s.endSliceAndSave()
    return aSourceNode
