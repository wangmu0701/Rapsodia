##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
# -----------------------------------------------------  #
# this AST design was derived from a code  generation    #
# step done in PETSc (see www.mcs.anl.gov/petsc)         #
##########################################################
class Node:
  def __init__(self):
    ## @var identifier
    # for anything that has a name
    self.identifier = None
    ## @var parent
    # parent node in the tree
    self.parent     = None
    ## @var children
    # list of children in the tree
    self.children   = []
    return

  def getChildren(self):
    return self.children

  def setChildren(self, children):
    ''' reset the list of children '''
    self.children = children
    for c in children:
      c.parent = self
    return

  def appendChild(self, child):
    ''' append a single child '''
    if not child is None:
      self.children.append(child)
      child.parent = self
    return

  def prependChild(self, child):
    ''' prepend a single child '''
    if not child is None:
      self.children.insert(0,child)
      child.parent = self
    return

  def copy(self):
    '''Deep copy of this node'''
    root = self.__class__()
    root.identifier = self.identifier
    root.children = [child.copy() for child in self.children]
    return root

  def accept(self, visitor):
    '''
    This method is called to act on this node with the given visitor
    It is intended to dispatch to the correct visitor callback,
    so we should not be here unless we are missing definitions
    '''
    print "undefined accept invoked for ", self, " identifier = ", self.identifier
    exit

class ObjectSource(Node):
  ''' a pair of declarations and definitions which in F90 live in a single
  module source file but in C++ are usually split into a header file and
  source files '''
  def __init__(self,aName,anObjectReferenceList):
    Node.__init__(self)
    self.identifier = aName
    self.objRefList=[]
    for i in anObjectReferenceList:
      if (isinstance(i,ObjectReference)):
        self.objRefList.append(i)
      else:
        self.objRefList.append(ObjectReference(i))
    ## @var decls
    # declarations  
    self.decls=None
    ## @var defs
    # definitions  
    self.defs=None
    self.externs=None
    self.cppOnly = False
    self.fortranOnly = False
    # fixed format F90 only
    self.fixedFormat=False
    return

  def accept(self, visitor):
    return visitor.visitObjectSource(self)

  def copy(self):
    root = Node.copy(self)
    root.objRefList=[anObjectReference.copy() for anObjectReference in self.objRefList]
    root.cppOnly = self.cppOnly 
    root.fortranOnly = self.fortranOnly 
    root.fixedFormat=self.fixedFormat
    return root

class SimpleSource(Node):
  ''' a source file; this is  a top level node '''
  def __init__(self,aFileBaseName,aFileExtension):
    Node.__init__(self)
    self.identifier = aFileBaseName
    self.extension = aFileExtension
    self.cppOnly = False
    self.fortranOnly = False
    # fixed format F90 only
    self.fixedFormat = False
    return

  def accept(self, visitor):
    return visitor.visitSimpleSource(self)

  def copy(self):
    root = Node.copy(self)
    root.extension=self.aFileExtension
    root.fortranOnly = self.fortranOnly 
    root.fortranQualifiers = self.fortranQualifiers
    root.fixedFormat=self.fixedFormat
    return root

class Include(Node):
  ''' plain include of another source file '''
  def __init__(self, aFileName):
    Node.__init__(self)
    self.identifier = aFileName
  
  def accept(self, visitor):
    return visitor.visitInclude(self)

class ObjectReference(Node):
  ''' in Fortran a USE, in C++ an include '''
  def __init__(self, identifier,qualifier=None):
    Node.__init__(self)
    self.identifier = identifier
    ##
    # in Fortran use statment module nature
    self.qualifier = qualifier
  
  def accept(self, visitor):
    return visitor.visitObjectReference(self)
  
class OverloadedSet(Node):
  ''' set of overloaded intrinsics '''
  def __init__(self,aName, anOperatorName):
    Node.__init__(self)
    self.identifier = aName
    self.operatorName = anOperatorName
  
  def accept(self, visitor):
    return visitor.visitOverloadedSet(self)

  def copy(self):
    root = Node.copy(self)
    root.operatorName = self.operatorName
    return root

