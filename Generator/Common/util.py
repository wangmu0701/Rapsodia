##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.ast as ast
import Common.names as cn
import Common.parameters as cp

def makeNaN():
  ''' generate a NaN '''
  return ast.FuncCall('makeFPE',[ast.Constant('0.0'),
                                 ast.Constant('0.0')])

def makeInf():
  ''' generate an Inf '''
  return ast.FuncCall('makeFPE',[ast.Constant('1.0'),
                                 ast.Constant('0.0')])

# Retrieve the derivation portion of var using a variable array access
# when slicing is enabled
def dOf(var, dir, deg, fullLoop=False):
  ''' var is the name of the variable; direction and degree start at 1 '''
  if cp.slices > 0 and (not cp.useQueue or fullLoop):
    arrayDeref = ast.ArrayDeref(cn.Fixed.sN)
    # variable reference to array
    arrayDeref.index = ast.Variable('i')
    return __getArrayStructDeref(var, dir, deg, arrayDeref)
  else:
    return __getStructDeref(var, dir, deg)

# Retrieve the derivation portion of var using a constant array access
# when slicing is enabled
def dOfC(var, dir, deg):
  ''' var is the name of the variable; direction and degree start at 1 '''
  if cp.slices > 0:
    arrayDeref = ast.ArrayDeref(cn.Fixed.sN)
    # constant reference to array
    arrayDeref.index = ast.Constant(str((dir-1) / cp.sliceSize + 1))
    return __getArrayStructDeref(var, dir, deg, arrayDeref)
  else:
    return __getStructDeref(var, dir, deg)

def __getArrayStructDeref(var, dir, deg, arrayDeref):
  return ast.StructDeref(ast.Variable(var), 
                         ast.StructDeref(arrayDeref, 
                                         ast.Variable(cn.Variable.dN
                                                      [(dir-1) % cp.sliceSize]
                                                      [deg-1])))

def __getStructDeref(var, dir, deg):
  return ast.StructDeref(ast.Variable(var),
                         ast.Variable(cn.Variable.dN[dir-1][deg-1]))

# Get the value component of the given variable name
def vOf(var):
  ''' var is the name of the variable '''
  return ast.StructDeref(ast.Variable(var), ast.Variable(cn.Fixed.vN))

def lOf(var):
  ''' var is the name of the variable '''
  return ast.StructDeref(ast.Variable(var), ast.Variable(cn.Fixed.lN))

def aOf(var):
  ''' var is the name of the variable '''
  return ast.StructDeref(ast.Variable(var), ast.Variable(cn.Fixed.aN))

def getVarGlobalName(varName):
  if cp.openmpUseOrphaning:
    return varName + 'Global'
  else:
    return varName

def getVarValueName(varName):
  if cp.useQueue:
    return varName + '_value' 
  else:
    return varName

def getVarSliceName(varName):
  return varName + '_slice'

def getVarStructName(varName):
  if cp.useQueue:
    return varName + '_struct'
  else:
    return varName

def appendDirDecls(type, uDefType):
  ''' append direction types to a user-defined type'''
  for i in cn.Variable.dN:
    for j in i:
      aDeclarator = ast.Declarator(j)
      aDeclarator.type = type
      uDefType.appendChild(aDeclarator)

def appendUsingNamespace(prec, intrinsic):
    intrinsic.appendChild(
        ast.Special('using namespace %s;' % (prec + 'Prec')))
     
import Cpp.QueueUtils as queue

