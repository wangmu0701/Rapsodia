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

class F90Printer(BasePrinter.Printer):
  ''' prints the AST to standard output as Fortran90 source '''

  def __init__(self):
    ''' initialize the FORTRAN printer '''
    BasePrinter.Printer.__init__(self)
    self.fixedFormatLineLength = 72
    self.freeFormatLineLength = 132
    self.fixedFormat = False
    self.fixedFormatLineStart = '      '
    self.fixedFormatContinuation = '     +'
    self.charsSinceLastBreak = 0
    if (params.reverse):
      self.typeList=['real']
    else:
      self.typeList = ['real','complex']

    self.precDict = {'S':(names.Fixed.pN+'sKind',1,ast.FuncCall('kind',[ast.Constant('1.0')])),
                     'D':(names.Fixed.pN+'dKind',2,ast.FuncCall('kind',[ast.Constant('1.0D0')]))}
    if (params.doubleOnly):
      self.precDict = {'D':(names.Fixed.pN+'dKind',1,ast.FuncCall('kind',[ast.Constant('1.0D0')]))}


    self.oP="TestLib/F90"
    self.sE=".f90" 
    self.iE=".i90"
    ## @var printAsDecl
    # if set to True prints IntrinsicDef as a declaration only
    self.printAsDecl=False
    self.boolType='logical'
    self.intType='integer'
    self.sequenceType=False
    self.withOpenADconversions=False
    ## @var inlineDefs
    # not used right now
    self.inlineDefs=False
    self.setActivePassiveTypeList()

  def setInteroperable(self,interoperable):
    if (interoperable):
      BasePrinter.Printer.setInteroperable(self,interoperable)
      # we curently do not support C++ complex
      # and the iso_c_binding prescribes separate kinds for
      # single and double precision complex numbers
      self.typeList.remove('complex') 
      self.precDict = {'S':(names.Fixed.pN+'sKind',1,ast.Variable('C_FLOAT')),
                       'D':(names.Fixed.pN+'dKind',2,ast.Variable('C_DOUBLE'))}
    # reset the list
    self.setActivePassiveTypeList()
    
  def isComplexType(self,aType):
    if (aType.baseType
        and
        aType.identifier == 'complex'):
      return True
    if (not aType.baseType):
      for n,t,k in self.activeTL:
        if (aType.identifier == n):
          return (t == 'complex')
    return False    

  def getMatchingReal(self,aComplexType):
    ''' given a complex type, return the matching real '''
    if (not self.isComplexType(aComplexType)):
      raise Exception('input '+str(aComplexType.identifier)+' is not a complex type.')
    if (aComplexType.baseType):
      rtype=ast.Type('real')
      if aComplexType.kind:  
        rtype.kind=aComplexType.type.kind
      return type
    if (not aComplexType.baseType):
      for n,ct,ck in self.activeTL:
        if (aComplexType.identifier == n
            and
            ct == 'complex'):
          break
      for n,rt,rk in self.activeTL:
        if (rt=='real' and rk==ck):
          rtype=ast.Type(n)
          rtype.baseType=False
          return rtype
    raise Exception('getMatchingReal, not found for input '+str(aComplexType.identifier))    

  def indent(self):
    if (self.fixedFormat):
      self.write(self.fixedFormatLineStart)
    BasePrinter.Printer.indent(self)

  def insertLineBreaks(self,s):
    ''' break long lines '''
    eolIndex=s.find('\n')
    if eolIndex==-1: # not found
      self.charsSinceLastBreak+=len(s)
    else:
      self.charsSinceLastBreak=len(s)-1-eolIndex
    if (self.fixedFormat):
      maxLineLength=self.fixedFormatLineLength
    else:
      # we may need to put the & in the last column
      # and here we have single character tokens
      maxLineLength=self.freeFormatLineLength-1
    if self.charsSinceLastBreak>maxLineLength:
      # insert a line break with continuations
      # the insertion point is insertAt characters 
      # from the end of the string
      insertAt=self.charsSinceLastBreak-maxLineLength
      if (self.fixedFormat):
        insertString='\n'+self.fixedFormatContinuation
        self.charsSinceLastBreak=len(self.fixedFormatContinuation)+insertAt
      else:
        insertString='&\n'
        insertAt+=1
        # we have to put the continuation character in the last position;
	# the standard says to put just one '&' at the end of the line to be continued 
	# except when a lexical token is split in which case the first character 
	# on the next line. The clean solution would be to collect the token 
	# information as we create the output but this would be overkill 
        # because in many cases the input is just a token
	# so we just do the following heuristic because we know what we generate
        if (len(s)>1): 
          tokenSplit=((not(s[len(s)-insertAt] in [' ','+','-','*','/','(',')'])) 
                      and
                      (not(s[len(s)-insertAt+1] in [' ','+','-','*','/','(',')']))) 
        else:
          tokenSplit=(s=='%') # this is a workaround for a PGI compiler bug, normally it should be FALSE
        if tokenSplit : 
          insertString+='&'
          self.charsSinceLastBreak=insertAt+1
        else : 
          self.charsSinceLastBreak=insertAt
      s=s[:-insertAt]+insertString+s[-insertAt:]
    return s
  
  def write(self, s):
    BasePrinter.Printer.write(self.insertLineBreaks(s))
  
  # here come all the AST specific visitor implementations
  # that need to override the default in DepthFirstVisitor

  def visitInclude(self, vertex):
    self.addDep(self.getFileName(),vertex.identifier)
    self.println('include \''+vertex.identifier+'\'')
  
  def visitObjectReference(self, vertex):
    self.indent()
    self.write('use')
    genUse=True
    if vertex.qualifier :
      self.write(', '+vertex.qualifier+' ::')
      if (vertex.qualifier.lower()=="intrinsic"):
        genUse=False
    if genUse:
      self.addDep(self.getFileName(),vertex.identifier+".o")
    self.write(' ' + vertex.identifier+'\n')

  def visitOverloadedSet(self, vertex):
    self.indent()
    self.write('interface ')
    if (vertex.operatorName):
      if (vertex.operatorName=='='):
        self.write('assignment('+vertex.operatorName+')')
      else:        
        self.write('operator('+vertex.operatorName+')')
    else:
      self.write(vertex.identifier)
    self.write('\n')  
    self.increaseIndent()
    for child in vertex.children:
      child.accept(self)
    self.decreaseIndent()
    self.indent()
    self.write('end interface ')
    if (not vertex.operatorName):
      self.write(vertex.identifier)
    self.write('\n')  

  def visitSubroutineDef(self, vertex):
    theName=vertex.identifier
    if vertex.pseudoMangling:
      theName+=vertex.pseudoMangling
    if self.printAsDecl:
      self.println('module procedure '+ theName)
    else:
      self.indent()
      if not (params.reverse):
        if (vertex.fortranQualifiers):
          self.write(vertex.fortranQualifiers+' ')
      self.write('subroutine '+theName+'(')
      for (c,p) in enumerate(vertex.parameters):
        if (c==0):
          self.write(p.identifier)
        else:
          self.write(','+p.identifier)
      self.write(')')
      if (vertex.bindName):
        self.write(' bind(c,name=\''+vertex.bindName+'\')')
      self.write('\n')
      self.increaseIndent()
      if (vertex.bindName):
        self.indent()
        self.write('use iso_c_binding\n')
      if (vertex.references):
        vertex.references.accept(self)
      for p in vertex.parameters:
        p.accept(self)
      for child in vertex.children:
        child.accept(self)
      self.decreaseIndent()
      self.println('end subroutine '+theName)

  def visitFunctionDef(self, vertex):
    theName=vertex.identifier
    if self.printAsDecl:
      self.println('module procedure '+ theName)
    else:
      self.indent()
      self.write('function '+theName+'(')
      for (c,p) in enumerate(vertex.parameters):
        if (c==0):
          self.write(p.identifier)
        else:
          self.write(','+p.identifier)
      self.write(')')
      if (vertex.bindName):
        self.write(' bind(c,name=\''+vertex.bindName+'\')')
      self.write('\n')
      self.increaseIndent()
      if (vertex.bindName):
        self.indent()
        self.write('use iso_c_binding\n')
      if (vertex.references):
        vertex.references.accept(self)
      for p in vertex.parameters:
        p.accept(self)
      vertex.returnType.accept(self)
      for child in vertex.children:
        child.accept(self)
      self.decreaseIndent()
      self.println('end function '+theName)


  def visitIntrinsicDef(self, vertex):
    theName=vertex.identifier
    # sort out special cases
    # which are not defined in the language standard
    # abs (complex) is defined in the standard but
    # we have to sort out the implementation later
    if ((theName in ['sinh','cosh','asin','acos','atan','nint','maxloc','maxval','abs'])
        and
        self.isComplexType(vertex.parameters[0].type)):
      # skip these
      return
    if ((theName in ['max','min','le','lt','ge','gt','sign'])
        and
        (self.isComplexType(vertex.parameters[0].type)
         or
         self.isComplexType(vertex.parameters[1].type))):
      # skip these
      return
    theName=vertex.identifier
    if vertex.pseudoMangling:
      theName+=vertex.pseudoMangling
    if self.printAsDecl:
      if (vertex.interface):
        self.println('interface '+ theName)
      else:
        self.println('module procedure '+ theName)
    else:
      self.indent()
      if not (params.reverse):
        if (vertex.fortranQualifiers):
          self.write(vertex.fortranQualifiers+' ')
      self.write('function ' + theName+'(')
      for (c,p) in enumerate(vertex.parameters):
        if (c==0):
          self.write(p.identifier)
        else:
          self.write(','+p.identifier)
      self.write(') result('+vertex.result.identifier+')\n')    
      self.increaseIndent()

      if params.openmpUseOrphaning:
        if vertex.result.type.identifier not in ['real', 'integer', 'logical']:
          self.println('use %sPrec' % vertex.result.type.identifier)

      for p in vertex.parameters:
        p.accept(self)
      vertex.result.accept(self)  
      for child in vertex.children:
        child.accept(self)
      self.decreaseIndent()
      self.println('end function ' + theName)

  def visitMethodParameter(self, vertex):
    needComma=False
    self.indent()
    if not (vertex.type is None):
      vertex.type.accept(self)
      needComma=True
    if not(vertex.intent is None):
      if needComma:
        self.write(',')
      self.write('intent('+vertex.intent+')')
      needComma=True
    if vertex.const:
      if needComma:
        self.write(',')
      self.write('parameter')
      needComma=True
    if vertex.valueOnly:
      if needComma:
        self.write(',')
      self.write('value')
      needComma=True
    if vertex.identifier:
      self.write('::')
      self.write(vertex.identifier)
      if (vertex.dimensions > 0):
        self.__printDimensions(vertex)
    if vertex.initializer:
      self.write(' = ')
      vertex.initializer.accept(self)
    self.write('\n')

  def visitTypeConversion(self,vertex):
    if (vertex.toType):
      self.write('real(')
      vertex.identifier.accept(self)
      if (vertex.toType.kind):
        self.write(',kind='+vertex.toType.kind)
      self.write(')')
    else:
      vertex.identifier.accept(self)
  
  def visitType(self, vertex):
    if not(vertex.baseType):
      self.write('type(')
    self.write(vertex.identifier)
    if vertex.kind:
      self.write('(kind='+vertex.kind+')')
    if not(vertex.baseType):
      self.write(')')
    return  
  
  def visitUDefType(self, vertex):
    self.indent()
    self.write('type')
    if (self.getInteroperable()):
      self.write(', bind(C) ::')
    self.write(' '+vertex.identifier+'\n')  
    self.increaseIndent()
    if (self.sequenceType):
      self.println('sequence')
    if vertex.children:
      self.visitChildren(vertex)
    if vertex.contains:
      self.indent()
      self.write('contains\n')
      for node in vertex.contains:
        node.accept(self)
    self.decreaseIndent()
    self.println('end type '+vertex.identifier)
  
  def visitDeclarator(self, vertex):
    needComma=False
    self.indent()
    if not (vertex.type is None):
      vertex.type.accept(self)
      needComma=True
    if vertex.public:
      if needComma:
        self.write(',')
      self.write('public')
      needComma=True
    if not(vertex.intent is None):
      if needComma:
        self.write(',')
      self.write('intent('+vertex.intent+')')
      needComma=True
    if vertex.const:
      if needComma:
        self.write(',')
      self.write('parameter')
      needComma=True
    if vertex.pointer:
      if needComma:
        self.write(',')
      self.write('pointer')
      needComma=True
    if vertex.identifier:
      self.write('::')
      self.write(vertex.identifier)
      if (vertex.dimensions>0):
        self.__printDimensions(vertex)
    if vertex.initializer:
      self.write(' = ')
      vertex.initializer.accept(self)
    self.write('\n')  
  
  def visitArray(self, vertex):
    if not (vertex.type is None):
      vertex.type.accept(self)
      if not (isinstance(vertex.type, Pointer)):
        self.write(' ')
    self.write(vertex.identifier)
    self.write('(')
    if vertex.size:
      vertex.size.accept(self)
    self.write(')')
    if vertex.initializer:
      self.write(' = ')
      vertex.initializer.accept(self)

  def visitArrayDeref(self, vertex):
    self.write(vertex.identifier)
    self.write('(')
    if isinstance(vertex.index, ast.Constant):
      self.write(vertex.index.identifier)
    elif isinstance(vertex.index, ast.Variable):
      vertex.index.accept(self)
    else:
      raise Exception('Object type %s must be either ast.Constant or '
                      'ast.Variable' % objType)
    self.write(')')
  
  def visitIf(self, vertex):
    self.indent()
    self.write('if (')
    vertex.children[0].accept(self)
    self.write(') then\n')
    self.increaseIndent()
    vertex.children[1].accept(self)
    self.decreaseIndent()
    if len(vertex.children) > 2:
      self.println('else')
      self.increaseIndent()
      vertex.children[2].accept(self)
      self.decreaseIndent()
    self.println('end if')
  
  def visitSwitch(self, vertex):
    self.indent()
    self.write('select case(')
    vertex.children[0].accept(self)
    self.write(')\n')
    self.increaseIndent()
    for child in vertex.children[1:]:
      child.accept(self)
    self.decreaseIndent()
    self.println('end select')

  def visitCase(self, vertex):
    self.println('case ('+vertex.identifier+')')
    self.increaseIndent()
    for caseChild in vertex.children:
      caseChild.accept(self)
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
    self.indent()
    self.write('do ')
    # the initialization
    self.write(vertex.identifier+'=')
    vertex.children[0].accept(self)
    self.write(', ')
    # the condition
    vertex.children[1].accept(self)
    self.write(', ')
    # the update
    vertex.children[2].accept(self)
    self.write('\n')  
    # the body  
    self.increaseIndent()
    vertex.children[3].accept(self)
    self.decreaseIndent()
    self.println('end do')
  
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
    if (self.fixedFormat):
      # no indentation here
      self.write('! '+vertex.identifier+'\n')
    else:
      self.println('! '+vertex.identifier)

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
    self.write(vertex.identifier)
    vertex.children[1].accept(self)
    self.write('\n')

  def visitStructDeref(self, vertex):
    vertex.children[0].accept(self)
    self.write(vertex.identifier)
    vertex.children[1].accept(self)

  def visitFuncCall(self, vertex):
    self.write(vertex.identifier+'(')
    num = len(vertex.children)
    for (a, argument) in enumerate(vertex.children):
      argument.accept(self)
      if a < (num - 1):
        self.write(', ')
    self.write(')')

  def visitSubroutineCall(self, vertex):
    self.indent()
    self.write('call '+vertex.identifier+'(')
    num = len(vertex.children)
    for (a, argument) in enumerate(vertex.children):
      argument.accept(self)
      if a < (num - 1):
        self.write(', ')
    self.write(')\n')
  
  def visitStop(self, vertex):
    self.indent()
    self.write('stop \''+vertex.identifier+'\'')
    self.write('\n')

