##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
# -----------------------------------------------------  #
# this class was derived from a code generation          #
# step done in PETSc (see www.mcs.anl.gov/petsc)         #
##########################################################
class DepthFirstVisitor:
  '''
  Traverses an AST in a depth first manner.
  Each AST vertex has a specific visit  method
  and the default implementation we provide
  for every language specific visitor ignores
  the given vertex and passes on to the child vertices
  '''

  def __init__(self):
    pass

  def visitChildren(self, vertex):
    '''
    default implementation for
    all vertices is to do nothing for
    vertex and visit children
    '''
    for aChild in vertex.children:
      aChild.accept(self)

  # here come all AST vertex specific default visit implementations 

  ##
  # a simple source file
  def visitSimpleSource(self, vertex):
    self.visitChildren(vertex)

  ##
  # declaration and definitions may be
  # in separate files
  def visitObjectSource(self, vertex):
    self.visitChildren(vertex)
  ##
  # a plain include
  def visitInclude(self, vertex):
    self.visitChildren(vertex)

  def visitBasicBlock(self, vertex):
    self.visitChildren(vertex)

  def visitStatementGroup(self, vertex):
    self.visitChildren(vertex)

  ##
  # a method declaration
  def visitOverloadedSet(self, vertex):
    self.visitChildren(vertex)

  ##
  # a subroutine definition
  def visitSubroutineDef(self, vertex):
    self.visitChildren(vertex)

  ##
  # a function definition
  def visitFunction(self, vertex):
    self.visitChildren(vertex)

  def visitModuleProcedure(self, vertex):
    self.visitChildren(vertex)

  def visitObjectReference(self, vertex):
    self.visitChildren(vertex)

  def visitType(self, vertex):
    self.visitChildren(vertex)

  def visitUDefType(self, vertex):
    self.visitChildren(vertex)

  def visitStruct(self, vertex):
    self.visitChildren(vertex)
  
  def visitGroup(self, vertex):
    self.visitChildren(vertex)
  
  def visitDeclarator(self, vertex):
    self.visitChildren(vertex)
  
  def visitDeclaratorGroup(self, vertex):
    self.visitChildren(vertex)
  
  def visitArray(self, vertex):
    self.visitChildren(vertex)

  def visitArrayDeref(self, vertex):
    self.visitChildren(vertex)
  
# def visitParameter(self, vertex):
#   self.visitChildren(vertex)
  
  def visitDeclaration(self, vertex):
    self.visitChildren(vertex)
  
  def visitStatement(self, vertex):
    self.visitChildren(vertex)

  def visitStructDeref(self, vertex):
    self.visitChildren(vertex)
  
  def visitCompoundStatement(self, vertex):
    self.visitChildren(vertex)
  
  def visitIf(self, vertex):
    self.visitChildren(vertex)
  
  def visitSwitch(self, vertex):
    self.visitChildren(vertex)
  
  def visitCase(self, vertex):
    self.visitChildren(vertex)
  
  def visitWhile(self, vertex):
    self.visitChildren(vertex)
  
  def visitFor(self, vertex):
    self.visitChildren(vertex)
  
  def visitIncrement(self, vertex):
    self.visitChildren(vertex)
  
# def visitGoto(self, vertex):
#   self.visitChildren(vertex)
# 
# def visitContinue(self, vertex):
#   self.visitChildren(vertex)
# 
# def visitBreak(self, vertex):
#   self.visitChildren(vertex)
# 
# def visitReturn(self, vertex):
#   self.visitChildren(vertex)
  
  def visitComment(self, vertex):
    self.visitChildren(vertex)
  
  def visitInitializer(self, vertex):
    self.visitChildren(vertex)
  
  def visitAssignment(self, vertex):
    self.visitChildren(vertex)
  
  def visitEquality(self, vertex):
    self.visitChildren(vertex)
  
  def visitAddition(self, vertex):
    self.visitChildren(vertex)
  
  def visitSubtraction(self, vertex):
    self.visitChildren(vertex)
  
  def visitMultiplication(self, vertex):
    self.visitChildren(vertex)
  
  def visitDivision(self, vertex):
    self.visitChildren(vertex)
  
  def visitModulo(self, vertex):
    self.visitChildren(vertex)
  
  def visitUnaryPlus(self, vertex):
    self.visitChildren(vertex)
  
  def visitUnaryMinus(self, vertex):
    self.visitChildren(vertex)
  
  def visitArrayReference(self, vertex):
    self.visitChildren(vertex)
  
  def visitFuncCall(self, vertex):
    self.visitChildren(vertex)
  
  def visitVariable(self, vertex):
    self.visitChildren(vertex)

  def visitArray(self, vertex):
    self.visitChildren(vertex)
  
  def visitConstant(self, vertex):
    self.visitChildren(vertex)

  def visitCast(self, vertex):
    self.visitChildren(vertex)
  
  def visitSpecial(self, vertex):
    self.visitChildren(vertex)

  def visitOpenmpLoop(self, vertex):
    self.visitChildren(vertex)
