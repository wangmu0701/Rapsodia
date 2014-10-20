##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

def genMult(sourceList,helper): 
    # the generic bits for multiplications
    sourceList.append(generateMultAABody(helper))
    # the generic bits for active/passive multiplications
    sourceList.append(generateMultAPBody(helper,True,'AP'))
    # the generic bits for passive/active multiplications
    sourceList.append(generateMultAPBody(helper,False,'PA'))
    # the mult intrinsic
    sourceList.append(helper.generateBinaryIntrinsic('mult','*',{},[],False,False,False,'merge'))

import Common.ast as ast
import Common.slice as slice

def generateMultAABody(helper):
    aSource = ast.SimpleSource(names.Fixed.pN+'multAA', helper.p.iE)

    if not parameters.useQueue:
      aLHS=util.vOf('r')
      aRHS=ast.Multiplication(util.vOf('a'),util.vOf('b'))
      aSource.appendChild(ast.Assignment(aLHS,aRHS))

    s = slice.Slice(aSource)
    for dir in range(1, parameters.sliceSize+1):
      for deg in range(1, parameters.o+1):
#       aLHS = util.dOf('r', dir, deg)
        aLHS = util.dOf(util.getVarGlobalName('r'), dir, deg)
        aRHS = helper.generateConvolution(('a',0,deg),('b',0,deg),dir,'plus')
        s.appendChild(ast.Assignment(aLHS,aRHS))
#   s.endSlice()
    s.endSliceAndSave()

    return aSource

def generateMultAPBody(helper,leftActive,name):
    if leftActive :
      activeName='a'
      passiveName='b'
    else :
      activeName='b'
      passiveName='a'

    aSource = ast.SimpleSource(names.Fixed.pN+'mult'+name, helper.p.iE)

    if not parameters.useQueue:
      aLHS=util.vOf('r')
      aRHS=ast.Multiplication(util.vOf(activeName), ast.Variable(passiveName))
      aSource.appendChild(ast.Assignment(aLHS,aRHS))

    s = slice.Slice(aSource)
    for direct in range(1, parameters.sliceSize+1):
      for deg in range(1, parameters.o+1):
#       aLHS=util.dOf('r',direct,deg)
        aLHS=util.dOf(util.getVarGlobalName('r'),direct,deg)
        aRHS=ast.Multiplication(util.dOf(activeName,direct,deg),
                                ast.Variable(passiveName))
        s.appendChild(ast.Assignment(aLHS,aRHS))
#   s.endSlice()
    s.endSliceAndSave()

    return aSource


def genMultReverse(sourceList,helper): 
    sourceList.append(helper.generateBinaryIntrinsicReverse('mult','*',{},[],False,False,False,'merge',getStatementAA,getStatementAP,getStatementPA))



def getStatementAA(helper,aSource,name,kl,kr,resultTypes):
    leftOperand=util.vOf('a')
    rightOperand=util.vOf('b')
    da=util.vOf('b')
    db=util.vOf('a')
    aLHS=util.vOf('r')
    aRHS=ast.Multiplication(leftOperand,rightOperand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushBinaryLocal(da,db,kl,kr,resultTypes,'r','a','b'))
    return aSource

def getStatementAP(helper,aSource,name,kl,resultTypes):
    leftOperand=util.vOf('a')
    rightOperand=ast.Variable('b')
    da=ast.Variable('b')
    aLHS=util.vOf('r')
    aRHS=ast.Multiplication(leftOperand,rightOperand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,kl,resultTypes,'r','a'))
    return aSource
    
def getStatementPA(helper,aSource,name,kr,resultTypes):
    leftOperand=ast.Variable('a')
    rightOperand=util.vOf('b')
    db=ast.Variable('a')
    aLHS=util.vOf('r')
    aRHS=ast.Multiplication(leftOperand,rightOperand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(db,kr,resultTypes,'r','b'))
    return aSource
    
    

