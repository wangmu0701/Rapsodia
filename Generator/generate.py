#!/usr/bin/env python

##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################

## \mainpage Rapsodia Code Generator
#  \author Isabelle Charpentier and Jean Utke
#    
#  \section intro Introduction
#  
# Rapsodia = <b>rap</b>ide <b>s</b>urcharge d'<b>o</b>p&eacute;rateur pour la <b>di</b>ff&eacute;rentiation <b>a</b>utomatique.
# 
# Rapsodia is a tool for the efficient computation of higher order derivative tensors. 
# It consists of two parts. 
# <ol>
# <li> A Python-based generator producing C++ or Fortran code for the forward propagation  of univariate Taylor polynomials.
# This code yields efficiency gains via explictly unrolled loops for a fixed derivative order and number of directions.
#
# <li> Implementations of the algorithm to interpolate derivative tensor entries from univariate 
# Taylor coefficients in C++ and Fortran  
# </ol> 
# This part of the documentation covers the Python-based generator.



import sys
import Common.ast 
import Common.util
import Common.parameters 
import Common.names 
import Common.slice

class Generator:
  ''' class to setup and run the code generation '''
  
  def __init__(self,aPrinter):
    ## @var u
    # printer dependent utility 
    self.u = Common.util.Util(aPrinter)
    ## @var sL
    # list of sources 
    self.sL = []

  def generateSources(self):
    ''' generate all source files '''
    import Common.genOpAsgn
    import Common.genOpAddSub
    import Common.genOpUMinus
    import Common.genOpMult
    import Common.genOpDiv
    import Common.genOpSqrt
    import Common.genOpLog
    import Common.genOpExp
    import Common.genOpPow
    import Common.genOpAsinAcos
    import Common.genOpSinCos
    import Common.genOpSinhCosh
    import Common.genOpMinMax
    import Common.genOpInt
    import Common.genOpNint
    import Common.genOpReal
    import Common.genOpAbs
    import Common.genOpSign
    import Common.genOpTan
    import Common.genOpAtan
    import Common.genOpSum
    import Common.genOpMatmul
    import Common.genOpMaxloc
    import Common.genOpMaxval
    import Common.genOpEqAddSub
    import Common.genCompOps
    import Common.genMakefile
    import Common.genCommonHead
    import Common.genDefines

    # language specific parts
    if not (Common.parameters.reverse):
      # language specific parts
      self.sL.append(self.u.p.generatePrecisions())
      self.sL.append(self.u.p.generateTypes(self.sL))

      # common parts
      Common.genOpAsgn.genAsgn(self.sL,self.u)                                  #r
      Common.genOpAddSub.genAddSub(self.sL,self.u)                              #r
      Common.genOpUMinus.genUMinus(self.sL,self.u)                              #r
      Common.genOpMult.genMult(self.sL,self.u)                                  #r
      Common.genOpDiv.genDiv(self.sL,self.u)                                    #r
      Common.genOpSqrt.genSqrt(self.sL,self.u)                                  #r
      Common.genOpLog.genLog(self.sL,self.u)                                    #r
      Common.genOpExp.genExp(self.sL,self.u)                                    #r
      Common.genOpPow.genPow(self.sL,self.u)                                    #r
      Common.genOpAsinAcos.genAsinAcos(self.sL,self.u)                          #r
      Common.genOpSinCos.genSinCos(self.sL,self.u)                              #r
      Common.genOpSinhCosh.genSinhCosh(self.sL,self.u)                          #r
      Common.genOpMinMax.genMinMax(self.sL,self.u)
      Common.genOpInt.genInt(self.sL,self.u)                                    #r
      Common.genOpNint.genNint(self.sL,self.u)                                  #r
      Common.genOpReal.genReal(self.sL,self.u)                                  #r
      Common.genOpAbs.genAbs(self.sL,self.u)                                    #r
      Common.genOpSign.genSign(self.sL,self.u)                                  #r
      Common.genOpTan.genTan(self.sL,self.u)                                    #r
      Common.genOpAtan.genAtan(self.sL,self.u)                                  #r
      Common.genOpSum.genSum(self.sL,self.u)
      Common.genOpMatmul.genMatmul(self.sL,self.u)
      Common.genOpMaxloc.genMaxloc(self.sL,self.u)
      Common.genOpMaxval.genMaxval(self.sL,self.u)
      Common.genCompOps.genCompOps(self.sL,self.u)				#r
      Common.genOpEqAddSub.genEqAddSub(self.sL,self.u)
      Common.genDefines.genDefines(self.sL,self.u)
    # a single file to be included in user sources
      self.sL.append(self.generateIncludeAll())
    else:
      self.sL.append(self.u.p.generatePrecisionsReverse())
      self.sL.append(self.u.p.generateTypesReverse(self.sL))
      # common parts
      Common.genOpAsgn.genAsgnReverse(self.sL,self.u)
      Common.genOpUMinus.genUMinusReverse(self.sL,self.u)     
      Common.genOpAddSub.genAddSubReverse(self.sL,self.u)
      Common.genOpMult.genMultReverse(self.sL,self.u)
      Common.genOpDiv.genDivReverse(self.sL,self.u)
      Common.genOpSqrt.genSqrtReverse(self.sL,self.u)
      Common.genOpLog.genLogReverse(self.sL,self.u)
      Common.genOpExp.genExpReverse(self.sL,self.u)
      Common.genOpPow.genPowReverse(self.sL,self.u)
      Common.genOpSinCos.genSinCosReverse(self.sL,self.u)
      Common.genOpTan.genTanReverse(self.sL,self.u)
      Common.genOpSinhCosh.genSinhCoshReverse(self.sL,self.u)
      Common.genOpAsinAcos.genAsinAcosReverse(self.sL,self.u)
      Common.genOpAtan.genAtanReverse(self.sL,self.u)
      Common.genCompOps.genCompOpsReverse(self.sL,self.u)                              
      Common.genOpInt.genIntReverse(self.sL,self.u)					
      Common.genOpNint.genNintReverse(self.sL,self.u)					
      Common.genOpAbs.genAbsReverse(self.sL,self.u)
      Common.genOpSign.genSignReverse(self.sL,self.u)
      Common.genOpEqAddSub.genEqAddSubReverse(self.sL,self.u)