# def visitConstant(self, vertex):
#   if not (vertex.identifier is None):
#     self.write(vertex.identifier)
#   else:
#     self.write(str(vertex.value))
  
  def visitObjectSource(self,vertex): 
    self.println('module ' + vertex.identifier)
    self.increaseIndent()
    for child in vertex.objRefList:
      child.accept(self)
    self.println('implicit none')
    self.printAsDecl=True
    vertex.decls.accept(self)
    self.printAsDecl=False
    if (vertex.externs):
      vertex.externs.accept(self)

    if (vertex.defs) and (vertex.defs.children):
      self.decreaseIndent()
      self.println('contains ')
      self.increaseIndent()
      vertex.defs.accept(self)
    self.decreaseIndent()
    self.println('end module ' + vertex.identifier)

  def visitSpecial(self,vertex):
    self.println(vertex.identifier)

  def visitOpenmpLoop(self, vertex):
    if vertex.isOpen:
      if not vertex.isOrphaned:
        self.println('!$OMP PARALLEL NUM_THREADS(%s)' % params.slices)
      self.println('!$OMP DO SCHEDULE(STATIC, %d)' % params.openmpChunkSize)
    else:
      self.println('!$OMP END DO')
      if not vertex.isOrphaned:
        self.println('!$OMP END PARALLEL')

  #
  # misc methods
  #

  def __printDimensions(self, vertex):
    self.write('(')
    lenDimBounds=len(vertex.dimensionBounds)
    if lenDimBounds>0:
      if lenDimBounds!=vertex.dimensions:
        raise Exception('have only '+str(vertex.dimensionBounds)+' for '+str(vertex.dimensions)+' dimensions')
      for i in range(0,vertex.dimensions-1):
        vertex.dimensionBounds[i].accept(self)
        self.write(',')
      vertex.dimensionBounds[-1].accept(self)
    else:  
      for i in range(1,vertex.dimensions):
        self.write(':,')
      self.write(':')  
    self.write(')')
    return

  #
  # extra generation parts not done with a single AST node 
  #

  def generatePrecisions(self):
    ''' top level generator for the kind module '''
    oRefList=[]
    if self.getInteroperable():
      oRefList.append(ast.ObjectReference("iso_c_binding","intrinsic"))
