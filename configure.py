#!/usr/bin/env python
##########################################################
# This file is part of Rapsodia released under the LGPL. #
# The full COPYRIGHT notice can be found in the top      #
# level directory of the Rapsodia distribution           #
##########################################################

import os
import sys
import subprocess
import shutil

ourTempDirName="confTmp"
ourMakeDefsName="MakeDefs.mk"
ourMakeDefsHandle=None
ourMakeRulesName="MakeRules.mk"
ourMakeRulesHandle=None
ourRootPath=None
ourConfLogHandle=None

class ConfException(Exception):
  def __init__(self,reason):
    Exception.__init__(self,reason)

class FlagPair:
  def __init__(self,
               debug="",
               opt=""):
    self.debug=debug
    self.opt=opt

class FortFlags:
  def __init__(self,
               modSearch,
               freeFormLongLines,
               fixedFormLongLines,
               fpp="cpp",
               fppFlag="",
               fppFixedForm="",
               testedVersions=[]):
      self.doFlags={} # non-debug,debug versions
      self.modSearch=modSearch
      self.freeFormLongLines=freeFormLongLines
      self.fixedFormLongLines=fixedFormLongLines
      self.fpp=fpp
      self.fppFlag=fppFlag
      self.fppFixedForm=fppFixedForm
      self.testedVersions=testedVersions

class CxxFlags:
  def __init__(self,
               testedVersions=[]):
      self.doFlags={} # non-debug,debug versions
      self.testedVersions=testedVersions

class MixedLanguageFlags:
  def __init__(self,
               cxx,
               f90,
               CXXLinker,
               F90Linker):
      self.flags={} # native/non-native main
      self.cxx=cxx
      self.f90=f90
      self.CXXLinker=CXXLinker
      self.F90Linker=F90Linker
  
def cleanUp():
  global ourRootPath
  os.chdir(ourRootPath)
  if (os.path.exists(ourTempDirName)):
    shutil.rmtree(ourTempDirName)
  if (ourMakeDefsHandle):
    ourMakeDefsHandle.close()
  if (os.path.exists(ourMakeDefsName)):
    os.remove(ourMakeDefsName)
  if (ourMakeRulesHandle):
    ourMakeRulesHandle.close()
  if (os.path.exists(ourMakeRulesName)):
    os.remove(ourMakeRulesName)

