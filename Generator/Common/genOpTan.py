##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util
def genTan(sourceList,helper): 
    # the generic bits for unary minus
    sourceList.append(generateTanBody(helper))
    # the Tan intrinsic
    sourceList.append(helper.generateUnaryOpAll('tan',
                                                None,
                                                names.Fixed.pN+'tan',
                                                None,
                                                'r',
                                                None,
                                                [],
                                                [],
                                                [],
                                                [names.Fixed.pN+'div',
                                                 names.Fixed.pN+'sin', 
                                                 names.Fixed.pN+'cos']))

import Common.ast as ast

def generateTanBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'tan', helper.p.iE)
    # compute Tan
    aSourceNode.appendChild(ast.Assignment(ast.Variable('r'),
                                           ast.Division(ast.FuncCall('sin',
                                                                     [ast.Variable('a')]),
                                                        ast.FuncCall('cos',
                                                                     [ast.Variable('a')]))))
    return aSourceNode

def genTanReverse(sourceList,helper): 
    sourceList.append(helper.generateUnaryIntrinsicReverse('tan',None,names.Fixed.pN+'tan',None,'r',None,[],[],[],[],getStatementA))


def getStatementA(helper,aSource,name,k,resultTypes):
    operand=util.vOf('a')
    aLHS=util.vOf('r')
    aRHS=ast.FuncCall('tan',[operand])
    da=ast.Division(ast.Constant('1.0'),ast.Multiplication(ast.FuncCall('cos',[operand]),ast.FuncCall('cos',[operand])))
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource

    

