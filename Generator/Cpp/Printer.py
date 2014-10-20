##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
# -----------------------------------------------------  #
# this class was derived from a code generation          #
# step done in PETSc (see www.mcs.anl.gov/petsc)         #
##########################################################
import Common.Printer as BasePrinter
import Common.ast as ast
import Common.names as names
import Common.parameters as params
import Common.util as util
import Cpp.QueueUtils as queue

class CppPrinter(BasePrinter.Printer):
  ''' prints the AST to standard output as C++ source '''

  def __init__(self):
    ''' initialize the C++ printer '''
    BasePrinter.Printer.__init__(self)
    self.typeList = ['float']
    self.precDict = {'S':('float',1,''),'D':('double',2,'')}
    if (params.doubleOnly):
      self.precDict = {'D':('double',1,'')}

    self.oP="TestLib/Cpp"
    self.sE=".cpp" 
    ## @var hE
    # header file extension
    self.hE=".hpp" 
    self.iE=".ipp" 
    self.boolType='bool'
    self.intType = 'int'
    ## @var inlineDefs
    # use the inline directive and include the source files in the header
    self.inlineDefs=False
    self.setActivePassiveTypeList()
 
  def isComplexType(self,aParameter):
    ''' no complex type in C++, so returns false '''
    return False

  def isFourByteType(self,aParameter):
    if (aParameter.type.baseType
        and
        (aParameter.type.identifier == 'float'
         and
         aParameter.type.kind == 'float')
        or
        (aParameter.type.identifier == 'int')):
      return True
    if (not aParameter.type.baseType):
      for n,t,k in self.activeTL:
        if (aParameter.type.identifier == n):
          return (self.precDict[k][0] == 'float')
    return False    

  # here come all the AST specific visitor implementations
  # that need to override the default in DepthFirstVisitor

  def visitInclude(self, vertex):
    self.addDep(self.getFileName(),vertex.identifier)
    self.println('#include \"'+vertex.identifier+'\"')
  
  def visitObjectReference(self, vertex):
    # filter out assignment references which are Fortran only.
    if (vertex.identifier!=names.Fixed.pN+'asgn'):
      self.addDep(self.getFileName(),vertex.identifier+self.hE)
      self.println('#include \"'+vertex.identifier+self.hE+'\"')

  def visitBasicBlock(self, vertex):
    self.println('{')
    self.increaseIndent()
    self.visitChildren(vertex)
    self.decreaseIndent()
    self.println('}')

  def visitSubroutineDef(self, vertex):
    vertex.result.type.accept(self)
    self.write(' '+vertex.identifier+'(')
    for (c,p) in enumerate(vertex.parameters):
      if (c!=0):
        self.write(', ')
      p.type.accept(self)
      self.write(' '+p.identifier)
    self.write(')')
    if vertex.children:
      self.write(' {\n')
      self.increaseIndent()
      for child in vertex.children:
        child.accept(self)
      self.decreaseIndent()
      self.indent()
      self.write('}\n')
    self.write('\n')

  def visitIntrinsicDef(self, vertex):
    theName=vertex.identifier
    # sort out special cases
    # which are not defined in the language standard
    if (theName in ['abs']):
      # in Fortran this is an intrinsic but in C++
      # this is a cast that should rather be coded
      # by explicitly calling getVal()
      theName='f'+theName
    # only use pow with doubles
    if ((theName in ['pow'])
        and
        (self.isFourByteType(vertex.parameters[0])
         or
         self.isFourByteType(vertex.parameters[1]))):
      # skip these
      return
    self.indent()
    if self.inlineDefs:
      self.write('inline ')
    # deal with the result type:
    if not vertex.ctor:
      # otherwise it is ctor
      if vertex.result is None:
        self.write('void')
      else:
        if vertex.result.const:
          self.write('const ')
        vertex.result.type.accept(self)
        if not(vertex.result.intent is None):
          if (vertex.result.intent=='out'
              or
              vertex.result.intent=='inout') :
            self.write('&')
      self.write(' ')
    if vertex.memberOf:
      self.write(vertex.memberOf+'::')  
    if (vertex.operatorName):
      if (theName=='pow'):
        self.write(theName)
      elif (vertex.operatorName=='\='):
        self.write('operator !=')
      else:  
        self.write('operator '+vertex.operatorName)
    else:
        self.write(theName)
    self.write('(')
    for (c,p) in enumerate(vertex.parameters):
      if (c!=0):
        self.write(', ')
      p.accept(self)
    self.write(')')
    if vertex.children:
      self.write(' {\n')
      self.increaseIndent()
      if not vertex.result is None and vertex.result.identifier != '*this':
        self.indent()
        vertex.result.accept(self)
        self.write(';\n')
      for child in vertex.children:
        child.accept(self)
      if not vertex.ctor and not vertex.result is None:
        # otherwise it is ctor
        self.println('return '+vertex.result.identifier+';')
      self.decreaseIndent()
      self.write('}\n')
    else:
      self.write(';')
    self.write('\n')

  def visitMethodParameter(self, vertex):
    if vertex.const or vertex.intent == 'in':
      self.write('const ')
    vertex.type.accept(self)
    if not(vertex.intent is None):
      if (vertex.intent=='out'
          or
          vertex.intent=='inout'
          or 
          vertex.intent=='in'):
        self.write('&')
    if (vertex.pointer):
      self.write('*')
    self.write(' '+vertex.identifier)
    if (vertex.dimensions > 0):
      self.__printDimensions(vertex)
    if vertex.initializer:
      self.write(' = ')
      vertex.initializer.accept(self)

  def visitType(self, vertex):
    if vertex.kind:
      self.write(vertex.kind)
    else:
      self.write(vertex.identifier)
  
  def visitTypeConversion(self, vertex):
    vertex.identifier.accept(self)

  def visitUDefType(self, vertex):
    self.indent()
    if vertex.qualifier:
      self.write(vertex.qualifier+" ")
    self.write('class '+vertex.identifier)
    if vertex.baseType:
      self.write(" : public "+vertex.baseType)    
    self.write(' {\n')
    self.increaseIndent()
    self.write('public:\n')
    if vertex.children:
      self.visitChildren(vertex)
    self.decreaseIndent()
    self.println('};')
  
  def visitDeclarator(self, vertex):
    self.indent()
    if vertex.static:
      self.write('static ')
    if vertex.const:
      self.write('const ')
    vertex.type.accept(self)
    if not(vertex.intent is None):
      if (vertex.intent=='out'
          or
          vertex.intent=='inout') :
        self.write('&')
    self.write(' ')
    self.write(vertex.identifier)
    if (vertex.dimensions > 0):
      self.__printDimensions(vertex)
    if vertex.initializer:
      self.write(' = ')
      vertex.initializer.accept(self)
    self.write(';\n')  
 
  def visitArray(self, vertex):
    if not (vertex.type is None):
      vertex.type.accept(self)
    self.write(vertex.identifier)
    self.write('[')
    if vertex.size:
      vertex.size.accept(self)
    self.write(']')
    if vertex.initializer:
      self.write(' = ')
      vertex.initializer.accept(self)

  def visitArrayDeref(self, vertex):
    self.write(vertex.identifier)
    self.write('[')
    if isinstance(vertex.index, ast.Constant):
      self.write(str(int(vertex.index.identifier)-1))
    elif isinstance(vertex.index, ast.Variable):
      vertex.index.accept(self)
    else:
      raise Exception('Index type in '+repr(vertex)+' must be either ast.Constant or ast.Variable but instead is ' +str(type(vertex.index)))
    self.write(']')
  
