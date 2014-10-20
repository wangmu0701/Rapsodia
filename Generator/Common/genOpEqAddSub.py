##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

import Common.ast as ast
import Common.slice as slice

def genEqAddSub(sourceList,helper):
    # the generic bits for additions
    aSource=generateEqAddSubBody(helper,True,True,'eqadd')
    aSource.cppOnly=True
    sourceList.append(aSource)
    aSource=generateEqAddSubBody(helper,True,False,'eqadd')
    aSource.cppOnly=True
    sourceList.append(aSource)
    aSource=helper.generateCompoundIntrinsic('eqadd','+=',names.Fixed.pN+'eqadd',[])
    aSource.cppOnly=True
    sourceList.append(aSource)

    # the generic bits for subtractions
    aSource=generateEqAddSubBody(helper,True,True,'eqsub')
    aSource.cppOnly=True
    sourceList.append(aSource)
    aSource=generateEqAddSubBody(helper,True,False,'eqsub')
    aSource.cppOnly=True
    sourceList.append(aSource)
    aSource=helper.generateCompoundIntrinsic('eqsub','-=',names.Fixed.pN+'eqsub',[])
    aSource.cppOnly=True
    sourceList.append(aSource)

    # the generic bits for multiplications
    aSource=generateEqMultAABody(helper)
    aSource.cppOnly=True
    sourceList.append(aSource)
    aSource=generateEqMultAPBody(helper)
    aSource.cppOnly=True
    sourceList.append(aSource)
    aSource=helper.generateCompoundIntrinsic('eqmult','*=',names.Fixed.pN+'eqmult',[])
    aSource.cppOnly=True
    sourceList.append(aSource)

    # the generic bits for divisions
    aSource=generateEqDivAABody(helper)
    aSource.cppOnly=True
    sourceList.append(aSource)
    aSource=generateEqDivAPBody(helper)
    aSource.cppOnly=True
    sourceList.append(aSource)
    aSource=helper.generateCompoundIntrinsic('eqdiv','/=',names.Fixed.pN+'eqdiv',['RAdiv'])
    aSource.cppOnly=True
    sourceList.append(aSource)


def generateEqAddSubBody(helper,leftActive,rightActive,name):
    sourceName=names.Fixed.pN+name
    sourceName+='A'
    if rightActive :
      sourceName+='A'
    else : 
      sourceName+='P'
    aSource = ast.SimpleSource(sourceName, helper.p.iE)
    leftOperand=util.vOf('r')
    aLHS=util.vOf('r')

    if rightActive :
      rightOperand=util.vOf('b')
    else :
      rightOperand=ast.Variable('b')

    if name=='eqadd' :
      aRHS=ast.Addition(leftOperand,rightOperand)
    elif name=='eqsub' : 
      aRHS=ast.Subtraction(leftOperand,rightOperand)
    else : 
      print >> sys.stderr, 'ERROR: generateAddSubBody: no logic for name '+name
      sys.exit(2)

    if not parameters.useQueue:
      aSource.appendChild(ast.Assignment(aLHS,aRHS))

    s = slice.Slice(aSource)
    for direct in range(1, parameters.sliceSize+1):
      for deg in range(1,parameters.o+1):
#       aLHS=util.dOf('r',direct,deg)
        aLHS=util.dOf(util.getVarGlobalName('r'),direct,deg)
        if leftActive and not(rightActive):   # AP
          aRHS=util.dOf('r',direct,deg)
        elif not(leftActive) and rightActive: # PA
          aRHS=util.dOf('b',direct,deg)
          if name=='eqsub' :
            aRHS=ast.UnaryMinus(aRHS)
        elif leftActive and rightActive:      # AA
          leftOperand=util.dOf('r',direct,deg)
          rightOperand=util.dOf('b',direct,deg)
          if name=='eqadd' :
            aRHS=ast.Addition(leftOperand,rightOperand)
          else : # names tested above 
            aRHS=ast.Subtraction(leftOperand,rightOperand)
        else:  
          print >> sys.stderr, 'ERROR: generateAddSubBody: leftActive and rightActive cannot both be false'
          sys.exit(2)
        s.appendChild(ast.Assignment(aLHS,aRHS))
