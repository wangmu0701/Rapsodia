#ifndef __RA_BLOCK_H__
#define __RA_BLOCK_H__

#include "common.h"


#define RA_BLK_SIZE (RA_PAGE_SIZE-RA_SIZE_INT*2-RA_SIZE_VOIDP)

#define RA_GET_SIZE(stackCursor,size) if (stackCursor->avlb_len<size){                                         \
                                          RA_blk_tmpBlock=newStackBlock();                                \
                                          RA_blk_tmpBlock->curr_len=0;                                         \
                                          RA_blk_tmpBlock->avlb_len=RA_BLK_SIZE;                               \
                                          RA_blk_tmpBlock->next=stackCursor->cur_blk;                          \
                                          stackCursor->cur_blk=RA_blk_tmpBlock;                                \
                                          stackCursor->curr_len=0;                                             \
                                          stackCursor->avlb_len=RA_BLK_SIZE;                                   \
                                      }                                                                        \
                                      RA_blk_ret=(void*)&stackCursor->cur_blk->data[stackCursor->curr_len];    \
                                      stackCursor->cur_blk->curr_len+=size;                                    \
                                      stackCursor->curr_len+=size;                                             \
                                      stackCursor->cur_blk->avlb_len-=size;                                    \
                                      stackCursor->avlb_len-=size;                                             \


#define RA_NEXT_SIZE(stackCursor,size) if (stackCursor->curr_len<size) {                                       \
                                           if (stackCursor->cur_blk->next==NULL) {                             \
                                               RA_blk_ret=NULL;                                                \
                                               stackCursor->curr_len=0;                                        \
                                               stackCursor->avlb_len=0;                                        \
                                           }                                                                   \
                                           else {                                                              \
                                               stackCursor->cur_blk=stackCursor->cur_blk->next;                \
                                               stackCursor->curr_len=stackCursor->cur_blk->curr_len;           \
                                               stackCursor->avlb_len=stackCursor->cur_blk->avlb_len;           \
                                           }                                                                   \
                                       }                                                                       \
                                       if (stackCursor->curr_len>=size) {                                      \
                                           stackCursor->curr_len-=size;                                            \
                                           stackCursor->avlb_len+=size;                                            \
                                           RA_blk_ret=(void*)&stackCursor->cur_blk->data[stackCursor->curr_len];    \
                                       }

#define RA_NEXT_LOCATION(stackCursor,loc) RA_NEXT_SIZE(stackCursor,RA_SIZE_LOCATION)                                  \
                                          if (RA_blk_ret==NULL) {                                                     \
                                            loc=(location)NULLLOC;                                                    \
                                            rev_endflag=true;                                                         \
                                          }                                                                           \
                                          else {                                                                      \
                                            loc=*(location*)RA_blk_ret;                                               \
                                          }                                                                           \


#define RA_PUSH_LOCATION(stackCursor,entry)  RA_GET_SIZE(stackCursor,RA_SIZE_LOCATION)                                   \
                                             *(location*)RA_blk_ret=entry;                                               \

#define RA_PUSH_INT(stackCursor,entry)       RA_GET_SIZE(stackCursor,RA_SIZE_INT)                                        \
                                             *(int*)RA_blk_ret=entry;                                                    \

#define RA_PUSH_DOUBLE(stackCursor,entry)    RA_GET_SIZE(stackCursor,RA_SIZE_DOUBLE)                                     \
                                             *(double*)RA_blk_ret=entry;                                                 \

#define RA_NEXT_INT(stackCursor,entry)       RA_NEXT_SIZE(stackCursor,RA_SIZE_INT)                                       \
                                             entry=*(int*)RA_blk_ret;                                                    \

#define RA_NEXT_DOUBLE(stackCursor,entry)    RA_NEXT_SIZE(stackCursor,RA_SIZE_DOUBLE)                                    \
                                             entry=*(double*)RA_blk_ret;                                                 \



struct StackBlock{
  char data[RA_BLK_SIZE];
  int curr_len;
  int avlb_len;
  struct StackBlock *next;
};

struct TargetStack{
  struct StackBlock *cur_blk;
  int curr_len;
  int avlb_len;
};
extern "C" {
struct StackBlock* newStackBlock();
void freeStackBlock(struct TargetStack*);
void initialStack();
void releaseStack();
void initCursorFromStack(struct TargetStack*,struct TargetStack*);
void popLocalStackToCursor(struct TargetStack*,struct TargetStack*);

void revInternalError(int);
void revInternalWarning(int);

void printTraceBrute(struct TargetStack*, int,int);
}

#endif