# def visitParameter(self, vertex):
#   self.writeComments(vertex)
#   vertex.type.accept(self)
#   if vertex.identifier:
#     if not (isinstance(vertex.type, Pointer)):
#       self.write(' ')
#     self.write(vertex.identifier)
  
  def visitDeclaration(self, vertex):
    self.indent()
    for child in vertex.children:
      child.accept(self)
      self.write(';\n')
  
  def visitIf(self, vertex):
    self.indent()
    self.write('if (')
    vertex.children[0].accept(self)
    self.write(')\n')
    self.increaseIndent()
    vertex.children[1].accept(self)
    self.decreaseIndent()
    if len(vertex.children) > 2:
      self.println('else')
      self.increaseIndent()
      vertex.children[2].accept(self)
      self.decreaseIndent()
  
  def visitSwitch(self, vertex):
    self.indent()
    self.write('switch(')
    vertex.children[0].accept(self)
    self.write(') {\n')
    self.increaseIndent()
    for child in vertex.children[1:]:
      child.accept(self)
    self.decreaseIndent()
    self.println('}')

  def visitCase(self, vertex):
    self.println('case '+vertex.identifier+':')
    self.increaseIndent()
    for caseChild in vertex.children:
      caseChild.accept(self)
      self.println('break;')
    self.decreaseIndent()

  def visitWhile(self, vertex):
    if vertex.getDoWhile():
      self.println('do')
      self.visitChildren(vertex)
      self.indent()
      self.write('while(')
      vertex.getBranch().accept(self)
      self.write(')\n')
    else:
      self.indent()
      self.write('while(')
      vertex.getBranch().accept(self)
      self.write(')\n')
      self.visitChildren(vertex)
  
  def visitFor(self, vertex):
    if vertex.slicing:
      for i in [0, 1]:
        vertex.children[i].identifier = \
            str(int(vertex.children[i].identifier) - 1)
    self.indent()
    self.write('for(')
    # the initialization
    self.write(vertex.identifier + '=')
    vertex.children[0].accept(self)
    self.write(';')
    # the condition
    self.write(vertex.identifier + '<=')
    vertex.children[1].accept(self)
    self.write(';')
    # the update
    self.write(vertex.identifier+'+=')
    vertex.children[2].accept(self)
    self.write(')\n')  
    # the body  
    self.increaseIndent()
    vertex.children[3].accept(self)
    self.decreaseIndent()
  
# def visitGoto(self, vertex):
#   self.println('goto ' + vertex.identifier + ';')
# 
# def visitContinue(self, vertex):
#   self.indent()
#   if not (vertex.identifier is None):
#     self.write(vertex.identifier + ': ')
#   self.write('continue;\n')
# 
# def visitReturn(self, vertex):
#   self.indent()
#   if not (vertex.identifier is None):
#     self.write(vertex.identifier + ': ')
#   self.write('return')
#   if len(vertex.children):
#     self.write(' ')
#     self.visitChildren(vertex)
#   self.write(';\n')
  
  def visitComment(self, vertex):
    self.println('// '+vertex.identifier)

# def visitInitializer(self, vertex):
#   num = len(vertex.children)
#   nested = (not (vertex.parent is None) and isinstance(vertex.parent, Initializer))
#   if num > 1:
#     self.write('{')
#     self.increaseIndent()
#     if not (nested):
#       self.write('\n')
#       self.indent()
#     for (c, child) in enumerate(vertex.children):
#       if not (nested):
#         if c > 0:
#           self.indent()
#       child.accept(self)
#       if nested:
#         if c < (num - 1):
#           if not (isinstance(child, Macro)):
#             self.write(',')
#           self.write(' ')
#       else:
#         if c < (num - 1):
#           if not (isinstance(child, Macro)):
#             self.write(',')
#           self.write('\n')
#     self.decreaseIndent()
#     self.write('}')
#   elif vertex.getList():
#     self.write('{')
#     vertex.children[0].accept(self)
#     self.write('}')
#   else:
#     self.visitChildren(vertex)
  
  def visitAssignment(self, vertex):
    self.indent()
    vertex.children[0].accept(self)
    self.write(' %s ' % vertex.identifier)
    vertex.children[1].accept(self)
    self.write(';\n')

  def visitStructDeref(self, vertex):
    vertex.children[0].accept(self)
    if vertex.pointer:
      self.write('->')
    else:
      self.write('.')
    vertex.children[1].accept(self)

  def visitLogicalOr(self, vertex):
    vertex.identifier='||'
    self.visitBinaryExpression(vertex)

  def visitLogicalAnd(self, vertex):
    vertex.identifier='&&'
    self.visitBinaryExpression(vertex)

  def visitLogicalNot(self, vertex):
    vertex.identifier='!'
    self.visitUnaryExpression(vertex)

  def visitInEquality(self, vertex):
    vertex.identifier='!='
    self.visitBinaryExpression(vertex)

  def visitPower(self, vertex):
    # this is not defined for integer arguments in C++
    # we do conversion if permitted
    self.write('pow(')
    for (c, argument) in enumerate(vertex.children):
      if (c!=0):
        self.write(', ')
      if ((c==0 and vertex.castArg1)
          or
          (c==1 and vertex.castArg2)):
        self.write('double(')
      argument.accept(self)
      if ((c==0 and vertex.castArg1)
          or
          (c==1 and vertex.castArg2)):
        self.write(')')
    self.write(')')

# def visitIncrement(self, vertex):
#   self.write(vertex.identifier+'='+vertex.identifier+'+1')
  
  def visitArrayReference(self, vertex):
    self.visitChildren(vertex)
    self.write('[')
    vertex.getIndex().accept(self)
    self.write(']')
  
  def visitFuncCall(self, vertex):
    if (vertex.identifier=='real'):
      # special case
      self.visitChildren(vertex)
    else:
      name=vertex.identifier
      if (name in ['max', 'min']):
        self.write('((')
        vertex.children[0].accept(self)
        if name=='max':
          self.write('>')
        else :
          self.write('<')
        vertex.children[1].accept(self)
        self.write(')?')
        vertex.children[0].accept(self)
        self.write(':')
        vertex.children[1].accept(self)
        self.write(')')
      else :
        if (name in ['abs']):
          name='f'+name
        self.write(name+'(')
        for (c, argument) in enumerate(vertex.children):
          if (c!=0):
            self.write(', ')
          argument.accept(self)
        self.write(')')
