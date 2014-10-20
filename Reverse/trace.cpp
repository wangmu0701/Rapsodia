#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <stdbool.h>
#include "common.h"

#include "trace.h"
#include "block.h"
#include "location.h"
#include "trcodes.h"

#define MACRO_CHECK_REVON if(!revTraceOn){return;}
#define NOT_IMPLEMENTED_YET fprintf(stderr,"This function is not implemented yet!\n");

extern struct StackBlock *RA_blk_tmpBlock;
extern void *RA_blk_ret;

extern struct TargetStack lStack,gStack;
extern struct TargetStack stackCursor;
extern bool revTraceOn;

void printaddress_(location operand){
  printf("Addr:<%lx>\n",(unsigned long)operand);
  fflush(stdout);
}

void pushConstGlobalS(location source){
  MACRO_CHECK_REVON
  RA_PUSH_INT((&gStack),0)
  RA_PUSH_INT((&gStack),const_s)
  RA_PUSH_LOCATION((&gStack),source)
}
void pushConstGlobalD(location source){
  MACRO_CHECK_REVON
#ifndef FAST_MODE_D
  RA_PUSH_INT((&gStack),0)
  RA_PUSH_INT((&gStack),const_d)
  RA_PUSH_LOCATION((&gStack),source)
#endif
#ifdef FAST_MODE_D
  RA_PUSH_INT((&gStack),0)
  RA_PUSH_LOCATION((&gStack),source)
#endif
}
void dePushConstGlobal(location source){
  MACRO_CHECK_REVON
  initCursorFromStack(&stackCursor,&gStack);
#ifndef FAST_MODE_D
  RA_NEXT_SIZE((&stackCursor),RA_SIZE_INT)
  RA_NEXT_SIZE((&stackCursor),RA_SIZE_INT)
  RA_NEXT_SIZE((&stackCursor),RA_SIZE_LOCATION)
#endif
#ifdef FAST_MODE_D
  RA_NEXT_SIZE((&stackCursor),RA_SIZE_INT)
  RA_NEXT_SIZE((&stackCursor),RA_SIZE_LOCATION)
#endif
  popLocalStackToCursor(&gStack,&stackCursor);
}

void pushUnaryLocalSS(location source, double val, location operand){
  MACRO_CHECK_REVON
  RA_PUSH_LOCATION((&lStack),operand)
  RA_PUSH_DOUBLE((&lStack),val)
  RA_PUSH_INT((&lStack),unary_s_s)
  RA_PUSH_LOCATION((&lStack),source)
}
void pushUnaryLocalSD(location source, double val, location operand){
  MACRO_CHECK_REVON
  RA_PUSH_LOCATION((&lStack),operand)
  RA_PUSH_DOUBLE((&lStack),val)
  RA_PUSH_INT((&lStack),unary_s_d)
  RA_PUSH_LOCATION((&lStack),source)
}
void pushUnaryLocalDS(location source, double val, location operand){
  MACRO_CHECK_REVON
  RA_PUSH_LOCATION((&lStack),operand)
  RA_PUSH_DOUBLE((&lStack),val)
  RA_PUSH_INT((&lStack),unary_d_s)
  RA_PUSH_LOCATION((&lStack),source)
}
void pushUnaryLocalDD(location source, double val, location operand){
  MACRO_CHECK_REVON
#ifndef FAST_MODE_D
  RA_PUSH_LOCATION((&lStack),operand)
  RA_PUSH_DOUBLE((&lStack),val)
  RA_PUSH_INT((&lStack),unary_d_d)
  RA_PUSH_LOCATION((&lStack),source)
#endif
#ifdef FAST_MODE_D
  RA_PUSH_LOCATION((&lStack),operand)
  RA_PUSH_DOUBLE((&lStack),val)
  RA_PUSH_INT((&lStack),1)
  RA_PUSH_LOCATION((&lStack),source)
#endif
}
void pushBinaryLocalSSS(location source, double val1, location operand1, double val2, location operand2){
  MACRO_CHECK_REVON
  RA_PUSH_LOCATION((&lStack),operand2)
  RA_PUSH_DOUBLE((&lStack),val2)
  RA_PUSH_LOCATION((&lStack),operand1)
  RA_PUSH_DOUBLE((&lStack),val1)
  RA_PUSH_INT((&lStack),binary_s_s_s)
  RA_PUSH_LOCATION((&lStack),source)
}