class Util:
  ''' low level support for code generation '''
  
  def __init__(self, aPrinter):
    self.p = aPrinter
    self.handleFPE = False

  def generateBinaryIntrinsic(self,
                              name,
                              operator,
                              extraVarsDict,
                              extraReferences,
                              separateIntBodies,
                              compOperator,
                              requireSameKind,
                              resultTypeRegime):
    ''' generate the generic interface and definitions (without definitions 
    body) for most binary intrinsic operators '''
    aSource = self.__getSource(name, operator, extraReferences)
    self.generateBinaryIntrinsicDefinitions(aSource.decls,
                                            name,
                                            operator,
                                            extraVarsDict,
                                            separateIntBodies,
                                            False,
                                            compOperator,
                                            requireSameKind,
                                            resultTypeRegime)
    self.generateBinaryIntrinsicDefinitions(aSource.defs,
                                            name,
                                            operator,
                                            extraVarsDict,
                                            separateIntBodies,
                                            True,
                                            compOperator,
                                            requireSameKind,
                                            resultTypeRegime)
    return aSource

  def generateBinaryIntrinsicDefinitions(self,
                                         aBlock,
                                         name,
                                         operator,
                                         extraVarsDict,
                                         separateIntBodies,
                                         withBody,
                                         compOperator,
                                         requireSameKind,
                                         resultTypeRegime):

    compOpsList = ['eq', 'ne', 'lt', 'le', 'gt', 'ge']

    # active/active combinations

    for (cl,(nl,tl,kl)) in enumerate(self.p.activeTL) : 
      for (cr,(nr,tr,kr)) in enumerate(self.p.activeTL) :
        if (requireSameKind and (tl!=tr or kl!=kr)):
          continue;
        paramsAndBodyDisc = self.__getBinaryIntrinsicArgs([ 'A', 'a', nl ],
                                                          [ 'A', 'b', nr ],
                                                          None)
        aParameterList = paramsAndBodyDisc[0]

        resultTypes = self.__getResultTypes(compOperator, resultTypeRegime,
                                            tl, kl, tr, kr, nl)

        anIntrinsic = self.__getIntrinsicDef(name, operator, nl + nr, 
                                             aParameterList, 
                                             'r', resultTypes[0])

        if withBody:
          if cp.useQueue and not (name in compOpsList or name == 'pow'):
            queue.genActiveActiveBinaryMethod(self, name, 
                                              nl, tl, kl, nr, tr, kr, 
                                              extraVarsDict, 
                                              resultTypes, aBlock)
          self.__appendBinaryIntrinsicBody(name, operator, nl, 
                                           tl, kl, tr, kr, 'AA', 
                                           extraVarsDict, 
                                           resultTypes, anIntrinsic)
        aBlock.appendChild(anIntrinsic)

    # active/passive combinations

    for (cl,(nl,tl,kl)) in enumerate(self.p.activeTL) : 
      hit = False
      for (cr,(tr,kr)) in enumerate(self.p.passiveTypeList) :
        if (requireSameKind and (tl!=tr or kl!=kr)):
          continue;
        paramsAndBodyDisc = self.__getBinaryIntrinsicArgs([ 'A', 'a', nl ],
                                                          [ 'P', 'b', tr, kr ],
                                                          separateIntBodies)
        aParameterList    = paramsAndBodyDisc[0]
        bodyDiscriminator = paramsAndBodyDisc[1]

        resultTypes = self.__getResultTypes(compOperator, resultTypeRegime,
                                            tl, kl, tr, kr, nl)

        # the mangled name for FORTRAN
        if not (kr is None):
          pMangle=nl+tr+kr
        else:
          pMangle=nl+tr

        anIntrinsic = self.__getIntrinsicDef(name, operator, pMangle, 
                                             aParameterList, 
                                             'r', resultTypes[0])

        if withBody:
          if cp.useQueue and not hit and not name in compOpsList:
            queue.genActivePassiveBinaryMethod(self, name, 
                                               nl, tl, kl, nr, tr, kr, 
                                               bodyDiscriminator, 
                                               extraVarsDict,
                                               resultTypes, aBlock)
            hit = True
          self.__appendBinaryIntrinsicBody(name, operator, nl, 
                                           tl, kl, tr, kr, 
                                           bodyDiscriminator, extraVarsDict, 
                                           resultTypes, anIntrinsic)
        aBlock.appendChild(anIntrinsic)

    # passive/active combinations

    hit = False
    for (cl,(tl,kl)) in enumerate(self.p.passiveTypeList) :
      for (cr,(nr,tr,kr)) in enumerate(self.p.activeTL) : 
        if (requireSameKind and (tl!=tr or kl!=kr)):
          continue;
        paramsAndBodyDisc = self.__getBinaryIntrinsicArgs([ 'P', 'a', tl, kl ],
                                                          [ 'A', 'b', nr     ],
                                                          separateIntBodies)
        aParameterList = paramsAndBodyDisc[0]
        bodyDiscriminator = paramsAndBodyDisc[1]

        # determine the result type
        if kl is None:
          leftKind = None
        else:
          leftKind = self.p.precDict[kl][0]

        resultTypes = self.__getResultTypes(compOperator, resultTypeRegime,
                                            tl, kl, tr, kr, tl, leftKind)

        # the mangled name for FORTRAN
        if not (kl is None):
          pMangle=tl+kl+nr
        else:
          pMangle=tl+nr

        anIntrinsic = self.__getIntrinsicDef(name, operator, pMangle, 
                                             aParameterList, 
                                             'r', resultTypes[0])
        
        if withBody:
          if cp.useQueue and not hit and \
             not (name in compOpsList or name == 'pow'):
            queue.genPassiveActiveBinaryMethod(self, name, 
                                               nl, tl, kl, nr, tr, kr, 
                                               bodyDiscriminator, 
                                               extraVarsDict,
                                               resultTypes, aBlock)
          self.__appendBinaryIntrinsicBody(name, operator, nr, 
                                           tl, kl, tr, kr, 
                                           bodyDiscriminator, extraVarsDict, 
                                           resultTypes, anIntrinsic)
        aBlock.appendChild(anIntrinsic)
      hit = True

  def generatePassivatingOp(self,name, returnTypeReduction):
    return self.generateUnaryOpAll(name,
                                   None,
                                   cn.Fixed.pN+name,
                                   None,
                                   'r',
                                   returnTypeReduction,
                                   [],
                                   [],
                                   [],
                                   [])

  def generateUnaryOp(self,name,opName,localActiveVarList,localPassiveVarList):
    return self.generateUnaryOpAll(name,
                                   opName,
                                   cn.Fixed.pN+name,
                                   None,
                                   'r',
                                   None,
                                   localActiveVarList,
                                   localPassiveVarList,
                                   [],
                                   [])

  ## generates a generic definition for unary operations/operators
  # @param self the class reference
  # @param name the operation name also part of the file name
  # @param opName the operator name, can be None for intrinsics that are not operators
  # @param bodyName the name part for the include file containing the generic logic
  # @param complexDiscriminator if the bodyName needs some distinction for complex arguments
  # @param returnName name the of the return variable
  # @param returnTypeReduction is not None if the return type does not follow the generic type inference from the argument types
  # @param localActiveVarList names of active local variables to be declared, type is the same as the result type
  # @param localPassiveVarList names of passive local variables to be declared, type is the same as the base floating point type used in the  result type
  # @param intParmList names of local  integer variables to be declared
  # @param extraReferences refers to other generated objectsources aside from precision and type definitions
  def generateUnaryOpAll(self,
                         name,
                         opName,
                         bodyName,
                         complexDiscriminator,
                         returnName,
                         returnTypeReduction,
                         localActiveVarList,
                         localPassiveVarList,
                         intParmList,
                         extraReferences):
    aSource = self.__getSource(name, opName, extraReferences)
    self.generateUnaryIntrinsicDefinitions(name,
                                           opName,
                                           bodyName,
                                           complexDiscriminator,
                                           returnName,
                                           returnTypeReduction,
                                           localActiveVarList,
                                           localPassiveVarList,
                                           intParmList,
                                           False,
                                           aSource.decls)
    self.generateUnaryIntrinsicDefinitions(name,
                                           opName,
                                           bodyName,
                                           complexDiscriminator,
                                           returnName,
                                           returnTypeReduction,
                                           localActiveVarList,
                                           localPassiveVarList,
                                           intParmList,
                                           True,
                                           aSource.defs)
    return aSource

  def generateUnaryIntrinsicDefinitions(self,
                                        name,
                                        opName,
                                        bodyName,
                                        complexDiscriminator,
                                        returnName,
                                        returnTypeReduction,
                                        localActiveVarList,
                                        localPassiveVarList,
                                        intParmNames,
                                        withBody,
                                        aDefinitionsBlock):

    if cp.useQueue and withBody and name != 'tan':
      queue.genUnaryMethod(self.p, name, bodyName, returnName, 
                           localActiveVarList, localPassiveVarList,
                           aDefinitionsBlock)

    for n,t,k in self.p.activeTL :
      aParameterList=[]
      # the active argument
      aType=ast.Type(n)
      aType.baseType=False
      if (returnTypeReduction
          and
          returnTypeReduction=='matchKindReturn'
          and
          not self.p.isComplexType(aType)) :
        continue
      aParameterList.append(ast.MethodParameter('a',aType,'in'))
      # optional integer parameters
      for intParm in intParmNames:
        aParameterList.append(ast.MethodParameter(intParm,ast.Type(self.p.passiveTypeList[0][0]),'in'))
      rType=None
      if returnTypeReduction:
        if (returnTypeReduction=='integerReturn'):
          # this is a hack, because it doesn't take into account the
          # optional KIND parameter provided for INT in the Fortran standard 
          rType=ast.Type(self.p.passiveTypeList[0][0])
        elif (returnTypeReduction=='matchKindReturn'):
          # reduce from complex to real with matching kind
          rType=self.p.getMatchingReal(aType)
        else:
          raise Exception('no logic for '+returnTypeReduction)
      else: # simple rule for active result
        rType=ast.Type(n)
        rType.baseType=False

      anIntrinsic = self.__getIntrinsicDef(name, opName, n, aParameterList,
                                           returnName, rType)
      if withBody:
        if cp.useQueue:
          if name == 'tan':
            anIntrinsic.appendChild(ast.Include(bodyName + self.p.iE))
            queue.appendToIntrinsicBody(self, n, k, anIntrinsic)
          else:
            queue.genUnaryOpBody(name, returnName, localActiveVarList, n, k, 
                                 anIntrinsic)
        else:
          anIntrinsic.appendChild(self.p.setIterator())
          # the local active variables
          for localVar in localActiveVarList:
            aDeclarator=ast.Declarator(localVar)
            anIntrinsic.appendChild(aDeclarator)
            aType=ast.Type(n)
            aType.baseType=False
            aDeclarator.type=aType
          # the local passive variables
          for localVar in localPassiveVarList:
            aDeclarator=ast.Declarator(localVar)
            anIntrinsic.appendChild(aDeclarator)
            aDeclarator.type=ast.Type(t)
            aDeclarator.type.kind=self.p.precDict[k][0]
          bodyDiscName=bodyName  
          if (self.p.isComplexType(aType) and not complexDiscriminator is None):
            bodyDiscName+=complexDiscriminator
          if cp.openmpUseOrphaning:
            appendUsingNamespace(n, anIntrinsic)
          anIntrinsic.appendChild(ast.Include(bodyDiscName+self.p.iE))
      aDefinitionsBlock.appendChild(anIntrinsic)
    return aDefinitionsBlock

  def generateUnaryArrayOpAll(self,
                              name,
                              opName,
                              bodyName,
                              bodyNameWithDim,
                              returnName,
                              returnTypeReduction,
                              extraVariables,
                              intParmList,
                              extraReferences):
    aSource = self.__getSource(name, opName, extraReferences)
    self.generateUnaryArrayOpDefinitions(name,
                                         opName,
                                         bodyName,
                                         bodyNameWithDim,
                                         returnName,
                                         returnTypeReduction,
                                         extraVariables,
                                         intParmList,
                                         False,
                                         aSource.decls)
    self.generateUnaryArrayOpDefinitions(name,
                                         opName,
                                         bodyName,
                                         bodyNameWithDim,
                                         returnName,
                                         returnTypeReduction,
                                         extraVariables,
                                         intParmList,
                                         True,
                                         aSource.defs)
    return aSource

  def generateUnaryArrayOpDefinitions(self,
                                      name,
                                      opName,
                                      bodyName,
                                      bodyNameWithDim,
                                      returnName,
                                      returnTypeReduction,
                                      extraVariables,
                                      intParmNames,
                                      withBody,
                                      aDefinitionsBlock):

    iterator = self.p.setIterator()

    for dimensions in range(1,8):
      for n,t,k in self.p.activeTL :      
        aParameterList=[]
        # the active argument
        aType=ast.Type(n)
        aType.baseType=False
        aParameterList.append(ast.MethodParameter('a',aType,'in',dimensions))
        # optional integer parameters
        for intParm in intParmNames:
          aParameterList.append(ast.MethodParameter(intParm,ast.Type(self.p.passiveTypeList[0][0]),'in'))
        if (returnTypeReduction and returnTypeReduction=='subscriptReturn'):
          rType=ast.Type(self.p.passiveTypeList[0][0])
          methodParam = ast.MethodParameter(returnName, rType, None, 
                                            1, [ast.Constant(str(dimensions))])
        else:
          rType=ast.Type(n)
          rType.baseType=False
          methodParam = ast.MethodParameter(returnName, rType, None)
        anIntrinsic = ast.IntrinsicDef(name, n + str(dimensions),
                                       aParameterList, methodParam)
        anIntrinsic.operatorName=opName
        if withBody:
          if (extraVariables):
            extraVariables(self,anIntrinsic,rType,dimensions)
          iName=bodyName  
          if (bodyNameWithDim):
            iName+=str(dimensions)
          anIntrinsic.appendChild(iterator)
          anIntrinsic.appendChild(ast.Include(iName+self.p.iE))
        aDefinitionsBlock.appendChild(anIntrinsic)
    return aDefinitionsBlock

  def generateConvolution(self,left,right,direct,sumOperation):
    ''' left and right must be a list that can be passed to dOf() 
        i.e., contains [variable name, degree start, degree end] '''
    # upper-lower+1, should match right's upper-lower+1
    summandCount=left[2]-left[1]+1 
    summands=[]
    for i in range(summandCount):
      if left[1]+i==0: 
        leftOp=vOf(getVarValueName(left[0]))
      else:
        leftOp=dOf(left[0],direct,left[1]+i)
      if right[2]-i==0: 
        rightOp=vOf(getVarValueName(right[0]))
      else:
        rightOp=dOf(right[0],direct,right[2]-i)
      summands.append(ast.Multiplication(leftOp,rightOp))
    if sumOperation=='minus':
      summands[0]=ast.UnaryMinus(summands[0])
    anExpression=self.buildConvTree(summands,sumOperation)
    return anExpression

  def buildConvTree(self,summands,sumOperation) :
    sumlen=len(summands)
    if sumlen==1:
      anExpression=summands[0]
    else:
      if sumOperation=='minus':
        anExpression=ast.Subtraction(self.buildConvTree(summands[:sumlen/2],
                                                        sumOperation), #left sub tree
                                        self.buildConvTree(summands[sumlen/2:],
                                                           sumOperation))   # right sub tree
      if sumOperation=='plus':
        anExpression=ast.Addition(self.buildConvTree(summands[:sumlen/2],
                                                     sumOperation), #left sub tree
                                     self.buildConvTree(summands[sumlen/2:],
                                                        sumOperation))   # right sub tree
    return anExpression
    
  def generateBinaryArrayOp(self,name,operator,extraVarsDict,extraReferences,
      separateIntBodies,compOperator,requireSameKind=False):
    ''' generate the generic interface and definitions (without definitions 
        body) for array ops '''
    aSource = self.__getSource(name, operator, extraReferences)
    self.generateBinaryArrayOpDefinitions(aSource.decls,
                                          name,
                                          operator,
                                          extraVarsDict,
                                          separateIntBodies,
                                          False,
                                          compOperator,
                                          requireSameKind)
    self.generateBinaryArrayOpDefinitions(aSource.defs,
                                          name,
                                          operator,
                                          extraVarsDict,
                                          separateIntBodies,
                                          True,
                                          compOperator,
                                          requireSameKind)
    return aSource

  def generateBinaryArrayOpDefinitions(self,
                                       aBlock,
                                       name,
                                       operator,
                                       extraVarsDict,
                                       separateIntBodies,
                                       withBody,
                                       compOperator,
                                       requireSameKind):
    for (diml,dimr) in [(2,2),(1,2),(2,1)] : 
      # active/active combinations
      for (cl,(nl,tl,kl)) in enumerate(self.p.activeTL) : 
        for (cr,(nr,tr,kr)) in enumerate(self.p.activeTL) :
          if (requireSameKind and (tl!=tr or kl!=kr)):
            continue;
          aParameterList=[]
          # the active arguments
          aType=ast.Type(nl)
          aType.baseType=False
          aParameterList.append(ast.MethodParameter('a',aType,'in',diml))
          aType=ast.Type(nr)
          aType.baseType=False
          aParameterList.append(ast.MethodParameter('b',aType,'in',dimr))
          # the active result
          # determine the result type
          resultTypes=self.__arrayResultType(tl,kl,diml,tr,kr,dimr)
          anIntrinsic=ast.IntrinsicDef(name,nl+nr+str(diml)+str(dimr),
                                       aParameterList,
                                       ast.MethodParameter('r',resultTypes[0],
                                                           None,resultTypes[2],
                                                           resultTypes[3]))
          anIntrinsic.operatorName=operator
          if withBody:
            if 'AA' in extraVarsDict :
              extraVarsDict['AA'](self,anIntrinsic,resultTypes,
                                  (tl,kl),diml,(tr,kr),dimr)
            anIntrinsic.appendChild(ast.Include(cn.Fixed.pN+name+str(diml)
                                                +str(dimr)+self.p.iE))
          aBlock.appendChild(anIntrinsic)
      # active/passive combinations
      for (cl,(nl,tl,kl)) in enumerate(self.p.activeTL) : 
        for (cr,(tr,kr)) in enumerate(self.p.passiveTypeList) :
          if (requireSameKind and (tl!=tr or kl!=kr)):
            continue;
          aParameterList=[]
          # the active arguments
          aType=ast.Type(nl)
          aType.baseType=False
          aParameterList.append(ast.MethodParameter('a',aType,'in',diml))
          # the passive argument
          aType=ast.Type(tr)
          bodyDiscriminator='AP'
          if not(kr is None):
            aType.kind=self.p.precDict[kr][0]
          else:
            if separateIntBodies:
              bodyDiscriminator='APi'
          aParameterList.append(ast.MethodParameter('b',aType,'in',dimr))
          # the active result
          # determine the result type
          resultTypes=self.__arrayResultType(tl,kl,diml,tr,kr,dimr)
          # the name
          if not (kr is None):
            pMangle=nl+tr+kr
          else:
            pMangle=nl+tr
          anIntrinsic=ast.IntrinsicDef(name,pMangle+str(diml)+str(dimr),
                                       aParameterList,
                                       ast.MethodParameter('r',resultTypes[0],
                                                           None,resultTypes[2],
                                                           resultTypes[3]))
          anIntrinsic.operatorName=operator
          if withBody:
            if bodyDiscriminator in extraVarsDict :
              extraVarsDict[bodyDiscriminator](self,anIntrinsic,resultTypes,
                                               (tl,kl),diml,(tr,kr),dimr)
            anIntrinsic.appendChild(ast.Include(cn.Fixed.pN+name+str(diml)
                                                +str(dimr)+self.p.iE))
          aBlock.appendChild(anIntrinsic)
      # passive/active combinations
      for (cl,(tl,kl)) in enumerate(self.p.passiveTypeList) :
        for (cr,(nr,tr,kr)) in enumerate(self.p.activeTL) : 
          if (requireSameKind and (tl!=tr or kl!=kr)):
            continue;
          aParameterList=[]
          # the passive argument
          aType=ast.Type(tl)
          bodyDiscriminator='PA'
          if not(kl is None):
            aType.kind=self.p.precDict[kl][0]
          else:
            if separateIntBodies:
              bodyDiscriminator='PiA'
          aParameterList.append(ast.MethodParameter('a',aType,'in',diml))
          # the active argument
          aType=ast.Type(nr)
          aType.baseType=False
          aParameterList.append(ast.MethodParameter('b',aType,'in',dimr))
          # the active result
          # determine the result type
          resultTypes=self.__arrayResultType(tl,kl,diml,tr,kr,dimr)
          if not (kl is None):
            pMangle=tl+kl+nr
          else:
            pMangle=tl+nr
          anIntrinsic=ast.IntrinsicDef(name,pMangle+str(diml)+str(dimr),
                                       aParameterList,
                                       ast.MethodParameter('r',resultTypes[0],
                                                           None,resultTypes[2],
                                                           resultTypes[3]))
          anIntrinsic.operatorName=operator
          if withBody:
            if bodyDiscriminator in extraVarsDict :
              extraVarsDict[bodyDiscriminator](self,anIntrinsic,resultTypes,
                                               (tl,kl),diml,(tr,kr),dimr)
            anIntrinsic.appendChild(ast.Include(cn.Fixed.pN+name+str(diml)
                                                +str(dimr)+self.p.iE))
          aBlock.appendChild(anIntrinsic)


  def generateCompoundIntrinsic(self,
                         name,
                         opName,
                         bodyName,
			 extraReferences):
    aSource = self.__getSource(name, opName,extraReferences)
    self.generateCompoundIntrinsicDefinition(name,opName,bodyName,False,aSource.decls)
    self.generateCompoundIntrinsicDefinition(name,opName,bodyName,True, aSource.defs)
    return aSource
  
  def generateCompoundIntrinsicDefinition(self,name,opName,bodyName,withBody,aBlock):
    # active/active combinations
    for (cl,(nl,tl,kl)) in enumerate(self.p.activeTL) : 
      for (cr,(nr,tr,kr)) in enumerate(self.p.activeTL) :
        if (kl=='S') and (kr=='D'):          #loss precision
          continue;
        aParameterList = []
        aType=ast.Type(nr)
        aType.baseType=False
        retType=ast.Type(nl)
        retType.baseType=False
        aParameterList.append(ast.MethodParameter('r',retType,'inout'))
        aParameterList.append(ast.MethodParameter('b',aType,'in'))
        anIntrinsic=ast.IntrinsicDef(name, None, aParameterList,None)
        anIntrinsic.operatorName=opName

        if withBody:
          if cp.useQueue:
            queue.genCompoundBinaryMethod(self, name, 
                                              nl, tl, kl, nr, tr, kr, 
                                              {}, 
                                              None, aBlock,'AA')
          self.__appendCompoundIntrinsicBody(name, opName, nl, 
                                           tl, kl, tr, kr,'AA',
                                           {}, 
                                           None, anIntrinsic)
        aBlock.appendChild(anIntrinsic)

    # active/passive combinations
    for (cl,(nl,tl,kl)) in enumerate(self.p.activeTL) : 
      hit = False
      for (cr,(tr,kr)) in enumerate(self.p.passiveTypeList) :
        if ((kl=='S') and (kr=='D')):          #loss precision
          continue;
        aParameterList = []
        if (kr):
          aType=ast.Type(self.p.precDict[kr][0])
        else:
          aType=ast.Type(tr)

        retType=ast.Type(nl)
        retType.baseType=False
        aParameterList.append(ast.MethodParameter('r',retType,'inout'))
        aParameterList.append(ast.MethodParameter('b',aType,'in'))

        anIntrinsic=ast.IntrinsicDef(name, None, aParameterList,None)
        anIntrinsic.operatorName=opName

        if withBody:
          if (cp.useQueue) and (not hit):
            queue.genCompoundBinaryMethod(self, name, 
                                               nl, tl, kl, nr, tr, kr,                                             
                                               {},
                                               None, aBlock,'AP')
          hit=True

          self.__appendCompoundIntrinsicBody(name, opName, nl, 
                                           tl, kl, tr, kr,'AP', 
                                           {}, 
                                           None, anIntrinsic)

        aBlock.appendChild(anIntrinsic)


  def __appendCompoundIntrinsicBody(self, name, op, precName, 
                                  tl, kl, tr, kr, bodyDiscriminator, 
                                  extraVarsDict, resultTypes, intrinsic):

    include = cn.Fixed.pN + name + bodyDiscriminator + self.p.iE

    if cp.openmpUseOrphaning and not cp.useQueue:
      appendUsingNamespace(precName, intrinsic)

    if cp.useQueue:
        queue.genCompoundBinaryOpBody(name, op,precName, kl, kr, intrinsic,bodyDiscriminator)
    else:
      if name=='eqdiv':
        aDeclarator=ast.Declarator('a')
        aDeclarator.type=ast.Type(precName)
        aDeclarator.base=False
        aDeclarator.initializer=ast.Variable('r')
        intrinsic.appendChild(aDeclarator)
        aDeclarator=ast.Declarator('recip')
        aDeclarator.type=ast.Type(self.p.precDict[kl][0])
        intrinsic.appendChild(aDeclarator)
      intrinsic.appendChild(self.p.setIterator())
      intrinsic.appendChild(ast.Include(include))
    