#      self.write(';\n')

  def visitSubroutineCall(self, vertex):
    self.indent()
    if (vertex.identifier=='real'):
      # special case
      self.visitChildren(vertex)
    else:
      name=vertex.identifier
      if (name in ['max', 'min']):
        self.write('((')
        vertex.children[0].accept(self)
        if name=='max':
          self.write('>')
        else :
          self.write('<')
        vertex.children[1].accept(self)
        self.write(')?')
        vertex.children[0].accept(self)
        self.write(':')
        vertex.children[1].accept(self)
        self.write(')')
      else :
        if (name in ['abs']):
          name='f'+name
        self.write(name+'(')
        for (c, argument) in enumerate(vertex.children):
          if (c!=0):
            self.write(', ')
          argument.accept(self)
        self.write(')')
      self.write(';\n')
  
  def visitStop(self, vertex):
    self.println('{std::cerr << \"'+vertex.identifier+'\"; exit(-1);}')

  def visitConstant(self, vertex):
    if not (vertex.identifier is None):
      self.write(vertex.identifier)
    else:
      self.write(str(vertex.value))
    if ((not (vertex.kind is None))
        and 
        vertex.kind =='float'):
      self.write('F')
      # indicate to the compiler to take this as a float constant
      # rather than the default double type for constants
  
  def visitObjectSource(self,vertex): 
    self.visitObjectDecls(vertex)
    self.visitObjectDefs(vertex)

  def visitObjectDecls(self,vertex): 
    self.increaseIndent()
    for child in vertex.objRefList:
      child.accept(self)
    self.visitChildren(vertex.decls)
    self.decreaseIndent()

  def visitObjectDefs(self,vertex):
    self.println('#include <iostream>')
    self.println('#include <cstdlib>')
    self.println('#include <cmath>')
    if params.useOpenmp:
      self.println('#include <omp.h>')
    if (not self.inlineDefs):
      self.addDep(self.getFileName(),vertex.identifier+self.hE)
      self.println('#include \"'+vertex.identifier+self.hE+'\"')
    self.println('')
    if (vertex.defs) : 
      self.visitChildren(vertex.defs)

  def visitCast(self, vertex):
    self.write('(')
    vertex.type.accept(self)
    self.write(vertex.op + ') ')
    vertex.child.accept(self)

  def visitSpecial(self,vertex):
    self.println(vertex.identifier)

  def visitOpenmpLoop(self, vertex):
    if vertex.isOpen:
      if vertex.isOrphaned:
        self.println('#pragma omp for schedule(static, %d)' 
            % params.openmpChunkSize)
      else:
        self.println('#pragma omp parallel for schedule(static, %d) '
                     'num_threads(%d)' 
            % (params.openmpChunkSize, params.slices))

  # misc code

  def __printDimensions(self, vertex):
    if vertex.dimensions > 2:
      raise Exception('cannot declare array larger than 2 dimensions in c++')
    dimBoundList = iter(vertex.dimensionBounds)
    for dimBound in dimBoundList:
      self.write('[')
      dimBound.accept(self)
      self.write(']')
    return

  # extra generation parts not done with a single AST node 

  def generatePrecisions(self):
    ''' top level generator for the precision type definition '''
    aSource = ast.SimpleSource(names.Fixed.precDeclN,self.hE)
    for  k,kv in self.precDict.items():
      tdName=names.Fixed.pN+k+'prec'
      aSpecialLine=ast.Special('typedef '+kv[0]+' '+tdName+';') 
      aSource.appendChild(aSpecialLine)
      # replace with new entry
      self.precDict[k]=(kv[0],kv[1],tdName)
    return aSource
  
  def generateTypes(self,sourceList):
    ''' top level generator for the type module '''
    aSource = ast.ObjectSource(names.Fixed.typeDeclN,
                               [names.Fixed.precDeclN])
    aSource.decls=self.generateTypeDecls()
    aSource.defs=self.generateTypeDefinitions(sourceList)
    return aSource

  def generateTypeDecls(self):
    ''' generator for the type declarations '''
    aDeclsGroup = ast.StatementGroup()

    # When using queuing, define RA_USE_QUEUE for user's use
    if params.useQueue:
      aDeclsGroup.appendChild(ast.Include('defines.hpp'))
      aDeclsGroup.appendChild(ast.Include('ActiveTypeQueue.hpp'))
      aDeclsGroup.appendChild(ast.Special('#ifndef RA_USE_QUEUE'))
      aDeclsGroup.appendChild(ast.Special('#define RA_USE_QUEUE'))
      aDeclsGroup.appendChild(ast.Special('#endif'))

    # the type definitions (i.e. RAfloatS / RAfloatD structs)
    for n,t,k in self.activeTL :

      aDeclsGroup.appendChild(ast.Comment(n))

      aType = ast.Type(t)
      aType.kind = self.precDict[k][0]

      # If we are using slices, generate the necessary slice types
      if params.slices > 0:
        sliceName = 'Slice' + k
        sliceDefType = ast.UDefType(sliceName)
        for i in names.Variable.dN:
          for j in i:
            aDeclarator = ast.Declarator(j)
            aDeclarator.type = aType
            sliceDefType.appendChild(aDeclarator)

        aDeclsGroup.appendChild(sliceDefType)


      structName = util.getVarStructName(n)
      aUDefType = ast.UDefType(structName)

      if params.slices > 0:
