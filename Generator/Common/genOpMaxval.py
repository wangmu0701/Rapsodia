##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util
def genMaxval(sourceList,helper): 
    # the generic bits for maxval
    for i in range(1,8): 
        sourceList.append(generateMaxvalBody(helper,i))
    # the maxval intrinsic
    aSourceNode=helper.generateUnaryArrayOpAll('maxval',
                                               None,
                                               names.Fixed.pN+'maxval',
                                               True,
                                               'r',
                                               'matchKindReturn',
                                               maxvalExtraVariables,
                                               [],
                                               [])
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)

import Common.ast as ast
import Common.slice as slice

def generateMaxvalBody(helper,dim):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'maxval'+str(dim),
                                 helper.p.iE)
    aSourceNode.fortranOnly=True
    # compute Maxval
    aSourceNode.appendChild(ast.Assignment(util.vOf('r'),ast.FuncCall('maxval',[util.vOf('a')])))
    aSourceNode.appendChild(ast.Assignment(ast.Variable('j'),ast.FuncCall('maxloc',[util.vOf('a')])))
    subscriptedArray='a('
    for i in range(1,dim):
        subscriptedArray+='j('+str(i)+'),'
    subscriptedArray+='j('+str(dim)+'))'
    aSourceNode.appendChild(ast.Assignment(ast.Variable('maxA'),ast.Variable(subscriptedArray)))

    s = slice.Slice(aSourceNode)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
#       s.appendChild(ast.Assignment(util.dOf('r',direct,deg),
        s.appendChild(ast.Assignment(util.dOf(util.getVarGlobalName('r'),direct,deg),
                                     util.dOf('maxA',direct,deg)))
#   s.endSlice()
    s.endSliceAndSave()
    return aSourceNode

def maxvalExtraVariables(helper,declarationBlock, rType, dimension):
    aDeclarator=ast.Declarator('j')
    declarationBlock.appendChild(aDeclarator)
    aDeclarator.type=ast.Type(helper.p.passiveTypeList[0][0])
    aDeclarator.dimensions=1
    aDeclarator.dimensionBounds=[ast.Constant(str(dimension))]
    aDeclarator=ast.Declarator('maxA')
    declarationBlock.appendChild(aDeclarator)
    aDeclarator.type=rType