#Reverse_Mode Begin, for the first version, we only implement very basic features. No queue, no slice
  def generateCompoundIntrinsicReverse(self,
                         name,
                         opName,
                         bodyName,
			 getStatementAA,
			 getStatementAP,
			 getStatementPA):
    aSource = self.__getSource(name, opName, [])
    self.generateCompoundIntrinsicDefinitionReverse(name,opName,bodyName,False,aSource.decls,getStatementAA,getStatementAP,getStatementPA)
    self.generateCompoundIntrinsicDefinitionReverse(name,opName,bodyName,True, aSource.defs, getStatementAA,getStatementAP,getStatementPA)
    return aSource
  
  def generateCompoundIntrinsicDefinitionReverse(self,name,opName,bodyName,withBody,aBlock,getStatementAA,getStatementAP,getStatementPA):
    # active/active combinations
    for (cl,(nl,tl,kl)) in enumerate(self.p.activeTL) : 
      for (cr,(nr,tr,kr)) in enumerate(self.p.activeTL) :
        if (kl=='S') and (kr=='D'):          #loss precision
          continue;
        aParameterList = []
        aType=ast.Type(nr)
        aType.baseType=False
        retType=ast.Type(nl)
        retType.baseType=False
        aParameterList.append(ast.MethodParameter('r',retType,'inout'))
        aParameterList.append(ast.MethodParameter('a',aType,'in'))
        anIntrinsic=ast.IntrinsicDef(name, None, aParameterList,None)
        anIntrinsic.operatorName=opName

        if withBody:
          getStatementAA(self,anIntrinsic,name,kl,kr,[retType])

        aBlock.appendChild(anIntrinsic)

    # active/passive combinations
    for (cl,(nl,tl,kl)) in enumerate(self.p.activeTL) : 
      hit = False
      for (cr,(tr,kr)) in enumerate(self.p.passiveTypeList) :
        if ((kl=='S') and (kr=='D')):          #loss precision
          continue;
        aParameterList = []
        if (kr):
          aType=ast.Type(self.p.precDict[kr][0])
        else:
          aType=ast.Type(tr)

        retType=ast.Type(nl)
        retType.baseType=False
        aParameterList.append(ast.MethodParameter('r',retType,'inout'))
        aParameterList.append(ast.MethodParameter('a',aType,'in'))

        anIntrinsic=ast.IntrinsicDef(name, None, aParameterList,None)
        anIntrinsic.operatorName=opName

        if withBody:
          getStatementAP(self,anIntrinsic,name,kl,[retType])

        aBlock.appendChild(anIntrinsic)

    

  def generateUnaryIntrinsicReverse(self,
                         name,
                         opName,
                         bodyName,
                         complexDiscriminator,
                         returnName,
                         returnTypeReduction,
                         localActiveVarList,
                         localPassiveVarList,
                         intParmList,
                         extraReferences,
			 getStatementA):
    aSource = self.__getSource(name, opName, extraReferences)
    self.generateUnaryIntrinsicDefinitionsReverse(name,
                                           opName,
                                           bodyName,
                                           complexDiscriminator,
                                           returnName,
                                           returnTypeReduction,
                                           localActiveVarList,
                                           localPassiveVarList,
                                           intParmList,
                                           False,
                                           aSource.decls,
					   getStatementA)
    self.generateUnaryIntrinsicDefinitionsReverse(name,
                                           opName,
                                           bodyName,
                                           complexDiscriminator,
                                           returnName,
                                           returnTypeReduction,
                                           localActiveVarList,
                                           localPassiveVarList,
                                           intParmList,
                                           True,
                                           aSource.defs,
					   getStatementA)
    return aSource

  def generateUnaryIntrinsicDefinitionsReverse(self,
                                        name,
                                        opName,
                                        bodyName,
                                        complexDiscriminator,
                                        returnName,
                                        returnTypeReduction,
                                        localActiveVarList,
                                        localPassiveVarList,
                                        intParmNames,
                                        withBody,
                                        aDefinitionsBlock,
					getStatementA):

    for n,t,k in self.p.activeTL :
      aParameterList=[]
      # the active argument
      aType=ast.Type(n)
      aType.baseType=False
      aParameterList.append(ast.MethodParameter('a',aType,'in'))
      # optional integer parameters
      rType=None
      if (returnTypeReduction):
        rType=ast.Type('integer')
      else:
        rType=ast.Type(n)
        rType.baseType=False
      anIntrinsic = self.__getIntrinsicDef(name, opName, n, aParameterList,
                                           returnName, rType)
      if withBody:
        for localVar in localPassiveVarList:
          aDeclarator=ast.Declarator(localVar)
          anIntrinsic.appendChild(aDeclarator)
          aDeclarator.type=ast.Type(t)
          aDeclarator.type.kind=self.p.precDict[k][0]

        if (cp.F90):
          aParameterList=[]
          aParameterList.append(lOf('r'))
          aParameterList.append(aOf('r'))
          if not (returnTypeReduction):
            anIntrinsic.appendChild(ast.SubroutineCall('getLocation',aParameterList))
        getStatementA(self,anIntrinsic,name,k,[rType])
      aDefinitionsBlock.appendChild(anIntrinsic)
    return aDefinitionsBlock


  def generateBinaryIntrinsicReverse(self,
                              name,
                              operator,
                              extraVarsList,
                              extraReferences,
                              separateIntBodies,
                              compOperator,
                              requireSameKind,
                              resultTypeRegime,
                              getStatementAA,
                              getStatementAP,
                              getStatementPA):
    ''' generate the generic interface and definitions (without definitions 
    body) for most binary intrinsic operators '''
    aSource = self.__getSource(name, operator, extraReferences)
    self.generateBinaryIntrinsicDefinitionsReverse(aSource.decls,
                                            name,
                                            operator,
                                            extraVarsList,
                                            separateIntBodies,
                                            False,
                                            compOperator,
                                            requireSameKind,
                                            resultTypeRegime,
                                            getStatementAA,
                                            getStatementAP,
                                            getStatementPA)
    self.generateBinaryIntrinsicDefinitionsReverse(aSource.defs,
                                            name,
                                            operator,
                                            extraVarsList,
                                            separateIntBodies,
                                            True,
                                            compOperator,
                                            requireSameKind,
                                            resultTypeRegime,
                                            getStatementAA,
                                            getStatementAP,
                                            getStatementPA)
    return aSource
  
  def generateBinaryIntrinsicDefinitionsReverse(self,
                                         aBlock,
                                         name,
                                         operator,
                                         extraVarsList,
                                         separateIntBodies,
                                         withBody,
                                         compOperator,
                                         requireSameKind,
                                         resultTypeRegime,
                                         getStatementAA,
                                         getStatementAP,
                                         getStatementPA):

    compOpsList = ['eq', 'ne', 'lt', 'le', 'gt', 'ge']

    # active/active combinations
    for (cl,(nl,tl,kl)) in enumerate(self.p.activeTL) : 
      for (cr,(nr,tr,kr)) in enumerate(self.p.activeTL) :
        if (requireSameKind and (tl!=tr or kl!=kr)):
          continue;
        paramsAndBodyDisc = self.__getBinaryIntrinsicArgs([ 'A', 'a', nl ],
                                                          [ 'A', 'b', nr ],
                                                          None)
        aParameterList = paramsAndBodyDisc[0]

        resultTypes = self.__getResultTypes(compOperator, resultTypeRegime,
                                            tl, kl, tr, kr, nl)

        anIntrinsic = self.__getIntrinsicDef(name, operator, nl + nr, 
                                             aParameterList, 
                                             'r', resultTypes[0])

        if withBody:
          for localVar in extraVarsList:
            aDeclarator=ast.Declarator(localVar)
            anIntrinsic.appendChild(aDeclarator)
            aDeclarator.type=ast.Type(tl)
            aDeclarator.type.kind=self.p.precDict[kl][0]


          if (cp.F90):
            aParameterList=[]
            aParameterList.append(lOf('r'))
            aParameterList.append(aOf('r'))
            if (not compOperator):
              anIntrinsic.appendChild(ast.SubroutineCall('getLocation',aParameterList))
          getStatementAA(self,anIntrinsic,name,kl,kr,resultTypes)

        aBlock.appendChild(anIntrinsic)

    # active/passive combinations

    for (cl,(nl,tl,kl)) in enumerate(self.p.activeTL) : 
      hit = False
      for (cr,(tr,kr)) in enumerate(self.p.passiveTypeList) :
        if (requireSameKind and (tl!=tr or kl!=kr)):
          continue;
        paramsAndBodyDisc = self.__getBinaryIntrinsicArgs([ 'A', 'a', nl ],
                                                          [ 'P', 'b', tr, kr ],
                                                          separateIntBodies)
        aParameterList    = paramsAndBodyDisc[0]
        bodyDiscriminator = paramsAndBodyDisc[1]

        resultTypes = self.__getResultTypes(compOperator, resultTypeRegime,
                                            tl, kl, tr, kr, nl)

        # the mangled name for FORTRAN
        if not (kr is None):
          pMangle=nl+tr+kr
        else:
          pMangle=nl+tr

        anIntrinsic = self.__getIntrinsicDef(name, operator, pMangle, 
                                             aParameterList, 
                                             'r', resultTypes[0])

        if withBody:
          for localVar in extraVarsList:
            aDeclarator=ast.Declarator(localVar)
            anIntrinsic.appendChild(aDeclarator)
            aDeclarator.type=ast.Type(tl)
            aDeclarator.type.kind=self.p.precDict[kl][0]

          if (cp.F90):
            aParameterList=[]
            aParameterList.append(lOf('r'))
            aParameterList.append(aOf('r'))
            if (not compOperator):
              anIntrinsic.appendChild(ast.SubroutineCall('getLocation',aParameterList))
          getStatementAP(self,anIntrinsic,name,kl,resultTypes)

        aBlock.appendChild(anIntrinsic)

    # passive/active combinations

    for (cl,(tl,kl)) in enumerate(self.p.passiveTypeList) :
      for (cr,(nr,tr,kr)) in enumerate(self.p.activeTL) : 
        if (requireSameKind and (tl!=tr or kl!=kr)):
          continue;

        paramsAndBodyDisc = self.__getBinaryIntrinsicArgs([ 'P', 'a', tl, kl ],
                                                          [ 'A', 'b', nr     ],
                                                          separateIntBodies)
        aParameterList = paramsAndBodyDisc[0]
        bodyDiscriminator = paramsAndBodyDisc[1]

        # determine the result type
        if kl is None:
          leftKind = None
        else:
          leftKind = self.p.precDict[kl][0]

        resultTypes = self.__getResultTypes(compOperator, resultTypeRegime,
                                            tl, kl, tr, kr, tl, leftKind)

        # the mangled name for FORTRAN
        if not (kl is None):
          pMangle=tl+kl+nr
        else:
          pMangle=tl+nr

        anIntrinsic = self.__getIntrinsicDef(name, operator, pMangle, 
                                             aParameterList, 
                                             'r', resultTypes[0])
        
        if withBody:
          if (not resultTypeRegime=='left'):
            for localVar in extraVarsList:
              aDeclarator=ast.Declarator(localVar)
              anIntrinsic.appendChild(aDeclarator)
              aDeclarator.type=ast.Type(tl)
              aDeclarator.type.kind=self.p.precDict[kl][0]

          if (cp.F90):
            aParameterList=[]
            aParameterList.append(lOf('r'))
            aParameterList.append(aOf('r'))
            if (not compOperator) and (not resultTypeRegime=='left'):
              anIntrinsic.appendChild(ast.SubroutineCall('getLocation',aParameterList))
          getStatementPA(self,anIntrinsic,name,kr,resultTypes)
        aBlock.appendChild(anIntrinsic)

  def generatePushBinaryLocal(self,da,db,kl,kr,resultTypes,retName,leftName,rightName):
    aType=ast.Type('real')
    aType.kind=self.p.precDict['D'][0]
    da=ast.TypeConversion(da,aType)
    db=ast.TypeConversion(db,aType)
    ki=self.getResultType(resultTypes)
    aParameterList=[]
    aParameterList.append(lOf(retName))
    aParameterList.append(da)
    aParameterList.append(lOf(leftName))
    aParameterList.append(db)
    aParameterList.append(lOf(rightName))
    aSubroutineCall=ast.SubroutineCall('pushBinaryLocal'+ki+kl+kr,aParameterList)
    return aSubroutineCall

  def generatePushUnaryLocal(self,d,k,resultTypes,retName,activeName):
    aType=ast.Type('real')
    aType.kind=self.p.precDict['D'][0]
    d=ast.TypeConversion(d,aType)
    ki=self.getResultType(resultTypes)
    aParameterList=[]
    aParameterList.append(lOf(retName))
    aParameterList.append(d)
    aParameterList.append(lOf(activeName))
    aSubroutineCall=ast.SubroutineCall('pushUnaryLocal'+ki+k,aParameterList)
    return aSubroutineCall

  def getResultType(self,resultTypes):
    for (c,(n,t,k)) in enumerate(self.p.activeTL): 
      if (resultTypes[0].identifier==n):
        ki=k
    return ki
