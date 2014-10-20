##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util
def genAbs(sourceList,helper): 
    # the generic bits for absolute value
    sourceList.append(generateAbsBody(helper))
    # the absolute value intrinsic
    sourceList.append(helper.generateUnaryOp('abs',None,[],
                                             ['factor_0','factor_d']))

import Common.ast as ast
import Common.slice as slice

def generateAbsBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'abs', helper.p.iE)
    # compute abs
    aSourceNode.appendChild(ast.Assignment(ast.Variable('factor_0'),
                                           ast.Constant('0.0')))
    argNotZeroBranch=ast.BasicBlock()
    aVal = util.getVarValueName('a')
    aSourceNode.appendChild(ast.If(ast.InEquality(util.vOf(aVal),
                                                  ast.Constant('0.0')),
                                   argNotZeroBranch))
    argGtZeroBranch=ast.BasicBlock()
    argGtZeroBranch.appendChild(ast.Assignment(ast.Variable('factor_0'),
                                               ast.Constant('1.0')))
    argLtZeroBranch=ast.BasicBlock()
    argLtZeroBranch.appendChild(ast.Assignment(ast.Variable('factor_0'),
                                               ast.Constant('-1.0')))
    testArgInner=ast.If(ast.LessThan(util.vOf(aVal), ast.Constant('0.0')),
                        argLtZeroBranch)
    testArgInner.appendChild(argGtZeroBranch)
    argNotZeroBranch.appendChild(testArgInner)

    if not parameters.useQueue:
      aSourceNode.appendChild(
        ast.Assignment(util.vOf('r'),
                       ast.FuncCall('abs',[util.vOf('a')])))
   
    s = slice.Slice(aSourceNode)
    for direct in range(1, parameters.sliceSize+1):
      s.appendChild(ast.Assignment(ast.Variable('factor_d'),
                                   ast.Variable('factor_0')))
      for deg in range(1, parameters.o+1):
        factorZeroBranch=ast.BasicBlock()
        isFactorZero=ast.If(ast.Equality(ast.Variable('factor_d'),
                                         ast.Constant('0.0')),
                            factorZeroBranch)
        dirNonZeroBranch=ast.BasicBlock()
        testDir=ast.If(ast.InEquality(util.dOf('a',direct,deg),
                                      ast.Constant('0.0')),
                       dirNonZeroBranch)
        factorZeroBranch.appendChild(testDir)
        dirGtZeroBranch=ast.BasicBlock()
        dirGtZeroBranch.appendChild(ast.Assignment(ast.Variable('factor_d'),
                                                   ast.Constant('1.0')))
        dirLtZeroBranch=ast.BasicBlock()
        dirLtZeroBranch.appendChild(ast.Assignment(ast.Variable('factor_d'),
                                                   ast.Constant('-1.0')))
        testDirInner=ast.If(ast.LessThan(util.dOf('a',direct,deg),
                                         ast.Constant('0.0')),
                       dirLtZeroBranch)
        testDirInner.appendChild(dirGtZeroBranch)
        dirNonZeroBranch.appendChild(testDirInner)

        s.appendChild(isFactorZero)
#       s.appendChild(ast.Assignment(util.dOf('r',direct,deg),
        s.appendChild(ast.Assignment(util.dOf(util.getVarGlobalName('r'),direct,deg),
                                     ast.Multiplication(util.dOf('a',direct,deg),
                                                        ast.Variable('factor_d'))))
    s.endSliceAndSave()
#   s.endSlice()
    return aSourceNode


def genAbsReverse(sourceList,helper):
    aSourceNode=helper.generateUnaryIntrinsicReverse('abs',None,names.Fixed.pN+'abs',None,'r',None,[],['factor'],[],[],getStatementA)
    sourceList.append(aSourceNode)

import Common.ast as ast

def getStatementA(helper,aSource,name,k,resultTypes):
    # do cast
    Operand=util.vOf('a')
    aSource.appendChild(ast.Assignment(util.vOf('r'),ast.FuncCall('abs',[util.vOf('a')])))
    argNotZeroBranch=ast.BasicBlock()
    aVal = util.getVarValueName('a')
    aSource.appendChild(ast.Assignment(ast.Variable('factor'),
                                           ast.Constant('0.0')))
    aSource.appendChild(ast.If(ast.InEquality(util.vOf(aVal),
                                                  ast.Constant('0.0')),
                                   argNotZeroBranch))
    argGtZeroBranch=ast.BasicBlock()
    argGtZeroBranch.appendChild(ast.Assignment(ast.Variable('factor'),
                                               ast.Constant('1.0')))
    argLtZeroBranch=ast.BasicBlock()
    argLtZeroBranch.appendChild(ast.Assignment(ast.Variable('factor'),
                                               ast.Constant('-1.0')))
    testArgInner=ast.If(ast.LessThan(util.vOf(aVal), ast.Constant('0.0')),
                        argLtZeroBranch)
    testArgInner.appendChild(argGtZeroBranch)
    argNotZeroBranch.appendChild(testArgInner)
    da=ast.Variable('factor')
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource
