##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################

import Common.ast as ast
import Common.names as names
import Common.parameters as params
from Common.util import vOf, getVarStructName, \
                        getVarSliceName, appendUsingNamespace

def generateStaticQueue(body):
    obj = 'ActiveTypeQueue'
    name = '%s::atQueue' % obj
    var = ast.Declarator(name)
    var.type = ast.Type(obj + ' *')
    var.initializer = ast.FuncCall('new ActiveTypeQueue', 
                                   [ast.Variable(str(params.slices))])
    body.appendChild(var)

def generateStaticObjects(name, kind, body):
    ''' generate any objects that must be instantiated on startup '''
    obj = 'WorkArray<%s, %s>' % (getVarStructName(name), getVarSliceName(name))
    objName = '%s::workArray%s' % (obj, kind)
    var = ast.Declarator(objName)
    var.type = ast.Type('template<> ' + obj + ' *')
    var.initializer = ast.FuncCall('new WorkArray', [])
    body.appendChild(var)

def generateDefaultConstructor(printer,name, kind, body):
    ''' generate the default constructor for the types '''
    obj = ast.Variable('WorkArray<%s, %s>::workArray%s' 
                       % (getVarStructName(name), getVarSliceName(name), kind))
    loc = ast.Variable('loc')

    # Constructor
    ctor = ast.IntrinsicDef(name, None, [], None)
    ctor.ctor = True
    ctor.memberOf = name
    funcPtr = ast.StructDeref(obj, ast.FuncCall('nextLocation', []))
    funcPtr.pointer = True
    ctor.appendChild(ast.Assignment(loc, funcPtr))
    if (params.temporariesBug):
        ctor.appendChild(ast.Assignment(ast.Variable('isTemp'), ast.Constant('false')))
    if (not params.disableInit):
        theZero=ast.Constant('0.0')
        theZero.kind=printer.precDict[kind][0]
        ctor.appendChild(ast.Assignment(ast.Variable(names.Fixed.vN), 
                                        theZero))
        appendGetLocation('l', name, kind, 'loc', 
                          False, ctor, isObj=True, getSlice=False)
        ctor.appendChild(printer.setIterator(force=True))
        ctor.appendChild(ast.Include(names.Fixed.pN+'asgnP'+printer.iE))

    body.appendChild(ctor)

    # Destructor
    dtor = ast.IntrinsicDef('~' + name, None, [], None)
    dtor.ctor = True
    dtor.memberOf = name
    funcPtr = ast.StructDeref(obj, ast.FuncCall('freeLocation', [loc]))
    funcPtr.pointer = True
    if (params.temporariesBug):
        dtor.appendChild(ast.If(ast.LogicalNot(ast.Variable('isTemp')),ast.Declaration([funcPtr])))
    else:
        dtor.appendChild(ast.Declaration([funcPtr]))
    body.appendChild(dtor)

def generateCopyConstructor(name, kind, body, isActive):
    if (params.useQueue and params.temporariesBug):
        obj = ast.Variable('WorkArray<%s, %s>::workArray%s' 
                           % (getVarStructName(name),
                              getVarSliceName(name),
                              kind))
        if (isActive):
            # need to set loc and isTemp
            # if the incoming r is a temporary, then we grab its loc and say this is not a temp
            loc = ast.Variable('loc')
            isTempBlock=ast.BasicBlock()
            isTempBlock.appendChild(ast.Assignment(loc, ast.StructDeref(ast.Variable('r'),
                                                                        ast.Variable('loc'))))
            isTempBlock.appendChild(ast.Assignment(ast.Variable('isTemp'), ast.Constant('false')))
            # else the incoming r is a not a temporary, then we declare ouselves  temp and make our loc
            isNotTempBlock=ast.BasicBlock()
            funcPtr = ast.StructDeref(obj, ast.FuncCall('nextLocation', []))
            funcPtr.pointer = True
            isNotTempBlock.appendChild(ast.Assignment(loc, funcPtr))
            isNotTempBlock.appendChild(ast.Assignment(ast.Variable('isTemp'), ast.Constant('true')))
            # put it all together
            ifNode=ast.If(ast.StructDeref(ast.Variable('r'),
                                          ast.Variable('isTemp')),
                          isTempBlock)
            ifNode.appendChild(isNotTempBlock)
            body.appendChild(ifNode)
        else:
            loc = ast.Variable('loc')
            funcPtr = ast.StructDeref(obj, ast.FuncCall('nextLocation', []))
            funcPtr.pointer = True
            body.appendChild(ast.Assignment(loc, funcPtr))
            body.appendChild(ast.Assignment(ast.Variable('isTemp'), ast.Constant('false')))
            
        body.appendChild(ast.Assignment(ast.Variable('*this'), 
                                        ast.Variable('r')))
    else: 
        body.appendChild(ast.Declaration([ast.FuncCall(name, [])]))
        body.appendChild(ast.Assignment(ast.Variable('*this'), 
                                        ast.Variable('r')))

