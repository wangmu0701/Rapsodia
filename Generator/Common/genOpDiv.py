##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util
def genDiv(sourceList,helper): 
    # the generic bits for divisions
    sourceList.append(generateDivAABody(helper))
    # the generic bits for active/passive divisions
    sourceList.append(generateDivPABody(helper))
    # the generic bits for passive/active divisions
    sourceList.append(generateDivAPBody(helper))
    # the div intrinsic
    sourceList.append(helper.generateBinaryIntrinsic('div','/',
                                                     {'AA':divExtraVariable},
                                                     [],
                                                     False,False,False,'merge'))

import Common.ast as ast
import Common.slice as slice

def generateDivAABody(helper):
    aSource = ast.SimpleSource(names.Fixed.pN+'divAA', helper.p.iE)
    aRHS=ast.Division(ast.Constant('1.0'), 
                      util.vOf(util.getVarValueName('b')))
    aRecipLHS=ast.Variable('recip')
    aSource.appendChild(ast.Assignment(aRecipLHS,aRHS))
    
    if not parameters.useQueue:
      aRHS=ast.Multiplication(util.vOf(util.getVarValueName('a')), aRecipLHS)
      aSource.appendChild(ast.Assignment(util.vOf('r'), aRHS))

#   rRet = 'r'
    rRet = util.getVarGlobalName('r')
    s = slice.Slice(aSource)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        leftOp=util.dOf('a',direct,deg)
        theOuterGroupedExpressions=ast.Subtraction(leftOp,
            ast.Group(helper.generateConvolution((rRet,0,deg-1),
              ('b',1,deg), direct, 'plus')))
        aRHS=ast.Multiplication(aRecipLHS,
                                ast.Group(theOuterGroupedExpressions))
        s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
#   s.endSlice()
    s.endSliceAndSave()
    return aSource


def generateDivPABody(helper):
    aSource = ast.SimpleSource(names.Fixed.pN+'divPA', helper.p.iE)

#   rRet = 'r'
    rRet = util.getVarGlobalName('r')

    aResLHS = util.vOf(util.getVarValueName(rRet))
    if not parameters.useQueue:
      aRHS=ast.Division(ast.Variable('a'),util.vOf('b'))
      aSource.appendChild(ast.Assignment(aResLHS,aRHS))
    
    s = slice.Slice(aSource)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        aRHS=ast.Multiplication(aResLHS,ast.Group(
          helper.generateConvolution((rRet,0,deg-1), ('b',1,deg), 
                                     direct, 'minus')))
        s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
#   s.endSlice()
    s.endSliceAndSave()
    return aSource

def generateDivAPBody(helper):
    aSource = ast.SimpleSource(names.Fixed.pN+'divAP', helper.p.iE)

    if not parameters.useQueue:
      aRHS=ast.Division(util.vOf('a'), ast.Variable('b'))
      aSource.appendChild(ast.Assignment(util.vOf('r'),aRHS))

#   rRet = 'r'
    rRet = util.getVarGlobalName('r')
    s = slice.Slice(aSource)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        aRHS=ast.Division(util.dOf('a',direct,deg), ast.Variable('b'))
        s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
#   s.endSlice()
    s.endSliceAndSave()
    return aSource

def divExtraVariable(helper,declarationBlock, theResTypes,leftArgType,rightArgType):
    aDeclarator=ast.Declarator('recip')
    # from the result type we need to get the respective base type
    aDeclarator.type=theResTypes[1]
    declarationBlock.appendChild(aDeclarator)
    
def genDivReverse(sourceList,helper): 
    sourceList.append(helper.generateBinaryIntrinsicReverse('div','/',{},[],False,False,False,'merge',getStatementAA,getStatementAP,getStatementPA))


def getStatementAA(helper,aSource,name,kl,kr,resultTypes):
    leftOperand=util.vOf('a')
    rightOperand=util.vOf('b')
    da=ast.Division(ast.Constant('1.0'),util.vOf('b'))
    db=ast.Division(ast.Multiplication(ast.Constant('-1.0'),util.vOf('a')),ast.Multiplication(util.vOf('b'),util.vOf('b')))
    aLHS=util.vOf('r')
    aRHS=ast.Division(leftOperand,rightOperand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushBinaryLocal(da,db,kl,kr,resultTypes,'r','a','b'))
    return aSource

def getStatementAP(helper,aSource,name,kl,resultTypes):
    leftOperand=util.vOf('a')
    rightOperand=ast.Variable('b')
    da=ast.Division(ast.Constant('1.0'),ast.Variable('b'))
    aLHS=util.vOf('r')
    aRHS=ast.Division(leftOperand,rightOperand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,kl,resultTypes,'r','a'))
    return aSource
    
def getStatementPA(helper,aSource,name,kr,resultTypes):
    leftOperand=ast.Variable('a')
    rightOperand=util.vOf('b')
    db=ast.Division(ast.Multiplication(ast.Constant('-1.0'),ast.Variable('a')),ast.Multiplication(util.vOf('b'),util.vOf('b')))
    aLHS=util.vOf('r')
    aRHS=ast.Division(leftOperand,rightOperand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(db,kr,resultTypes,'r','b'))
    return aSource
    
    

    

