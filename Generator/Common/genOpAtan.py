##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

def genAtan(sourceList,helper): 
    # the generic bits for atan
    sourceList.append(generateAtanBody(helper))
    # the atan intrinsic
    sourceList.append(helper.generateUnaryOpAll('atan',
                                                None,
                                                names.Fixed.pN+'atan',
                                                None,
                                                'r',
                                                None,
                                                ['y','s'],
                                                ['one'],
                                                [],
                                                [names.Fixed.pN+'add',
                                                 names.Fixed.pN+'div',
                                                 names.Fixed.pN+'mult']))

import Common.ast as ast
import Common.slice as slice

def generateAtanBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'atan', helper.p.iE)
    if not parameters.useQueue:
      aSourceNode.appendChild(ast.Assignment(ast.Variable('one'),
                                             ast.Constant('1.0')))
      # compute y = 1.0 / (1.0 + x*x)
      aRHS=ast.Division(ast.Variable('one'),
                        ast.Group(ast.Addition(ast.Variable('one'),
                                               ast.Multiplication(ast.Variable('a'),
                                                                  ast.Variable('a')))))
      aSourceNode.appendChild(ast.Assignment(ast.Variable('y'),aRHS))
    
      # compute atan
      aRHS=ast.FuncCall('atan',[util.vOf('a')])
      aSourceNode.appendChild(ast.Assignment(util.vOf('r'),aRHS))

#   rRet = 'r'
    rRet = util.getVarGlobalName('r')

    #derivatives
    s = slice.Slice(aSourceNode)
    for direct in range(1,parameters.sliceSize+1,1):
        for deg in range(1,parameters.o+1,1):
            # 's' is 'a' scaled by the deriviative degree
            aRHS=ast.Multiplication(ast.Constant(str(deg)),
                                    util.dOf('a',direct,deg))
            s.appendChild(ast.Assignment(util.dOf('s',direct,deg),aRHS))
             # multiply with y 
            aRHS=ast.Multiplication(util.vOf(util.getVarValueName('y')),
                                    util.dOf('a',direct,deg))
            s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
             # scale r
            aRHS=ast.Multiplication(ast.Constant(str(deg)),
                                    util.dOf(rRet,direct,deg))
            s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
            # increment r
            for iConv in range(1,deg):
                aRHS=ast.Addition(util.dOf(rRet,direct,deg),
                                  ast.Multiplication(util.dOf('s',direct,deg-iConv),
                                                     util.dOf('y',direct,iConv)))
                s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
            # unscale r
            aRHS=ast.Division(util.dOf(rRet,direct,deg),
                              ast.Constant(str(deg)))
            s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
#   s.endSlice()
    s.endSliceAndSave()
    return aSourceNode



def genAtanReverse(sourceList,helper):
    sourceList.append(helper.generateUnaryIntrinsicReverse('atan',None,names.Fixed.pN+'atan',None,'r',None,[],[],[],[],getStatementA))


def getStatementA(helper,aSource,name,k,resultTypes):
    operand=util.vOf('a')
    aLHS=util.vOf('r')
    aRHS=ast.FuncCall('atan',[operand])
    da=ast.Division(ast.Constant('1.0'),ast.Addition(ast.Constant('1.0'),ast.Multiplication(operand,operand)))
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource

    