#      Common.genOpReal.genRealReverse(self.sL,self.u)					#No complex type, not needed
      self.sL.append(self.generateIncludeAll())
      Common.genCommonHead.genCommonHead(self.sL,self.u)

  def generateIncludeAll(self):
    ''' this file is to be included by the user ''' 
    import F90.Printer
    import Cpp.Printer
    includeS = Common.ast.SimpleSource(Common.names.Fixed.pN+'include',
                                       self.u.p.iE)
    includeS.fixedFormat=True
    for aSource in self.sL :
      if (isinstance(aSource, Common.ast.ObjectSource)
          and
          ((isinstance(self.u.p, F90.Printer.F90Printer)
            and
            not aSource.cppOnly)
           or
           (isinstance(self.u.p, Cpp.Printer.CppPrinter)
            and
            not aSource.fortranOnly))):
        includeS.appendChild(Common.ast.ObjectReference(aSource.identifier))
    return includeS    

import sys
from optparse import OptionParser

def main():
  import F90.Printer
  import Cpp.Printer
  usage = '%prog { -d <DIRECTION> -o <ORDER> { -f <FDIR> | -c <CDIR> } [options] } | {-r [options]}'
  parser = OptionParser(usage=usage)
  parser.add_option('-d', '--directions',
                    type='int',
                    help='the number of univariate directions (required)')
  parser.add_option('-o', '--order', 
                    type='int',
                    help='the maximal order of Taylor coefficients (required)')
  parser.add_option('-f', '--fdir',
                    help='if specified, generate F90 files into FDIR')
  parser.add_option('-c', '--cdir',
                    help='if specified, generate C++ files into CDIR')
  parser.add_option('-s', '--slices',
                    type='int',
                    help='number of data slices; '
                         'defaults to 1')

  parser.add_option('', '--openmp',
                    action="store_true",
                    help='if specified along with --slices, adds OpenMP '
                         'directives to parallelize sliced code')
  parser.add_option('', '--openmpChunkSize',
                    type='int',
                    help='if specified along with --openmp, sets the chunk '
                         'size to schedule per iteration (defaults to 1)')
  parser.add_option('', '--orphan',
                    action="store_true",
                    help='if specified along with --openmp, uses orphaned '
                         'OpenMP directives (EXPERIMENTAL)')
  parser.add_option('-q', '--queue',
                    action="store_true",
                    help='use a queue and threads to calculate derivatives asynchronously; '
                         'usable only with -c, conflicts with -f')
  parser.add_option('-t', '--temporariesBug',
                    action="store_true",
                    help='workaround compiler bugs in sunCC and xlC related to unnamed temporaries in expressions; '
                         'requires  -q')
  parser.add_option('', '--disableInit',
                    action="store_true",
                    help='use this to improve efficiency but only if the code does not contain array initialization with partial initialization lists; refer to the  manual for details; ')
  parser.add_option('', '--useOPA',
                    action="store_true",
                    help='use OpenPA in queue implementation; '
                         'implies -q')
  parser.add_option('', '--inline',
                    action="store_true",
                    help='generate C++ files using the inline directive')
  parser.add_option('', '--interoperable',
                    action="store_true",
                    help='generate interoperable type declarations using C structs for C++ and iso_c_binding for Fortran')
  parser.add_option('', '--fixedFormat',
                    action="store_true",
                    help='generate Fortran files in fixed format; '
                         'default is free format')
  parser.add_option('', '--cppHeaderExtension',
                    help='file extension for C++ header files; '
                         'default is \'.hpp\'')
  parser.add_option('', '--cppIncludeExtension',
                    help='file extension for common C++ code snippets included in the generated code; '
                         'default is \'.ipp\'')
  parser.add_option('', '--cppSourceExtension',
                    help='file extension for C++ source files; '
                         'default is \'.cpp\'')
  parser.add_option('', '--fortranIncludeExtension',
                    help='file extension for Fortran includes; '
                         'default is \'.i90\'')
  parser.add_option('', '--fortranSourceExtension',
                    help='file extension for Fortran source files; '
                         'default is \'.f90\'')
  parser.add_option('', '--floatingPointExceptions',
                    action="store_true",
                    help='generate extra code that tests for boundary cases and prevents some floating point exceptions')
  parser.add_option('', '--sequenceType',
                    action="store_true",
                    help='generate Fortran derived types as SEQUENCE types needed for use in common blocks or other sequence types')
  parser.add_option('', '--withOpenADconversions',
                    action="store_true",
                    help='generate definitions for conversion routines reference in code that has was transformed for type change with OpenAD')
  parser.add_option('-r', '--reverse',
                    action="store_true",
                    help='enable reverse mode')
  parser.add_option('', '--doubleOnly',
                    action="store_true",
                    help='double presicion only [Default=False] [Reverse Mode]')
  parser.add_option('', '--tl',
                    type='int',
                    help='local tape size       [Default=1000]  [Reverse Mode]')
  parser.add_option('', '--ll',
                    type='int',
                    help='initial location size [Default=4000]  [Reverse Mode]')
  parser.add_option('', '--bs',
                    type='int',
                    help='stack block size      [Default=4096]  [Reverse Mode]')
  parser.add_option('', '--loc',
                    action="store_true",
                    help='accumulation on int   [Default=False] [Reverse Mode] [Fortran Only]')

  (options, args) = parser.parse_args()

  if ((options.directions is None)
      or
      (options.order is None)) and (not options.reverse):
    parser.error('-d and -o must be specified')
  if ((options.cdir is None)
      and
      (options.fdir is None)):
    parser.error('at least one output directory for C++ (-c) or F90 (-f) files must be specified')
  if ((options.cdir is None)
      and
      (options.inline)):
    parser.error('-i can be specified only together with -c')
  if ((options.queue)
      and
      (options.fdir)):
    parser.error('-q cannot be specified together with -f')
  if ((options.queue)
      and
      (not options.cdir)):
    parser.error('-q requires -c')
  if ((options.temporariesBug)
      and
      (not options.queue)):
    parser.error('-t requires -q')
  if (options.sequenceType):
    if (not (options.fdir)):
      parser.error('--sequenceType can be specified only together with -f')
    if (options.interoperable):
      parser.error('--sequenceType cannot be specified together with --interoperable')      
  if ((options.withOpenADconversions)
      and
      not (options.fdir)):
    parser.error('--withOpenADconversions can be specified only together with -f')
  Common.parameters.d=options.directions
  Common.parameters.o=options.order

  if (options.reverse):
    Common.parameters.d=1
    Common.parameters.o=1
    Common.parameters.reverse=True
    if (options.doubleOnly):
      Common.parameters.doubleOnly=True
    if (options.loc):
      Common.parameters.accOnLoc=True
    if (options.tl):
      if (options.tl>=Common.parameters.tapeLen):
        Common.parameters.tapeLen=options.tl
      else:
         print "-tl smaller than default: Ignored."
    if (options.ll):
      if (options.ll>=Common.parameters.locationLen):
        Common.parameters.locationLen=options.ll
      else:
         print "-ll smaller than default: Ignored."
    if (options.bs):
      if (options.bs>=Common.parameters.blockSize):
        Common.parameters.blockSize=options.bs
      else:
         print "-bs smaller than default: Ignored."
        