class SubroutineDef(Node):
  '''
  subroutine definition;
  aName is the subroutine name
  thePseudoMangling contains the F90 extension onto the baseName for the implementing subroutine
  aParameterList consists of MethodParameters
  the children are the remaining parts of the intrinsic body
  '''
  def __init__(self,aName,thePseudoMangling,aParameterList):
    Node.__init__(self)
    self.identifier = aName
    self.pseudoMangling = thePseudoMangling
    self.parameters = aParameterList
    self.memberOf = None
    self.references = None
    self.references2 = None
    self.fortranQualifiers = None
    self.bindName=None

  def accept(self, visitor):
    return visitor.visitSubroutineDef(self)

  def copy(self):
    root = Node.copy(self)
    root.pseudoMangling = self.pseudoMangling
    root.parmeters = self.parameters
    root.memberOf = self.memberOf
    root.fortranQualifiers = self.fortranQualifiers
    root.references = self.references
    root.references2 = self.references2
    root.bindName=self.bindName
    return root

class FunctionDef(Node):
  '''
  function definition;  solely used in fortran to retrive adjoint values.
  '''
  def __init__(self,aName,returnType,aParameterList):
    Node.__init__(self)
    self.identifier = aName
    self.returnType = returnType
    self.parameters = aParameterList
    self.fortranQualifiers = None
    self.references = None
    self.references2 = None
    self.bindName=None

  def accept(self, visitor):
    return visitor.visitFunctionDef(self)

  def copy(self):
    root = Node.copy(self)
    root.returnType = self.returnType
    root.parmeters = self.parameters
    root.fortranQualifiers = self.fortranQualifiers
    root.references = self.references
    root.references2 = self.references2
    root.bindName=self.bindName
    return root

class BasicBlock(Node):
  ''' a basic block, the statements are the children '''
  def __init__(self):
    Node.__init__(self)
    self.identifier = None
  
  def accept(self, visitor):
    return visitor.visitBasicBlock(self)
  
class StatementGroup(Node):
  ''' group of statements that are not bracketed '''
  def __init__(self):
    Node.__init__(self)
    self.identifier = None
  
  def accept(self, visitor):
    return visitor.visitStatementGroup(self)
  
class IntrinsicDef(Node):
  '''
  intrinsic (function) definition;
  baseName is the built-in name or  in case of operators the name of the implementing subroutine
  thePseudoMangling contains the F90 extension onto the baseName for the implementing subroutine
  aParameterList consists of MethodParameters
  aResult is a MethodParameter
  the children are the remaining parts of the intrinsic body
  '''
  def __init__(self,baseName,thePseudoMangling,aParameterList,aResult):
    Node.__init__(self)
    self.identifier = baseName
    self.pseudoMangling = thePseudoMangling
    self.parameters = aParameterList
    self.result = aResult
    self.interface = False
    ## @var operatorName
    # the built-in operator for intrinsics of operator format
    self.operatorName = None
    self.memberOf = None
    self.ctor = False
    self.cppOnly = False
    self.fortranOnly = False
    self.fortranQualifiers = None
  
  def accept(self, visitor):
    return visitor.visitIntrinsicDef(self)

  def copy(self):
    root = Node.copy(self)
    root.pseudoMangling = self.pseudoMangling
    root.parmeters = self.parameters
    root.result = self.result
    root.operatorName = self.operatorName
    root.memberOf = self.memberOf
    root.cppOnly = self.cppOnly 
    root.fortranOnly = self.fortranOnly 
    root.fortranQualifiers = self.fortranQualifiers
    print 'in copy'+str(root.fortranQualifiers)
    return root

class Type(Node):
  ''' type '''
  def __init__(self,name):
    Node.__init__(self)
    self.baseType = True # if it is not a base type we need to wrap it in type
    self.kind = None
    self.identifier=name
    return

  def accept(self, visitor):
    return visitor.visitType(self)

  def copy(self):
    root = Node.copy(self)
    root.baseType = self.baseType
    root.kind = self.kind
    return root

class UDefType(Node):
  ''' user defined type. The children are type members if present '''
  def __init__(self,typeName):
    Node.__init__(self)
    self.identifier=typeName
    ##
    # qualifier, for example extern "C"
    self.qualifier=None
    ##
    # base type
    self.baseType=None
    self.contains=None
    return

  def accept(self, visitor):
    return visitor.visitUDefType(self)

class Declarator(Node):
  ''' declarator '''
  def __init__(self,varNamesString):
    Node.__init__(self)
    self.type = None
    self.public = False
    self.private = False
    self.const = False
    self.static = False
    self.intent = None
    self.initializer = None
    self.pointer=False
    self.identifier = varNamesString

    self.dimensions=0 #scalar, 1=vector, 2=matrix,...
    self.dimensionBounds=[]
    return

  def accept(self, visitor):
    return visitor.visitDeclarator(self)

  def copy(self):
    root = Node.copy(self)
    root.type = self.type
    root.public = self.public
    root.private = self.private
    root.const = self.const
    root.static = self.static
    root.intent = self.intent
    root.initializer = self.initializer
    return root

