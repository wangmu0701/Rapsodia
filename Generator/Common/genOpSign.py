##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

# For FORTRAN only

def genSign(sourceList,helper): 
    # the generic bits for sign
    sourceList.append(generateSignBody(helper,True,True,'sign'))
    # the generic bits for active/passive sign
    sourceList.append(generateSignBody(helper,True,False,'sign'))
    # the generic bits for passive/active sign
    sourceList.append(generateSignBody(helper,False,True,'sign'))
    # the sign intrinsic
    aSourceNode=helper.generateBinaryIntrinsic('sign',None,
                                               {'AA':signExtraVariables,
                                                'AP':signExtraVariables,
                                                'PA':signExtraVariables},
                                               [names.Fixed.pN+'abs',
                                                names.Fixed.pN+'asgn',
                                                names.Fixed.pN+'mult'],
                                               False,False,True,'left')
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)

import Common.ast as ast

def generateSignBody(helper,leftActive,rightActive,name):
    sourceName=names.Fixed.pN+name
    if leftActive :
      sourceName+='A'
    else :
      sourceName+='P'
    if rightActive :
      sourceName+='A'
    else :
      sourceName+='P'
    aSource = ast.SimpleSource(sourceName,
                               helper.p.iE)
    aSource.fortranOnly=True
    aLHS=ast.Variable('r')
    leftOperand=ast.Variable('a')
    if rightActive :
      rightOperand=util.vOf('b')
    else :
      rightOperand=ast.Variable('b')
    # if we don't assign it to a variable the compile will complain
    # kind mismatch when we don't modify the constant. So the variable
    # is to bypass the kind matching requirement. 
    aSource.appendChild(ast.Assignment(ast.Variable('one'),ast.Constant('1.0')))
    aSource.appendChild(ast.Assignment(aLHS,
                                       ast.Multiplication(ast.FuncCall('abs',[leftOperand]),
                                                          ast.FuncCall('sign',[ast.Variable('one'),
                                                                               rightOperand]))))
    return aSource


def signExtraVariables(helper,declarationBlock, theResTypes,leftArgType,rightArgType):
    aDeclarator=ast.Declarator('one')
    # from the result type we need to get the respective base type
    aDeclarator.type=ast.Type(rightArgType[0])
    if not(rightArgType[1] is None):
        aDeclarator.type.kind=helper.p.precDict[rightArgType[1]][0]
    declarationBlock.appendChild(aDeclarator)
    return 






def genSignReverse(sourceList,helper):
    aSourceNode=helper.generateBinaryIntrinsicReverse('sign',None,['factor'],[],False,False,True,'left',getStatementAA,getStatementAP,getStatementPA)
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)

import Common.ast as ast

def getStatementAA(helper,aSource,name,kl,kr,resultTypes):
    # do cast
    aSource.appendChild(ast.Assignment(util.vOf('r'),ast.FuncCall('sign',[util.vOf('a'),util.vOf('b')])))
    argNotZeroBranch=ast.BasicBlock()
    aVal = ast.Multiplication(util.vOf('a'),util.vOf('b'))
    aSource.appendChild(ast.Assignment(ast.Variable('factor'),
                                           ast.Constant('0.0')))
    aSource.appendChild(ast.If(ast.InEquality(aVal,
                                                  ast.Constant('0.0')),
                                   argNotZeroBranch))
    argGtZeroBranch=ast.BasicBlock()
    argGtZeroBranch.appendChild(ast.Assignment(ast.Variable('factor'),
                                               ast.Constant('1.0')))
    argLtZeroBranch=ast.BasicBlock()
    argLtZeroBranch.appendChild(ast.Assignment(ast.Variable('factor'),
                                               ast.Constant('-1.0')))
    testArgInner=ast.If(ast.LessThan(aVal, ast.Constant('0.0')),
                        argLtZeroBranch)
    testArgInner.appendChild(argGtZeroBranch)
    argNotZeroBranch.appendChild(testArgInner)
    da=ast.Variable('factor')
    aSource.appendChild(helper.generatePushUnaryLocal(da,kl,resultTypes,'r','a'))
    return aSource
def getStatementAP(helper,aSource,name,k,resultTypes):
    aSource.appendChild(ast.Assignment(util.vOf('r'),ast.FuncCall('sign',[util.vOf('a'),ast.Variable('b')])))
    argNotZeroBranch=ast.BasicBlock()
    aVal = ast.Multiplication(util.vOf('a'),ast.Variable('b'))
    aSource.appendChild(ast.Assignment(ast.Variable('factor'),
                                           ast.Constant('0.0')))
    aSource.appendChild(ast.If(ast.InEquality(aVal,
                                                  ast.Constant('0.0')),
                                   argNotZeroBranch))
    argGtZeroBranch=ast.BasicBlock()
    argGtZeroBranch.appendChild(ast.Assignment(ast.Variable('factor'),
                                               ast.Constant('1.0')))
    argLtZeroBranch=ast.BasicBlock()
    argLtZeroBranch.appendChild(ast.Assignment(ast.Variable('factor'),
                                               ast.Constant('-1.0')))
    testArgInner=ast.If(ast.LessThan(aVal, ast.Constant('0.0')),
                        argLtZeroBranch)
    testArgInner.appendChild(argGtZeroBranch)
    argNotZeroBranch.appendChild(testArgInner)
    da=ast.Variable('factor')
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource

def getStatementPA(helper,aSource,name,k,resultTypes):
    aSource.appendChild(ast.Assignment(ast.Variable('r'),ast.FuncCall('sign',[ast.Variable('a'),util.vOf('b')])))
    return aSource