#    print "reverse enabled"


  if (options.disableInit):
    Common.parameters.disableInit = True

  # Slices
  if not (options.slices is None):
    if (options.slices <= 0 or options.slices > Common.parameters.d):
      parser.error('number of slices must be greater than 0 and less than '
                   'or equal the number of directions')
    Common.parameters.slices = options.slices
  else:
    Common.parameters.slices = 0
  Common.slice.Slice.initialize()
  # OpenMP
  if not options.openmp is None:
    if options.slices is None:
      parser.error('--openmp can only be specified together with --slices')
    Common.parameters.useOpenmp = True
    if not options.openmpChunkSize is None:
      if options.openmpChunkSize < 1 or \
         options.openmpChunkSize > options.slices:
        parser.error('Chunk size must be greater than 0 and less than '
                     'or equal the number of slices')
      Common.parameters.openmpChunkSize = options.openmpChunkSize
    else:
      Common.parameters.openmpChunkSize = 1
  else:
    Common.parameters.useOpenmp = False

  if not options.orphan is None:
    if options.openmp is None:
      parser.error('--orphan can only be specified together with --openmp')
    Common.parameters.openmpUseOrphaning = True
  else:
    Common.parameters.openmpUseOrphaning = False

  if options.queue is not None:

    # if we are using a queue we need to get the rapsodia root directory
    #   to locate the queue header files
    import inspect
    import os
    Common.parameters.rootdir = \
        os.path.realpath(inspect.currentframe().f_code.co_filename).rsplit('/', 1)[0]
    Common.parameters.useOPA = options.useOPA

    if options.cdir is None:
      parser.error('--queue can only be specified together with -c')
    Common.parameters.useQueue = True
    if (options.temporariesBug):
      Common.parameters.temporariesBug = True
  else:
    Common.parameters.useQueue = False

  # make the variable names
  Common.names.init(Common.parameters.d, Common.parameters.o)
  if (options.fdir): 
    Common.parameters.F90=True
    aPrinter=F90.Printer.F90Printer()
    if (options.fortranIncludeExtension):
      aPrinter.iE=options.fortranIncludeExtension
    if (options.fortranSourceExtension):
      aPrinter.sE=options.fortranSourceExtension
    if (options.sequenceType):
      aPrinter.sequenceType=True
    if (options.interoperable):
      aPrinter.setInteroperable(True)
    if (options.withOpenADconversions):
      aPrinter.withOpenADconversions=True
    if (not options.fixedFormat is None):
      aPrinter.fixedFormat=True
    aGenerator=Generator(aPrinter)
    if (options.floatingPointExceptions):
      aGenerator.u.handleFPE=True
    aGenerator.generateSources()
    aWriter=F90.Printer.F90Output()
    aWriter.iE=aPrinter.iE
    aWriter.sE=aPrinter.sE
    aWriter.fixedFormat=aPrinter.fixedFormat
    aWriter.oP=options.fdir
    aWriter.sequenceType=options.sequenceType    
    aWriter.setInteroperable(aPrinter.getInteroperable())
    for aSource in aGenerator.sL :
      aWriter.visitSource(aSource)
    if not (Common.parameters.reverse):
      Common.genMakefile.genMakefile(aWriter)
    else:
      Common.genMakefile.genMakefileReverse(aWriter)

  if (options.cdir):
    Common.parameters.Cpp=True
    aPrinter=Cpp.Printer.CppPrinter()
    if (options.cppIncludeExtension):
      aPrinter.iE=options.cppIncludeExtension
    if (options.cppSourceExtension):
      aPrinter.sE=options.cppSourceExtension
    if (options.cppHeaderExtension):
      aPrinter.hE=options.cppHeaderExtension
    if (options.interoperable):
      aPrinter.setInteroperable(True)
    if options.inline is None:
      aPrinter.inlineDefs=False
    else:
      aPrinter.inlineDefs=True
    aGenerator=Generator(aPrinter)
    if (options.floatingPointExceptions):
      aGenerator.u.handleFPE=True
    aGenerator.generateSources()
    aWriter=Cpp.Printer.CppOutput()
    aWriter.iE=aPrinter.iE
    aWriter.sE=aPrinter.sE
    aWriter.hE=aPrinter.hE
    aWriter.oP=options.cdir
    aWriter.setInteroperable(aPrinter.getInteroperable())
    if options.inline is None:
      aWriter.inlineDefs=False
    else:
      aWriter.inlineDefs=True
    for aSource in aGenerator.sL :
      aWriter.visitSource(aSource)
    if not (Common.parameters.reverse):
      Common.genMakefile.genMakefile(aWriter)
    else:
      Common.genMakefile.genMakefileReverse(aWriter)

if __name__ == "__main__":
  sys.exit(main())