class Declaration(Node):
  def __init__(self, children):
    self.children = children

  def accept(self, visitor):
    return visitor.visitDeclaration(self)

class MethodParameter(Node):
  ''' a parameter in a method '''
  def __init__(self,varNamesString,aType,anIntent, dim=0, dimBounds=[]):
    Node.__init__(self)
    self.type = aType
    self.const = False
    self.intent = anIntent
    self.initializer = None
    self.valueOnly=False
    self.pointer=False
    self.identifier = varNamesString
    self.dimensions=dim #scalar, 1=vector, 2=matrix,...
    self.dimensionBounds=dimBounds
    return

  def accept(self, visitor):
    return visitor.visitMethodParameter(self)

  def copy(self):
    root = Node.copy(self)
    root.type = self.type
    root.const = self.const
    root.intent = self.intent
    root.initializer = self.initializer
    return root
 
class BinaryExpression(Node):
  def __init__(self, left, right, op):
    Node.__init__(self)
    self.identifier = op
    self.children = [left, right]

  def accept(self, visitor):
    return visitor.visitBinaryExpression(self)

class Assignment(Node):
  ''' assignment; The children are the lvalue and rvalue '''
  def __init__(self,lvalue,rvalue):
    Node.__init__(self)
    self.identifier='='
    self.setChildren([lvalue,rvalue])
  
  def accept(self, visitor):
    return visitor.visitAssignment(self)
  
class FuncCall(Node):
  ''' function call expression, children are the parameters '''
  def __init__(self,funcName,parameterList):
    self.identifier=funcName
    self.setChildren(parameterList)
  
  def accept(self, visitor):
    return visitor.visitFuncCall(self)

class SubroutineCall(Node):
  ''' function call expression, children are the parameters '''
  def __init__(self,funcName,parameterList):
    self.identifier=funcName
    self.setChildren(parameterList)
  
  def accept(self, visitor):
    return visitor.visitSubroutineCall(self)

class Equality(Node):
  '''  ==; The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='=='
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitBinaryOp(self)
  
class InEquality(Node):
  '''  !=; The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='/='
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitInEquality(self)
  
class GreaterThan(Node):
  '''  >; The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='>'
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitBinaryOp(self)
  
class GreaterThanOrEqual(Node):
  '''  >=; The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='>='
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitBinaryOp(self)
  

class LessThan(Node):
  '''  <; The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='<'
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitBinaryOp(self)

class LessThanOrEqual(Node):
  '''  <=; The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='<='
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitBinaryOp(self)

class LogicalOr(Node):
  '''  the children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='.or.'
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitLogicalOr(self)
  
class LogicalAnd(Node):
  '''  .or.; The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='.and.'
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitLogicalAnd(self)
  
class LogicalNot(Node):
  '''  .not.; The child is the subexpressions '''
  def __init__(self,expr):
    Node.__init__(self)
    self.identifier='.not.'
    self.setChildren([expr])
  
  def accept(self, visitor):
    return visitor.visitLogicalNot(self)
  
class StructDeref(Node):
  '''  .or.; The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='%'
    self.pointer = False
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitStructDeref(self)

class Group(Node):
  ''' expression grouped using parentheses '''
  def __init__(self,exprInGroup):
    Node.__init__(self)
    self.appendChild(exprInGroup)
  
  def accept(self, visitor):
    return visitor.visitGroup(self)
  
class Addition(Node):
  ''' (+) The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='+'
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitAddition(self)
  
class Constant(Node):
  ''' constant '''
  def __init__(self, theConstant):
    Node.__init__(self)
    self.identifier = theConstant
    self.kind=None # C converts floating point contants to double by default 
    return

  def accept(self, visitor):
    return visitor.visitConstant(self)

  def copy(self):
    root = Node.copy(self)
    root.kind = self.kind
    return root

class Division(Node):
  ''' (/) The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='/'
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitDivision(self)

class Power(Node):
  ''' (**) The children are the two subexpressions '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='**'
    ## @var castArg1
    # when fewer variable combinations are allowed
    # we may need to recast
    self.castArg1=None
    ## @var castArg1
    # when fewer variable combinations are allowed
    # we may need to recast
    self.castArg2=None
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitPower(self)
  