#    print "names.Fixed.precDeclN:", names.Fixed.precDeclN
#    print "oRefList:",oRefList
    aSource = ast.ObjectSource(names.Fixed.precDeclN,oRefList)
    aSource.decls=self.generateKindModuleInterface()
#    print "aSource.decls:", aSource.decls
    return aSource
  
  def generateKindModuleInterface(self):
    ''' generate the kind module interface '''
#    print "self.precDict:",self.precDict
    aModuleInterface=ast.StatementGroup()
    for varName,order,init in self.precDict.values(): 
      aDeclarator=ast.Declarator(varName)
      aDeclarator.public=True
      aDeclarator.const=True
      aDeclarator.type=ast.Type('integer')
      aDeclarator.initializer=init
      aModuleInterface.appendChild(aDeclarator)  
    return aModuleInterface

  def generateConversion(self,withBody,aSourceSection,toFromInfo):
      aParameterList=[]  
      pName=''
      exprs=[]
      for k,v in toFromInfo.items():
        aType=ast.Type(v[0]) # type name
        pName+=v[0]
        if not v[1]: # active type has no kind 
            aType.baseType=False 
            exprs.append(util.vOf(k))   
        else: # passive type has a kind
            aType=ast.Type(v[0])
            aType.kind=self.precDict[v[1]][0]
            pName+=v[1]
            exprs.append(ast.Variable(k))
        aParameterList.append(ast.MethodParameter(k,aType,v[2]))
      aFunction=ast.SubroutineDef('convert',pName,aParameterList)
      if withBody:
          if not params.useOpenmp:
              aFunction.fortranQualifiers = 'elemental'
              aFunction.appendChild(ast.Assignment(exprs[0],exprs[1]))
      aSourceSection.appendChild(aFunction)

  def generateConversions(self,withBody,aSourceSection):
    # make the interdace start
    for (n,t,k) in self.activeTL : 
        self.generateConversion(withBody,aSourceSection,{'to':(n,None,'out'),
                                                         'from':(t,k,'in')})
        self.generateConversion(withBody,aSourceSection,{'to':(t,k,'out'),
                                                         'from':(n,None,'in')})

  def generateTypes(self,sourceList):
    ''' top level generator for the type module '''
    aSource = ast.ObjectSource(
        names.Fixed.typeDeclN,[names.Fixed.precDeclN])
    aSource.decls=self.generateTypeDecls()
    aSource.defs=ast.StatementGroup()
    self.generateFPE(True,aSource.defs)
    if self.withOpenADconversions:  
      self.generateConversions(True,aSource.defs)
    for i in ['set','get']:
      self.generateTypeGetterSetter(True,i,aSource.defs)
      # make the subroutine bodies as includes  
      anIncludeSource=ast.SimpleSource(names.Fixed.pN+i, self.iE)
      self.generateTypeGetterSetterBody(i,anIncludeSource)
      sourceList.append(anIncludeSource)
    for i in ['to','from']:
      self.generateToFromArray(True,i,aSource.defs)
      # make the subroutine bodies as includes  
      anIncludeSource=ast.SimpleSource(names.Fixed.pN+i+"Array", self.iE)
      self.generateToFromArrayBody(i,anIncludeSource)
      sourceList.append(anIncludeSource)
    if params.openmpUseOrphaning:
      self.generateGlobals(sourceList)
    return aSource

  def generateGlobals(self, sourceList):
    for n,t,k in self.activeTL:
      aType = ast.Type(n)
      aType.baseType = False

      decls = ast.StatementGroup()
      declarator = ast.Declarator('rGlobal')
      declarator.public = True
      declarator.type = aType
      decls.appendChild(declarator)
      declarator = ast.Declarator('cGlobal')
      declarator.public = True
      declarator.type = aType
      decls.appendChild(declarator)
      declarator = ast.Declarator('sGlobal')
      declarator.public = True
      declarator.type = aType
      decls.appendChild(declarator)
      src = ast.ObjectSource(n + 'Prec', 
                             [names.Fixed.typeDeclN])
      src.decls = decls
      sourceList.append(src)

  def generateTypeDecls(self):
    ''' generator for the type module interface '''
    aModuleInterface=ast.StatementGroup()
    pasDecl=ast.Declarator("arrSz")
    pasDecl.type=ast.Type("integer") 
    pasDecl.const=True
    pasDecl.initializer=ast.Constant(str(1+(params.o*params.d)))
    aModuleInterface.appendChild(pasDecl)
    # all the types
    for n,t,k in self.activeTL : 
      aPublicDeclarator=ast.Declarator(n)
      aPublicDeclarator.public=True
      aModuleInterface.appendChild(aPublicDeclarator)
    # the generic getter/setters
    for i in ['set','get']:
      aPublicDeclarator=ast.Declarator(names.Fixed.pN+i)
      aPublicDeclarator.public=True
      aModuleInterface.appendChild(aPublicDeclarator)
      anInterface=ast.OverloadedSet(names.Fixed.pN+i,None)
      self.generateTypeGetterSetter(False,i,anInterface)
      aModuleInterface.appendChild(anInterface)
    for i in ['to','from']:
      aPublicDeclarator=ast.Declarator(names.Fixed.pN+i+"Array")
      aPublicDeclarator.public=True
      aModuleInterface.appendChild(aPublicDeclarator)
      anInterface=ast.OverloadedSet(names.Fixed.pN+i+"Array",None)
      self.generateToFromArray(False,i,anInterface)
      aModuleInterface.appendChild(anInterface)

    # the type definitions
    for n,t,k in self.activeTL :

      aType = ast.Type(t)
      aType.kind = self.precDict[k][0]

      if params.slices > 0:
        sliceName = 'Slice' + k + t
        sliceDefType = ast.UDefType(sliceName)
        util.appendDirDecls(aType, sliceDefType)
        aModuleInterface.appendChild(sliceDefType)

      value = ast.Declarator(names.Fixed.vN)
      value.type = aType
      # the user defined type
      aUDefType = ast.UDefType(n) 
      aUDefType.appendChild(value)

      aModuleInterface.appendChild(aUDefType)

      # the slice component
      if params.slices > 0:
        sliceType = ast.Type(sliceName)
        sliceType.baseType = False
        sliceDeclarator = ast.Declarator(names.Fixed.sN)
        sliceDeclarator.dimensions = 1
        sliceDeclarator.dimensionBounds.append(ast.Constant(str(params.slices)))
        sliceDeclarator.type = sliceType
        aUDefType.appendChild(sliceDeclarator)
      else:   # no slicing
        util.appendDirDecls(aType, aUDefType)

    aPublicDeclarator=ast.Declarator('makeFPE')
    aPublicDeclarator.public=True
    aModuleInterface.appendChild(aPublicDeclarator)
    anOverloadedSet=ast.OverloadedSet('makeFPE',None)
    self.generateFPE(False,anOverloadedSet)
    aModuleInterface.appendChild(anOverloadedSet)
    if self.withOpenADconversions:  
        anOverloadedSet=ast.OverloadedSet('oad_convert',None)
        self.generateConversions(False,anOverloadedSet)
        aModuleInterface.appendChild(anOverloadedSet)
    return aModuleInterface

  def generateToFromArray(self,withBody,toFrom,aDefinitionsSection):
    ''' generator for the type module definitions '''
    # the generic getter/setters
    for n,t,k in self.activeTL :
      aParameterList=[]
      # parameter declarations
      # the active type
      aType=ast.Type(n)
      aType.baseType=False
      aParm=ast.MethodParameter('active',aType,None)
      # the passive type
      pType=ast.Type(t)
      pType.kind=self.precDict[k][0]
      pParm=ast.MethodParameter('arr',pType,None,1,[ast.Variable('arrSz')])
      if toFrom=='from':
        aParm.intent='out'
        pParm.intent='in'
      else: 
        pParm.intent='out'
        aParm.intent='in'
      aParameterList.append(aParm)
      aParameterList.append(pParm)
      aSubroutineDef=ast.SubroutineDef(toFrom+"Array",n,aParameterList)
      aDefinitionsSection.appendChild(aSubroutineDef)
      if withBody:  
        aSubroutineDef.appendChild(ast.Include(names.Fixed.pN+toFrom+"Array"+self.iE))

  def generateToFromArrayBody(self,toFrom,aSourceNode):
    arrIndex=1;
    activeVarRef = util.vOf('active')
    arrDeref = ast.ArrayDeref('arr')
    arrDeref.index=ast.Constant(str(arrIndex))
    arrIndex+=1
    if (toFrom=='to') : 
      aSourceNode.appendChild(ast.Assignment(arrDeref,activeVarRef))
    else:
      aSourceNode.appendChild(ast.Assignment(activeVarRef,arrDeref))
    for direct in range(1,params.d+1,1):
      for deg in range(1,params.o+1,1):
        activeVarRef = util.dOfC('active', direct, deg)
        arrDeref = ast.ArrayDeref('arr')
        arrDeref.index=ast.Constant(str(arrIndex))
        arrIndex+=1
        if (toFrom=='to') : 
          aSourceNode.appendChild(ast.Assignment(arrDeref,activeVarRef))
        else:
          aSourceNode.appendChild(ast.Assignment(activeVarRef,arrDeref))
    return

  def generateTypeGetterSetter(self,withBody,setOrGet,aDefinitionsSection):
    ''' generator for the type module definitions '''
    # the generic getter/setters
    for n,t,k in self.activeTL :
      aParameterList=[]
      # parameter declarations
      # the active type
      aType=ast.Type(n)
      aType.baseType=False
      aParameterList.append(ast.MethodParameter('active',aType,'inout'))
      aParameterList.append(ast.MethodParameter('direction',ast.Type('integer'),'in'))
      aParameterList.append(ast.MethodParameter('degree',ast.Type('integer'),'in'))
      # the passive type
      aType=ast.Type(t)
      aType.kind=self.precDict[k][0]
      if setOrGet=='set':
        anIntent='in'
      else: 
        anIntent='out'
      aParameterList.append(ast.MethodParameter('passive',aType,anIntent))
      aSubroutineDef=ast.SubroutineDef(setOrGet,n,aParameterList)
      aDefinitionsSection.appendChild(aSubroutineDef)
      if withBody:  
        aSubroutineDef.appendChild(ast.Include(names.Fixed.pN+setOrGet+self.iE))
  
  def generateTypeGetterSetterBody(self,getOrSet,aSourceNode):
    BasePrinter.Printer.generateTypeGetterSetterBody(self, getOrSet, aSourceNode) 
    aSwitch=ast.Switch(ast.Variable('direction'))
    aSourceNode.appendChild(aSwitch)
    for direct in range(1, params.d+1, 1):
      aCase=ast.Case(str(direct))
      innerSwitch=ast.Switch(ast.Variable('degree'))
      for deg in range(1, params.o+1, 1):
        innerCase=ast.Case(str(deg))
        theActiveVarRef=util.dOfC('active',direct,deg)
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
    return

  def generateFPE(self,withBody,aDefinitionsSection):
    aDef=ast.IntrinsicDef('makeFPE',
                          '_i',
                          [ast.MethodParameter('n',ast.Type('real'),'in'),
                           ast.MethodParameter('d',ast.Type('real'),'in')],
                          ast.MethodParameter('r',ast.Type('real'),None))
    if not params.useOpenmp:
      aDef.fortranQualifiers = 'elemental'
    if withBody:
      aDef.appendChild(ast.Assignment(ast.Variable('r'),
                                      ast.Division(ast.Variable('n'),
                                                   ast.Variable('d'))))
    aDefinitionsSection.appendChild(aDef)  

  def generateAsgn(self):
    ''' top level generator for the assignment module '''
    aSource = ast.ObjectSource(names.Fixed.pN+'asgn',
                               [names.Fixed.precDeclN,
                                names.Fixed.typeDeclN])
    aSource.decls=ast.OverloadedSet('asgn','=')
    self.generateAsgnDefinitions(False,aSource.decls)
    aSource.defs=ast.StatementGroup()
    self.generateAsgnDefinitions(True,aSource.defs)
    return aSource

  def generateAsgnDefinitions(self,withBody,aDefinitionsBlock):
    ''' generate the assignment definitions '''

    iterator = self.setIterator()

    # active/active combinations
    for (nl,tl,kl) in self.activeTL : 
      for (nr,tr,kr) in self.activeTL :
        if (nr==nl and not params.reverse):
          # the compiler generated copy ctor/assignment should be faster
          # but for reverse we need it
          continue
        if self.lossyAsgn(kl, kr, tl, tr):
          continue
        pName=nl+nr
        aParameterList=[]
        # the active result
        # determine the result type
        aType=ast.Type(nl)
        aType.baseType=False
        aParameterList.append(ast.MethodParameter('l',aType,'out'))
        # the active argument
        aType=ast.Type(nr)
        aType.baseType=False
        aParameterList.append(ast.MethodParameter('r',aType,'in'))
        aFunction=ast.SubroutineDef(names.Fixed.pN+'asgn',pName,aParameterList)
        if not params.useOpenmp:
          aFunction.fortranQualifiers = 'elemental'
        if withBody:
          aFunction.appendChild(iterator)
          aFunction.appendChild(ast.Include(names.Fixed.pN+'asgnA'+self.iE))
        aDefinitionsBlock.appendChild(aFunction)
    # active/passive combinations
    for (nl,tl,kl) in self.activeTL : 
      for (tr,kr) in self.passiveTypeList :
        if not (kr is None):
          if self.lossyAsgn(kl, kr, tl, tr):
            continue
          pName=nl+tr+kr
        else: 
          pName=nl+tr
        aParameterList=[]  
        # the active result
        # determine the result type
        aType=ast.Type(nl)
        aType.baseType=False
        aParameterList.append(ast.MethodParameter('l',aType,'out'))
        # the passive argument
        aType=ast.Type(tr)
        if not(kr is None):
          aType.kind=self.precDict[kr][0]
        aParameterList.append(ast.MethodParameter('r',aType,'in'))
        aFunction=ast.SubroutineDef(names.Fixed.pN+'asgn',pName,aParameterList)
        if withBody:
          aFunction.appendChild(iterator)
          aFunction.appendChild(ast.Include(names.Fixed.pN+'asgnP'+self.iE))
          if not params.useOpenmp:
            aFunction.fortranQualifiers = 'elemental'
        aDefinitionsBlock.appendChild(aFunction)