#Reverse_Mode End

# Helper Methods

  def __getSource(self, name, op, extraRefs):
    includes = [cn.Fixed.precDeclN, cn.Fixed.typeDeclN] + extraRefs
    if cp.useQueue:
      includes.append('WorkArray')
    src = ast.ObjectSource(cn.Fixed.pN + name, includes)
    src.decls = ast.OverloadedSet(name, op)
    src.defs = ast.StatementGroup()
    return src

  def __getResultTypes(self, compOperator, resultTypeRegime, leftType, 
                     leftKindKey, rightType, rightKindKey, leftName,
                     leftKind=None):
    if compOperator:
      return [ast.Type(self.p.boolType)]
    elif resultTypeRegime == 'merge':
      return self.__resultType(leftType, leftKindKey, rightType, rightKindKey)
    elif resultTypeRegime == 'left':
      aType = ast.Type(leftName)
      if not leftKind is None:
        aType.kind = leftKind
      else:
        aType.baseType = False
      return (aType,None)
    else:
      raise Exception('no logic for resultTypeRegime ' + 
                      str(resultTypeRegime))

  def __resultType(self,leftType,leftKindKey,rightType,rightKindKey):
    ''' this is an incomplete (but sufficient for us) type derivation '''
    if (leftKindKey is None) : # this is the integer type
      ksearch=rightKindKey
      tsearch=rightType # this must be the active one
    elif (rightKindKey is None) : # this is the integer type
      ksearch=leftKindKey
      tsearch=leftType # this must be the active one
    else:
      if self.p.precDict[rightKindKey][1]>self.p.precDict[leftKindKey][1] : 
        # pick the higher kind
        ksearch=rightKindKey
      else:
        ksearch=leftKindKey
      if self.p.typeList.index(leftType)<self.p.typeList.index(rightType): 
        # pick the higher type
        tsearch=rightType
      else:
        tsearch=leftType
    # search for the type in the active list
    for ns,ts,ks in self.p.activeTL :
      if (ts==tsearch and ks==ksearch):
        aType = ast.Type(ns)
        aType.baseType=False
        aBaseType=ast.Type(ts)
        aBaseType.kind=self.p.precDict[ks][0]
        break
    return (aType,aBaseType)

  def __arrayResultType(self,leftType,leftKindKey,leftDim,
                        rightType,rightKindKey,rightDim):
    (aType,aBaseType)=self.__resultType(leftType,leftKindKey,
                                        rightType,rightKindKey)
    # we spell it out explicitly because it doesn't exist in C++ anyway
    if (leftDim==2 and rightDim==2):
      dimensions = 2
      dimensionBounds=[ast.BinaryExpression(ast.FuncCall('lbound',[ast.Variable('a'),ast.Constant('1')]),
                                            ast.FuncCall('ubound',[ast.Variable('a'),ast.Constant('1')]),':'),
                       ast.BinaryExpression(ast.FuncCall('lbound',[ast.Variable('b'),ast.Constant('2')]),
                                            ast.FuncCall('ubound',[ast.Variable('b'),ast.Constant('2')]),':')]
    elif (leftDim==1 and rightDim==2):
      dimensions = 1
      dimensionBounds=[ast.BinaryExpression(ast.FuncCall('lbound',[ast.Variable('b'),ast.Constant('2')]),
                                            ast.FuncCall('ubound',[ast.Variable('b'),ast.Constant('2')]),':')]
    elif (leftDim==2 and rightDim==1):
      dimensions = 1
      dimensionBounds=[ast.BinaryExpression(ast.FuncCall('lbound',[ast.Variable('a'),ast.Constant('1')]),
                                            ast.FuncCall('ubound',[ast.Variable('a'),ast.Constant('1')]),':')]
    else:
      raise Exception('no logic for leftdim='+str(leftdim)+
                                ', rightdim='+str(rightdim))
    return (aType,aBaseType,dimensions,dimensionBounds)

  def __getIntrinsicDef(self, name, op, pMangle, paramList, retName, retType):

    intrinsic = ast.IntrinsicDef(name, pMangle, paramList,
                                 ast.MethodParameter(retName, retType, None))
    if cp.useOpenmp:
      intrinsic.fortranQualifiers = ''
    else:
      intrinsic.fortranQualifiers = 'elemental'