def generateAsgnA(printer,kind, body):
    body.appendChild(ast.Assignment(ast.Variable(names.Fixed.vN), 
                                    vOf('r')))
    appendPush(['r', '(*this)'], ast.Variable('&asgnA_' + kind),
               kind, body)

def generateAsgnP(printer,name,kind, body):
    body.appendChild(ast.Assignment(ast.Variable(names.Fixed.vN), 
                                    ast.Variable('r')))
    appendGetLocation('l', name, kind, 'loc', 
                      False, body, isObj=True, getSlice=False)
    body.appendChild(printer.setIterator(force=True))
    body.appendChild(ast.Include(names.Fixed.pN+'asgnP'+printer.iE))

# Unary generation

def genUnaryMethod(printer, name, bodyName, returnName, activeVarNames, 
                   passiveVarNames, block):

    locList = ['y', 'z']
    for n,t,k in printer.activeTL:

      intrinsic = genIntrinsic(name + '_' + k)
      appendLock(n, k, intrinsic)
      appendGetLocation('a', n, k, 'x_loc', True, intrinsic)
      for var, loc in zip(activeVarNames, locList):
        appendGetLocation(var, n, k, loc + '_loc', False, intrinsic)
      appendGetLocation(returnName, n, k, 'r_loc', False, intrinsic)

      # Special cases for various operators
      if name == 'abs' or name == 'log':
        appendValueDeclarator('a', n, k, 'x', intrinsic)
      if name == 'exp':
        appendValueDeclarator(returnName, n, k, 'r', intrinsic)
      if name == 'sqrt':
        appendValueDeclarator(returnName, n, k, 'r', intrinsic)
      if name == 'sin'  or name == 'cos' or \
         name == 'sinh' or name == 'cosh':
        appendValueDeclarator(activeVarNames[0], n, k, locList[0], intrinsic)
        appendValueDeclarator(returnName, n, k, 'r', intrinsic)
      if name == 'atan':
        appendValueDeclarator('y', n, k, 'y', intrinsic)
      if name == 'acos' or name == 'asin':
        appendValueDeclarator('h', n, k, 'y', intrinsic)

      for var in passiveVarNames:
        dec = ast.Declarator(var)
        dec.type = getType(k)
        intrinsic.appendChild(dec)

      intrinsic.appendChild(printer.setIterator())
      intrinsic.appendChild(ast.Include(bodyName + printer.iE))
      appendUnlock(n, k, intrinsic)
      block.appendChild(intrinsic)

def genUnaryOpBody(name, returnName, activeVarNames, type, kindKey, body):

    varList = []
    varList.append('a')
    for var in activeVarNames:
      varList.append(var)
      dec = ast.Declarator(var)
      dec.type = ast.Type(type)
      body.appendChild(dec)
    varList.append(returnName)

    trig = { 'cos':'sin', 'sin':'cos', 'cosh':'sinh', 'sinh':'cosh' }
    if name in trig:
      appendAssignment(vOf(activeVarNames[0]),
                       ast.FuncCall(trig[name], [ vOf('a') ]), kindKey, body)

    if name == 'uminus':
      funcName = '-'
    else:
      funcName = name

    appendAssignment(vOf(returnName), ast.FuncCall(funcName, [vOf('a')]), 
                     kindKey, body)

    # for atan, acos, asin, we need to compute some code which must be
    #  pushed to the queue eventually, so we can't compute it within
    #  the function call and must compute it here
    if name == 'atan' or name == 'acos' or name == 'asin':
      one = ast.Constant('1.0')
      one.kind = getType(kindKey).identifier
      square = ast.Multiplication(ast.Variable('a'), ast.Variable('a'))
      if name == 'acos' or name == 'asin':
        sqrt = ast.FuncCall('sqrt', [ast.Subtraction(one, square)])
        aRHS = ast.Division(one, sqrt)
        if name == 'acos':
          aRHS = ast.UnaryMinus(aRHS)
        body.appendChild(ast.Assignment(ast.Variable('h'), aRHS))
      if name == 'atan':
        aRHS = ast.Division(one, ast.Group(ast.Addition(one, square)))
        body.appendChild(ast.Assignment(ast.Variable('y'), aRHS))

    appendPush(varList, ast.Variable('&' + name + '_' + kindKey), kindKey, body)
    if (params.temporariesBug):
        body.appendChild(ast.Assignment(ast.StructDeref(ast.Variable(returnName),
                                                        ast.Variable('isTemp')),
                                        ast.Constant('true')))


