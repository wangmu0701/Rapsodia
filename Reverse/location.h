#ifndef __RA_LOCATION_H__
#define __RA_LOCATION_H__

#include "common.h"
//Use array to mimic link list
extern "C" {
#ifdef INTEGER_LOC
void getLocationD(int *loc, double *addr);
void getLocationS(int *loc, float *addr);
void* getLocationAddr(int loc);
void getAdjointLocD(int *loc, double *addr);
void getAdjointLocS(int *loc, float *addr);

void freeLocationD(int *loc,double *addr);
void freeLocationS(int *loc,float *addr);

void dequeue_free(int);
void destack_reuse(int);
void enstack_reuse(int);

#ifdef RA_ACC_ON_LOC
void setAdjointLocD(int *loc, double *val);
void getAdjointLocD(int *loc, double *val);
void setAdjointLocS(int *loc, float *val);
void getAdjointLocS(int *loc, float *val);
#endif

#endif
}
#endif