#       if params.useQueue:
#         # If using a queue, add slice information directly into struct
#         #   instead of creating a separate Slice struct
#         util.appendDirDecls(aType, aUDefType)
#       else:
          # Generate slice udef
          sliceName = util.getVarSliceName(n) #'Slice' + k
          sliceDefType = ast.UDefType(sliceName)
          util.appendDirDecls(aType, sliceDefType)
          aDeclsGroup.appendChild(sliceDefType)
          # Add slice array to main udef
          sliceDeclarator = ast.Declarator(names.Fixed.sN)
          sliceDeclarator.dimensions = 1
          sliceDeclarator.dimensionBounds.append(ast.Constant(str(params.slices)))
          sliceDeclarator.type = ast.Type(sliceName)
          aUDefType.appendChild(sliceDeclarator)
      else:
        util.appendDirDecls(aType, aUDefType)
      aDeclsGroup.appendChild(aUDefType)

      value = ast.Declarator(names.Fixed.vN)
      value.type = aType

      # if we are using a queue, create the *real* active type now
      #   (i.e., rather than the one with the var struct name)
      if params.useQueue:
        aUDefType = ast.UDefType(n)
        aUDefType.appendChild(ast.Special('~'+n+'();')) # destructor
        location = ast.Declarator('loc')
        location.type = ast.Type('locint')
        aUDefType.appendChild(location)
        if params.temporariesBug:
          location = ast.Declarator('isTemp')
          location.type = ast.Type('bool')
          aUDefType.appendChild(location)
        aDeclsGroup.appendChild(aUDefType)
        # create a struct to store the value of the active type
        valDefType = ast.UDefType(util.getVarValueName(n))
        valDefType.appendChild(value)
        aDeclsGroup.appendChild(valDefType)

      aUDefType.prependChild(value)

      if (self.getInteroperable()):
        # adorn the type build so far as an extern C type
        aUDefType.qualifier="extern \"C\""
        origName=aUDefType.identifier
        cName=origName+"_C"
        aUDefType.identifier=cName
        # make a new type inheriting from the C type
        aUDefType=ast.UDefType(origName)
        aUDefType.baseType=cName
        aDeclsGroup.appendChild(aUDefType)

      if (params.disableInit and not params.useQueue) :
        aUDefType.appendChild(ast.Special(n+'(){};'))   # constructor
      else : 
        aUDefType.appendChild(ast.Special(n+'();'))   # constructor

      if params.openmpUseOrphaning:
        aDeclsGroup.appendChild(
            ast.Special('namespace %sPrec {\n'
                        '    extern %s rGlobal;\n'
                        '    extern %s cGlobal;\n'
                        '    extern %s sGlobal;\n'
                        '  }' % (n, structName, structName, structName)))
        

      self.generateTypeGetter(False,n,t,k,aUDefType)
      self.generateTypeSetter(False,n,t,k,aUDefType)
      self.generateCopies(False,None,'=',n,t,k,aUDefType) # assignments
      self.generateCopies(False,n,None,n,t,k,aUDefType) # copy constructor
#      self.generateValueCopies(False,None,'=',n,t,k,aUDefType) #value Copy
      pasDecl=ast.Declarator("arrSz")
      pasDecl.type=ast.Type("unsigned int") 
      pasDecl.const=True
      pasDecl.static=True
      pasDecl.initializer=ast.Constant(str(1+(params.o*params.d)))
      aUDefType.appendChild(pasDecl)
      self.generateToFromArrayDecl(n,t,k,aUDefType,'to')
      self.generateToFromArrayDecl(n,t,k,aUDefType,'from')
    self.generateFPE(False,aDeclsGroup)
    return aDeclsGroup

  def generateAsgn(self):
    ''' not used in C++, so returns None '''
    ''' top level generator for the assignment module '''
#    aSource = ast.ObjectSource(names.Fixed.pN+'asgn',
#                               [names.Fixed.precDeclN,
#                                names.Fixed.typeDeclN])
#    aSource.decls=ast.OverloadedSet('asgn','=')
#    self.generateAsgnDefinitions(False,aSource.decls)
#    aSource.defs=ast.StatementGroup()
#    self.generateAsgnDefinitions(True,aSource.defs)
#    return aSource
    return None

  def generateValueCopies(self,withBody,ctorName,operatorName,activeName,type,
                     kind,aDefinitionsBlock):
    ''' generate the assignment definitions '''

    # passive/active combinations
    for (tl,kl) in self.passiveTypeList :
      if (tl!=type):
        continue
      if (kl is None):
        continue
      if self.lossyAsgn(kl, kind, tl, type):
        continue
      pName=tl+kind+activeName
      aParameterList=[]  
      # the active result
      # determine the result type
      aType=ast.Type(tl)
      if not(kl is None):
        aType.kind=self.precDict[kl][0]
      aReturn=ast.MethodParameter('r',aType,None)
      aReturn.const=True
      aReturn.intent='inout'
#        aParameterList.append(ast.MethodParameter('l',aType,'inout'))
        # the passive argument
      aType=ast.Type(activeName)
      aType.baseType=False
      aParameterList.append(ast.MethodParameter('r',aType,'in'))
#        aFunction=ast.FunctionDef(names.Fixed.pN+'asgn',pName,aParameterList)
      aFunction=ast.IntrinsicDef(names.Fixed.pN+'asgn', None, aParameterList, aReturn)
      aFunction.operatorName='='
      if withBody:
        aFunction.memberOf=activeName
        aFunction.appendChild(ast.Include(names.Fixed.pN+'asgnPA'+self.iE))
      aDefinitionsBlock.appendChild(aFunction)


  def generateCopies(self,withBody,ctorName,operatorName,activeName,type,
                     kind,aDefinitionsSection):
    ''' generate an assignment for LHS with type activeName '''

    activeType = ast.Type(activeName)
    activeType.baseType = False

    def __genIntrinsicDefForCopies(paramType):
      anArgument = ast.MethodParameter('r', paramType, None)
      anArgument.const = True
      anArgument.intent = 'inout'
      if params.useQueue:
        aReturn = ast.MethodParameter('*this', activeType, None)
      else:
        aReturn = ast.MethodParameter('ret', activeType, None)
        aReturn.initializer = ast.Variable('*this')
      aReturn.const = True
      aReturn.intent = 'inout'
      aCopyDef = ast.IntrinsicDef(ctorName, None, [anArgument], aReturn)
      aCopyDef.operatorName = operatorName
      if ctorName:
        aCopyDef.ctor = True
      return aCopyDef

    if withBody:
      def __genBodyForCopies(activeOrPassive, body):
        aLHS = ast.Declarator('l')
        aLHS.type = activeType
        aLHS.intent = 'inout'
        aLHS.initializer = ast.Variable('*this')
        body.appendChild(aLHS)
        body.appendChild(self.setIterator())
        body.appendChild(ast.Include(names.Fixed.pN + 'asgn' + 
                                     activeOrPassive + self.iE))

    # active right hand sides:
    for (nr,tr,kr) in self.activeTL:
      # if useQueue and not temporariesBug we can skip the identical copy ctors
      # if not useQueue (implies temporariesBug false)  we skip identical copy ctors and assignments
      # because the compiler generated ones should be faster. 

