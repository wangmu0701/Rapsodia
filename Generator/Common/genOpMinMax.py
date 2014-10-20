##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

def genMinMax(sourceList,helper): 
    # the generic bits for minimum
    sourceList.append(generateMinMaxBody(helper,True,True,'min'))
    # the generic bits for active/passive minimum
    sourceList.append(generateMinMaxBody(helper,True,False,'min'))
    # the generic bits for passive/active minimum
    sourceList.append(generateMinMaxBody(helper,False,True,'min'))
    # the min intrinsic
    sourceList.append(helper.generateBinaryIntrinsic('min',None,{},[],
                                                     False,False,False,
                                                     'merge'))
    # the generic bits for maximum
    sourceList.append(generateMinMaxBody(helper,True,True,'max'))
    # the generic bits for active/passive maximum
    sourceList.append(generateMinMaxBody(helper,True,False,'max'))
    # the generic bits for passive/active maximum
    sourceList.append(generateMinMaxBody(helper,False,True,'max'))
    # the max intrinsic
    sourceList.append(helper.generateBinaryIntrinsic('max',None,{},[],
                                                     False,False,False,
                                                     'merge'))

import Common.ast as ast
import Common.slice as slice

def generateMinMaxBody(helper,leftActive,rightActive,name):
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
      leftOperand=util.vOf(util.getVarValueName('a'))
    else :
      leftOperand=ast.Variable('a')
    if rightActive :
      rightOperand=util.vOf(util.getVarValueName('b'))
    else :
      rightOperand=ast.Variable('b')
    # left argument is less than right:
    a_LT_b=ast.BasicBlock()
    not_a_LT_b=ast.BasicBlock()
    theIf=ast.If(ast.LessThan(leftOperand,rightOperand), a_LT_b)
    theIf.appendChild(not_a_LT_b)
    aSource.appendChild(theIf)
    if (name=='min'):
      if not parameters.useQueue:
        if leftActive: 
          a_LT_b.appendChild(ast.Assignment(util.vOf('r'),util.vOf('a')))
        else:
          a_LT_b.appendChild(ast.Assignment(util.vOf('r'),ast.Variable('a')))
        if rightActive:
          not_a_LT_b.appendChild(ast.Assignment(util.vOf('r'),util.vOf('b')))
        else:
          not_a_LT_b.appendChild(ast.Assignment(util.vOf('r'),
                                                ast.Variable('b')))
      for deg in range(1,parameters.o+1,1):
        sA = slice.Slice(a_LT_b, False)
        sB = slice.Slice(not_a_LT_b, False)
        for direct in range(1,parameters.sliceSize+1,1):
          if leftActive:
            sA.appendChild(ast.Assignment(util.dOf('r',direct,deg), 
                                          util.dOf('a',direct,deg)))
          else: 
            sA.appendChild(ast.Assignment(util.dOf('r',direct,deg),
                                          ast.Variable('0')))
          if rightActive:
            sB.appendChild(ast.Assignment(util.dOf('r',direct,deg),
                                          util.dOf('b',direct,deg)))
          else: 
            sB.appendChild(ast.Assignment(util.dOf('r',direct,deg),
                                          ast.Variable('0')))

        sA.endSlice()
        sB.endSlice()
    else:
      # this must be the max
      if not parameters.useQueue:
        if rightActive:
          a_LT_b.appendChild(ast.Assignment(util.vOf('r'),util.vOf('b')))
        else:
          a_LT_b.appendChild(ast.Assignment(util.vOf('r'),ast.Variable('b')))
        if leftActive:
          not_a_LT_b.appendChild(ast.Assignment(util.vOf('r'),util.vOf('a')))
        else:
          not_a_LT_b.appendChild(ast.Assignment(util.vOf('r'),
                                                ast.Variable('a')))

      for deg in range(1,parameters.o+1,1):
        sA = slice.Slice(a_LT_b, False)
        sB = slice.Slice(not_a_LT_b, False)
        for direct in range(1,parameters.sliceSize+1,1):
          if rightActive:
            sA.appendChild(ast.Assignment(util.dOf('r',direct,deg),
                                          util.dOf('b',direct,deg)))
          else:
            sA.appendChild(ast.Assignment(util.dOf('r',direct,deg),
                                          ast.Variable('0')))
          if leftActive:
            sB.appendChild(ast.Assignment(util.dOf('r',direct,deg),
                                          util.dOf('a',direct,deg)))
          else:
            sB.appendChild(ast.Assignment(util.dOf('r',direct,deg),
                                          ast.Variable('0')))
        sA.endSlice()
        sB.endSlice()
    return aSource


#def genMinMaxReverse(sourceList,helper): 
#    aSourceNode=helper.generateBinaryIntrinsicReverse('min',None,[],[],False,False,True,'merge',getStatementAA,getStatementAP,getStatementPA)
#    sourceList.append(aSourceNode)
#    aSourceNode=helper.generateBinaryIntrinsicReverse('max',None,[],[],False,False,True,'merge',getStatementAA,getStatementAP,getStatementPA)
#    sourceList.append(aSourceNode)



