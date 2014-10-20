##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.names as names
import Common.parameters as parameters
import Common.util as util

# For FORTRAN only

def genMaxloc(sourceList,helper): 
    # the generic bits for maxloc
    sourceList.append(generateMaxlocBody(helper))
    # the maxloc intrinsic
    aSourceNode=helper.generateUnaryArrayOpAll('maxloc',
                                               None,
                                               names.Fixed.pN+'maxloc',
                                               False,
                                               'r',
                                               'subscriptReturn',
                                               None,
                                               [],
                                               [])
    aSourceNode.fortranOnly=True
    sourceList.append(aSourceNode)

import Common.ast as ast

def generateMaxlocBody(helper):
    aSourceNode=ast.SimpleSource(names.Fixed.pN+'maxloc',
                                 helper.p.iE)
    aSourceNode.fortranOnly=True
    # compute Maxloc
    aSourceNode.appendChild(ast.Assignment(ast.Variable('r'),ast.FuncCall('maxloc',[util.vOf('a')])))
    return aSourceNode

    

