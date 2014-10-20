##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

# For FORTRAN only

def genInt(sourceList,helper): 
    # the generic bits for cast to int
    sourceList.append(generateIntBody(helper))
    # the int intrinsic
    aSourceNode=helper.generatePassivatingOp('int','integerReturn')
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)

import Common.ast as ast

def generateIntBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'int',
                                 helper.p.iE)
    aSourceNode.fortranOnly=True
    # do cast
    aSourceNode.appendChild(ast.Assignment(ast.Variable('r'),
                                           ast.FuncCall('int',[util.vOf('a')])))
    return aSourceNode




def genIntReverse(sourceList,helper):
    aSourceNode=helper.generateUnaryIntrinsicReverse('int',None,names.Fixed.pN+'int',None,'r','integerReturn',[],[],[],[],getStatementA)
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)

import Common.ast as ast

def getStatementA(helper,aSource,name,k,resultTypes):
    # do cast
    aSource.appendChild(ast.Assignment(ast.Variable('r'),
                                           ast.FuncCall('int',[util.vOf('a')])))
    return aSource
