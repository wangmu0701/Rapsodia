##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

def genSqrt(sourceList,helper): 
    # the generic bits for square root
    sourceList.append(generateSqrtBody(helper,False))
    sourceList.append(generateSqrtBody(helper,True))
    # the sqrt intrinsic
    sourceList.append(helper.generateUnaryOpAll('sqrt',
                                                None,
                                                names.Fixed.pN+'sqrt',
                                                'Z',
                                                'r',
                                                None,
                                                [],
                                                ['recip'],
                                                [],[]))

import Common.ast as ast
import Common.slice as slice

def generateSqrtBody(helper,complexArg):
    if complexArg:
      aSourceNode = ast.SimpleSource(names.Fixed.pN+'sqrtZ', helper.p.iE)
    else:
      aSourceNode = ast.SimpleSource(names.Fixed.pN+'sqrt', helper.p.iE)

    if not parameters.useQueue:
      # compute sqrt
      aRHS=ast.FuncCall('sqrt',[util.vOf('a')])
      aSourceNode.appendChild(ast.Assignment(util.vOf('r'),aRHS))

    if (not helper.handleFPE or complexArg) :
      aRHS=ast.Division(ast.Constant('0.5'), 
                        util.vOf(util.getVarValueName('r')))
      aRecipLHS=ast.Variable('recip')
      aSourceNode.appendChild(ast.Assignment(aRecipLHS,aRHS))
#   ret = 'r'
    ret = util.getVarGlobalName('r')
    s = slice.Slice(aSourceNode)
    for direct in range(1,parameters.sliceSize+1,1):
      if helper.handleFPE and not complexArg:
        nonNullArgBranch=ast.BasicBlock()
        aRHS=ast.Division(ast.Constant('0.5'), util.vOf('r'))
        aRecipLHS=ast.Variable('recip')
        nonNullArgBranch.appendChild(ast.Assignment(aRecipLHS,aRHS))
        isArgNotZero=ast.If(ast.InEquality(util.vOf('a'),ast.Constant('0.0')),
                            nonNullArgBranch)
        nullArgBranch=ast.BasicBlock()  
        nullArgBranch.appendChild(ast.Assignment(ast.Variable('recip'),ast.Constant('0.0')))
        isArgNotZero.appendChild(nullArgBranch)
        s.appendChild(isArgNotZero)
      for deg in range(1,parameters.o+1,1):
        if helper.handleFPE and not complexArg :
          dirGTZeroBranch=ast.BasicBlock()
          dirGTZeroBranch.appendChild(ast.Assignment(aRecipLHS,
                                                     util.makeInf()))
          testDirGTZero=ast.If(ast.GreaterThan(util.dOf('a',direct,deg),
                                               ast.Constant('0.0')),
                               dirGTZeroBranch)
          dirGTZeroElseBranch=ast.BasicBlock()
          testDirGTZero.appendChild(dirGTZeroElseBranch)
          dirLTZeroBranch=ast.BasicBlock()
          dirLTZeroBranch.appendChild(ast.Assignment(aRecipLHS,
                                                     util.makeNaN()))
          testDirLTZero=ast.If(ast.LessThan(util.dOf('a',direct,deg),
                                            ast.Constant('0.0')),
                               dirLTZeroBranch)
          dirGTZeroElseBranch.appendChild(testDirLTZero)
          nullRecipBranch=ast.BasicBlock()
          nullRecipBranch.appendChild(testDirGTZero)
          isRecipZero=ast.If(ast.Equality(aRecipLHS,ast.Constant('0.0')),
                             nullRecipBranch)
          s.appendChild(isRecipZero)
        leftOp=util.dOf('a',direct,deg)
        if deg == 1:
          theOuterGroupedExpressions=leftOp
        else:
          theOuterGroupedExpressions=ast.Subtraction(leftOp,
             ast.Group(helper.generateConvolution((ret,1,deg-1),
                                                  (ret,1,deg-1),
                                                  direct,
                                                  'plus')))
        aRHS=ast.Multiplication(aRecipLHS,ast.Group(theOuterGroupedExpressions))
        s.appendChild(ast.Assignment(util.dOf(ret,direct,deg),aRHS))
#   s.endSlice()
    s.endSliceAndSave()
    return aSourceNode



def genSqrtReverse(sourceList,helper):
    sourceList.append(helper.generateUnaryIntrinsicReverse('sqrt',None,names.Fixed.pN+'sqrt',None,'r',None,[],[],[],[],getStatementA))


def getStatementA(helper,aSource,name,k,resultTypes):
    operand=util.vOf('a')
    aLHS=util.vOf('r')
    aRHS=ast.FuncCall('sqrt',[operand])
    da=ast.Division(ast.Constant('0.5'),aRHS)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,k,resultTypes,'r','a'))
    return aSource

    