# Compound Binary generation
def genCompoundBinaryMethod(util,name,nl,tl,kl,nr,tr,kr,extraVars,resultTypes,block,bodyDiscriminator):
    if (not kr):
      kr=kl

    if bodyDiscriminator=='AA':
      intrinsic=genIntrinsic(name+bodyDiscriminator+'_'+kl+kr)
    else:
      intrinsic=genIntrinsic(name+bodyDiscriminator+'_'+kl)

    appendLock(nl,kl,body=intrinsic)
    if kl!=kr:
      appendLock(nr,kr,body=intrinsic)

    if name=='eqdiv':
      appendGetLocation('a',nl,kl,'x_loc',True,intrinsic)

    if bodyDiscriminator=='AA':
      appendGetLocation('b', nr, kr, 'y_loc', True, intrinsic)

    appendGetLocation('r', nl, kl, 'r_loc', False, intrinsic)

    if (name == 'eqmult' or name=='eqdiv'):
      if (bodyDiscriminator=='AA'):
        appendValueDeclarator('b', nr, kr, 'y', intrinsic)
      else:
        appendPassiveDeclarator('b', tl, kl, 'y', intrinsic)
 
      appendValueDeclarator('r', nl, kl, 'r', intrinsic)

    if (name=='eqdiv'):
      aDeclarator=ast.Declarator('recip')
      aDeclarator.type=ast.Type(util.p.precDict[kl][0])
      intrinsic.appendChild(aDeclarator)

    intrinsic.appendChild(ast.Include(names.Fixed.pN+name+bodyDiscriminator+util.p.iE))

    appendUnlock(nl, kl, body=intrinsic)
    if kl != kr:
      appendUnlock(nr, kr, body=intrinsic)

    block.appendChild(intrinsic)

def genCompoundBinaryOpBody(name, operator,nl, kl, kr, intrinsic,bodyDiscriminator):
    if name!='eqdiv':
      if bodyDiscriminator=='AA':
        appendPush([ 'r', 'b', 'r' ], ast.Variable('&' + name + 'AA_' + kl+kr), kl, intrinsic)
        intrinsic.appendChild(ast.Special('r.v'+operator+'b.v'+';'))
      else:
        appendPush([ 'r', ['UNUSED','b'], 'r' ], ast.Variable('&' + name + 'AP_' +kl), kl, intrinsic)
        intrinsic.appendChild(ast.Special('r.v'+operator+'b'+';'))
    else:
      aDeclarator=ast.Declarator('a')
      aDeclarator.type=ast.Type(nl)
      aDeclarator.base=False
      aDeclarator.initializer=ast.Variable('r')
      intrinsic.appendChild(aDeclarator)
      if bodyDiscriminator=='AA':
        intrinsic.appendChild(ast.Special('r.v'+operator+'b.v'+';'))
        appendPush([ 'a', 'b', 'r' ], ast.Variable('&' + name + 'AA_' + kl+kr), kl, intrinsic)
      else:
        intrinsic.appendChild(ast.Special('r.v'+operator+'b'+';'))
        appendPush([ 'a', ['UNUSED','b'], 'r' ], ast.Variable('&' + name + 'AP_' +kl), kl, intrinsic)

    if (params.temporariesBug):
        intrinsic.appendChild(ast.Assignment(ast.StructDeref(ast.Variable('r'),
                                                             ast.Variable('isTemp')),
                                             ast.Constant('true')))


