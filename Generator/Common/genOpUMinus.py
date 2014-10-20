##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util
def genUMinus(sourceList,helper): 
    # the generic bits for unary minus
    sourceList.append(generateUMinusBody(helper))
    # the UMinus intrinsic
    sourceList.append(helper.generateUnaryOp('uminus','-',[],[]))

import Common.ast as ast
import Common.slice as slice

def generateUMinusBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'uminus', helper.p.iE)
    if not parameters.useQueue:
      # compute UMinus
      aSourceNode.appendChild(ast.Assignment(util.vOf('r'),
                                             ast.UnaryMinus(util.vOf('a'))))

    s = slice.Slice(aSourceNode)
    for direct in range(1,parameters.sliceSize+1):
      for deg in range(1,parameters.o+1):
#       s.appendChild(ast.Assignment(util.dOf('r',direct,deg),
        s.appendChild(ast.Assignment(util.dOf(util.getVarGlobalName('r'),direct,deg),
                                     ast.UnaryMinus(util.dOf('a',direct,deg))))
    s.endSliceAndSave()
    return aSourceNode



def genUMinusReverse(sourceList,helper):
    sourceList.append(helper.generateUnaryIntrinsicReverse('uminus','-',names.Fixed.pN+'uminus',None,'r',None,[],[],[],[],getStatementA))


def getStatementA(helper,aSource,name,k,resultTypes):
    operand=util.vOf('a')
    aLHS=util.vOf('r')
    aRHS=ast.Multiplication(ast.Constant('-1.0'),operand)
    da=ast.Constant('-1.0')
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource

    




