##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util
def genSinCos(sourceList,helper): 
    # the generic steps for sin and cos
    sourceList.append(generateSinCosBody(helper))
    # the sin intrinsic
    sourceList.append(generateSinModule(helper))
    # the cos intrinsic
    sourceList.append(generateCosModule(helper))
    
import Common.ast as ast
import Common.slice as slice

def generateSinModule(helper):
    return helper.generateUnaryOpAll('sin',
                                     None,
                                     names.Fixed.pN+'sincos',
                                     None,
                                     's',
                                     None,
                                     ['c','t'],
                                     [], [], [])


def generateCosModule(helper):
    return helper.generateUnaryOpAll('cos',
                                     None,
                                     names.Fixed.pN+'sincos',
                                     None,
                                     'c',
                                     None,
                                     ['s','t'],
                                     [], [], [])

def generateSinCosBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'sincos', helper.p.iE)

#   cRet = 'c'
#   sRet = 's'
    cRet = util.getVarGlobalName('c')
    sRet = util.getVarGlobalName('s')

    if not parameters.useQueue:
      # compute cos
      aRHS=ast.FuncCall('cos',[util.vOf('a')])
      aSourceNode.appendChild(ast.Assignment(util.vOf('c'),aRHS))
      # compute sin
      aRHS=ast.FuncCall('sin',[util.vOf('a')])
      aSourceNode.appendChild(ast.Assignment(util.vOf('s'),aRHS))
      if parameters.openmpUseOrphaning:
        aSourceNode.appendChild(ast.Assignment(util.vOf(cRet),util.vOf('c')))
        aSourceNode.appendChild(ast.Assignment(util.vOf(sRet),util.vOf('s')))

    s = slice.Slice(aSourceNode)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        # 't' is 'a' scaled by the deriviative degree
        aRHS=ast.Multiplication(ast.Constant(str(deg)),
                                util.dOf('a',direct,deg))
        s.appendChild(ast.Assignment(util.dOf('t',direct,deg),aRHS))
        # cos coefficients
        s.appendChild(ast.Assignment(util.dOf(cRet,direct,deg),
                                     helper.generateConvolution(('t',1,deg),(sRet,0,deg-1),direct,'minus')))
        # sin coefficients
        s.appendChild(ast.Assignment(util.dOf(sRet,direct,deg),
                                     helper.generateConvolution(('t',1,deg),(cRet,0,deg-1),direct,'plus')))
        # scale c
        aRHS=ast.Division(util.dOf(cRet,direct,deg), ast.Constant(str(deg)))
        s.appendChild(ast.Assignment(util.dOf(cRet,direct,deg),aRHS))
        # scale s
        aRHS=ast.Division(util.dOf(sRet,direct,deg), ast.Constant(str(deg)))
        s.appendChild(ast.Assignment(util.dOf(sRet,direct,deg),aRHS))
    s.endSlice()
    s.saveGlobals(['c', 's'])
    
    return aSourceNode




def genSinCosReverse(sourceList,helper):
    sourceList.append(helper.generateUnaryIntrinsicReverse('sin',None,names.Fixed.pN+'sin',None,'r',None,[],[],[],[],getStatementA))
    sourceList.append(helper.generateUnaryIntrinsicReverse('cos',None,names.Fixed.pN+'cos',None,'r',None,[],[],[],[],getStatementA))


def getStatementA(helper,aSource,name,k,resultTypes):
    operand=util.vOf('a')
    aLHS=util.vOf('r')
    if (name=='sin'):
      aRHS=ast.FuncCall('sin',[operand])
      da=ast.FuncCall('cos',[operand])
    elif (name=='cos'):
      aRHS=ast.FuncCall('cos',[operand])
      da=ast.FuncCall('-sin',[operand])
      
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource

    