class Multiplication(Node):
  '''  (*) '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='*'
    self.setChildren([left,right])
    
  def accept(self, visitor):
    return visitor.visitMultiplication(self)

class Subtraction(Node):
  '''
  (-)
  The children are the two subexpressions
  '''
  def __init__(self,left,right):
    Node.__init__(self)
    self.identifier='-'
    self.setChildren([left,right])
  
  def accept(self, visitor):
    return visitor.visitSubtraction(self)
  

class UnaryMinus(Node):
  '''
  unary minus expression (-)
  The child is the expression whose negative is returned
  '''
  def __init__(self,operand):
    Node.__init__(self)
    self.identifier='-'
    self.appendChild(operand)
  
  def accept(self, visitor):
    '''
    Overridden to dispatch correctly
    '''
    return visitor.visitUnaryMinus(self)
  
class Variable:
  ''' variable reference, this is a leaf '''
  def __init__(self,name):
    self.identifier=name
  
  def accept(self, visitor):
    return visitor.visitVariable(self)

class TypeConversion:
  def __init__(self,identifier,toType):
    self.identifier=identifier
    self.toType=toType
  def accept(self,visitor):
    return visitor.visitTypeConversion(self)


class Array:
  ''' array reference; this is a leaf '''
  def __init__(self, name):
    self.identifier=name
    self.initializer=None
    self.size=None
    self.type=None

  def accept(self, visitor):
    return visitor.visitArray(self)

class ArrayDeref(Node):
  ''' array dereference; this is a leaf '''
  def __init__(self, name):
    Node.__init__(self)
    self.identifier = name
    self.index = None

  def accept(self, visitor):
    return visitor.visitArrayDeref(self)

class Stop:
  ''' stop statement, this is a leaf '''
  def __init__(self,errorString):
    self.identifier=errorString
  
  def accept(self, visitor):
    return visitor.visitStop(self)

class For(Node):
  ''' do loop; it has 4 children '''
  def __init__(self,loopvar,init,cond,update,body):
    Node.__init__(self)
    self.identifier=loopvar
    self.setChildren([init,cond,update,body])
    # Set slicing to True if the for loop is used for slicing.  This 
    #   effects what is printed for C++
    self.slicing = False

  def accept(self, visitor):
    return visitor.visitFor(self)

#class Increment(Node):
#  ''' Increment a simple variable '''
#  def __init__(self,variableName):
#    Node.__init__(self)
#    self.identifier=variableName
#
#  def accept(self, visitor):
#    return visitor.visitIncrement(self)
  
class If(Node):
  ''' if statement. The first child is the  condition, the second the true branch,
      the optional third child the false branch '''
  def __init__(self,aCondition, trueBranch):
    Node.__init__(self)
    self.setChildren([aCondition,trueBranch])
  
  def accept(self, visitor):
    return visitor.visitIf(self)
  
#class Return:
#  ''' return statement '''
#  def __init__(self):
#    pass
#  
#  def accept(self, visitor):
#    return visitor.visitReturn(self)
  
class Comment:
  ''' (separate) comment line '''
  def __init__(self,commentString):
    self.identifier=commentString
  
  def accept(self, visitor):
    return visitor.visitComment(self)

class GenComment(Comment): 
  ''' added to all generated files '''
  def __init__(self): 
     self.identifier="This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)" 
 
class Switch(Node):
  ''' switch statement '''
  def __init__(self,switchExpression):
    root = Node.__init__(self)
    self.appendChild(switchExpression)
  
  def accept(self, visitor):
    return visitor.visitSwitch(self)
  
class Case(Node):
  ''' case in a swicth; children are the statements in the case block '''
  def __init__(self,literal):
    root = Node.__init__(self)
    self.identifier=literal
  
  def accept(self, visitor):
    return visitor.visitCase(self)

class Cast(Node):
  def __init__(self, type, child):
    root = Node.__init__(self)
    self.type = type
    self.child = child
    self.op = ''

  def accept(self, visitor):
    return visitor.visitCast(self)

class Special(Node):
  ''' single lines of code special to the target language
      this should only be used in the language specific Printer code '''
  def __init__(self,line):
    root = Node.__init__(self)
    self.identifier=line
  
  def accept(self, visitor):
    return visitor.visitSpecial(self)

class OpenmpLoop(Node):

  def __init__(self, isOpen, isOrphaned):
    root = Node.__init__(self)
    # True if we are generating the opening openmp clause, False otherwise
    self.isOpen = isOpen
    # True if we are using orphaning
    self.isOrphaned = isOrphaned

  def accept(self, visitor):
    return visitor.visitOpenmpLoop(self)

class Address(Node):
  def __init__(self,target):
    root=Node.__init__(self)
    self.children=target

  def accept(self,visitor):
    return visitor.visitAddress(self)