#   s.endSlice()
    s.endSliceAndSave()
    return aSource



def generateEqMultAABody(helper):
    aSource = ast.SimpleSource(names.Fixed.pN+'eqmultAA', helper.p.iE)
    s = slice.Slice(aSource)
    for dir in range(1, parameters.sliceSize+1):
      deg=parameters.o
      while(deg>0):
#      for deg in range(1, parameters.o+1):
#       aLHS = util.dOf('r', dir, deg)
        aLHS = util.dOf(util.getVarGlobalName('r'), dir, deg)
        aRHS = helper.generateConvolution(('r',0,deg),('b',0,deg),dir,'plus')
        s.appendChild(ast.Assignment(aLHS,aRHS))
        deg=deg-1;
#   s.endSlice()
    s.endSliceAndSave()

    if not parameters.useQueue:
      aLHS=util.vOf('r')
      aRHS=ast.Multiplication(util.vOf('r'),util.vOf('b'))
      aSource.appendChild(ast.Assignment(aLHS,aRHS))
    return aSource

def generateEqMultAPBody(helper):
    activeName='r'
    passiveName='b'
    aLHS=util.vOf('r')
    aSource = ast.SimpleSource(names.Fixed.pN+'eqmultAP', helper.p.iE)
    s = slice.Slice(aSource)
    for direct in range(1, parameters.sliceSize+1):
      for deg in range(1, parameters.o+1):
#       aLHS=util.dOf('r',direct,deg)
        aLHS=util.dOf(util.getVarGlobalName('r'),direct,deg)
        aRHS=ast.Multiplication(util.dOf(activeName,direct,deg),
                                ast.Variable(passiveName))
        s.appendChild(ast.Assignment(aLHS,aRHS))
#   s.endSlice()
    s.endSliceAndSave()

    if not parameters.useQueue:
      aRHS=ast.Multiplication(util.vOf(activeName), ast.Variable(passiveName))
      aSource.appendChild(ast.Assignment(aLHS,aRHS))
    return aSource


def generateEqDivAABody(helper):
    aSource = ast.SimpleSource(names.Fixed.pN+'eqdivAA', helper.p.iE)
    aRHS=ast.Division(ast.Constant('1.0'), util.vOf(util.getVarValueName('b')))
    aRecipLHS=ast.Variable('recip')
    aSource.appendChild(ast.Assignment(aRecipLHS,aRHS))

    if not parameters.useQueue:
      aRHS=ast.Multiplication(util.vOf(util.getVarValueName('a')), aRecipLHS)
      aSource.appendChild(ast.Assignment(util.vOf('r'), aRHS))

#   rRet = 'r'
    rRet = util.getVarGlobalName('r')
    s = slice.Slice(aSource)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        leftOp=util.dOf('a',direct,deg)
        theOuterGroupedExpressions=ast.Subtraction(leftOp,
            ast.Group(helper.generateConvolution((rRet,0,deg-1),
              ('b',1,deg), direct, 'plus')))
        aRHS=ast.Multiplication(aRecipLHS,
                                ast.Group(theOuterGroupedExpressions))
        s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
#   s.endSlice()
    s.endSliceAndSave()
    return aSource


def generateEqDivAPBody(helper):
    aSource = ast.SimpleSource(names.Fixed.pN+'eqdivAP', helper.p.iE)

    if not parameters.useQueue:
      aRHS=ast.Division(util.vOf('a'), ast.Variable('b'))
      aSource.appendChild(ast.Assignment(util.vOf('r'),aRHS))

#   rRet = 'r'
    rRet = util.getVarGlobalName('r')
    s = slice.Slice(aSource)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        aRHS=ast.Division(util.dOf('a',direct,deg), ast.Variable('b'))
        s.appendChild(ast.Assignment(util.dOf(rRet,direct,deg),aRHS))
