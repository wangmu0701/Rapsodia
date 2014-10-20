##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util
def genAddSub(sourceList,helper):  
    # the generic bits for additions
    sourceList.append(generateAddSubBody(helper,True,True,'add'))
    # the generic bits for active/passive additions
    sourceList.append(generateAddSubBody(helper,True,False,'add'))
    # the generic bits for passive/active additions
    sourceList.append(generateAddSubBody(helper,False,True,'add'))
    # the add intrinsic
    sourceList.append(helper.generateBinaryIntrinsic('add','+',{},[],False,False,False,'merge'))
    # the generic bits for subtractions
    sourceList.append(generateAddSubBody(helper,True,True,'sub'))
    # the generic bits for active/passive subtractions
    sourceList.append(generateAddSubBody(helper,True,False,'sub'))
    # the generic bits for passive/active subtractions
    sourceList.append(generateAddSubBody(helper,False,True,'sub'))
    # the sub intrinsic
    sourceList.append(helper.generateBinaryIntrinsic('sub','-',{},[],False,False,False,'merge'))


import Common.ast as ast
import Common.slice as slice

def generateAddSubBody(helper,leftActive,rightActive,name):
    sourceName=names.Fixed.pN+name
    if leftActive :
      sourceName+='A'
    else :
      sourceName+='P'
    if rightActive :
      sourceName+='A'
    else : 
      sourceName+='P'
    aSource = ast.SimpleSource(sourceName, helper.p.iE)
    aLHS=util.vOf('r')
    if leftActive :
      leftOperand=util.vOf('a')
    else :
      leftOperand=ast.Variable('a')
    if rightActive :
      rightOperand=util.vOf('b')
    else :
      rightOperand=ast.Variable('b')
    if name=='add' :
      aRHS=ast.Addition(leftOperand,rightOperand)
    elif name=='sub' : 
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
          aRHS=util.dOf('a',direct,deg)
        elif not(leftActive) and rightActive: # PA
          aRHS=util.dOf('b',direct,deg)
          if name=='sub' :
            aRHS=ast.UnaryMinus(aRHS)
        elif leftActive and rightActive:      # AA
          leftOperand=util.dOf('a',direct,deg)
          rightOperand=util.dOf('b',direct,deg)
          if name=='add' :
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


#Reverse_Mode Begin, for the first version, we only implement very basic features. No queue, no slice

def genAddSubReverse(sourceList,helper):  
    sourceList.append(helper.generateBinaryIntrinsicReverse('add','+',{},[],False,False,False,'merge',getStatementAA,getStatementAP,getStatementPA))
    sourceList.append(helper.generateBinaryIntrinsicReverse('sub','-',{},[],False,False,False,'merge',getStatementAA,getStatementAP,getStatementPA))

def getStatementAA(helper,aSource,name,kl,kr,resultTypes):
    leftOperand=util.vOf('a')
    rightOperand=util.vOf('b')
    da=ast.Constant('1.0')
    aLHS=util.vOf('r')
    if name=='add' :
      aRHS=ast.Addition(leftOperand,rightOperand)
      db=ast.Constant('1.0')
    elif name=='sub' : 
      aRHS=ast.Subtraction(leftOperand,rightOperand)
      db=ast.Constant('-1.0')
    else : 
      print >> sys.stderr, 'ERROR: generateAddSubBody: no logic for name '+name
      sys.exit(2)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushBinaryLocal(da,db,kl,kr,resultTypes,'r','a','b'))
    return aSource

def getStatementAP(helper,aSource,name,kl,resultTypes):
    leftOperand=util.vOf('a')
    rightOperand=ast.Variable('b')
    da=ast.Constant('1.0')
    aLHS=util.vOf('r')
    if name=='add' :
      aRHS=ast.Addition(leftOperand,rightOperand)
    elif name=='sub' : 
      aRHS=ast.Subtraction(leftOperand,rightOperand)
    else : 
      print >> sys.stderr, 'ERROR: generateAddSubBody: no logic for name '+name
      sys.exit(2)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(da,kl,resultTypes,'r','a'))
    return aSource
    
def getStatementPA(helper,aSource,name,kr,resultTypes):
    leftOperand=ast.Variable('a')
    rightOperand=util.vOf('b')
    aLHS=util.vOf('r')
    if name=='add' :
      aRHS=ast.Addition(leftOperand,rightOperand)
      db=ast.Constant('1.0')
    elif name=='sub' : 
      aRHS=ast.Subtraction(leftOperand,rightOperand)
      db=ast.Constant('-1.0')
    else : 
      print >> sys.stderr, 'ERROR: generateAddSubBody: no logic for name '+name
      sys.exit(2)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(helper.generatePushUnaryLocal(db,kr,resultTypes,'r','b'))
    return aSource
    
    

