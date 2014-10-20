##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

def genAsgn(sourceList,helper): 
    # the generic bits for assignments
    generateAsgnBody(helper, sourceList)
    # assignments from passive variables
    aSource=helper.p.generateAsgn()
    if aSource :
      sourceList.append(aSource)
    
import Common.ast as ast
import Common.slice as slice

def generateAsgnBody(helper, aSourceList):
    ''' generate the generic body of all assignments '''
    # passive
    aSource = ast.SimpleSource(names.Fixed.pN+'asgnP', helper.p.iE)
    if not parameters.useQueue:
      aSource.appendChild(ast.Assignment(util.vOf('l'), ast.Variable('r')))

    s = slice.Slice(aSource, fullLoop=True, useOpenmp=False)
    for direct in range(1,parameters.sliceSize+1):
      for deg in range(1,parameters.o+1,1):
        s.appendChild(ast.Assignment(util.dOf('l',direct,deg, fullLoop=True),
                                     ast.Constant('0')))
    s.endSlice()
    aSourceList.append(aSource)

    # active 
    aSource = ast.SimpleSource(names.Fixed.pN+'asgnA', helper.p.iE)
    if not parameters.useQueue:
      aSource.appendChild(ast.Assignment(util.vOf('l'), util.vOf('r')))

    if parameters.useQueue:
      right = 'a'
    else:
      right = 'r'
    s = slice.Slice(aSource, useOpenmp=False)
    for direct in range(1,parameters.sliceSize+1,1):
      for deg in range(1,parameters.o+1,1):
        s.appendChild(ast.Assignment(util.dOf('l',direct,deg),
                                     util.dOf(right,direct,deg)))
    s.endSlice()
    aSourceList.append(aSource)

def genAsgnReverse(sourceList,helper): 
    # the generic bits for assignments
#    generateAsgnBodyReverse(helper, sourceList)
    # assignments from passive variables
    aSource=helper.p.generateAsgnReverse()
    if aSource :
      sourceList.append(aSource)


def generateAsgnBodyReverse(helper, aSourceList):
    ''' generate the generic body of all assignments '''
    # from passive
    aSource = ast.SimpleSource(names.Fixed.pN+'asgnP', helper.p.iE)
    aAssignment=helper.p.getLocationAssigned('l');
    if aAssignment:
      aSource.appendChild(aAssignment)
    aSource.appendChild(ast.Assignment(util.vOf('l'),ast.Variable('r')))
    aParameterList=[]
    aParameterList.append(helper.p.getLocation('l'))
    aSubroutineCall=ast.SubroutineCall('pushConstGlobal',aParameterList)
    aSource.appendChild(aSubroutineCall)
    aSourceList.append(aSource)

    # from active 
    aSource = ast.SimpleSource(names.Fixed.pN+'asgnA', helper.p.iE)
    aAssignment=helper.p.getLocationAssigned('l');
    if aAssignment:
      aSource.appendChild(aAssignment)
    aSource.appendChild(ast.Assignment(util.vOf('l'), util.vOf('r')))
    aParameterList=[]
    aParameterList.append(helper.p.getLocation('l'))
    aParameterList.append(ast.Constant('1.0'))
    aParameterList.append(helper.p.getLocation('r'))
    aSubroutineCall=ast.SubroutineCall('pushUnaryLocal',aParameterList)
    aSource.appendChild(aSubroutineCall)
    aParameterList=[]
    aSubroutineCall=ast.SubroutineCall('preAcc',aParameterList)
    aSource.appendChild(aSubroutineCall)
    aSourceList.append(aSource)


    # from Teporary to be done