#original code begins
      if (nr == activeName # same type
          and
          ((not (ctorName is None)) # is a ctor
           or
           not (params.useQueue)) # not using the queue
          and
          not params.temporariesBug): # don't have to deal with temporariesBug
        continue


      if self.lossyAsgn(kind, kr, type, tr):
        continue
      aCopyDef = __genIntrinsicDefForCopies(ast.Type(nr))
      if withBody:  
        aCopyDef.memberOf = activeName
        if params.useQueue:
          if operatorName is None:
            queue.generateCopyConstructor(activeName, kind, aCopyDef,True)
          else:
            queue.generateAsgnA(self,kind, aCopyDef)
        else:
          __genBodyForCopies('A', aCopyDef)
      aDefinitionsSection.appendChild(aCopyDef)

    # and now the same for passive right hand sides:   
    for (tr,kr) in self.passiveTypeList:
      if not (kr is None):
        if self.lossyAsgn(kind, kr, type, tr):
          continue
      aType = ast.Type(tr)
      if not (kr is None):
        aType.kind = self.precDict[kr][0]
      aCopyDef = __genIntrinsicDefForCopies(aType)
      if withBody:
        aCopyDef.memberOf = activeName
        if params.useQueue:
          if operatorName is None:
            queue.generateCopyConstructor(activeName, kind, aCopyDef,False)
          else:
            queue.generateAsgnP(self,activeName,kind, aCopyDef)
        else:
          __genBodyForCopies('P', aCopyDef)
      aDefinitionsSection.appendChild(aCopyDef)

  def generateTypeGetter(self,withBody,activeName,type,kind,
                         aDefinitionsSection):
    # the generic getters
    aParameterList=[]
    # parameter declarations
    aParameterList.append(ast.MethodParameter('direction',ast.Type('int'),'in'))
    aParameterList.append(ast.MethodParameter('degree',ast.Type('int'),'in'))
    # the return type
    aType=ast.Type(type)
    aType.kind=self.precDict[kind][0]
    aGetterDef=ast.IntrinsicDef('get',None,aParameterList,
                                ast.MethodParameter('passive',aType,None))
    if withBody:
      aGetterDef.memberOf = activeName
      if params.useQueue:
        queue.appendGetLocation('r', activeName, kind, 'loc', 
                                True, aGetterDef, isObj=True, getSlice=False)
        funcPtr = ast.StructDeref(ast.Variable('ActiveTypeQueue::atQueue'),
                                  ast.FuncCall('blockUntilEmpty', []))
        funcPtr.pointer = True
        aGetterDef.appendChild(ast.Declaration([funcPtr]))

      aGetterDef.appendChild(ast.Include(names.Fixed.pN+'get'+self.iE))
    aDefinitionsSection.appendChild(aGetterDef)

  def generateTypeSetter(self,withBody,activeName,type,kind,
                         aDefinitionsSection):
    # the generic setters
    aParameterList=[]
    # parameter declarations
    aParameterList.append(ast.MethodParameter('direction',ast.Type('int'),'in'))
    aParameterList.append(ast.MethodParameter('degree',ast.Type('int'),'in'))
    # the passive type
    aType=ast.Type(type)
    aType.kind=self.precDict[kind][0]
    aParameterList.append(ast.MethodParameter('passive',aType,'in'))
    aSetterDef=ast.IntrinsicDef('set',None,aParameterList,None)
    if withBody:  
      aSetterDef.memberOf = activeName
      if params.useQueue:
        queue.appendGetLocation('r', activeName, kind, 'loc', 
                                False, aSetterDef, isObj=True, getSlice=False)
      aSetterDef.appendChild(ast.Include(names.Fixed.pN+'set'+self.iE))
    aDefinitionsSection.appendChild(aSetterDef)

  def generateDefaultConstructor(self,name, type, kind, body):
      if params.useQueue:
        queue.generateDefaultConstructor(self,name,kind,body)
      else :
        if (not params.disableInit) :
          ctor = ast.IntrinsicDef(name, None, [], None)
          ctor.ctor = True
          ctor.memberOf = name
          aLHS = ast.Declarator('l')
          aLHS.type = ast.Type(name)
          aLHS.intent = 'inout'
          aLHS.initializer = ast.Variable('*this')
          ctor.appendChild(aLHS)
          aRHS = ast.Declarator('r')
          aRHS.type = ast.Type(type)
          aRHS.type.kind=self.precDict[kind][0]
          aRHS.const = True
          aRHS.initializer = ast.Constant('0.0')
          aRHS.initializer.kind=self.precDict[kind][0]
          ctor.appendChild(aRHS)
          ctor.appendChild(self.setIterator())
          ctor.appendChild(ast.Include(names.Fixed.pN + 'asgn' + 'P' + self.iE))
          body.appendChild(ctor)

  def generateTypeDefinitions(self,sourceList):
    ''' generator for the type module definitions '''
    aDefinitionsSection=ast.StatementGroup()

    if params.useQueue:
      aDefinitionsSection.appendChild(ast.Include('WorkArray.hpp'))
      queue.generateStaticQueue(aDefinitionsSection)
      # Initialize work arrays
      for n,t,k in self.activeTL:
        queue.generateStaticObjects(n, k, aDefinitionsSection)
      # Generate assignment functions
      queue.genUnaryMethod(self, 'asgnA', names.Fixed.pN + 'asgnA', 'l', 
                           [], [], aDefinitionsSection)

    # the generic getter/setters
    for n,t,k in self.activeTL :

      if params.openmpUseOrphaning:
        structName = util.getVarStructName(n)
        aDefinitionsSection.appendChild(
          ast.Special('%s %sPrec::rGlobal;\n'
                      '%s %sPrec::cGlobal;\n'
                      '%s %sPrec::sGlobal;\n' 
                      % (structName, n, structName, n, structName, n)))
      if (not self.inlineDefs):
          pasDecl=ast.Declarator(n+"::arrSz")
          pasDecl.type=ast.Type("unsigned int") 
          pasDecl.const=True
          aDefinitionsSection.appendChild(pasDecl)
      self.generateDefaultConstructor(n,t,k,aDefinitionsSection)
      self.generateTypeSetter(True,n,t,k,aDefinitionsSection)
      self.generateTypeGetter(True,n,t,k,aDefinitionsSection)
      self.generateCopies(True,None,'=',n,t,k,aDefinitionsSection) # assignments
      self.generateCopies(True,n,None,n,t,k,aDefinitionsSection) # copy constructor