#Reverse_Mode Begin, for the first version, we only implement very basic features. No queue, no slice
  def generateAsgnReverse(self):
    ''' top level generator for the assignment module '''
    aSource = ast.ObjectSource(names.Fixed.pN+'asgn',
                               [names.Fixed.precDeclN,
                                names.Fixed.typeDeclN])
    aSource.decls=ast.OverloadedSet('asgn','=')
    self.generateAsgnDefinitionsReverse(False,aSource.decls)
    aSource.defs=ast.StatementGroup()
    self.generateAsgnDefinitionsReverse(True,aSource.defs)
    return aSource

  def generateAsgnDefinitionsReverse(self,withBody,aDefinitionsBlock):
    ''' generate the assignment definitions '''
    # active/active combinations
    for (nl,tl,kl) in self.activeTL : 
      for (nr,tr,kr) in self.activeTL :
#        if (nr==nl):
          # the compiler generated copy ctor/assignment should be faster
#          continue
        if self.lossyAsgn(kl, kr, tl, tr):
          continue
        pName=nl+nr
        aParameterList=[]
        # the active result
        # determine the result type
        aType=ast.Type(nl)
        aType.baseType=False
        aParameterList.append(ast.MethodParameter('l',aType,'out'))
        # the active argument
        aType=ast.Type(nr)
        aType.baseType=False
        aParameterList.append(ast.MethodParameter('r',aType,'in'))
        aFunction=ast.SubroutineDef(names.Fixed.pN+'asgn',pName,aParameterList)
        if withBody:
          aFunction.appendChild(ast.Assignment(util.vOf('l'),util.vOf('r')))
          aParameterList=[]
          aParameterList.append(util.lOf('l'))
          aParameterList.append(util.aOf('l'))
          aFunction.appendChild(ast.SubroutineCall('getLocation',aParameterList))
          aParameterList=[]
          aParameterList.append(util.lOf('l'))
          aParameterList.append(ast.Constant('1.0D0'))
          aParameterList.append(util.lOf('r'))
          aFunction.appendChild(ast.SubroutineCall('pushUnaryLocal'+kl+kr,aParameterList))
          aParameterList=[]
          aFunction.appendChild(ast.SubroutineCall('preAcc',aParameterList))
        aDefinitionsBlock.appendChild(aFunction)
    # active/passive combinations
    for (nl,tl,kl) in self.activeTL : 
      for (tr,kr) in self.passiveTypeList :
        if not (kr is None):
          if self.lossyAsgn(kl, kr, tl, tr):
            continue
          pName=nl+tr+kr
        else: 
          pName=nl+tr
        aParameterList=[]  
        # the active result
        # determine the result type
        aType=ast.Type(nl)
        aType.baseType=False
        aParameterList.append(ast.MethodParameter('l',aType,'out'))
        # the passive argument
        aType=ast.Type(tr)
        if not(kr is None):
          aType.kind=self.precDict[kr][0]
        aParameterList.append(ast.MethodParameter('r',aType,'in'))
        aFunction=ast.SubroutineDef(names.Fixed.pN+'asgn',pName,aParameterList)
        if withBody:
          aFunction.appendChild(ast.Assignment(util.vOf('l'), ast.Variable('r')))
          aParameterList=[]
          aParameterList.append(util.lOf('l'))
          aParameterList.append(util.aOf('l'))
          aFunction.appendChild(ast.SubroutineCall('getLocation',aParameterList))
          aParameterList=[]
          aParameterList.append(util.lOf('l'))
          aFunction.appendChild(ast.SubroutineCall('pushConstGlobal'+kl,aParameterList))
        aDefinitionsBlock.appendChild(aFunction)


  def generatePrecisionsReverse(self):
    ''' top level generator for the kind module '''
    oRefList=[]
    if self.getInteroperable():
      oRefList.append(ast.ObjectReference("iso_c_binding","intrinsic"))