# Binary generation

def genActiveActiveBinaryMethod(util, name, nl, tl, kl, nr, tr, kr, 
                                extraVars, resultTypes, block):

    intrinsic = genIntrinsic(name + 'AA_' + kl + kr)
    # Hack to get the correct result kind
    for ns,ts,ks in util.p.activeTL:
      if ns == resultTypes[0].identifier:
        break

    appendLock(nl, kl, body=intrinsic)
    if nl != nr:
      appendLock(nr, kr, body=intrinsic)
    if ns != nl and ns != nr:
      appendLock(ns, ks, body=intrinsic)

    appendGetLocation('a', nl, kl, 'x_loc', True, intrinsic)
    appendGetLocation('b', nr, kr, 'y_loc', True, intrinsic)
    appendGetLocation('r', ns, ks, 'r_loc', False, intrinsic)

    if name == 'div':
      appendValueDeclarator('b', nr, kr, 'y', intrinsic)
      appendValueDeclarator('r', ns, ks, 'r', intrinsic)
    if name == 'max' or name == 'min' or name == 'mult':
      appendValueDeclarator('a', nl, kl, 'x', intrinsic)
      appendValueDeclarator('b', nr, kr, 'y', intrinsic)

    if 'AA' in extraVars:
      extraVars['AA'](util, intrinsic, resultTypes, (tl,kl), (tr,kr))
    intrinsic.appendChild(util.p.setIterator())
    intrinsic.appendChild(ast.Include(names.Fixed.pN+name+'AA'+util.p.iE))

    appendUnlock(nl, kl, body=intrinsic)
    if nl != nr:
      appendUnlock(nr, kr, body=intrinsic)
    if ns != nl and ns != nr:
      appendUnlock(ns, ks, body=intrinsic)

    block.appendChild(intrinsic)

def genActiveActiveBinaryOpBody(name, operator, kParamsStr, kRet, intrinsic):
    if operator is None:
      op = ast.FuncCall(name, [vOf('a'), vOf('b')])
    else:
      op = ast.BinaryExpression(vOf('a'), vOf('b'), operator)
    appendAssignment(vOf('r'), op, kRet, intrinsic)
    appendPush([ 'a', 'b', 'r' ], 
               ast.Variable('&' + name + 'AA_' + kParamsStr), kRet, intrinsic)
    if (params.temporariesBug):
        intrinsic.appendChild(ast.Assignment(ast.StructDeref(ast.Variable('r'),
                                                             ast.Variable('isTemp')),
                                             ast.Constant('true')))
        

def genActivePassiveBinaryMethod(util, name, nl, tl, kl, nr, tr, kr, 
                                bodyDiscriminator, extraVars, resultTypes,
                                block):
    intrinsic = genIntrinsic(name + 'AP_' + kl)
    appendLock(name=nl, kind=kl, body=intrinsic)
    appendGetLocation('a', nl, kl, 'x_loc', True, intrinsic)
    appendGetLocation('r', nl, kl, 'r_loc', False, intrinsic)

    if name == 'div':
      appendPassiveDeclarator('b', tl, kl, 'y', intrinsic)
    if name == 'max' or name == 'min':
      appendValueDeclarator('a', nl, kl, 'x', intrinsic)
      appendPassiveDeclarator('b', tl, kl, 'y', intrinsic)
    if name == 'mult':
      appendPassiveDeclarator('b', tl, kl, 'y', intrinsic)
    if name == 'pow':
      appendGetLocation('s', nl, kl, 'y_loc', False, intrinsic)
      appendGetLocation('t', nl, kl, 'z_loc', False, intrinsic)
      appendValueDeclarator('a', nl, kl, 'x', intrinsic)
      appendValueDeclarator('r', nl, kl, 'r', intrinsic)
      appendPassiveDeclarator('b', tl, kl, 'y', intrinsic)

    if bodyDiscriminator in extraVars:
     extraVars[bodyDiscriminator](util, intrinsic, resultTypes,
                                  (tl,kl), (tr,kr))
    intrinsic.appendChild(util.p.setIterator())
    intrinsic.appendChild(ast.Include(names.Fixed.pN + name + 'AP' + util.p.iE))
    appendUnlock(name=nl, kind=kl, body=intrinsic)
    block.appendChild(intrinsic)
    return