#      self.generateValueCopies(True,None,'=',n,t,k,aDefinitionsSection) #value Copy
      self.generateToFromArray(n,t,k,aDefinitionsSection,'to')
      self.generateToFromArray(n,t,k,aDefinitionsSection,'from')
    # make the subroutine bodies as includes  
    anIncludeSource=ast.SimpleSource(names.Fixed.pN+'set', self.iE)
    self.generateTypeGetterSetterBody('set',anIncludeSource)
    sourceList.append(anIncludeSource)
    anIncludeSource=ast.SimpleSource(names.Fixed.pN+'get', self.iE)
    self.generateTypeGetterSetterBody('get',anIncludeSource)
    sourceList.append(anIncludeSource)
    anIncludeSource=ast.SimpleSource(names.Fixed.pN+'toArray', self.iE)
    self.generateToFromArrayBody('to',anIncludeSource)
    sourceList.append(anIncludeSource)
    anIncludeSource=ast.SimpleSource(names.Fixed.pN+'fromArray', self.iE)
    self.generateToFromArrayBody('from',anIncludeSource)
    sourceList.append(anIncludeSource)
    self.generateFPE(True,aDefinitionsSection)
    return aDefinitionsSection

  def generateToFromArrayDecl(self,n,t,k,aDeclarationSection,toFrom):
      pType=ast.Type(t)
      pType.kind=self.precDict[k][0]
      anArgument = ast.MethodParameter('arr', pType, None, 1,[ast.Variable("arrSz")])
      aDecl = ast.IntrinsicDef(toFrom+"Array", None, [anArgument], None)
      aDeclarationSection.appendChild(aDecl)
      return aDecl

  def generateToFromArray(self,n,t,k,aDefinitionsSection,toFrom):
      pType=ast.Type(t)
      pType.kind=self.precDict[k][0]
      anArgument = ast.MethodParameter('arr', pType, None, 1,[ast.Variable(n+"::arrSz")])
      aDef = ast.IntrinsicDef(toFrom+"Array", None, [anArgument], None)
      aDef.memberOf=n
      activeVarRef=None
      if params.useQueue:
        if (toFrom=="to"):
          queue.appendGetLocation('l', n, k, 'loc', 
                                  True, aDef, isObj=True, getSlice=False)
          funcPtr = ast.StructDeref(ast.Variable('ActiveTypeQueue::atQueue'),
                                    ast.FuncCall('blockUntilEmpty', []))
          funcPtr.pointer = True
          aDef.appendChild(ast.Declaration([funcPtr]))
        else:
          queue.appendGetLocation('l', n, k, 'loc', 
                                  False, aDef, isObj=True, getSlice=False)
        activeVarRef = ast.Variable(names.Fixed.vN)
      else: 
        lVarDecl = ast.Declarator('l')
        lVarDecl.type = ast.Type(n)
        lVarDecl.intent = 'inout'
        lVarDecl.initializer = ast.Variable('*this')
        aDef.appendChild(lVarDecl)
        activeVarRef = util.vOf('l')
      arrDeref = ast.ArrayDeref('arr')
      arrDeref.index=ast.Constant(1)
      if (toFrom=='to') : 
        aDef.appendChild(ast.Assignment(arrDeref,activeVarRef))
      else:
        aDef.appendChild(ast.Assignment(activeVarRef,arrDeref))
      aDef.appendChild(ast.Include(names.Fixed.pN + toFrom + 'Array' + self.iE))
      aDefinitionsSection.appendChild(aDef)
      return aDef

  def generateToFromArrayBody(self,toFrom,aSourceNode):
    arrIndex=2;
    for direct in range(1,params.d+1,1):
      for deg in range(1,params.o+1,1):
        activeVarRef = util.dOfC('l', direct, deg)
        arrDeref = ast.ArrayDeref('arr')
        arrDeref.index=ast.Constant(arrIndex)
        arrIndex+=1
        if (toFrom=='to') : 
          aSourceNode.appendChild(ast.Assignment(arrDeref,activeVarRef))
        else:
          aSourceNode.appendChild(ast.Assignment(activeVarRef,arrDeref))
    return 

  def generateFPE(self,withBody,aDefinitionsSection):
    aDef=ast.IntrinsicDef('makeFPE',
                          None,
                          [ast.MethodParameter('n',ast.Type('float'),'in'),
                           ast.MethodParameter('d',ast.Type('float'),'in')],
                          ast.MethodParameter('r',ast.Type('float'),None))
    if withBody:
      aDef.appendChild(ast.Assignment(ast.Variable('r'),
                                      ast.Division(ast.Variable('n'),
                                                   ast.Variable('d'))))
    aDefinitionsSection.appendChild(aDef)  
  
  def generateTypeGetterSetterBody(self,getOrSet,aSourceNode):
    BasePrinter.Printer.generateTypeGetterSetterBody(self, getOrSet, aSourceNode) 
    aSwitch=ast.Switch(ast.Variable('direction'))
    for direct in range(1,params.d+1,1):
      aCase=ast.Case(str(direct))
      innerSwitch=ast.Switch(ast.Variable('degree'))
      for deg in range(1,params.o+1,1):
        innerCase=ast.Case(str(deg))
        if params.useQueue:
          var = 'r'
        else:
          var = '(*this)'
        theActiveVarRef = util.dOfC(var, direct, deg)
        thePassiveVarRef=ast.Variable('passive')
        if (getOrSet=='set'):
          aLHS=theActiveVarRef
          aRHS=thePassiveVarRef
        else:
          aRHS=theActiveVarRef
          aLHS=thePassiveVarRef
        innerCase.appendChild(ast.Assignment(aLHS,aRHS))
        innerSwitch.appendChild(innerCase)
      aCase.appendChild(innerSwitch)
      aSwitch.appendChild(aCase)
    aSourceNode.appendChild(aSwitch)
    return


#Reverse_Mode Begin, for the first version, we only implement very basic features. No queue, no slice
  def generateAsgnReverse(self):
    ''' not used in C++, so returns None '''
    return None


  def generatePrecisionsReverse(self):
    ''' top level generator for the precision type definition '''
    aSource = ast.SimpleSource(names.Fixed.precDeclN,self.hE)
    for  k,kv in self.precDict.items():
      tdName=names.Fixed.pN+k+'prec'
      aSpecialLine=ast.Special('typedef '+kv[0]+' '+tdName+';') 
      aSource.appendChild(aSpecialLine)
      # replace with new entry
      self.precDict[k]=(kv[0],kv[1],tdName)
    return aSource

  def generateTypesReverse(self,sourceList):
    ''' top level generator for the type module '''
    aSource = ast.ObjectSource(names.Fixed.typeDeclN,
                               [names.Fixed.precDeclN])
    aSource.decls=self.generateTypeDeclsReverse()
    aSource.defs=self.generateTypeDefinitionsReverse(sourceList)
    return aSource

  def generateTypeDeclsReverse(self):
    ''' generator for the type declarations '''
    aDeclsGroup = ast.StatementGroup()
    aDeclsGroup.appendChild(ast.Special('extern "C"{\n    #include "trace.h"\n    #include "reverse.h"\n    #include "common.h"\n    #include "location.h"\n    #include <stdio.h>\n }\n'))
    for n,t,k in self.activeTL :
      aDeclsGroup.appendChild(ast.Special('class '+n+';'))
    for n,t,k in self.activeTLE :
      aDeclsGroup.appendChild(ast.Special('class '+n+';'))
   
    # the type Declearations (i.e. RAfloatS / RAfloatD structs)
    # This is the temporary/base type, which means only internally visiable
    # User will use explicit/derived type, which is defined in self.activeTLE
    for n,t,k in self.activeTL :
      aDeclsGroup.appendChild(ast.Comment(n))
      aType = ast.Type(t)
      aType.kind = self.precDict[k][0]
      structName = util.getVarStructName(n)
      aUDefType = ast.UDefType(structName)
      aDeclsGroup.appendChild(aUDefType)
      value = ast.Declarator(names.Fixed.lN)
      value.type = ast.Type(aType.kind+'*')
      aUDefType.prependChild(value)
      value = ast.Declarator(names.Fixed.aN)
      value.type = aType
      aUDefType.prependChild(value)
      value = ast.Declarator(names.Fixed.vN)
      value.type = aType
      aUDefType.prependChild(value)
      aUDefType.appendChild(ast.Special(n+'();'))   # constructor
      aUDefType.appendChild(ast.Special('~'+n+'();'))   # destructor

    for n,t,k in self.activeTLE :
      aDeclsGroup.appendChild(ast.Comment(n))
      aType = ast.Type(t)
      aType.kind = self.precDict[k][0]
      structName = util.getVarStructName(n)
      aUDefType = ast.UDefType(structName)
      for nb,tb,kb in self.activeTL :
        if (kb==k):
          break;
      aUDefType.baseType = nb; 
      aDeclsGroup.appendChild(aUDefType)
      aUDefType.appendChild(ast.Special(n+'();'))   # constructor
      aUDefType.appendChild(ast.Special('~'+n+'();'))   # destructor
      self.generateCopiesReverse(False,None,'=',n,t,k,aUDefType) # assignments
      self.generateCopiesReverse(False,n,None,n,t,k,aUDefType) # copy constructor
      self.generateTypeSetterReverse(False,n,t,k,aUDefType)
      self.generateTypeGetterReverse(False,n,t,k,aUDefType)

    self.generateFPE(False,aDeclsGroup)
    return aDeclsGroup

  def generateTypeDefinitionsReverse(self,sourceList):
    ''' generator for the type module definitions '''
    aDefinitionsSection=ast.StatementGroup()
    aDefinitionsSection.appendChild(ast.Special('extern "C"{\n    #include "trace.h"\n    #include "reverse.h"\n    #include "common.h"\n    #include "location.h"\n    #include <stdio.h>\n  }\n'))

    # the generic getter/setters
    for n,t,k in self.activeTL :
      self.generateDefaultConstructorReverse(n,t,k,aDefinitionsSection)
      self.generateDefaultDestructorReverse(n,t,k,aDefinitionsSection)

    for n,t,k in self.activeTLE :
      self.generateDefaultConstructorReverse(n,t,k,aDefinitionsSection)
      self.generateDefaultDestructorReverse(n,t,k,aDefinitionsSection)
      self.generateCopiesReverse(True,None,'=',n,t,k,aDefinitionsSection) # assignments
      self.generateCopiesReverse(True,n,None,n,t,k,aDefinitionsSection) # copy constructor
      self.generateTypeSetterReverse(True,n,t,k,aDefinitionsSection)
      self.generateTypeGetterReverse(True,n,t,k,aDefinitionsSection)

