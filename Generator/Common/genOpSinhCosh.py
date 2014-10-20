##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util
def genSinhCosh(sourceList,helper): 
    # the generic steps for sinh and cosh
    sourceList.append(generateSinhCoshBody(helper))
    # the sinh intrinsic
    sourceList.append(generateSinhModule(helper))
    # the cosh intrinsic
    sourceList.append(generateCoshModule(helper))
    
import Common.ast as ast
import Common.slice as slice

def generateSinhModule(helper):
    return helper.generateUnaryOpAll('sinh',
                                     None,
                                     names.Fixed.pN+'sinhcosh',
                                     None,
                                     's',
                                     None,
                                     ['c','t'],
                                     [], [], [])


def generateCoshModule(helper):
    return helper.generateUnaryOpAll('cosh',
                                     None,
                                     names.Fixed.pN+'sinhcosh',
                                     None,
                                     'c',
                                     None,
                                     ['s','t'],
                                     [], [], [])

def generateSinhCoshBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'sinhcosh', helper.p.iE)

#   cRet = 'c'
#   sRet = 's'
    cRet = util.getVarGlobalName('c')
    sRet = util.getVarGlobalName('s')

    if not parameters.useQueue:
      # compute cosh
      aRHS=ast.FuncCall('cosh',[util.vOf('a')])
      aSourceNode.appendChild(ast.Assignment(util.vOf('c'),aRHS))
      # compute sinh
      aRHS=ast.FuncCall('sinh',[util.vOf('a')])
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
        # cosh coefficients
        s.appendChild(ast.Assignment(util.dOf(cRet,direct,deg),
                                     helper.generateConvolution(('t',1,deg),(sRet,0,deg-1),direct,'plus')))
        # sinh coefficients
        s.appendChild(ast.Assignment(util.dOf(sRet,direct,deg),
                                     helper.generateConvolution(('t',1,deg),(cRet,0,deg-1),direct,'plus')))
        # scale c
        aRHS=ast.Division(util.dOf(cRet,direct,deg), ast.Constant(str(deg)))
        s.appendChild(ast.Assignment(util.dOf(cRet,direct,deg),aRHS))
        # scale s
        aRHS=ast.Division(util.dOf(sRet,direct,deg), ast.Constant(str(deg)))
        s.appendChild(ast.Assignment(util.dOf(sRet,direct,deg),aRHS))
    s.endSlice()
    s.saveGlobals(['c','s'])

    return aSourceNode

def genSinhCoshReverse(sourceList,helper):
    sourceList.append(helper.generateUnaryIntrinsicReverse('sinh',None,names.Fixed.pN+'sinh',None,'r',None,[],[],[],[],getStatementA))
    sourceList.append(helper.generateUnaryIntrinsicReverse('cosh',None,names.Fixed.pN+'cosh',None,'r',None,[],[],[],[],getStatementA))


def getStatementA(helper,aSource,name,k,resultTypes):
    operand=util.vOf('a')
    aLHS=util.vOf('r')
    if (name=='sinh'):
      aRHS=ast.FuncCall('sinh',[operand])
      da=ast.FuncCall('cosh',[operand])
    elif (name=='cosh'):
      aRHS=ast.FuncCall('cosh',[operand])
      da=ast.FuncCall('sinh',[operand])
      
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource

    



