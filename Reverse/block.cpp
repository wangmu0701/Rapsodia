#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "block.h"
extern struct TargetStack lStack,gStack;
extern bool revTraceOn;

struct StackBlock *RA_blk_tmpBlock;
void *RA_blk_ret;

struct StackBlock* newStackBlock(){
  RA_blk_tmpBlock=(struct StackBlock*)malloc(sizeof(struct StackBlock));
  RA_blk_tmpBlock->curr_len=0;
  RA_blk_tmpBlock->avlb_len=RA_BLK_SIZE;
  RA_blk_tmpBlock->next=NULL;
  return RA_blk_tmpBlock;
}
void initialStack(){
  lStack.cur_blk=newStackBlock();
  lStack.curr_len=0;
  lStack.avlb_len=RA_BLK_SIZE;
  gStack.cur_blk=newStackBlock();
  gStack.curr_len=0;
  gStack.avlb_len=RA_BLK_SIZE;
}
void releaseStack(){
  while(lStack.cur_blk!=NULL){
    freeStackBlock(&lStack);
  }
  lStack.curr_len=0;
  lStack.avlb_len=0;
  while(gStack.cur_blk!=NULL){
    freeStackBlock(&gStack);
  }
  gStack.curr_len=0;
  gStack.avlb_len=0;
}
void initCursorFromStack(struct TargetStack *cursor,struct TargetStack *stack){
  cursor->cur_blk=stack->cur_blk;
  cursor->curr_len=stack->cur_blk->curr_len;
  cursor->avlb_len=stack->cur_blk->avlb_len;
}
void popLocalStackToCursor(struct TargetStack *stack,struct TargetStack *cursor){
  while(stack->cur_blk!=cursor->cur_blk){
    freeStackBlock(stack);
  }
  stack->cur_blk->curr_len=cursor->curr_len;
  stack->cur_blk->avlb_len=cursor->avlb_len;
  stack->curr_len=cursor->curr_len;
  stack->avlb_len=cursor->avlb_len;
}

void freeStackBlock(struct TargetStack *stack){
  RA_blk_tmpBlock=stack->cur_blk->next;
  free(stack->cur_blk);
  stack->cur_blk=RA_blk_tmpBlock;
}

//Internal Errors and Warnings
void revInternalError(int errCode){
  fprintf(stderr,"Reverse Mode Internal Error #%d : ", errCode);
  switch (errCode) {
    case -1:
      fprintf(stderr,"Trying to read from empty stack.\n");
      break;
    case -2:
      fprintf(stderr,"Error number of NOP (Number of OPerands).\n");
      break;
    case -3:
      fprintf(stderr,"Local tape out of boundary (reset -tl with a larger parameter).\n");
      break;
    case -4:
      fprintf(stderr,"Error Type Code in Pre-Accumulation\n");
      break;
    case -5:
      fprintf(stderr,"Error Type Code in Global-Accumulation\n");
      break;
    case -6:
      fprintf(stderr,"Error Location in getAdjoint\n");
      break;
    case -7:
      fprintf(stderr,"Trying to set adjoint at invalid location\n");
      break;
  }
  exit(-1);
}

void revInternalWarning(int warnCode){
  fprintf(stderr,"Reverse Mode Internal Warning #%d : ", warnCode);
  switch (warnCode) {
    case -1:
      fprintf(stderr,"Expand Location Array. (If you see this multiple times, please enlarge the -ll parameter\n)");
      break;
    case -2:
      fprintf(stderr,"Trying to get adjoint from invalid location\n");
      break;
    case -3:
      fprintf(stderr,"Another active section starts without stop the previous one\n");
      break;
    case -4:
      fprintf(stderr,"Active section stops before starts\n");
      break;
   }
}

void printTraceBrute(struct TargetStack *stack, int s, int e){
  int i;
  unsigned int *p=(unsigned int*)&(stack->cur_blk->data[s]);
  printf("\n %d :",stack->cur_blk->curr_len);
  for(i=s;(i<e)&&(i-s<stack->cur_blk->curr_len);i+=sizeof(unsigned int)){
    printf(" %x ",*p);
    p++;
  }
  printf("\n");
}

