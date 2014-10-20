##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.depthFirstVisitor
import Common.ast as ast
import Common.names as names
import Common.parameters as params
import Common.util as util

class Printer(Common.depthFirstVisitor.DepthFirstVisitor):

  def __init__(self):
    ''' initialize the printer '''
    Common.depthFirstVisitor.DepthFirstVisitor.__init__(self)
    import sys
    self.tab = '  '
    self.indentSize = 0
    self.output = sys.stdout
    ## @var typeList
    # the list of types for which we generate operations. 
    # the order is important because we use it to determine return types 
    #   of binary intrinsics
    self.typeList = []
    ## @var precDict
    # the equivalent of single and double precision for now
    # order is important here for determining return types of binary intrinsics
    # the key is used in the type specific names, in the triple, the
    # first is the built-in name, the second is for precision comparison
    # the third one is set to the generated typedef name
    self.precDict = {}
    ## @var activeTL
    # contains names for all combinations of type and kind
    self.activeTL = []
    ## @var passiveTypeList
    # the passive types that may occur in combination with active types 
    #   in binary intrinsics
    self.passiveTypeList = []
    ## @var oP
    # output path 
    self.oP = ""
    ## @var sE
    # source extension
    self.sE = "" 
    ## @var iE
    # include extension
    self.iE = "" 
    ## @var boolType
    # the name of the boolean type
    self.boolType = ""
    ## @var intType
    # the name of the int type
    self.intType = ""
    ## @var fileName
    # the fileName to be printed
    self.fileName=None
    ## @var depPairs
    # target : preequisit make deoendency pairs
    self.depPairs=[]
    ## @var objNames
    # names of object files to be compiled (without the .o extension)
    self.objNames=[]
    ##
    # types should be created to be interoperable between Fortran and C++
    self.__interoperable=False

  def setFileName(self,fileName):
    self.fileName=fileName
  
  def getFileName(self):
    return self.fileName

  def getObjNames(self):
    return self.objNames

  def addObjName(self,objName):
    self.objNames.append(objName)

  def addDep(self,target,preReq):
    self.depPairs.append((target,preReq))

  def getGenDeps(self):
    return self.depPairs

  def setInteroperable(self,interoperable):
    self.__interoperable=interoperable

  def getInteroperable(self):
    return self.__interoperable
  
  def isComplexType(self, type):
    ''' check whether a given type is complex '''
    pass

  def increaseIndent(self):
    '''
    Increase the index size by one
    '''
    self.indentSize += 1
  
  def decreaseIndent(self):
    '''
    Decrease the index size by one
    Throws an exception on a negative indent size
    '''
    self.indentSize -= 1
    if self.indentSize < 0:
      raise RuntimeError('Indent size decreased below zero: ' + 
                         str(self.indentSize))

  def indent(self):
    '''
    Output the current indent (the indent size in tabs)
    '''
    for i in range(self.indentSize):
      self.write(self.tab)

  def write(self, s):
    '''
    Output a string to stdOut 
    '''
    self.output.write(s)

  def println(self, s):
    '''
    Output a string, properly indented and followed by a newline
    '''
    self.indent()
    self.write(s + '\n')

  # AST specific visitor implementations

  def visitInclusiveOrAssignment(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitExclusiveOrAssignment(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitAndAssignment(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitLeftShiftAssignment(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitRightShiftAssignment(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitAdditionAssignment(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitSubtractionAssignment(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitMultiplicationAssignment(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitDivisionAssignment(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitModuloAssignment(self, vertex):
    self.visitBinaryExpression(vertex)

  def visitLogicalOr(self, vertex):
    self.visitBinaryExpression(vertex)

  def visitLogicalAnd(self, vertex):
    self.visitBinaryExpression(vertex)

  def visitLogicalNot(self, vertex):
    self.visitUnaryExpression(vertex)

  def visitInEquality(self, vertex):
    self.visitBinaryExpression(vertex)

  def visitPower(self, vertex):
    self.visitBinaryExpression(vertex)

  def visitBinaryOp(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitAddition(self, vertex):
    self.visitNaryExpression(vertex)
  
  def visitSubtraction(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitMultiplication(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitDivision(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitModulo(self, vertex):
    self.visitBinaryExpression(vertex)
  
  def visitUnaryPlus(self, vertex):
    self.visitUnaryExpression(vertex)
  
  def visitUnaryMinus(self, vertex):
    self.visitUnaryExpression(vertex)
  
  def visitComplement(self, vertex):
    self.visitUnaryExpression(vertex)

  def visitVariable(self, vertex):
    self.write(vertex.identifier)

  def visitConstant(self, vertex):
    if not (vertex.identifier is None):
      self.write(vertex.identifier)
    else:
      self.write(str(vertex.value)) 

  def visitUnaryExpression(self, vertex):
    children = vertex.children
    if not (len(children) == 1):
      raise RuntimeError('Unary expressions must have exactly one child')
    self.write(vertex.identifier)
    if (params.reverse):
      self.write('(')
    children[0].accept(self)
    if (params.reverse):
      self.write(')')
    return
  
  def visitGroup(self, vertex):
    children = vertex.children
    if not (len(children) == 1):
      raise RuntimeError('Grouped expressions must have exactly one child')
    self.write('(')
    children[0].accept(self)
    self.write(')')
    return
  
  def visitBinaryExpression(self, vertex):
    children = vertex.children
    if not (len(children) == 2):
      raise RuntimeError('Binary expressions must have exactly two children')
    if (params.reverse):
      self.write('(')
    children[0].accept(self)
    if (params.reverse):
      self.write(')')
    self.write(' ' + vertex.identifier + ' ')
    if (params.reverse):
      self.write('(')
    children[1].accept(self)
    if (params.reverse):
      self.write(')')
    return

  def visitNaryExpression(self, vertex):
    children = vertex.children
    if len(children) < 2:
      raise RuntimeError('Nary expressions must have at least two children')
    children[0].accept(self)
    for child in children[1:]:
      self.write(' ' + vertex.identifier + ' ')
      child.accept(self)
    return

  # misc code

  def __printDimensions(self, vertex):
    pass

  # extra generation parts not done with a single AST node

  def generatePrecisions(self):
    pass

  def generateTypes(self, sourceList):
    pass

  def generateTypeDecls(self):
    pass

  def generateTypeGetterSetterBody(self, getOrSet, aSourceNode):
    ''' the generator for the active type getter and setter method bodies '''
    # out of bounds checks
    anIf=ast.If(ast.LogicalOr(ast.LessThan(ast.Variable('direction'),
                                           ast.Constant('1')),
                                        ast.GreaterThan(ast.Variable('direction'),
                                                        ast.Constant(str(params.d)))),
                ast.Stop('RE1: Rapsodia '+getOrSet+' called with an out-of-bounds [1,' + 
                         str(params.d)+'] direction'))
    aSourceNode.appendChild(anIf)
    anIf=ast.If(ast.LogicalOr(ast.LessThan(ast.Variable('degree'),
                                           ast.Constant('1')),
                              ast.GreaterThan(ast.Variable('degree'),
                                              ast.Constant(str(params.o)))),
                ast.Stop('RE2: Rapsodia '+getOrSet+' called with an out-of-bounds [1,' + 
                         str(params.o)+'] order'))
    aSourceNode.appendChild(anIf)
    # the derived classes should fill in the rest...
    return

  def generateAsgn(self):
    pass

  def generateFPE(self, withBody, aDefinitionsSection):
    pass

  # extra methods

  def setActivePassiveTypeList(self):
    # E means explicit, which is the user used type
    if (params.Cpp) and (params.reverse):
      self.activeTL = [ (names.Fixed.rN + '%s%s' % (t,k), t, k) 
                          for t in self.typeList
                          for k,kn in self.precDict.items() ]
      
      self.activeTLE = [ (names.Fixed.pN + '%s%s' % (t,k), t, k) 
                          for t in self.typeList
                          for k,kn in self.precDict.items() ]
    else:
      self.activeTL = [ (names.Fixed.pN + '%s%s' % (t,k), t, k) 
                          for t in self.typeList
                          for k,kn in self.precDict.items() ]
  
    self.passiveTypeList = [(self.intType, None)]
    self.passiveTypeList.extend( [ (t,k) 
                                   for t in self.typeList
                                   for k,kn in self.precDict.items() ])
#    print "Printer.activeTL:", self.activeTL
#    print "Printer.passiveTypeList:", self.passiveTypeList


  def lossyAsgn(self, kl, kr, tl, tr):
    # filter out lossy assignments
    if self.precDict[kl][1] < self.precDict[kr][1]:
      # assignments to lower kinds aren't good
      return True
    if self.typeList.index(tl) < self.typeList.index(tr):
      # assignments to lower types aren't good
      return True
    return False

  # Create an iterator variable 'i' when slicing is enabled
  def setIterator(self, force=False):
    if params.slices > 0 and (not params.useQueue or force):
      iterator = ast.Declarator('i')
      iterator.type = ast.Type(self.intType)
    else:
      iterator = None
    return iterator