void pushBinaryLocalSSD(location source, double val1, location operand1, double val2, location operand2){
  MACRO_CHECK_REVON
  RA_PUSH_LOCATION((&lStack),operand2)
  RA_PUSH_DOUBLE((&lStack),val2)
  RA_PUSH_LOCATION((&lStack),operand1)
  RA_PUSH_DOUBLE((&lStack),val1)
  RA_PUSH_INT((&lStack),binary_s_s_d)
  RA_PUSH_LOCATION((&lStack),source)
}

void pushBinaryLocalSDS(location source, double val1, location operand1, double val2, location operand2){
  MACRO_CHECK_REVON
  RA_PUSH_LOCATION((&lStack),operand2)
  RA_PUSH_DOUBLE((&lStack),val2)
  RA_PUSH_LOCATION((&lStack),operand1)
  RA_PUSH_DOUBLE((&lStack),val1)
  RA_PUSH_INT((&lStack),binary_s_d_s)
  RA_PUSH_LOCATION((&lStack),source)
}

void pushBinaryLocalSDD(location source, double val1, location operand1, double val2, location operand2){
  MACRO_CHECK_REVON
  RA_PUSH_LOCATION((&lStack),operand2)
  RA_PUSH_DOUBLE((&lStack),val2)
  RA_PUSH_LOCATION((&lStack),operand1)
  RA_PUSH_DOUBLE((&lStack),val1)
  RA_PUSH_INT((&lStack),binary_s_d_d)
  RA_PUSH_LOCATION((&lStack),source)
}

void pushBinaryLocalDSS(location source, double val1, location operand1, double val2, location operand2){
  MACRO_CHECK_REVON
  RA_PUSH_LOCATION((&lStack),operand2)
  RA_PUSH_DOUBLE((&lStack),val2)
  RA_PUSH_LOCATION((&lStack),operand1)
  RA_PUSH_DOUBLE((&lStack),val1)
  RA_PUSH_INT((&lStack),binary_d_s_s)
  RA_PUSH_LOCATION((&lStack),source)
}

void pushBinaryLocalDSD(location source, double val1, location operand1, double val2, location operand2){
  MACRO_CHECK_REVON
  RA_PUSH_LOCATION((&lStack),operand2)
  RA_PUSH_DOUBLE((&lStack),val2)
  RA_PUSH_LOCATION((&lStack),operand1)
  RA_PUSH_DOUBLE((&lStack),val1)
  RA_PUSH_INT((&lStack),binary_d_s_d)
  RA_PUSH_LOCATION((&lStack),source)
}

void pushBinaryLocalDDS(location source, double val1, location operand1, double val2, location operand2){
  MACRO_CHECK_REVON
  RA_PUSH_LOCATION((&lStack),operand2)
  RA_PUSH_DOUBLE((&lStack),val2)
  RA_PUSH_LOCATION((&lStack),operand1)
  RA_PUSH_DOUBLE((&lStack),val1)
  RA_PUSH_INT((&lStack),binary_d_d_s)
  RA_PUSH_LOCATION((&lStack),source)
}

void pushBinaryLocalDDD(location source, double val1, location operand1, double val2, location operand2){
  MACRO_CHECK_REVON
#ifndef FAST_MODE_D
  RA_PUSH_LOCATION((&lStack),operand2)
  RA_PUSH_DOUBLE((&lStack),val2)
  RA_PUSH_LOCATION((&lStack),operand1)
  RA_PUSH_DOUBLE((&lStack),val1)
  RA_PUSH_INT((&lStack),binary_d_d_d)
  RA_PUSH_LOCATION((&lStack),source)
#endif
#ifdef FAST_MODE_D
  RA_PUSH_LOCATION((&lStack),operand2)
  RA_PUSH_DOUBLE((&lStack),val2)
  RA_PUSH_LOCATION((&lStack),operand1)
  RA_PUSH_DOUBLE((&lStack),val1)
  RA_PUSH_INT((&lStack),2)
  RA_PUSH_LOCATION((&lStack),source)
#endif
}

