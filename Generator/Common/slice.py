##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################
import Common.parameters as params
import Common.ast as ast
import Common.util as util

class Slice(ast.Node):

  # Static method to initialize the slicing parameters
  # We assume params.slices is > 0 and <= params.d
  def initialize():
    if not params.sliceSize is None:
      raise Exception('cannot call initialize() twice')
    if params.slices == 0:
      params.sliceSize = params.d
    else:
      if params.d % params.slices == 0:
        params.sliceSize = params.d / params.slices
      else:
        # Calculate the direction size if num dirs % num slices != 0
        tmpDir = params.slices
        while tmpDir < params.d:
          tmpDir += params.slices
        print \
'Warning: Number of directions not divisible by number of slices.\n' \
'         Increasing number of directions from %d to %d to accommodate\n' \
'         number of slices.' % (params.d, tmpDir)
        params.d = tmpDir
        params.sliceSize = tmpDir / params.slices

  initialize = staticmethod(initialize)

  # Object methods

  def __init__(self, src, fullLoop=False, useOpenmp=True):
    ast.Node.__init__(self)
    # src contains the ast.SimpleSource file we write to
    self.src = src
    self.fullLoop = fullLoop
    # useOpenmp can be set to False to turn off openmp generation even
    #   if the user specifies it (useful for, e.g., genOpAsgn.py)
    self.useOpenmp = useOpenmp

    if params.sliceSize is None:
      raise Exception('must call initialize() before using a Slice object')
    if params.useOpenmp and self.useOpenmp:
      self.src.appendChild(ast.OpenmpLoop(True, params.openmpUseOrphaning))

  def accept(self, visitor):
    if params.slices > 0 and (not params.useQueue or self.fullLoop):
      return visitor.visitBasicBlock(self) 
    else:
      return visitor.visitStatementGroup(self)

  def endSlice(self):
    if params.slices > 0 and (not params.useQueue or self.fullLoop):
      aFor = ast.For('i', ast.Constant('1'), 
                     ast.Constant(str(params.slices)), 
                     ast.Constant('1'), self)
      aFor.slicing = True
      self.src.appendChild(aFor)
      if params.useOpenmp and self.useOpenmp:
        self.src.appendChild(ast.OpenmpLoop(False, params.openmpUseOrphaning))
    else:
      self.src.appendChild(self)

  def saveGlobals(self, returnVals = ['r']):
    if params.openmpUseOrphaning:
      for ret in returnVals:
        body = ast.BasicBlock()
        for dir in range(1, params.sliceSize+1):
          for deg in range(1, params.o+1):
            body.appendChild(ast.Assignment(util.dOf(ret,            dir, deg),
                                            util.dOf(ret + 'Global', dir, deg)))
        aFor = ast.For('i', ast.Constant('1'), 
                       ast.Constant(str(params.slices)), 
                       ast.Constant('1'), body)
        aFor.slicing = True
        self.src.appendChild(aFor)

  def endSliceAndSave(self, returnVals = ['r']):
    self.endSlice()
    self.saveGlobals(returnVals)
