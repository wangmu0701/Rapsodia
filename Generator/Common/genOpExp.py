##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

def genExp(sourceList,helper): 
    # the generic bits for exp
    sourceList.append(generateExpBody(helper))
    # the exp intrinsic
    sourceList.append(helper.generateUnaryOp('exp',
                                             None,
                                             ['s','t'],
                                             []))

import Common.ast as ast
import Common.slice as slice

def generateExpBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'exp', helper.p.iE)

#   sRet = 's'
#   rRet = 'r'
    sRet = util.getVarGlobalName('s')
    rRet = util.getVarGlobalName('r')

    if not parameters.useQueue:
      # compute exp
      aRHS=ast.FuncCall('exp',[util.vOf('a')])
      aSourceNode.appendChild(ast.Assignment(util.vOf('r'),aRHS))

      if parameters.openmpUseOrphaning:
        aSourceNode.appendChild(ast.Assignment(util.vOf(rRet), util.vOf('r')))

    s = slice.Slice(aSourceNode)
    for direct in range(1,parameters.sliceSize+1,1):
      s.appendChild(ast.Comment('scale input'))
      for deg in range(1,parameters.o+1,1):
        aRHS=ast.Multiplication(ast.Constant(str(deg)),util.dOf('a',direct,deg))
        s.appendChild(ast.Assignment(util.dOf(sRet,direct,deg),aRHS))
      s.appendChild(ast.Comment('compute output')) 
      for deg in range(1,parameters.o+1,1):
        # 't' is the convolution result
        s.appendChild(ast.Assignment(util.dOf('t',direct,deg),
                                     helper.generateConvolution((rRet,0,deg-1),
                                                                (sRet,1,deg),
                                                                direct,'plus')))
        # scale the result
        aRHS=ast.Division(util.dOf('t',direct,deg),ast.Constant(str(deg)+'.0'))
        s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
#   s.endSlice()
    s.endSliceAndSave()
    return aSourceNode


def genExpReverse(sourceList,helper):
    sourceList.append(helper.generateUnaryIntrinsicReverse('exp',None,names.Fixed.pN+'exp',None,'r',None,[],[],[],[],getStatementA))


def getStatementA(helper,aSource,name,k,resultTypes):
    operand=util.vOf('a')
    aLHS=util.vOf('r')
    aRHS=ast.FuncCall('exp',[operand])
    da=ast.FuncCall('exp',[operand])
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource

    


