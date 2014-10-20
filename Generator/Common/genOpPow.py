##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util
def genPow(sourceList,helper): 
    # the generic bits for the power operator
    sourceList.append(generatePowAABody(helper))
    sourceList.append(generatePowAPBody(helper,False))
    sourceList.append(generatePowAPBody(helper,True))
    sourceList.append(generatePowPABody(helper))
    sourceList.append(generatePowPiABody(helper))
    # the power intrinsic
    sourceList.append(helper.generateBinaryIntrinsic('pow','**',
                                                     {'AP' :powExtraVariables,
                                                      'APi':powExtraVariables},
                                                     [ names.Fixed.pN+'mult', 
                                                       names.Fixed.pN+'log', 
                                                       names.Fixed.pN+'exp' ],
                                                     True,False,False,'merge'))

import Common.ast as ast
import Common.slice as slice

def generatePowPABody(helper):
    aSource = ast.SimpleSource(names.Fixed.pN+'powPA', helper.p.iE)
    aSource.appendChild(ast.Assignment(ast.Variable('r'),
                                       ast.FuncCall('exp',
                                                    [ast.Multiplication(ast.Variable('b'),
                                                                        ast.FuncCall('log',
                                                                                     [ast.Variable('a')]))])))
    return aSource

def generatePowPiABody(helper):
    aSource = ast.SimpleSource(names.Fixed.pN+'powPiA', helper.p.iE)
    aSource.appendChild(ast.Assignment(ast.Variable('r'),
                                       ast.FuncCall('exp',
                                                    [ast.Multiplication(ast.Variable('b'),
                                                                        ast.FuncCall('log',
                                                                                     [ast.FuncCall('real',
                                                                                                   [ast.Variable('a')])]))])))
    return aSource

def generatePowAABody(helper):
    aSource = ast.SimpleSource(names.Fixed.pN+'powAA', helper.p.iE)
    aSource.appendChild(ast.Assignment(ast.Variable('r'),
                                       ast.FuncCall('exp',
                                                    [ast.Multiplication(ast.Variable('b'),
                                                                        ast.FuncCall('log',
                                                                                     [ast.Variable('a')]))])))
    return aSource

def generatePowAPBody(helper,forIntegerExponent):
    if forIntegerExponent:
      name=names.Fixed.pN+'powAPi'
    else:
      name=names.Fixed.pN+'powAP'

    aSource = ast.SimpleSource(name, helper.p.iE)

    theBasis = util.vOf(util.getVarValueName('a'))
    theExponent = ast.Variable('b')
    if not parameters.useQueue:
      aPowerCall=ast.Power(theBasis,theExponent)
      aPowerCall.castArg1='double' 
      aPowerCall.castArg2='double' 
      aSource.appendChild(ast.Assignment(util.vOf('r'),aPowerCall))
    # is the argument zero or not:
    argZeroBranch=ast.BasicBlock()
    argNonzeroBranch=ast.BasicBlock()
    isArgZero=ast.If(ast.Equality(theBasis,ast.Constant('0.0')),
                     argZeroBranch)
    isArgZero.appendChild(argNonzeroBranch)
    aSource.appendChild(isArgZero)
    # the argument is zero:
    # is the exponent le Zero or not:
    expLEZeroBranch=ast.BasicBlock()
    expGTZeroBranch=ast.BasicBlock()
    if forIntegerExponent:
      expCondition=ast.LessThanOrEqual(theExponent,
                                       ast.Constant('0'))
    else:
      expCondition=ast.LessThanOrEqual(ast.FuncCall('real',
                                                    [theExponent]),
                                       ast.Constant('0.0'))
    isExpLEZero=ast.If(expCondition, expLEZeroBranch)
    isExpLEZero.appendChild(expGTZeroBranch)
    argZeroBranch.appendChild(isExpLEZero)
    # the exponent is le zero:

