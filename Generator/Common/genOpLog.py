##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

def genLog(sourceList,helper): 
    # the generic bits for log
    sourceList.append(generateLogBody(helper))
    # the exp intrinsic
    sourceList.append(helper.generateUnaryOp('log',
                                             None,
                                             ['s','t'],
                                             ['recip']))

import Common.ast as ast
import Common.slice as slice

def generateLogBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'log',helper.p.iE)

    aRecipLHS=ast.Variable('recip')
    aRHS=ast.Division(ast.Constant('1.0'),
                      util.vOf(util.getVarValueName('a')))
    aSourceNode.appendChild(ast.Assignment(aRecipLHS,aRHS))
    
    if not parameters.useQueue:
      aRHS=ast.FuncCall('log',[util.vOf('a')])
      aSourceNode.appendChild(ast.Assignment(util.vOf('r'),aRHS))

#   sRet = 's'
    sRet = util.getVarGlobalName('s')

    s = slice.Slice(aSourceNode)
    for direct in range(1,parameters.sliceSize+1,1):
      s.appendChild(ast.Comment('scale input'))
      for deg in range(1,parameters.o+1,1):
        # 's' is 'a' scaled by the deriviative degree
        aRHS=ast.Multiplication(ast.Constant(str(deg)),util.dOf('a',direct,deg))
        s.appendChild(ast.Assignment(util.dOf(sRet,direct,deg),aRHS))
      s.appendChild(ast.Comment('compute output'))
      for deg in range(1,parameters.o+1,1):
        leftOp=util.dOf(sRet,direct,deg)
        
        if deg == 1:
          theOuterGroupedExpressions=leftOp
        if deg > 1:
          theOuterGroupedExpressions=ast.Subtraction(leftOp,
              ast.Group(helper.generateConvolution(('t',1,deg-1), 
              ('a',1,deg-1), direct, 'plus')))
        aRHS=ast.Multiplication(aRecipLHS,
                                ast.Group(theOuterGroupedExpressions))

        s.appendChild(ast.Assignment(util.dOf('t',direct,deg),aRHS))

        # scale the result
        aRHS=ast.Division(util.dOf('t',direct,deg),
                          ast.Constant(str(deg)+'.0'))
#       s.appendChild(ast.Assignment(util.dOf('r',direct,deg),aRHS))
        s.appendChild(ast.Assignment(util.dOf(util.getVarGlobalName('r'),direct,deg),aRHS))
    s.endSlice()
    s.saveGlobals()

    # TODO
    
    return aSourceNode




def genLogReverse(sourceList,helper):
    sourceList.append(helper.generateUnaryIntrinsicReverse('log',None,names.Fixed.pN+'sqrt',None,'r',None,[],[],[],[],getStatementA))


def getStatementA(helper,aSource,name,k,resultTypes):
    operand=util.vOf('a')
    aLHS=util.vOf('r')
    aRHS=ast.FuncCall('log',[operand])
    da=ast.Division(ast.Constant('1.0'),operand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource

    