def compileAndRun(aCode,isFortran,errMsg):
  if (os.path.exists(ourTempDirName)):
    shutil.rmtree(ourTempDirName)
  os.makedirs(ourTempDirName)
  os.chdir(ourTempDirName)
  confTestName="confTest."
  makeFile=open("Makefile","w")
  makeFile.write("include ../"+ourMakeDefsName+"\n")
  makeFile.write("include ../"+ourMakeRulesName+"\n")
  makeFile.write("confTest: confTest.o\n")
  makeFile.write("\t")
  if (isFortran) :
    confTestName+="f90"
    makeFile.write("$(F90C) $(FFLAGS)")
  else :
    confTestName+="cpp"
    makeFile.write("$(CXX) $(CXXFLAGS)")
  makeFile.write(" -o confTest $^\n")
  makeFile.close()
  global ourConfLogHandle
  ourConfLogHandle.write("# Makefile begin #######\n")
  t=open("Makefile","r")
  ourConfLogHandle.write(t.read())
  t.close()
  ourConfLogHandle.write("# Makefile end #########\n")
  confTestFile=open(confTestName,"w")
  confTestFile.write(aCode)
  confTestFile.close()
  ourConfLogHandle.write("# "+confTestName+" begin #######\n")
  t=open(confTestName,"r")
  ourConfLogHandle.write(t.read())
  t.close()
  ourConfLogHandle.write("# "+confTestName+" end #########\n")
  p=subprocess.Popen("make confTest",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  ourConfLogHandle.write(p.stdout.read())
  ourConfLogHandle.write(p.stderr.read())
  if (p.wait()):
    raise ConfException(errMsg+" compilation failed")
  p=subprocess.Popen("./confTest",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  ourConfLogHandle.write(p.stdout.read())
  ourConfLogHandle.write(p.stderr.read())
  if (p.wait()):
    raise ConfException(errMsg+" execution failed")
  global ourRootPath
  os.chdir(ourRootPath)
  if (os.path.exists(ourTempDirName)):
    shutil.rmtree(ourTempDirName)

def testAndWrite(stream,varName,varVal):
    stream.write("ifdef "+varName+"\n")
    stream.write(" ifneq \"$(origin "+varName+")\" \"default\"\n")
    stream.write("  ifneq ($("+varName+"),"+varVal+")\n")
    stream.write("   $(error \"environment variable "+varName+" is set to ${"+varName+"} but Rapsodia is configured with "+varVal+"\")\n")
    stream.write("  endif\n")
    stream.write(" endif\n")
    stream.write("endif\n")
    stream.write("export "+varName+"="+varVal+"\n")

def main():
    import copy
    from optparse import OptionParser
    usage = \
          '%prog [options] \n\
          used to set up make rules and definitions for building Rapsodia generated sources and support libraries'
    opt = OptionParser(usage=usage)
    fortFlags={}; cxxFlags={}; mixedLanguageFlags={};
    # the first compilers appended to the above empty containers are used as defaults
    #########################################################################################
    # GNU compiler settings
    # Fortran
    compName='gfortran'
    fortCompDefault=compName
    fortFlags[compName]=FortFlags("-I",
                                  "-ffree-line-length-none",
                                  "-ffixed-line-length-none -ffixed-form",
                                  "cpp",
                                  "-traditional-cpp",
                                  testedVersions=["4.5.1","4.6.3","4.7.2","4.8.0"])
    fortFlags[compName].doFlags[False]=FlagPair(opt="-O3")
    fortFlags[compName].doFlags[True]=FlagPair("-g -pedantic -std=f2003 -Wall -Wextra -Wno-unused-variable -fcheck=all","-O0")
    # C++
    compName='g++';
    cxxCompDefault=compName
    cxxFlags[compName]=CxxFlags(fortFlags["gfortran"].testedVersions)
    cxxFlags[compName].doFlags[False]=FlagPair(opt="-O3")
    cxxFlags[compName].doFlags[True]=FlagPair("-g -pedantic -Wall -Wextra -Wno-unused-variable","-O0")
    # mixed Language linking
    mixedLanguageFlags[('g++','gfortran')]=MixedLanguageFlags('g++','gfortran','g++','g++')
    # native main:
    mixedLanguageFlags[('g++','gfortran')].flags['CXX']="-lgfortran"
    # non-native main:
    mixedLanguageFlags[('g++','gfortran')].flags['F90']="-lgfortran"
    #########################################################################################
    # g95 settings
    compName='g95'
    fortFlags[compName]=copy.deepcopy(fortFlags['gfortran'])
    fortFlags[compName].testedVersions=[]
    #########################################################################################
    # Intel compiler settings
    # Fortran
    compName='ifort'
    fortFlags[compName]=FortFlags("-I",
                                  "",
                                  "-extend-source -fixed",
                                  compName,
                                  "-P",
                                  "-extend-source -fixed",
                                  testedVersions=["12.1.0","13.0.0"])
    fortFlags[compName].doFlags[False]=FlagPair(opt="-O3")
    fortFlags[compName].doFlags[True]=FlagPair("-check all -g  -traceback -fpe0","-O0")
    # C++
    compName='icpc'
    cxxFlags[compName]=copy.deepcopy(cxxFlags['g++'])
    cxxFlags[compName].testedVersions=fortFlags['ifort'].testedVersions
    # mixed Language linking
    mixedLanguageFlags[('icpc','ifort')]=MixedLanguageFlags('icpc','ifort','ifort','ifort')
    # native main:
    mixedLanguageFlags[('icpc','ifort')].flags['CXX']="-cxxlib -nofor_main"
    # non-native main:
    mixedLanguageFlags[('icpc','ifort')].flags['F90']="-cxxlib"
    #########################################################################################
    # NAG compiler settings
    compName='nagfor'
    fortFlags[compName]=FortFlags("-I",
                                  "-132",
                                  "-132 -fixed",
                                  compName,
                                  "-F",
                                  "-132 -fixed",
                                  ["5.2","5.3","5.3.1"])
    fortFlags[compName].doFlags[False]=FlagPair(opt="-w -O4")
    fortFlags[compName].doFlags[True]=FlagPair("-g -strict95 -C=all -gline -ieee=full","-O0")
    # mixed Language linking
    mixedLanguageFlags[('g++','nagfor')]=MixedLanguageFlags('g++','nagfor','nagfor','nagfor')
    # native main:
    mixedLanguageFlags[('g++','nagfor')].flags['CXX']="-Wl,-lstdc++"
    # non-native main:
    mixedLanguageFlags[('g++','nagfor')].flags['F90']="-Wl,-lstdc++"
    #########################################################################################
    # SUN compiler settings 
    # Fortran
    compName='sunf95'
    fortFlags[compName]=FortFlags("-M",
                                  "-e",
                                  "-fixed -e",
                                  compName,
                                  "-F",
                                  "-fixed -e")
    fortFlags[compName].doFlags[False]=FlagPair(opt="-xO3 -vpara")
    fortFlags[compName].doFlags[True]=FlagPair("-g","-O0")
    # C++
    compName='sunCC'
    cxxFlags[compName]=copy.deepcopy(cxxFlags['g++'])
    cxxFlags[compName].testedVersions=[]
    #########################################################################################
    # PGF compiler settings 
    # Fortran
    compName='pgf95'
    fortFlags[compName]=FortFlags("-module ",
                                  "",
                                  "",
                                  testedVersions=["12.4-0"])
    fortFlags[compName].doFlags[False]=FlagPair(opt="-O4")
    fortFlags[compName].doFlags[True]=FlagPair("-g","-O0")
    # C++
    compName='pgcpp'
    cxxFlags[compName]=CxxFlags(["12.4-0"])
    cxxFlags[compName].doFlags[False]=FlagPair(opt="-O4")
    cxxFlags[compName].doFlags[True]=FlagPair("-g","-O0")
    compName='pgf95'
    # mixed Language linking
    mixedLanguageFlags[('pgcpp','pgf95')]=MixedLanguageFlags('pgcpp','pgf95','pgcpp','pgf95')
    # native main:
    mixedLanguageFlags[('pgcpp','pgf95')].flags[('CXX','CXX')]="-pgf90libs"
    mixedLanguageFlags[('pgcpp','pgf95')].flags[('CXX','F90')]="-pgf90libs"
    # non-native main:
    mixedLanguageFlags[('pgcpp','pgf95')].flags[('F90','CXX')]="-pgcpplibs"
    mixedLanguageFlags[('pgcpp','pgf95')].flags[('F90','F90')]="-pgcpplibs"

    #########################################################################################
    # Absoft compiler settings 
    # Fortran
    compName='af95'
    fortFlags[compName]=FortFlags("-p",
                                  "",
                                  "",
                                  testedVersions=["11.0.3"])
    fortFlags[compName].doFlags[False]=FlagPair(opt="-O3 -YEXT_NAMES=LCS -s -B108 -YCFRL=1 -w")
    fortFlags[compName].doFlags[True]=FlagPair("-g -YEXT_NAMES=LCS -s -B108 -YCFRL=1 -w","-O0")
    #########################################################################################
    # IBM compiler settings 
    # Fortran
    compName='xlf'
    fortFlags[compName]=FortFlags("-I",
                                  "",
                                  "")
    fortFlags[compName].doFlags[False]=FlagPair(opt="-O4 -qstrict")
    fortFlags[compName].doFlags[True]=FlagPair("-g","-O0")
    # C++
    compName='xlC'
    cxxFlags[compName]=CxxFlags()
    cxxFlags[compName].doFlags[False]=FlagPair(opt="-O4 -qstrict")
    cxxFlags[compName].doFlags[True]=FlagPair("-g","-O0")
    #########################################################################################
    # IBM Blue Gene compiler settings 
    # Fortran
    compName='bgxlf'
    fortFlags[compName]=copy.deepcopy(fortFlags['xlf'])
    # C++
    compName='bgxlC'
    cxxFlags[compName]=copy.deepcopy(cxxFlags['xlC'])
    #########################################################################################
    # IBM Blue Gene MPI compiler wrapper settings 
    # Fortran
    compName='mpixlf90'
    fortFlags[compName]=copy.deepcopy(fortFlags['xlf'])
    # C++
    compName='mpixlcxx'
    cxxFlags[compName]=copy.deepcopy(cxxFlags['xlC'])
    #########################################################################################
    # generic MPI compiler wrappers 
    # Fortran
    compName='mpif90'
    fortFlags[compName]=FortFlags("-I",
                                  "",
                                  "")
    fortFlags[compName].doFlags[False]=FlagPair(opt="-O")
    fortFlags[compName].doFlags[True]=FlagPair("-g","-O0")
    # C++
    compName='mpicxx'
    cxxFlags[compName]=CxxFlags()
    cxxFlags[compName].doFlags[False]=FlagPair(opt="-O")
    cxxFlags[compName].doFlags[True]=FlagPair("-g","-O0")
    #########################################################################################
    # C++
    compName='nvcc'
    cxxFlags[compName]=CxxFlags()
    cxxFlags[compName].doFlags[False]=FlagPair(opt="-O3")
    cxxFlags[compName].doFlags[True]=FlagPair("-g","-O0")
    #########################################################################################
    mixedLanguageLinkers=mixedLanguageFlags.keys()

    fortComps=fortFlags.keys()
    cxxComps=cxxFlags.keys()
    opt.add_option('-f','--fortranCompiler',dest='fortComp',
                   type='choice', choices=fortComps,
                   help="pick a Fortran compiler (defaults to "+fortCompDefault+") from: [ " +" | ".join(fortComps)+" ] - the compiler should be in your PATH",
                   default=fortCompDefault)
    opt.add_option('-c','--cPlusPlusCompiler',dest='cxxComp',
                   type='choice', choices=cxxComps,
                   help="pick a C++ compiler (defaults to "+cxxCompDefault+") from: [ " +" | ".join(cxxComps)+" ] - the compiler should be in your PATH",
                   default=cxxCompDefault)
    opt.add_option('-m','--mixedLanguageLinker',dest='mixedLinker',
                   help="pick a linker for mixed language applications - the linker should be in your PATH (default none); this configure knows flags for: "+ ", ".join([str (x) for x in mixedLanguageLinkers]))
    opt.add_option('-d','--debug',dest='debug',
                   help="setup for compiling with full debug information (defaults to False)",
                   action='store_true',
                   default=False)
    opt.add_option('--fortranLongLines',dest='fortranLongLines',
                   help="permit lines longer than the standard length (default False)",
                   action='store_true',
                   default=False)
    opt.add_option('--fortranFixedFormat',dest='fortranFixedFormat',
                   help="use fixed instead of free format (default False)",
                   action='store_true',
                   default=False)
    opt.add_option('-q','--queue',dest='queue',
                   help="set up for multithreaded queue(default False)",
                   action='store_true',
                   default=False)
    opt.add_option('--withOpenPA',dest='openPA',
                   help="use the OpenPA library (defaults to False); implies -q",
                   metavar='<path_to_openpa>',
                   default=False)
    opt.add_option('--noCheck',dest='noCheck',
                   help="do not run checks during configuration (defaults to False)",
                   action='store_true',
                   default=False)
    opt.add_option('--noCleanup',dest='noCleanup',
                   help="if the configuration check fails do not remove the associated files (defaults to False)",
                   action='store_true',
                   default=False)
    opt.add_option('--compilerConfigs',dest='compilerConfigs',
                   help="print the flags for all the compilers that this configure script covers (defaults to False)",
                   action='store_true',
                   default=False)
    (options, args) = opt.parse_args()
    ourMakeDefsHandle=None
    ourMakeRulesHandle=None
    try:
        if (options.compilerConfigs):
          sys.stdout.write("Fortran:\n")
          for k in sorted(fortFlags.keys()):
            v=fortFlags[k]
            sys.stdout.write("  "+k)
            if (v.testedVersions) :
              sys.stdout.write("\t (currently tested versions: "+', '.join(v.testedVersions)+" )")
            sys.stdout.write("\n")
            for df,f in v.doFlags.items():
              if (df): 
                sys.stdout.write("    debug:                   "+f.debug+" "+f.opt+"\n")
              else :
                sys.stdout.write("    optimized                "+f.opt+"\n")
            if (v.modSearch):
              sys.stdout.write("    module search path:      "+v.modSearch+"\n")
            if (v.fpp):
              sys.stdout.write("    preprocessor:            "+v.fpp+"\n")
            if (v.fppFlag):
              sys.stdout.write("    preprocessor flags:      "+v.fppFlag+"\n")
            if (v.fppFixedForm):
              sys.stdout.write("    preproc. fixed format:   "+v.fppFixedForm+"\n")
            if (v.freeFormLongLines):
              sys.stdout.write("    free format long lines:  "+v.freeFormLongLines+"\n")
            if (v.fixedFormLongLines):
              sys.stdout.write("    fixed format long lines: "+v.fixedFormLongLines+"\n")
            sys.stdout.write("\n")
          sys.stdout.write("C++:\n")
          for k in sorted(cxxFlags.keys()):
            v=cxxFlags[k]
            sys.stdout.write("  "+k)
            if (v.testedVersions) :
              sys.stdout.write("\t (currently tested versions: "+', '.join(v.testedVersions)+" )")
            sys.stdout.write("\n")
            for df,f in v.doFlags.items():
              if (df): 
                sys.stdout.write("    debug:                   "+f.debug+" "+f.opt+"\n")
              else :
                sys.stdout.write("    optimized                "+f.opt+"\n")
            sys.stdout.write("\n")
          sys.stdout.write("mixed language linking:\n")
          for (l,k) in mixedLanguageLinkers:
            sys.stdout.write("  "+l+" / "+k+"\n")
            if (mixedLanguageFlags[(l,k)].CXXLinker!=mixedLanguageFlags[(l,k)].F90Linker):
              sys.stdout.write("    CXX \"main\" linker:    "+mixedLanguageFlags[(l,k)].CXXLinker+"\n")
              if ('CXX','CXX') in mixedLanguageFlags[(l,k)].flags:
                sys.stdout.write("      CXX library link flags:  "+mixedLanguageFlags[(l,k)].flags[('CXX','CXX')]+"\n")
              sys.stdout.write("    F90 \"program\" linker: "+mixedLanguageFlags[(l,k)].F90Linker+"\n")
              if ('F90','F90') in mixedLanguageFlags[(l,k)].flags:
                sys.stdout.write("      F90 library link flags:  "+mixedLanguageFlags[(l,k)].flags[('F90','F90')]+"\n")
            else:
              sys.stdout.write("    common linker: "+mixedLanguageFlags[(l,k)].CXXLinker+"\n")
              for main,flags in mixedLanguageFlags[(l,k)].flags.items():
                if main=='CXX':
                  sys.stdout.write("    CXX \"main\" / F90 library link flags:     "+flags+"\n")
                elif main=='F90':
                  sys.stdout.write("    F90 \"program\" / CXX library link flags:  "+flags+"\n")
            sys.stdout.write("\n")

        if (not options.noCheck
            and
            os.path.dirname( os.path.realpath( __file__ ) )!=os.path.realpath(os.getcwd())):
            raise ConfException("the configure.py script has to be invoked from within the Rapsodia root directory("+os.path.dirname( os.path.realpath( __file__ ) )+") but it was invoked from "+ os.path.realpath(os.getcwd()))
        if (options.openPA):
          options.queue=True
        global ourRootPath
        ourRootPath=os.path.realpath(os.getcwd())
        global ourConfLogHandle
        ourConfLogHandle=open("config.log","w")
        ourConfLogHandle.write("# "+" ".join(sys.argv)+"\n\n")
        ourMakeDefsHandle = open(ourMakeDefsName, 'w')
        ourMakeDefsHandle.write("# generated by: "+" ".join(sys.argv)+"\n\n\n")
        testAndWrite(ourMakeDefsHandle,"F90C",options.fortComp)
        fFlags=fortFlags[options.fortComp]
        flagsString=fFlags.doFlags[options.debug].debug+" "+fFlags.doFlags[options.debug].opt
        if (options.fortranLongLines):
            flagsString+=" "+fFlags.freeFormLongLines
        if (options.fortranFixedFormat):
            flagsString+=" "+fFlags.fixedFormLongLines
        testAndWrite(ourMakeDefsHandle,"FFLAGS",flagsString)
        if (fFlags.modSearch!=''):
          testAndWrite(ourMakeDefsHandle,"MODSEARCHFLAG",fFlags.modSearch)
        testAndWrite(ourMakeDefsHandle,"CXX",options.cxxComp)
        cFlags=cxxFlags[options.cxxComp]
        flagsString=cFlags.doFlags[options.debug].debug+" "+cFlags.doFlags[options.debug].opt
        testAndWrite(ourMakeDefsHandle,"CXXFLAGS",flagsString)
        for (l,k) in mixedLanguageLinkers:
          if (l==options.cxxComp) and (k==options.fortComp):
            if (mixedLanguageFlags[(l,k)].CXXLinker!=mixedLanguageFlags[(l,k)].F90Linker):
              testAndWrite(ourMakeDefsHandle,"MIXLANG_LD_TOPCXX",mixedLanguageFlags[(l,k)].CXXLinker)
              for main,flags in mixedLanguageFlags[(l,k)].flags.items():
                if main==('CXX','CXX'):
                  testAndWrite(ourMakeDefsHandle,"MIXLANG_LDFLAGS_TOPCXX_LIBSCXX",flags)
                elif main==('CXX','F90'):
                  testAndWrite(ourMakeDefsHandle,"MIXLANG_LDFLAGS_TOPCXX_LIBSF90",flags)
              testAndWrite(ourMakeDefsHandle,"MIXLANG_LD_TOPF90",mixedLanguageFlags[(l,k)].F90Linker)
              for main,flags in mixedLanguageFlags[(l,k)].flags.items():
                if main==('F90','CXX'):
                  testAndWrite(ourMakeDefsHandle,"MIXLANG_LDFLAGS_TOPF90_LIBSCXX",flags)
                elif main==('F90','F90'):
                  testAndWrite(ourMakeDefsHandle,"MIXLANG_LDFLAGS_TOPF90_LIBSF90",flags)
            else:
              testAndWrite(ourMakeDefsHandle,"MIXLANG_LD_TOPCXX",mixedLanguageFlags[(l,k)].CXXLinker)
              for main,flags in mixedLanguageFlags[(l,k)].flags.items():
                if main=='CXX':
                  testAndWrite(ourMakeDefsHandle,"MIXLANG_LDFLAGS_TOPCXX_LIBSCXX",flags)
                elif main=='F90':
                  testAndWrite(ourMakeDefsHandle,"MIXLANG_LDFLAGS_TOPCXX_LIBSF90",flags)
              testAndWrite(ourMakeDefsHandle,"MIXLANG_LD_TOPF90",mixedLanguageFlags[(l,k)].F90Linker)
              for main,flags in mixedLanguageFlags[(l,k)].flags.items():
                if main=='CXX':
                  testAndWrite(ourMakeDefsHandle,"MIXLANG_LDFLAGS_TOPF90_LIBSCXX",flags)
                elif main=='F90':
                  testAndWrite(ourMakeDefsHandle,"MIXLANG_LDFLAGS_TOPF90_LIBSF90",flags)


        ourMakeDefsHandle.write('''
export HOTF90NAMES= multiIndexUtil higherOrderTensorUtil
export HOTCPPNAMES= MultiIndex HigherOrderTensor HessianIndex
export RA_CXX_LIBS=-lRapsodia
export RA_F90_LIBS=-lRapsodia
''')
        if (options.queue): 
          ourMakeDefsHandle.write('''
export RA_USE_QUEUE=y
export RA_CXX_LIBS+= -lpthread
export QUEUEOBJS=ActiveTypeQueue.o ActiveTypeQueueEntry.o
export QUEUEFILES=ActiveTypeQueue.hpp ActiveTypeQueue.cpp  ActiveTypeQueueEntry.hpp ActiveTypeQueueEntry.cpp WorkArray.hpp
''')
	  if (os.uname()[0]=='SunOS'): 
            ourMakeDefsHandle.write("RA_CXX_LIBS+= -lrt\n")
        if (options.openPA):
          ourMakeDefsHandle.write('''
export HAVE_OPA=y
export OPAROOT=%s
''' % (options.openPA))
        ourMakeDefsHandle.close()

        ourMakeRulesHandle = open(ourMakeRulesName, 'w')
        ourMakeRulesHandle.write("# generated by: "+" ".join(sys.argv)+"\n")
        ourMakeRulesHandle.write('''
# generic rules
%.o: %.f90
	$(F90C) $(FFLAGS) $(IPATH) $(MPATH) ''' )
        if (options.fortComp in ["mpif90","mpixlf"]) : 
          ourMakeRulesHandle.write(" -DRA_USE_MPI")
        if (options.debug) : 
          ourMakeRulesHandle.write(" -DRA_DEBUG")
        ourMakeRulesHandle.write(''' -c $< -o $@
        
%.o: %.F90
	$(F90C) $(FFLAGS) $(IPATH) $(MPATH) ''' )
        if (options.fortComp in ["mpif90","mpixlf"]) : 
          ourMakeRulesHandle.write(" -DRA_USE_MPI")
        if (options.debug) : 
          ourMakeRulesHandle.write(" -DRA_DEBUG")
        ourMakeRulesHandle.write(''' -c $< -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(IPATH)''' )

        ourMakeRulesHandle.write(''' -c $< -o $@ ''')
        if (options.queue): 
          ourMakeRulesHandle.write(" -DRA_USE_QUEUE")
        if (options.cxxComp in ["mpicxx","mpixlcxx"]) : 
          ourMakeRulesHandle.write(" -DRA_USE_MPI")
        if (options.debug) : 
          ourMakeRulesHandle.write(" -DRA_DEBUG")
        if (options.openPA):
            ourMakeRulesHandle.write(" -DRA_HAVE_OPA -I"+os.path.join("$(OPAROOT)","include"))
        ourMakeRulesHandle.close()
        if (not options.noCheck):
          # to be able to run the tests set here locally:
          os.environ['RAPSODIAROOT']=os.getcwd()


          if (os.environ.has_key("FXX")):
            print "have FXX: "+os.environ["FXX"]
          compileAndRun('''
      program p
        print *, "OK"
      end program
''',
                        True,"Fortran compiler test:")

          if (os.environ.has_key("CXX")):
            print "have CXX: "+os.environ["CXX"]
          compileAndRun('''
#include <iostream>
          
int main (void) {
  std::cout << "OK" << std::endl;
  return 0;
}
''',
                        False,"C++ compiler test:")
          if (options.openPA):
            compileAndRun('''
#include <iostream>
#include "opa_primitives.h"
          
int main (void) {
  OPA_int_t atomic_int;
  OPA_store_int(&atomic_int, 1);
  OPA_add_int(&atomic_int, 2);
  if (atomic_int.v!=3) { 
    std::cout << "atomic_int.v is " << atomic_int.v << " but should be 3"  << std::endl;
    return 1;
  }
  return 0;
}
''',
                          False,
                          "C++ compiler test (with OpenPA):")
          enableReverse=True
          try: 
            compileAndRun('''
      module ftest
        type atype
          real::a
        contains
          final::closee
        end type atype
      contains
        subroutine closee(this)
          type(atype)::this
          print *, "OK"
        end subroutine closee
      end module ftest
      program p
        use ftest
        type(atype)::a
        a%a=1.0
        print *, "OK"
      end program
''',
                          True,
                          "Fortran compiler finalization support test for reverse mode:")
          except ConfException, e:
            enableReverse=False
            os.chdir(ourRootPath)
          ourMakeDefsHandle = open(ourMakeDefsName, "a")
          if (enableReverse):
            ourMakeDefsHandle.write('''
export ENABLEREVERSEF90=1
''')
          else:
            print "Note: Fortran compiler ("+options.fortComp+") does not support FINALIZE; therefore reverse mode for Fortran is not supported"
            ourMakeDefsHandle.write('''
export ENABLEREVERSEF90=0
''')
            if (os.path.exists(ourTempDirName)):
              shutil.rmtree(ourTempDirName)

          ourMakeDefsHandle.close()
        ourConfLogHandle.close()
    except ConfException, e:
        sys.stderr.write("ERROR: "+str(e)+"\n")
        if (not options.noCleanup): 
          cleanUp()
        return -1
    return 0

if __name__ == "__main__":
    sys.exit(main())
