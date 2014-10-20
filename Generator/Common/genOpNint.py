##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

# For FORTRAN only

def genNint(sourceList,helper): 
    # the generic bits for cast to nint
    sourceList.append(generateNintBody(helper))
    # the nint intrinsic
    aSourceNode=helper.generatePassivatingOp('nint','integerReturn')
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)

import Common.ast as ast

def generateNintBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'nint',
                                 helper.p.iE)
    aSourceNode.fortranOnly=True
    # do cast
    aSourceNode.appendChild(ast.Assignment(ast.Variable('r'),
                                           ast.FuncCall('nint',[util.vOf('a')])))
    return aSourceNode



def genNintReverse(sourceList,helper):
    aSourceNode=helper.generateUnaryIntrinsicReverse('nint',None,names.Fixed.pN+'nint',None,'r','integerReturn',[],[],[],[],getStatementA)
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)

import Common.ast as ast

def getStatementA(helper,aSource,name,k,resultTypes):
    # do cast
    aSource.appendChild(ast.Assignment(ast.Variable('r'),
                                           ast.FuncCall('nint',[util.vOf('a')])))
    return aSource
