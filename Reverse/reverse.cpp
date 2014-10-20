#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <stdbool.h>

#include "trace.h"
#include "block.h"
#include "common.h"
#include "reverse.h"
#include "location.h"
#include "trcodes.h"

#ifdef INTEGER_LOC
extern double *loc_ad;
extern void **loc_addr;
#endif
//void *__gxx_personality_v0;
struct TargetStack lStack,gStack;
bool revTraceOn=false;
bool revInitialized=false;

extern struct StackBlock *RA_blk_tmpBlock;
extern void *RA_blk_ret;
double *tape;
location *tape_key;
int *tape_type;

int tape_len;

int rev_i;
int rev_nop;
struct TargetStack stackCursor;
bool rev_endflag=false;
int rev_trcode;
location rev_source;
location rev_operand; 
int rev_taploc, rev_staploc;
int rev_type,rev_stype,rev_ttype;
double rev_vald,rev_wd;
float rev_vals,rev_ws;
void* rev_ret;

void revStart(){
  if (!revInitialized){
    initialStack();
    tape=(double*)malloc(sizeof(double)*MAX_LOCAL_TAPE);
    tape_key=(location*)malloc(sizeof(location)*MAX_LOCAL_TAPE);
    tape_type=(int*)malloc(sizeof(int)*MAX_LOCAL_TAPE);
  }
  else{
    revInternalWarning(-3);
  }
  revInitialized=true;
  revTraceOn=true;
}
void revStop(){
  if (revInitialized){
    releaseStack();
    free(tape);
    free(tape_key);
    free(tape_type);
  }
  else{
    revInternalWarning(-4);
  }
  revInitialized=false;
  revTraceOn=false;
}
void revOn(){
  revTraceOn=true;
}
void revOff(){
  revTraceOn=false;
}
bool inActiveSource(location source){
  if (source==(location)NULLLOC){
    return true;
  }
  for(rev_i=0;rev_i<tape_len;rev_i++){
    if ((tape_type[rev_i]!=NULLType)){
      return false;
    }
  }
  return true;
}

#ifndef FAST_MODE_D
#include "RA_adacc.c"
#endif

#ifdef FAST_MODE_D
#include "RA_adacc_d.c"
#endif