#   intrinsic.fortranQualifiers = 'elemental'
    intrinsic.operatorName = op
    return intrinsic

  def __getBinaryIntrinsicArgs(self, left, right, separateIntBodies):
    ''' Lists contain (ActiveOrPassive, name, type [, kindKey]) '''
    paramList = []
    bodyDiscriminator = ''
    for info in left, right:
      bodyDiscriminator += info[0]
      aType = ast.Type(info[2])
      if info[0] == 'A':
        aType.baseType = False
      elif info[0] == 'P':
        if not info[3] is None:
          aType.kind = self.p.precDict[info[3]][0]
        else:
          if separateIntBodies:
            bodyDiscriminator += 'i'
      paramList.append(ast.MethodParameter(info[1], aType, 'in'))
    return (paramList, bodyDiscriminator)

  def __appendBinaryIntrinsicBody(self, name, op, precName, 
                                  tl, kl, tr, kr, bodyDiscriminator, 
                                  extraVarsDict, resultTypes, intrinsic):

    include = cn.Fixed.pN + name + bodyDiscriminator + self.p.iE

    resType = self.__resultType(tl, kl, tr, kr)
    for ns,ts,ks in self.p.activeTL:
      if ns == resType[0].identifier:
        break
    if cp.openmpUseOrphaning and not cp.useQueue:
      appendUsingNamespace(precName, intrinsic)
    if cp.useQueue:
      # Skip all the comparison operators, as we do not need to
      #   push these to the queue
      if name == 'eq' or name == 'ne' or name == 'lt' or \
         name == 'le' or name == 'gt' or name == 'ge':

        intrinsic.appendChild(ast.Include(include))

      # 'pow' acts strangely, so treat it separately
      elif name == 'pow':

        if bodyDiscriminator == 'AA':
          intrinsic.appendChild(ast.Include(include))
          queue.appendToIntrinsicBody(self, ns, ks, intrinsic)
        elif bodyDiscriminator == 'AP' or bodyDiscriminator == 'APi':
          queue.genActivePassivePowBody(self, ns, ks, intrinsic)
        elif bodyDiscriminator == 'PA' or bodyDiscriminator == 'PiA':
          intrinsic.appendChild(ast.Include(include))
          queue.appendToIntrinsicBody(self, ns, ks, intrinsic)          
      else:

        if bodyDiscriminator == 'AA':
          queue.genActiveActiveBinaryOpBody(name, op, kl + kr, ks, intrinsic)
        if bodyDiscriminator == 'AP' or bodyDiscriminator == 'APi':
          queue.genActivePassiveBinaryOpBody(name, op, kl, ks, intrinsic)
        if bodyDiscriminator == 'PA' or bodyDiscriminator == 'PiA':
          queue.genPassiveActiveBinaryOpBody(name, op, kr, ks, intrinsic)

    else:
      if bodyDiscriminator in extraVarsDict:
       extraVarsDict[bodyDiscriminator](self, intrinsic, resultTypes,
                                        (tl,kl), (tr,kr))
      intrinsic.appendChild(self.p.setIterator())
      intrinsic.appendChild(ast.Include(include))