#    print "names.Fixed.precDeclN:", names.Fixed.precDeclN
#    print "oRefList:",oRefList
    aSource = ast.ObjectSource(names.Fixed.precDeclN,oRefList)
    aSource.decls=self.generateKindModuleInterface()
#    print "aSource.decls:", aSource.decls
    return aSource
  
  def generateTypesReverse(self,sourceList):
    ''' top level generator for the type module '''
    aSource = ast.ObjectSource(
        names.Fixed.typeDeclN,[names.Fixed.precDeclN])
    aSource.decls=self.generateTypeDeclsReverse()
    aSource.externs=self.generateExternDeclReverse()
    aSource.defs=ast.StatementGroup()
    self.generateFinalizer(aSource.defs)
    self.generateSetGetBody(aSource.defs)

    return aSource
  def generateFinalizer(self,aDefinitionsSection):
    for n,t,k in self.activeTL :
      self.generateFinalizerBody(aDefinitionsSection,n,k)
  def generateFinalizerBody(self, aDefinitionsSection,n,k):
    aType=ast.Type(n);
    aType.baseType=False;
    aDef=ast.SubroutineDef('freeloc'+k,None,[ast.MethodParameter('this',aType,None)])
#Comments: We do not want the finalizer in fortran trigger the pushConstGlobal as Cpp does.
#          Because Cpp will call the dtor when a variable is not alive.
#          But F90 will also call the dtor when it's left value of an assignment.
#          It will erase the adjoint.
#          The current code may have potential problems when reuse uninitialized stack.
#          But I don't know how to deal with this other than make a global table of living variables.

    aDef.appendChild(ast.SubroutineCall('pushConstGlobal'+k,[util.lOf('this')]))
    aDef.appendChild(ast.SubroutineCall('freeLocation'+k,[util.lOf('this'),util.aOf('this')]))
    aDefinitionsSection.appendChild(aDef)  
  

  def generateTypeDeclsReverse(self):
    ''' generator for the type module interface '''
    aModuleInterface=ast.StatementGroup()
    # all the types
    for n,t,k in self.activeTL : 
      aPublicDeclarator=ast.Declarator(n)
      aPublicDeclarator.public=True
      aModuleInterface.appendChild(aPublicDeclarator)
    # the type definitions
    for n,t,k in self.activeTL :

      aType = ast.Type(t)
      aType.kind = self.precDict[k][0]
      value = ast.Declarator(names.Fixed.vN)
      value.type = aType
      # the user defined type
      aUDefType = ast.UDefType(n) 
      aUDefType.appendChild(value)
      aModuleInterface.appendChild(aUDefType)
      value=ast.Declarator(names.Fixed.aN)
      value.type=aType
      aUDefType.appendChild(value)
      value=ast.Declarator(names.Fixed.lN)
      value.type=ast.Type('integer')
      value.initializer=ast.Constant('-1')
      aUDefType.appendChild(value)
      aUDefType.contains=[]
      value=ast.Declarator('freeloc'+k)
      value.type=ast.Type('final')
      aUDefType.contains.append(value)

    aPublicDeclarator=ast.Declarator('makeFPE')
    aPublicDeclarator.public=True
    aModuleInterface.appendChild(aPublicDeclarator)
    anOverloadedSet=ast.OverloadedSet('makeFPE',None)
    aModuleInterface.appendChild(anOverloadedSet)
    self.generateSetGetInterface(aModuleInterface)



    return aModuleInterface

  def generateSetGetInterface(self,aModuleInterface):
    self.generateSetGetAdjointInterface('setAdjoint',aModuleInterface)
    self.generateSetGetAdjointInterface('getAdjoint',aModuleInterface)

  def generateSetGetBody(self,aModuleInterface):
    self.generateSetGetAdjointBody('setAdjoint',aModuleInterface)
    self.generateSetGetAdjointBody('getAdjoint',aModuleInterface)

  def generateSetGetAdjointInterface(self,name,aDefinitionSection):
    anOverloadedSet=ast.OverloadedSet(name,None)
    for (cl,(nl,tl,kl)) in enumerate(self.activeTL) : 
      aParameterList=[]
      aType=ast.Type(nl)
      aType.baseType=False
      aMethodParameter=ast.MethodParameter('source',aType,'inout')
      aParameterList.append(aMethodParameter)
      aType=ast.Type(tl)
      aType.kind= self.precDict[kl][0]
      aMethodParameter=ast.MethodParameter('value',aType,'inout')
      aParameterList.append(aMethodParameter)
      aDef=ast.IntrinsicDef(name,kl,aParameterList,None)
      anOverloadedSet.appendChild(aDef)
    aDefinitionSection.appendChild(anOverloadedSet)

  def generateSetGetAdjointBody(self,name,aDefinitionSection):
    for (cl,(nl,tl,kl)) in enumerate(self.activeTL) : 
