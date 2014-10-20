##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

# For FORTRAN only

def genMatmul(sourceList,helper): 
    # the generic bits for 
    sourceList.append(generateMatmulBody(helper,2,2))
    sourceList.append(generateMatmulBody(helper,1,2))
    sourceList.append(generateMatmulBody(helper,2,1))
    # the matmul intrinsic
    aSourceNode=helper.generateBinaryArrayOp('matmul',
                                             None,
                                             {'AA':signExtraVariables,
                                              'AP':signExtraVariables,
                                              'PA':signExtraVariables},
                                             [names.Fixed.pN+'sum',
                                              names.Fixed.pN+'mult'],
                                             False,
                                             False)
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)

import Common.ast as ast

def generateMatmulBody(helper,dim1,dim2):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'matmul'+str(dim1)+str(dim2),
                                 helper.p.iE)
    aSourceNode.fortranOnly=True
    # spell it out, it is relevant only for Fortran anyway...
    if (dim1==2 and dim2==2) :
        innerLoopBody=ast.Assignment(ast.Variable('r(j,k)'),
                                     ast.FuncCall('sum',
                                                  [ast.Multiplication(ast.Variable('a(j,:)'),
                                                                      ast.Variable('b(:,k)'))]))
        innerLoop=ast.For('j',
                          ast.FuncCall('lbound',
                                       [ast.Variable('a'),
                                        ast.Constant('1')]),
                          ast.FuncCall('ubound',
                                       [ast.Variable('a'),
                                        ast.Constant('1')]),
                          ast.Constant('1'),
                          innerLoopBody)
        outerLoop=ast.For('k',
                          ast.FuncCall('lbound',
                                       [ast.Variable('b'),
                                        ast.Constant('2')]),
                          ast.FuncCall('ubound',
                                       [ast.Variable('b'),
                                        ast.Constant('2')]),
                          ast.Constant('1'),
                          innerLoop)
        aSourceNode.appendChild(outerLoop)
    elif (dim1==1 and dim2==2):
        loopBody=ast.Assignment(ast.Variable('r(k)'),
                                ast.FuncCall('sum',
                                             [ast.Multiplication(ast.Variable('a(:)'),
                                                                 ast.Variable('b(:,k)'))]))
        loop=ast.For('k',
                     ast.FuncCall('lbound',
                                  [ast.Variable('b'),
                                   ast.Constant('2')]),
                     ast.FuncCall('ubound',
                                  [ast.Variable('b'),
                                   ast.Constant('2')]),
                     ast.Constant('1'),
                     loopBody)
        aSourceNode.appendChild(loop)
    elif (dim1==2 and dim2==1):
        loopBody=ast.Assignment(ast.Variable('r(j)'),
                                ast.FuncCall('sum',
                                             [ast.Multiplication(ast.Variable('a(j,:)'),
                                                                 ast.Variable('b(:)'))]))
        loop=ast.For('j',
                     ast.FuncCall('lbound',
                                  [ast.Variable('a'),
                                   ast.Constant('1')]),
                     ast.FuncCall('ubound',
                                  [ast.Variable('a'),
                                   ast.Constant('1')]),
                     ast.Constant('1'),
                     loopBody)
        aSourceNode.appendChild(loop)
    else:
        raise Exception('no logic for dim1='+str(dim1)+', dim2='+str(dim2))
    return aSourceNode

def signExtraVariables(helper,declarationBlock, theResTypes,leftArgType,leftDim,rightArgType,rightDim):
    if (leftDim>1) :
        aDeclarator=ast.Declarator('j')
        aDeclarator.type=ast.Type(helper.p.passiveTypeList[0][0])
        aDeclarator.type.baseType=True
        declarationBlock.appendChild(aDeclarator)
    if (rightDim>1) :  
        aDeclarator=ast.Declarator('k')
        aDeclarator.type=ast.Type(helper.p.passiveTypeList[0][0])
        aDeclarator.type.baseType=True
        declarationBlock.appendChild(aDeclarator)
        
