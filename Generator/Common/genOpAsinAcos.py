##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

def genAsinAcos(sourceList,helper): 
    # the generic steps for asin 
    sourceList.append(generateAsinAcosBody(helper,'asin'))
    # the asin intrinsic
    sourceList.append(generateAsinModule(helper))
    # the generic steps for acos 
    sourceList.append(generateAsinAcosBody(helper,'acos'))
    # the acos intrinsic
    sourceList.append(generateAcosModule(helper))
    
import Common.ast as ast
import Common.slice as slice

def generateAsinModule(helper):
    return helper.generateUnaryOpAll('asin',
                                     None,
                                     names.Fixed.pN+'asin',
                                     None,
                                     'r',
                                     None,
                                     ['h','t'],
                                     [],
                                     [],
                                     [names.Fixed.pN+'sqrt',
                                      names.Fixed.pN+'div',
                                      names.Fixed.pN+'mult',
                                      names.Fixed.pN+'sub'])


def generateAcosModule(helper):
    return helper.generateUnaryOpAll('acos',
                                     None,
                                     names.Fixed.pN+'acos',
                                     None,
                                     'r',
                                     None,
                                     ['h','t'],
                                     [],
                                     [],
                                     [names.Fixed.pN+'sqrt',
                                      names.Fixed.pN+'div',
                                      names.Fixed.pN+'mult',
                                      names.Fixed.pN+'sub',
                                      names.Fixed.pN+'uminus'])

def generateAsinAcosBody(helper,name):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+name, helper.p.iE)
    if not parameters.useQueue:
      # compute result
      aRHS=ast.FuncCall(name,[util.vOf('a')])
      aSourceNode.appendChild(ast.Assignment(util.vOf('r'),aRHS))
      # compute derivative helper 1.0/sqrt(1.0-x*x)
      oneConstant=ast.Constant('1.0')
      oneConstant.kind=helper.p.precDict.values()[0][0]
      aRHS=ast.Division(oneConstant,
                        ast.FuncCall('sqrt',
                                     [ast.Subtraction(oneConstant,
                                                      ast.Multiplication(ast.Variable('a'),
                                                                         ast.Variable('a')))]))
      if(name=='acos'):
          aRHS=ast.UnaryMinus(aRHS)
      aSourceNode.appendChild(ast.Assignment(ast.Variable('h'),aRHS))

#   rRet = 'r'
    rRet = util.getVarGlobalName('r')

    s = slice.Slice(aSourceNode)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        # 't' is 'a' scaled by the deriviative degree
        aRHS=ast.Multiplication(ast.Constant(str(deg)),
                                util.dOf('a',direct,deg))
        s.appendChild(ast.Assignment(util.dOf('t',direct,deg),aRHS))
        # convolution between helper and scaled argument
        s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),
                                     helper.generateConvolution(('t',1,deg),
                                                                ('h',0,deg-1),
                                                                direct,'plus')))
        # scale r
        aRHS=ast.Division(util.dOf(rRet,direct,deg), ast.Constant(str(deg)))
        s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
#   s.endSlice()
    s.endSliceAndSave()
    return aSourceNode





def genAsinAcosReverse(sourceList,helper):
    sourceList.append(helper.generateUnaryIntrinsicReverse('asin',None,names.Fixed.pN+'asin',None,'r',None,[],[],[],[],getStatementA))
    sourceList.append(helper.generateUnaryIntrinsicReverse('acos',None,names.Fixed.pN+'acos',None,'r',None,[],[],[],[],getStatementA))


def getStatementA(helper,aSource,name,k,resultTypes):
    operand=util.vOf('a')
    aLHS=util.vOf('r')
    if (name=='asin'):
      aRHS=ast.FuncCall('asin',[operand])
      da=ast.Division(ast.Constant('1.0'),ast.FuncCall('sqrt',[ast.Subtraction(ast.Constant('1.0'),ast.Multiplication(operand,operand))]))
    elif (name=='acos'):
      aRHS=ast.FuncCall('acos',[operand])
      da=ast.Division(ast.Constant('-1.0'),ast.FuncCall('sqrt',[ast.Subtraction(ast.Constant('1.0'),ast.Multiplication(operand,operand))]))
    else:
      print "wrong name?="+name
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource

    