def genActivePassivePowBody(util, n, k, intrinsic):
    
    for var in ['s', 't']:
      dec = ast.Declarator(var)
      dec.type = ast.Type(n)
      intrinsic.appendChild(dec)

    op = ast.FuncCall('pow', [vOf('a'), ast.Variable('b')])
    appendAssignment(vOf('r'), op, k, intrinsic)
    appendPush([ 'a', ['s.loc', 'b'], ['t.loc', '0'], 'r' ],
               ast.Variable('&powAP_' + k), k, intrinsic)
    if (params.temporariesBug):
        intrinsic.appendChild(ast.Assignment(ast.StructDeref(ast.Variable('r'),
                                                             ast.Variable('isTemp')),
                                             ast.Constant('true')))
    return

def appendToIntrinsicBody(util, n, k, intrinsic):
    if (params.temporariesBug):
        intrinsic.appendChild(ast.Assignment(ast.StructDeref(ast.Variable('r'),
                                                             ast.Variable('isTemp')),
                                             ast.Constant('true')))
    return

def genActivePassiveBinaryOpBody(name, operator, kl, kres, intrinsic):
    if operator is None:
      op = ast.FuncCall(name, [vOf('a'), ast.Variable('b')])
    else:
      op = ast.BinaryExpression(vOf('a'), ast.Variable('b'), operator)
    appendAssignment(vOf('r'), op, kres, intrinsic)
    appendPush([ 'a', ['UNUSED', 'b'], 'r' ], 
               ast.Variable('&' + name + 'AP_' + kl), kres, intrinsic)
    if (params.temporariesBug):
        intrinsic.appendChild(ast.Assignment(ast.StructDeref(ast.Variable('r'),
                                                             ast.Variable('isTemp')),
                                             ast.Constant('true')))
    return

def genPassiveActiveBinaryMethod(util, name, nl, tl, kl, nr, tr, kr, 
                                bodyDiscriminator, extraVars, resultTypes,
                                block):

    intrinsic = genIntrinsic(name + 'PA_' + kr)
    appendLock(name=nr, kind=kr, body=intrinsic)
    appendGetLocation('b', nr, kr, 'y_loc', True, intrinsic)
    appendGetLocation('r', nr, kr, 'r_loc', False, intrinsic)
    if name == 'div':
      appendValueDeclarator('r', nr, kr, 'r', intrinsic)
    if name == 'max' or name == 'min':
      appendPassiveDeclarator('a', tr, kr, 'x', intrinsic)
      appendValueDeclarator('b', nr, kr, 'y', intrinsic)
    if name == 'mult':
      appendPassiveDeclarator('a', tr, kr, 'x', intrinsic)
    intrinsic.appendChild(util.p.setIterator())
    intrinsic.appendChild(ast.Include(names.Fixed.pN+name+'PA'+util.p.iE))
    appendUnlock(name=nr, kind=kr, body=intrinsic)
    block.appendChild(intrinsic)

def genPassiveActiveBinaryOpBody(name, operator, kr, kresult, intrinsic):
    if operator is None:
      op = ast.FuncCall(name, [ast.Variable('a'), vOf('b')])
    else:
      op = ast.BinaryExpression(ast.Variable('a'), vOf('b'), operator)
    appendAssignment(vOf('r'), op, kresult, intrinsic)
    appendPush([ ['UNUSED', 'a'], 'b', 'r' ], 
               ast.Variable('&' + name + 'PA_' + kr), kresult, intrinsic)
    if (params.temporariesBug):
        intrinsic.appendChild(ast.Assignment(ast.StructDeref(ast.Variable('r'),
                                                             ast.Variable('isTemp')),
                                             ast.Constant('true')))

#######################################################################

def genIntrinsic(name):
    entryType = ast.Type('ActiveTypeQueueEntry')
    sliceType = ast.Type('int')
    entryMethodParam = ast.MethodParameter('entry', entryType, 'in')
    sliceMethodParam = ast.MethodParameter('slice', sliceType, 'in')
    return ast.IntrinsicDef(name, None, 
                            [ entryMethodParam, sliceMethodParam ], None)

