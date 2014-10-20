##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util
import Common.ast as ast

def genCompOps(sourceList,helper):  
    # the generic bits for operators
    compOpDict={"lt":(ast.LessThan,'<'), 
                "le":(ast.LessThanOrEqual,'<='),
                "gt":(ast.GreaterThan,'>'),
                "ge":(ast.GreaterThanOrEqual,'>='),
                "eq":(ast.Equality,'=='),
                "ne":(ast.InEquality,'/=')}
    for k,t in compOpDict.items():
      sourceList.append(generateBody(helper,True,True,k,t))
      # the generic bits for active/passive additions  
      sourceList.append(generateBody(helper,True,False,k,t))
      # the generic bits for passive/active additions
      sourceList.append(generateBody(helper,False,True,k,t))
      # the add intrinsic
      sourceList.append(helper.generateBinaryIntrinsic(k,t[1],{},[],
                                                       False,True,False,
                                                       'merge'))

def generateBody(helper,leftActive,rightActive,name,opTuple):
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
    aLHS=ast.Variable('r')
    if leftActive :
      leftOperand=util.vOf('a')
    else :
      leftOperand=ast.Variable('a')
    if rightActive :
      rightOperand=util.vOf('b')
    else :
      rightOperand=ast.Variable('b')
    aRHS=opTuple[0](leftOperand,rightOperand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    return aSource

def genCompOpsReverse(sourceList,helper):  
    # the generic bits for operators
    compOpDict={"lt":(ast.LessThan,'<'), 
                "le":(ast.LessThanOrEqual,'<='),
                "gt":(ast.GreaterThan,'>'),
                "ge":(ast.GreaterThanOrEqual,'>='),
                "eq":(ast.Equality,'=='),
                "ne":(ast.InEquality,'/=')}
    for k,t in compOpDict.items():
      sourceList.append(helper.generateBinaryIntrinsicReverse(k,t[1],{},[],False,True,False,'merge',getStatementAA,getStatementAP,getStatementPA))
  

def getStatementAA(helper,aSource,name,kl,kr,resultTypes):
    compOpDict={"lt":(ast.LessThan,'<'), 
                "le":(ast.LessThanOrEqual,'<='),
                "gt":(ast.GreaterThan,'>'),
                "ge":(ast.GreaterThanOrEqual,'>='),
                "eq":(ast.Equality,'=='),
                "ne":(ast.InEquality,'/=')}

    leftOperand=util.vOf('a')
    rightOperand=util.vOf('b')
    aLHS=ast.Variable('r')
    aRHS=compOpDict[name][0](leftOperand,rightOperand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(ast.SubroutineCall('eliminateResiduals',[util.lOf('a'),util.lOf('b')]))
    return aSource

def getStatementAP(helper,aSource,name,kl,resultTypes):
    compOpDict={"lt":(ast.LessThan,'<'), 
                "le":(ast.LessThanOrEqual,'<='),
                "gt":(ast.GreaterThan,'>'),
                "ge":(ast.GreaterThanOrEqual,'>='),
                "eq":(ast.Equality,'=='),
                "ne":(ast.InEquality,'/=')}

    leftOperand=util.vOf('a')
    rightOperand=ast.Variable('b')
    aLHS=ast.Variable('r')
    aRHS=compOpDict[name][0](leftOperand,rightOperand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(ast.SubroutineCall('eliminateResidual',[util.lOf('a')]))
    return aSource
    
def getStatementPA(helper,aSource,name,kr,resultTypes):
    compOpDict={"lt":(ast.LessThan,'<'), 
                "le":(ast.LessThanOrEqual,'<='),
                "gt":(ast.GreaterThan,'>'),
                "ge":(ast.GreaterThanOrEqual,'>='),
                "eq":(ast.Equality,'=='),
                "ne":(ast.InEquality,'/=')}

    leftOperand=ast.Variable('a')
    rightOperand=util.vOf('b')
    aLHS=ast.Variable('r')
    aRHS=compOpDict[name][0](leftOperand,rightOperand)
    aSource.appendChild(ast.Assignment(aLHS,aRHS))
    aSource.appendChild(ast.SubroutineCall('eliminateResidual',[util.lOf('b')]))
    return aSource
    