#   ret = 'r'
    ret = util.getVarGlobalName('r')

    s = slice.Slice(expLEZeroBranch)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        s.appendChild(ast.Assignment(util.dOf(ret,direct,deg),
                                     util.makeNaN()))
    s.endSlice()
    # the exponent is gt zero:
    # is the exponent value not an integer:
    isNotIntExponentBranch=ast.BasicBlock()
    isIntExponentBranch=ast.BasicBlock()
    isIntExponent=ast.If(ast.InEquality(ast.Group(ast.Subtraction(theExponent,
                                                                  ast.FuncCall('floor',
                                                                               [ast.FuncCall('real',
                                                                                             [theExponent])]))),
                                        ast.Constant('0')),
                         isNotIntExponentBranch)
    isIntExponent.appendChild(isIntExponentBranch)
    if (not forIntegerExponent): 
      expGTZeroBranch.appendChild(isIntExponent)
    else: 
      expGTZeroBranch.appendChild(isIntExponentBranch)  
    # the exponent value is not an integer:
    # for the degree:
    for deg in range(1,parameters.o+1,1):
      theDifference=ast.Variable('expDiff')
      isNotIntExponentBranch.appendChild(ast.Assignment(theDifference,
                                                        ast.Subtraction(theExponent,
                                                                        ast.Constant(str(deg)))))
      # exponent - degree > 1
      expVsDegreeBranch1=ast.BasicBlock()
      isNotIntExponentBranch.appendChild(ast.If(ast.GreaterThan(theDifference,
                                                                ast.Constant('1')),
                                                expVsDegreeBranch1))
      s = slice.Slice(expVsDegreeBranch1)
      for direct in range(1,parameters.sliceSize+1,1):
        s.appendChild(ast.Assignment(util.dOf(ret,direct,deg),
                                     ast.Constant('0.0')))
      s.endSlice()
      # 0 < exponent - degree < 1  
      expVsDegreeBranch2=ast.BasicBlock()
      aCondition=ast.LogicalAnd(ast.GreaterThan(theDifference,
                                                ast.Constant('0')),
                                ast.LessThan(theDifference,
                                             ast.Constant('1')))
      isNotIntExponentBranch.appendChild(ast.If(aCondition,
                                                expVsDegreeBranch2))
      s = slice.Slice(expVsDegreeBranch2)
      for direct in range(1,parameters.sliceSize+1,1):
        s.appendChild(ast.Assignment(util.dOf(ret,direct,deg),util.makeInf()))
      s.endSlice()
      # exponent - degree < 0
      expVsDegreeBranch3=ast.BasicBlock()
      isNotIntExponentBranch.appendChild(ast.If(ast.LessThan(theDifference,
                                                             ast.Constant('0')),
                                                expVsDegreeBranch3))
      s = slice.Slice(expVsDegreeBranch3)
      for direct in range(1,parameters.sliceSize+1,1):
        s.appendChild(ast.Assignment(util.dOf(ret,direct,deg),util.makeNaN()))
      s.endSlice()
    # the exponent value is an integer:
    # is the exponent 1 ?  
    exponentIsOneBranch=ast.BasicBlock()
    exponentIsNotOneBranch=ast.BasicBlock()
    isExponentOne=ast.If(ast.Equality(theExponent, ast.Constant('1')),
                         exponentIsOneBranch)
    isExponentOne.appendChild(exponentIsNotOneBranch)
    isIntExponentBranch.appendChild(isExponentOne)
    # the exponent is 1 !
    s = slice.Slice(exponentIsOneBranch)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        s.appendChild(ast.Assignment(util.dOf(ret,direct,deg),
                                     util.dOf('a',direct,deg)))
    s.endSlice()
    # the exponent is not one !
    s = slice.Slice(exponentIsNotOneBranch)
    for direct in range(1,parameters.sliceSize+1,1):
      s.appendChild(ast.Assignment(util.dOf(ret,direct,1),ast.Constant('0.0')))
      for deg in range(2,parameters.o+1,1):
        aConvolution=helper.generateConvolution(('a',1,deg-1),('a',1,deg-1),
                                                direct,'plus')
        s.appendChild(ast.Assignment(util.dOf(ret,direct,deg),aConvolution))
    s.endSlice()
    # for the the powers from 3 to the exponent:
    aLoopBody=ast.BasicBlock()
    exponentIsNotOneBranch.appendChild(ast.For('j',
                                               ast.Constant('3'),
                                               ast.FuncCall('int',[ast.FuncCall('real',[theExponent])]),
                                               ast.Constant('1'),
                                               aLoopBody))
    # in the loop:
    for deg in range(parameters.o,0,-1):
      s = slice.Slice(aLoopBody)
      for direct in range(1,parameters.sliceSize+1,1):
        aConvolution=helper.generateConvolution((ret,0,deg-1),('a',0,deg-1),
                                                direct,'plus')
        s.appendChild(ast.Assignment(util.dOf(ret,direct,deg),aConvolution))
      s.endSlice()
    # the argument is not zero:
    aRHS=ast.Division(ast.Constant('1.0'), theBasis)
    aRecipLHS=ast.Variable('recip')
    argNonzeroBranch.appendChild(ast.Assignment(aRecipLHS,aRHS))
    if parameters.openmpUseOrphaning:
      ast.Assignment(util.vOf(ret), util.vOf('r'))
    s = slice.Slice(argNonzeroBranch)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        # scale the argument
        aRHS=ast.Multiplication(ast.Constant(str(deg)),
                                util.dOf('a',direct,deg))
        s.appendChild(ast.Assignment(util.dOf('s',direct,deg),aRHS))
        if (deg > 1) :
          aConvolution=helper.generateConvolution(('a',1,deg-1),('t',1,deg-1),
                                                  direct,'plus')
        else:
          aConvolution=ast.Constant('0.0')
        # make the scaled result
        aRHS=ast.Multiplication(aRecipLHS, 
            ast.Group(ast.Subtraction(ast.Multiplication(ast.Variable('b'),
              ast.Group(helper.generateConvolution((ret,0,deg-1),('s',1,deg),direct,'plus'))),
              ast.Group(aConvolution))))
        s.appendChild(ast.Assignment(util.dOf('t',direct,deg), aRHS))
        # scale the result 
        aRHS=ast.Division(util.dOf('t',direct,deg),
                          ast.Constant(str(deg)))
        s.appendChild(ast.Assignment(util.dOf(ret,direct,deg),aRHS))
    s.endSlice()