#   s.endSlice()
    s.endSliceAndSave()
    return aSource




#Reverse_Mode Begin, for the first version, we only implement very basic features. No queue, no slice

def genEqAddSubReverse(sourceList,helper):
    aSource=helper.generateCompoundIntrinsicReverse('eqadd','+=',names.Fixed.pN+'eqadd',getStatementAA,getStatementAP,getStatementPA)
    aSource.cppOnly=True;
    sourceList.append(aSource)
    aSource=helper.generateCompoundIntrinsicReverse('eqsub','-=',names.Fixed.pN+'eqsub',getStatementAA,getStatementAP,getStatementPA)
    aSource.cppOnly=True;
    sourceList.append(aSource)
    aSource=helper.generateCompoundIntrinsicReverse('eqmult','*=',names.Fixed.pN+'eqmult',getStatementAA,getStatementAP,getStatementPA)
    aSource.cppOnly=True;
    sourceList.append(aSource)
    aSource=helper.generateCompoundIntrinsicReverse('eqdiv','/=',names.Fixed.pN+'eqdiv',getStatementAA,getStatementAP,getStatementPA)
    aSource.cppOnly=True;
    sourceList.append(aSource)

def getStatementAA(helper,aSource,name,kl,kr,resultTypes):
    leftOperand=util.vOf('r')
    rightOperand=util.vOf('a')
    aLHS=util.vOf('r')
    if name=='eqadd' :
      aRHS=ast.Addition(leftOperand,rightOperand)
      da=ast.Constant('1.0')
      db=ast.Constant('1.0')
    elif name=='eqsub' : 
      aRHS=ast.Subtraction(leftOperand,rightOperand)
      da=ast.Constant('1.0')
      db=ast.Constant('-1.0')
    elif name=='eqmult' :
      aRHS=ast.Multiplication(leftOperand,rightOperand)
      da=rightOperand
      db=leftOperand
    elif name=='eqdiv' :
      aRHS=ast.Division(leftOperand,rightOperand)
      da=ast.Division(ast.Constant('1.0'),rightOperand)
      db=ast.Division(ast.Multiplication(ast.Constant('-1.0'),leftOperand),ast.Multiplication(rightOperand,rightOperand))
    else: 
      print >> sys.stderr, 'ERROR: generateOpEqOpsBody: no logic for name '+name
      sys.exit(2)
    aSource.appendChild(helper.generatePushBinaryLocal(da,db,kl,kr,resultTypes,'r','r','a'))
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aParameterList=[]
    aSubroutineCall=ast.SubroutineCall('preAcc',aParameterList)
    aSource.appendChild(aSubroutineCall)
    return aSource

def getStatementAP(helper,aSource,name,kl,resultTypes):
    leftOperand=util.vOf('r')
    rightOperand=ast.Variable('a')
    aLHS=util.vOf('r')
    if name=='eqadd' :
      aRHS=ast.Addition(leftOperand,rightOperand)
      da=ast.Constant('1.0')
    elif name=='eqsub' : 
      aRHS=ast.Subtraction(leftOperand,rightOperand)
      da=ast.Constant('1.0')
    elif name=='eqmult' :
      aRHS=ast.Multiplication(leftOperand,rightOperand)
      da=rightOperand
    elif name=='eqdiv' :
      aRHS=ast.Division(leftOperand,rightOperand)
      da=ast.Division(ast.Constant('1.0'),rightOperand)
    else: 
      print >> sys.stderr, 'ERROR: generateOpEqOpsBody: no logic for name '+name
      sys.exit(2)
    aSource.appendChild(helper.generatePushUnaryLocal(da,kl,resultTypes,'r','r'))
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aParameterList=[]
    aSubroutineCall=ast.SubroutineCall('preAcc',aParameterList)
    aSource.appendChild(aSubroutineCall)
    return aSource
    
def getStatementPA(helper,aSource,name,kr,resultTypes):
    return aSource
    