#      anOverloadedSet=ast.OverloadedSet(name+kl,None)
      aParameterList=[]
      aType=ast.Type(nl)
      aType.baseType=False
      bType=ast.Type(tl)
      bType.kind= self.precDict[kl][0]
      if (name=='setAdjoint'):
        aMethodParameter=ast.MethodParameter('source',aType,'inout')
        aParameterList.append(aMethodParameter)
        aMethodParameter=ast.MethodParameter('value',bType,'in')
        aParameterList.append(aMethodParameter)
        aDef=ast.SubroutineDef(name+kl,None, aParameterList)
        aDef.references=ast.ObjectReference(names.Fixed.precDeclN)
        if (not params.accOnLoc):
          aDef.appendChild(ast.Assignment(self.getAdjoint('source'),ast.Variable('value')))
        else:
          aDef.appendChild(ast.SubroutineCall('setAdjointLoc'+kl,[ast.Variable('source%loc'),ast.Variable('value')]))
      elif (name=='getAdjoint'):
        aMethodParameter=ast.MethodParameter('source',aType,'inout')
        aParameterList.append(aMethodParameter)
        aMethodParameter=ast.MethodParameter('getAdjoint'+kl,bType,None)
        aDef=ast.FunctionDef(name+kl,aMethodParameter, aParameterList)
        aDef.references=ast.ObjectReference(names.Fixed.precDeclN)
        if (not params.accOnLoc):
          aDef.appendChild(ast.Assignment(ast.Variable('getAdjoint'+kl),self.getAdjoint('source')))
        else:
          aDef.appendChild(ast.SubroutineCall('getAdjointLoc'+kl,[ast.Variable('source%loc'),ast.Variable('getAdjoint'+kl)]))

      aDefinitionSection.appendChild(aDef)


  def generateExternDeclReverse(self):
    aModuleInterface=ast.StatementGroup()
    self.generateGetLocation(aModuleInterface)
    self.generateFreeLocation(aModuleInterface)
    if (params.accOnLoc):
      self.generateSetGetAdjointLoc('setAdjointLoc',aModuleInterface)
      self.generateSetGetAdjointLoc('getAdjointLoc',aModuleInterface)
    self.generateConstGlobalExterns(aModuleInterface)
    self.generateUnaryLocalExterns(aModuleInterface)
    self.generateBinaryLocalExterns(aModuleInterface)
    self.generateVoidExterns('preAcc',aModuleInterface)
    self.generateVoidExterns('revStart',aModuleInterface)
    self.generateVoidExterns('revStop',aModuleInterface)
    self.generateVoidExterns('revOn',aModuleInterface)
    self.generateVoidExterns('revOff',aModuleInterface)
    self.generateVoidExterns('reduction',aModuleInterface)
    self.generateEliminateResiduals('eliminateResidual',aModuleInterface)
    return aModuleInterface

  def generateEliminateResiduals(self,name,aDefinitionSection):
    anOverloadedSet=ast.OverloadedSet(name+'s',None)
    aParameterList=[]
    aType=ast.Type('integer')
    aMethodParameter=ast.MethodParameter('a',aType,None)
    aMethodParameter.valueOnly=True
    aParameterList.append(aMethodParameter)
    aMethodParameter=ast.MethodParameter('b',aType,None)
    aMethodParameter.valueOnly=True
    aParameterList.append(aMethodParameter)
    fname=name+'s'
    aDef=ast.SubroutineDef(fname,None, aParameterList)
    aDef.bindName=fname
    aDef.references=ast.ObjectReference(names.Fixed.precDeclN)
    anOverloadedSet.appendChild(aDef)
    aDefinitionSection.appendChild(anOverloadedSet)

    anOverloadedSet=ast.OverloadedSet(name,None)
    aParameterList=[]
    aType=ast.Type('integer')
    aMethodParameter=ast.MethodParameter('a',aType,None)
    aMethodParameter.valueOnly=True
    aParameterList.append(aMethodParameter)
    fname=name
    aDef=ast.SubroutineDef(fname,None, aParameterList)
    aDef.bindName=fname
    aDef.references=ast.ObjectReference(names.Fixed.precDeclN)
    anOverloadedSet.appendChild(aDef)
    aDefinitionSection.appendChild(anOverloadedSet)
    
  def generateGetLocation(self,aDefinitionSection):
    anOverloadedSet=ast.OverloadedSet('getLocation',None)
    for (c,(n,t,k)) in enumerate(self.activeTL):
      aParameterList=[]
      aType=ast.Type('integer')
      aMethodParameter=ast.MethodParameter('loc',aType,None)
      aParameterList.append(aMethodParameter)
      aType=ast.Type(t)
      aType.kind=self.precDict[k][0]
      aMethodParameter=ast.MethodParameter('addr',aType,None)
      aParameterList.append(aMethodParameter)
      name='getLocation'+k
      aDef=ast.SubroutineDef(name,None, aParameterList)
      aDef.bindName=name
      aDef.references=ast.ObjectReference(names.Fixed.precDeclN)
      anOverloadedSet.appendChild(aDef)
    aDefinitionSection.appendChild(anOverloadedSet)

  def generateFreeLocation(self,aDefinitionSection):
    for (c,(n,t,k)) in enumerate(self.activeTL):
      anOverloadedSet=ast.OverloadedSet('',None)
      aParameterList=[]
      aType=ast.Type('integer')
      aMethodParameter=ast.MethodParameter('loc',aType,None)
      aParameterList.append(aMethodParameter)
      aType=ast.Type(t)
      aType.kind=self.precDict[k][0]
      aMethodParameter=ast.MethodParameter('addr',aType,None)
      aParameterList.append(aMethodParameter)
      name='freeLocation'+k
      aDef=ast.SubroutineDef(name,None, aParameterList)
      aDef.bindName=name
      aDef.references=ast.ObjectReference(names.Fixed.precDeclN)
      anOverloadedSet.appendChild(aDef)
      aDefinitionSection.appendChild(anOverloadedSet)
    

  def generateSetGetAdjointLoc(self,name,aDefinitionSection):
    for (c,(n,t,k)) in enumerate(self.activeTL):
      anOverloadedSet=ast.OverloadedSet('',None)
      aParameterList=[]
      aType=ast.Type('integer')
      aMethodParameter=ast.MethodParameter('loc',aType,None)
      aParameterList.append(aMethodParameter)
      aType=ast.Type(t)
      aType.kind=self.precDict[k][0]
      aMethodParameter=ast.MethodParameter('value',aType,None)
      aParameterList.append(aMethodParameter)
      theName=name+k
      aDef=ast.SubroutineDef(theName,None, aParameterList)
      aDef.bindName=theName
      aDef.references=ast.ObjectReference(names.Fixed.precDeclN)
      anOverloadedSet.appendChild(aDef)
      aDefinitionSection.appendChild(anOverloadedSet)

  def generateVoidExterns(self,name,aDefinitionSection):
    anOverloadedSet=ast.OverloadedSet(name,None)
    aParameterList=[]
    aDef=ast.SubroutineDef(name,None,aParameterList)
    aDef.bindName=name
    anOverloadedSet.appendChild(aDef)
    aDefinitionSection.appendChild(anOverloadedSet)

  def generateConstGlobalExterns(self,aDefinitionSection):
    self.generateStackInterface(aDefinitionSection,'pushConstGlobal',[],0,0)

  def generateUnaryLocalExterns(self,aDefinitionSection):
    self.generateStackInterface(aDefinitionSection,'pushUnaryLocal',[],0,1)

  def generateBinaryLocalExterns(self,aDefinitionSection):
    self.generateStackInterface(aDefinitionSection,'pushBinaryLocal',[],0,2)

  def generateStackInterface(self, aDefinitionSection, name, aParameterList, currLevel, level):
    if (currLevel<=level):
      for (cl,(nl,tl,kl)) in enumerate(self.activeTL):
        if (currLevel==0):
          aType=ast.Type('integer')
          aMethodParameter=ast.MethodParameter('source',aType,'in')
          aMethodParameter.valueOnly=True
          aParameterList.append(aMethodParameter)
        else:
          aType=ast.Type(tl)
          aType.kind=self.precDict['D'][0]
          aMethodParameter=ast.MethodParameter('val'+str(currLevel),aType,'in')
          aMethodParameter.valueOnly=True
          aParameterList.append(aMethodParameter)
          aType=ast.Type('integer')
          aMethodParameter=ast.MethodParameter('operand'+str(currLevel),aType,'in')
          aMethodParameter.valueOnly=True
          aParameterList.append(aMethodParameter)
        self.generateStackInterface(aDefinitionSection,name+kl,aParameterList,currLevel+1,level)
        aParameterList.pop()
        if (currLevel!=0):
          aParameterList.pop()