#   s = slice.Slice(aSource, False)
    s.saveGlobals()
    return aSource

def powExtraVariables(helper,declarationBlock, theResTypes,leftArgType,rightArgType):
    aDeclarator=ast.Declarator('recip')
    # from the result type we need to get the respective base type
    aDeclarator.type=theResTypes[1]
    declarationBlock.appendChild(aDeclarator)
    if not parameters.useQueue:
      # local active variable
      aDeclarator=ast.Declarator('s')
      declarationBlock.appendChild(aDeclarator)
      aDeclarator.type=theResTypes[0]
      aDeclarator.type.baseType=False
      # local active variable
      aDeclarator=ast.Declarator('t')
      declarationBlock.appendChild(aDeclarator)
      aDeclarator.type=theResTypes[0]
      aDeclarator.type.baseType=False
    # local integers
    aDeclarator=ast.Declarator('j')
    declarationBlock.appendChild(aDeclarator)
    aDeclarator.type=ast.Type(helper.p.passiveTypeList[0][0])
    aDeclarator=ast.Declarator('expDiff')
    declarationBlock.appendChild(aDeclarator)
    aDeclarator.type=ast.Type(helper.p.typeList[0])
    return 

def genPowReverse(sourceList,helper):  
    sourceList.append(helper.generateBinaryIntrinsicReverse('pow','**',{},[],False,False,False,'merge',getStatementAA,getStatementAP,getStatementPA))

def getStatementAA(helper,aSource,name,kl,kr,resultTypes):
    baseOperand=util.vOf('a')
    expOperand=util.vOf('b')
    aLHS=util.vOf('r')
    aRHS=ast.Power(baseOperand,expOperand)
    da=ast.Multiplication(ast.FuncCall('log',[baseOperand]),aRHS)
    db=ast.Multiplication(expOperand,ast.Power(baseOperand,ast.Subtraction(expOperand,ast.Constant('1.0'))))
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushBinaryLocal(da,db,kl,kr,resultTypes,'r','a','b'))
    return aSource

def getStatementAP(helper,aSource,name,kl,resultTypes):
    baseOperand=util.vOf('a')
    expOperand=ast.Variable('b')
    aLHS=util.vOf('r')
    aRHS=ast.Power(baseOperand,expOperand)
    da=ast.Multiplication(expOperand,ast.Power(baseOperand,ast.Subtraction(expOperand,ast.Constant('1.0'))))
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,kl,resultTypes,'r','a'))
    return aSource
    
def getStatementPA(helper,aSource,name,kr,resultTypes):
    aType=ast.Type('real')
    aType.kind=helper.p.precDict[kr][0]
    baseOperand=ast.Variable('a')
    expOperand=util.vOf('b')
    aLHS=util.vOf('r')
    aRHS=ast.Power(baseOperand,expOperand)
    db=ast.Multiplication(ast.FuncCall('log',[ast.TypeConversion(baseOperand,aType)]),aRHS)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(db,kr,resultTypes,'r','b'))
    return aSource
    
    