def appendAssignment(lhs, rhs, kind, body):
#   if getTypeIdentifier(kind) == 'float':
#     rhs = ast.Cast(getType(kind), rhs)
    body.appendChild(ast.Assignment(lhs, rhs))

def appendLock(name, kind, body):
    var = ast.StructDeref(ast.Variable('WorkArray<%s, %s>::workArray%s'
                                       % (getVarStructName(name),
                                          getVarSliceName(name),
                                          kind)),
                          ast.FuncCall('lock', []))
    var.pointer = True
    body.appendChild(ast.Declaration([var]))

def appendUnlock(name, kind, body):
    var = ast.StructDeref(ast.Variable('WorkArray<%s, %s>::workArray%s'
                                       % (getVarStructName(name),
                                          getVarSliceName(name),
                                          kind)),
                          ast.FuncCall('unlock', []))
    var.pointer = True
    body.appendChild(ast.Declaration([var]))

def appendGetLocation(varName, name, kind, loc, isConst, body, isObj=False, 
                      getSlice=True):
    if isObj:
      locStruct = ast.Variable(loc)
    else:
      locStruct = ast.StructDeref(ast.Variable('entry'), ast.Variable(loc))
    if getSlice:
      funcCall = ast.FuncCall('getLocation', [locStruct, ast.Variable('slice')])
      lhs = getVarSliceName(name)
    else:
      funcCall = ast.FuncCall('getLocation', [locStruct])
      lhs = getVarStructName(name)
    var = ast.Declarator(varName)
    var.const = isConst
    var.intent = 'inout'
    var.type = ast.Type(lhs)
    var.initializer = ast.StructDeref(ast.Variable('WorkArray<%s, %s>::workArray%s'
                                                   % (getVarStructName(name), 
                                                      getVarSliceName(name),
                                                      kind)), 
                                      funcCall)
    var.initializer.pointer = True
    body.appendChild(var)

def appendValueDeclarator(varName, type, kind, loc, body):
    var = ast.Declarator(varName + '_value')
    var.const = True
    var.intent = 'inout'
    var.type = ast.Type(type + '_value')
    var.initializer = \
        ast.Cast(var.type,
                 ast.StructDeref(ast.Variable('entry'),
                                 ast.StructDeref(ast.Variable(loc + '_val'),
                                                 ast.Variable(kind))))
    var.initializer.op = '&'
    body.appendChild(var)

def appendPassiveDeclarator(varName, type, kind, loc, body):
    var = ast.Declarator(varName)
    var.const = True
    var.type = ast.Type(type)
    var.initializer = \
        ast.Cast(var.type,
                 ast.StructDeref(ast.Variable('entry'),
                                 ast.StructDeref(ast.Variable(loc + '_val'),
                                                 ast.Variable(kind))))
    body.appendChild(var)

import types

def appendPush(varList, func, kind, body):

    numVars = 0;
    castType = getType(kind)
    pushParams = []   # List of parameters to be placed within push()
    for var in varList:
      numVars = numVars + 1

      if numVars == len(varList):
        zero = ast.Constant('0.0')
        zero.kind = getTypeIdentifier(kind)
        while numVars < 4:
          pushParams.append(ast.Variable('UNUSED'))
          pushParams.append(zero)
          numVars = numVars + 1

      if isinstance(var, types.ListType):
        pushParams.append(ast.Variable(var[0]))
        pushParams.append(ast.Cast(castType, ast.Variable(var[1])))
      else:
        pushParams.append(ast.StructDeref(ast.Variable(var), 
                                          ast.Variable('loc')))
        pushParams.append(ast.Cast(castType, vOf(var)))
    pushParams.append(func)
    funcPtr = ast.StructDeref(ast.Variable('ActiveTypeQueue::atQueue'),
                              ast.FuncCall('push', pushParams))
    funcPtr.pointer = True
    body.appendChild(ast.Declaration([funcPtr]))

def getTypeIdentifier(kind):
    if kind == 'S':
      return 'float'
    elif kind == 'D':
      return 'double'
    else:
      raise Exception("kind " + str(kind) + " must be either 'S' or 'D'")

def getType(kind):
    return ast.Type(getTypeIdentifier(kind))