#INTEGER PARAMETER is probable
    else:
      newName=name
      newParameterList=list(aParameterList)
      anOverloadedSet=ast.OverloadedSet('',None)
      aDef=ast.SubroutineDef(newName,None, newParameterList)
      aDef.bindName=newName
      aDef.references=ast.ObjectReference(names.Fixed.precDeclN)
#      aDef.fortranQualifiers = 'elemental'
      anOverloadedSet.appendChild(aDef)
      aDefinitionSection.appendChild(anOverloadedSet)


  def visitAddress(self,vertex):
    self.write('>')
    vertex.children.accept(self)

  def getLocationAssigned(self,name):
    return None

  def getLocation(self,name):
    return ast.StructDeref(ast.Variable(name),ast.Variable(names.Fixed.aN))
  def getAdjoint(self,name):
    return ast.StructDeref(ast.Variable(name),ast.Variable(names.Fixed.aN))

#Reverse_Mode End

#type convertion problem
# 1 is not 1.0 is not 1.0d0
# a tricky way is use constant equations to auto generate them. like (a/a) = 1 with the same type. (a-a)=0 with the same type.


class F90Output(F90Printer):
  '''
  This class prints the ast to the file system as Fortran90 source
  '''
  def __init__(self):
    F90Printer.__init__(self)
    self.f = None # the file handle
    return

  def visitSource(self, vertex):
    import os
    import Common.ast
    import filecmp
    if vertex.cppOnly :
      return
    tempExt='.tmp'
    if not (os.path.exists(self.oP)):
      os.makedirs(self.oP)
    if (isinstance(vertex, Common.ast.SimpleSource)):
      self.setFileName(vertex.identifier+vertex.extension)
      filename=self.oP+'/'+vertex.identifier+vertex.extension
      # print 'Creating', filename
      self.f = file(filename+tempExt, 'w')
      defaultFormat=self.fixedFormat
      if (not self.fixedFormat): 
        self.fixedFormat=vertex.fixedFormat
      if (vertex.identifier!='common'):
        ast.GenComment().accept(self)	
      num = len(vertex.children)
      for (c, child) in enumerate(vertex.children):
        child.accept(self)
      # reset possibly overwritten format
      self.fixedFormat=defaultFormat
    else:
      self.setFileName(vertex.identifier+self.sE)
      self.addObjName(vertex.identifier)
      filename=self.oP+'/'+vertex.identifier+self.sE
      # print 'Creating', filename
      self.f = file(filename+tempExt, 'w')
      defaultFormat=self.fixedFormat
      if (not self.fixedFormat): 
        self.fixedFormat=vertex.fixedFormat
      ast.GenComment().accept(self)	
      self.visitObjectSource(vertex)
      # reset possibly overwritten format
      self.fixedFormat=defaultFormat
    self.f.close()
    # see if the file is different
    if ((os.path.exists(filename)
         and
         not(filecmp.cmp(filename+tempExt,filename)))
        or
        not(os.path.exists(filename))):
      os.rename(filename+tempExt,filename)
    else:
      os.remove(filename+tempExt)
    return  
  
  def write(self, s):
    '''
    This is overridden to redirect output to a file
    and breaks long lines 
    '''
    self.f.write(self.insertLineBreaks(s))