#     make the subroutine bodies as includes  
#    anIncludeSource=ast.SimpleSource(names.Fixed.pN+'set', self.iE)
#    self.generateTypeGetterSetterBodyReverse('set',anIncludeSource)
#    sourceList.append(anIncludeSource)
#    anIncludeSource=ast.SimpleSource(names.Fixed.pN+'get', self.iE)
#    self.generateTypeGetterSetterBodyReverse('get',anIncludeSource)
#    sourceList.append(anIncludeSource)
    self.generateFPE(True,aDefinitionsSection)
    return aDefinitionsSection
    
  def generateTypeGetterReverse(self,withBody,activeName,type,kind,
                         aDefinitionsSection):
    # the generic getters
    aParameterList=[]
    # parameter declarations
    # the return type
    aType=ast.Type(type)
    aType.kind=self.precDict[kind][0]
    aGetterDef=ast.IntrinsicDef('getAdjoint',None,aParameterList,
                                ast.MethodParameter('adjoint',aType,None))
    if withBody:
      aGetterDef.memberOf = activeName
      var = '(*this)'
      theActiveVarRef =ast.StructDeref(ast.Variable('(*this)'),ast.Variable('a'))
      thePassiveVarRef=ast.Variable('adjoint')
      aLHS=thePassiveVarRef
      aRHS=theActiveVarRef
      aGetterDef.appendChild(ast.Assignment(aLHS,aRHS))
    aDefinitionsSection.appendChild(aGetterDef)

  def generateTypeSetterReverse(self,withBody,activeName,type,kind,
                         aDefinitionsSection):
    # the generic setters
    aParameterList=[]
    # parameter declarations
    aType=ast.Type(type)
    aType.kind=self.precDict[kind][0]
    aParameterList.append(ast.MethodParameter('adjoint',aType,'in'))
    # the passive type
    aSetterDef=ast.IntrinsicDef('setAdjoint',None,aParameterList,None)
    if withBody:  
      aSetterDef.memberOf = activeName
 #     aSetterDef.appendChild(ast.Include(names.Fixed.pN+'set'+self.iE))
      var = '(*this)'
      theActiveVarRef =ast.StructDeref(ast.Variable('(*this)'),ast.Variable('a'))
      thePassiveVarRef=ast.Variable('adjoint')
      aLHS=theActiveVarRef
      aRHS=thePassiveVarRef
      aSetterDef.appendChild(ast.Assignment(aLHS,aRHS))
    aDefinitionsSection.appendChild(aSetterDef)

  def generateDefaultConstructorReverse(self,name, type, kind, body):
      ctor = ast.IntrinsicDef(name, None, [], None)
      ctor.ctor = True
      ctor.memberOf = name
      aLHS = ast.Declarator('l')
      aLHS.type = ast.Type(name)
      aLHS.intent = 'inout'
      aLHS.initializer = ast.Variable('*this')
      ctor.appendChild(aLHS)
      aRHS = ast.Declarator('r')
      aRHS.type = ast.Type(type)
      aRHS.type.kind=self.precDict[kind][0]
      aRHS.const = True
      aRHS.initializer = ast.Constant('0.0')
      aRHS.initializer.kind=self.precDict[kind][0]
      ctor.appendChild(aRHS)
      ctor.appendChild(self.setIterator())
      ctor.appendChild(ast.Assignment(util.aOf('l'),ast.Constant('0.0')))
      ctor.appendChild(ast.Assignment(ast.StructDeref(ast.Variable('l'),ast.Variable('loc')),ast.Address(ast.StructDeref(ast.Variable('l'),ast.Variable('a')))))
