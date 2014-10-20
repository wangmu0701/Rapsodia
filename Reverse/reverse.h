#ifndef __RA_REVERSE_H__
#define __RA_REVERSE_H__
#include "common.h"
#include "trcodes.h"

//The only two functions that the user may explicitly call
extern "C" {
void revOn();
void revOff();
void revStart();
void revStop();
void reduction();
void preAcc();
}
#ifdef FAST_MODE_D
#include "RA_adacc_d.h"
#endif

#ifndef FAST_MODE_D
#include "RA_adacc.h"
#endif
#endif

