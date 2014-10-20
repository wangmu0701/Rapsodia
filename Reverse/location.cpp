#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "common.h"
#include "location.h"
#include "block.h"
#include "trace.h"

//Free: the untouched locations
//used: maintain locations which are being used. (actually not necessary)
//reuse: a Stack for reuse locations. (for fortran LHS finalizer)


#ifdef INTEGER_LOC
//This is a compensate for the free/reassign behavior introduced by fortran
//Which will call the finalizer for the left value of an assignment just before the assignment happens.
//So a free and reassign happens for the same memory address
//We do not want to write an finalizer for this on the global trace.
//1: definalize on the global trace. (This is what we are doing here)
//2: detect this and do nothing. (may be harder)
void* last_addr;
int last_loc;

void **loc_addr;
int *loc_next;
double *loc_ad;
int free_first;
int free_last;
int reuse_first;
int reuse_last;
int loc_len;
bool locOn=false;
int loc_ret;
int loc_i;

void initialLocation(){
  loc_len=INITIAL_LOCATION_LEN;
  loc_addr=(void**)malloc(sizeof(void*)*INITIAL_LOCATION_LEN);
  loc_next=(int*)malloc(sizeof(int)*INITIAL_LOCATION_LEN);
  loc_ad=(double*)malloc(sizeof(double)*INITIAL_LOCATION_LEN);
  loc_next[0]=1;
  for(loc_i=1;loc_i<INITIAL_LOCATION_LEN-1;loc_i++){
    loc_next[loc_i]=loc_i+1;
  }
  loc_next[loc_i]=NULLLOC;
  free_first=0;
  free_last=loc_i;
  reuse_first=NULLLOC;
  reuse_last=NULLLOC;
  last_loc=NULLLOC;
  last_addr=NULL;
}
void printLocation(){
  int i;
  printf("free_first=<%d>,free_last=<%d>,reuse_first=<%d>,reuse_last=<%d>\n",free_first,free_last,reuse_first,reuse_last);
  for(i=0;i<10;i++){
    printf("<%d:n=%d,a=%lx>",i,loc_next[i],(unsigned long)loc_addr[i]);
  }
  printf("\n");
}

void getLocation(int *loc,void *addr){
  if (!locOn){
    initialLocation();
    locOn=true;
  }
  location ret=0;
  if (reuse_first!=NULLLOC){
    loc_ret=reuse_first;
    destack_reuse(loc_ret);
  }
  else if (free_first!=NULLLOC){
//free list
    loc_ret=free_first;
    dequeue_free(loc_ret);
  }
  else{
    void **tmp_addr;
    int *tmp_next;
    double *tmp_ad;
    tmp_addr=(void**)malloc(sizeof(void*)*loc_len*2);
    tmp_next=(int*)malloc(sizeof(int)*loc_len*2);
    tmp_ad=(double*)malloc(sizeof(double)*loc_len*2);
    for(loc_i=0;loc_i<loc_len;loc_i++){
      tmp_addr[loc_i]=loc_addr[loc_i];
      tmp_next[loc_i]=loc_next[loc_i];
      tmp_ad[loc_i]=loc_ad[loc_i];
    }
    free(loc_addr);loc_addr=tmp_addr;
    free(loc_next); loc_next=tmp_next;
    free(loc_ad);loc_ad=tmp_ad;
    for(;loc_i<loc_len*2-1;loc_i++){
      loc_next[loc_i]=loc_i+1;
    }
    loc_next[loc_i]=NULLLOC;
    free_first=loc_len;
    free_last=loc_i;
    loc_len*=2;
    loc_ret=free_first;
    dequeue_free(loc_ret);
//have to expand
    revInternalWarning(-1);
  }
  loc_addr[loc_ret]=addr;
  *loc=loc_ret;

//definalizer if reassign happens right after free.
  if (last_addr==addr){
    dePushConstGlobal(loc_ret);
  }
  else{
    last_addr=NULL;
  }
//  printf("get : loc=<%d> addr=<%lx>\n",*loc,(unsigned long)addr);
  if (*loc!=NULLLOC){
    return;
  }
}

void freeLocation(int *loc,void *addr){
//  printf("free: loc=<%d> addr=<%lx>\n",*loc,(unsigned long)addr);
  last_loc=*loc;
  last_addr=addr;
  if (*loc!=NULLLOC){
    enstack_reuse(*loc);  
  }
  *loc=NULLLOC;
}

void getLocationD(int *loc, double *addr){
  getLocation(loc,(void*)addr);
}
void getLocationS(int *loc, float *addr){
  getLocation(loc,(void*)addr);
}
void freeLocationD(int *loc, double *addr){
  freeLocation(loc, (void*)addr);
}
void freeLocationS(int *loc, float *addr){
  freeLocation(loc, (void*)addr);
}


void dequeue_free(int loc){
  free_first=loc_next[loc];
  if (free_first==NULLLOC){
    free_last=NULLLOC;
  }
}
void enstack_reuse(int loc){
  loc_next[loc]=reuse_first;
  if (reuse_first==NULLLOC){
    reuse_last=loc;
  }
  reuse_first=loc;
}
void destack_reuse(int loc){
  reuse_first=loc_next[loc];
}

#ifdef RA_ACC_ON_LOC
void setAdjointLocD(int *loc, double *val){
  if (*loc==NULLLOC){
    revInternalError(-7);
  }
  loc_ad[*loc]=*val;
  *(double*)loc_addr[*loc]=*val;
}
void getAdjointLocD(int *loc, double *val){
  if (*loc==NULLLOC){
    revInternalWarning(-2);
  }
  else{
    *val=loc_ad[*loc];
    *(double*)loc_addr[*loc]=*val;
  }
}
void setAdjointLocS(int *loc, float *val){
  if (*loc==NULLLOC){
    revInternalError(-7);
  }
  loc_ad[*loc]=*val;
  *(float*)loc_addr[*loc]=*val;
}
void getAdjointLocS(int *loc, float *val){
  if (*loc==NULLLOC){
    revInternalWarning(-2);
  }
  else{
    *val=(float)loc_ad[*loc];
    *(float*)loc_addr[*loc]=*val;
  }
}
#endif
#endif