#      ctor.appendChild(ast.Include(names.Fixed.pN + 'asgn' + 'P' + self.iE))
      body.appendChild(ctor)

  def generateDefaultDestructorReverse(self,name, type, kind, body):
      ctor = ast.IntrinsicDef('~'+name, None, [], None)
      ctor.ctor = True
      ctor.memberOf = name
      aLHS = ast.Declarator('l')
      aLHS.type = ast.Type(name)
      aLHS.intent = 'inout'
      aLHS.initializer = ast.Variable('*this')
      ctor.appendChild(aLHS)
      aParameterList=[]
      aParameterList.append(util.lOf('l'))
      ctor.appendChild(ast.SubroutineCall('pushConstGlobal'+kind,aParameterList))
      body.appendChild(ctor)

  def generateCopiesReverse(self,withBody,ctorName,operatorName,activeName,type,
                     kind,aDefinitionsSection):
    ''' generate an assignment for LHS with type activeName '''

    activeType = ast.Type(activeName)
    activeType.baseType = False
    def __genIntrinsicDefForCopies(paramType):
      anArgument = ast.MethodParameter('r', paramType, None)
      anArgument.const = True
      anArgument.intent = 'inout'
      aReturn = ast.MethodParameter('ret', activeType, None)
      aReturn.initializer = ast.Variable('*this')
      aReturn.const = True
      aReturn.intent = 'inout'
      aCopyDef = ast.IntrinsicDef(ctorName, None, [anArgument], aReturn)
      aCopyDef.operatorName = operatorName
      if ctorName:
        aCopyDef.ctor = True
      return aCopyDef

    def __genBodyForCopies(activeOrPassive, body):
      aLHS = ast.Declarator('l')
      aLHS.type = activeType
      aLHS.intent = 'inout'
      aLHS.initializer = ast.Variable('*this')
      body.appendChild(aLHS)


    # active right hand sides:
    for (nr,tr,kr) in self.activeTLE:
      if self.lossyAsgn(kind, kr, type, tr):
        continue
      aCopyDef = __genIntrinsicDefForCopies(ast.Type(nr))
      if withBody:  
        aCopyDef.memberOf = activeName
        __genBodyForCopies('A', aCopyDef)
        aCopyDef.appendChild(ast.Assignment(util.vOf('l'), util.vOf('r')))
        if (not operatorName):
          aCopyDef.appendChild(self.getLocationAssigned('l'))
        d=ast.Constant('1.0')
        aParameterList=[]
        aParameterList.append(util.lOf('l'))
        aParameterList.append(d)
        aParameterList.append(util.lOf('r'))
        aCopyDef.appendChild(ast.SubroutineCall('pushUnaryLocal'+kind+kr,aParameterList))
        aParameterList=[]
        aCopyDef.appendChild(ast.SubroutineCall('preAcc',aParameterList))

      aDefinitionsSection.appendChild(aCopyDef)
 
    for (nr,tr,kr) in self.activeTL:
      if self.lossyAsgn(kind, kr, type, tr):
        continue
      aCopyDef = __genIntrinsicDefForCopies(ast.Type(nr))
      if withBody:  
        aCopyDef.memberOf = activeName
        __genBodyForCopies('A', aCopyDef)
        aCopyDef.appendChild(ast.Assignment(util.vOf('l'), util.vOf('r')))
        if (not operatorName):
          aCopyDef.appendChild(self.getLocationAssigned('l'))
        d=ast.Constant('1.0')
        aParameterList=[]
        aParameterList.append(util.lOf('l'))
        aParameterList.append(d)
        aParameterList.append(util.lOf('r'))
        aCopyDef.appendChild(ast.SubroutineCall('pushUnaryLocal'+kind+kr,aParameterList))
        aParameterList=[]
        aCopyDef.appendChild(ast.SubroutineCall('preAcc',aParameterList))

      aDefinitionsSection.appendChild(aCopyDef)

    # and now the same for passive right hand sides:   
    for (tr,kr) in self.passiveTypeList:
      if not (kr is None):
        if self.lossyAsgn(kind, kr, type, tr):
          continue
      aType = ast.Type(tr)
      if not (kr is None):
        aType.kind = self.precDict[kr][0]
      aCopyDef = __genIntrinsicDefForCopies(aType)
      if withBody:
        aCopyDef.memberOf = activeName
        __genBodyForCopies('P', aCopyDef)
        aCopyDef.appendChild(ast.Assignment(util.vOf('l'), ast.Variable('r')))
        if (not operatorName):
          aCopyDef.appendChild(self.getLocationAssigned('l'))
        aParameterList=[]
        aParameterList.append(util.lOf('l'))
        aCopyDef.appendChild(ast.SubroutineCall('pushConstGlobal'+kind,aParameterList))

      aDefinitionsSection.appendChild(aCopyDef)

  def visitAddress(self,vertex):
    self.write('&(')
    vertex.children.accept(self)
    self.write(')')

  def getLocationAssigned(self,name):
    aAssignment=ast.Assignment(ast.StructDeref(ast.Variable('l'),ast.Variable('loc')),ast.Address(ast.StructDeref(ast.Variable('l'),ast.Variable('a'))))
    return aAssignment

  def getLocation(self,name):
    return ast.StructDeref(ast.Variable(name),ast.Variable(names.Fixed.lN))


#Reverse_Mode End



class CppOutput(CppPrinter):
  '''
  This class prints the AST to the file system as C++ source
  '''
  def __init__(self):
    CppPrinter.__init__(self)
    self.f = None # the file handle
    return

  def visitSource(self, vertex):
    import os
    import Common.ast
    if vertex.fortranOnly :
      return
    tempExt='.tmp'
    if not (os.path.exists(self.oP)):
      os.makedirs(self.oP)
    if (isinstance(vertex, Common.ast.SimpleSource)):
      self.setFileName(vertex.identifier+vertex.extension)
      filename=self.oP+'/'+vertex.identifier+vertex.extension
      self.f = file(filename+tempExt, 'w')
      ast.GenComment().accept(self)
      if (vertex.extension == self.hE):
        # make an include guard:
        self.println('#ifndef _'+vertex.identifier+'_INCLUDE_') 
        self.println('#define _'+vertex.identifier+'_INCLUDE_') 
      for child in vertex.children:
        child.accept(self)
      if (vertex.extension == self.hE):
        # end the include guard:
        self.println('#endif') 
      self.f.close()
      self.replaceIfDifferent(filename+tempExt,filename)
    else:
      # declarations
      self.setFileName(vertex.identifier+self.hE)
      filename=self.oP+'/'+vertex.identifier+self.hE
      self.f = file(filename+tempExt, 'w')
      ast.GenComment().accept(self)
      # make an include guard:
      self.println('#ifndef _'+vertex.identifier+'_INCLUDE_') 
      self.println('#define _'+vertex.identifier+'_INCLUDE_') 
      self.visitObjectDecls(vertex)
      if self.inlineDefs:
        self.addDep(self.getFileName(),vertex.identifier+self.sE)
        self.println('#include \"'+vertex.identifier+self.sE+'\"')
      self.println('#endif') 
      self.f.close()
      self.replaceIfDifferent(filename+tempExt,filename)
      # definitions
      self.setFileName(vertex.identifier+self.sE)
      filename=self.oP+'/'+vertex.identifier+self.sE
      self.addObjName(vertex.identifier)
      # print 'Creating', filename
      self.f = file(filename+tempExt, 'w')
      ast.GenComment().accept(self)
      self.visitObjectDefs(vertex)
      self.f.close()
      self.replaceIfDifferent(filename+tempExt,filename)
    return  

  def replaceIfDifferent(self,source,dest):
    import os
    import filecmp
    # see if the file is different
    if os.path.exists(dest) and filecmp.cmp(dest, source):
      os.remove(source)
    else:
      os.rename(source, dest)
    return  
  
  def write(self, s):
    ''' This is overridden to redirect output to a file '''
    self.f.write(s)
  
