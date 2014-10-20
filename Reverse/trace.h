#ifndef __RA_TRACE_H__
#define __RA_TRACE_H__
#include "common.h"
extern "C" {
void printaddress_(location operand);

void dePushConstGlobal(location source);

void pushConstGlobalS(location);
void pushConstGlobalD(location);
void pushUnaryLocalSS(location, double, location);
void pushUnaryLocalSD(location, double, location);
void pushUnaryLocalDS(location, double, location);
void pushUnaryLocalDD(location, double, location);
void pushBinaryLocalSSS(location, double, location, double, location);
void pushBinaryLocalSSD(location, double, location, double, location);
void pushBinaryLocalSDS(location, double, location, double, location);
void pushBinaryLocalSDD(location, double, location, double, location);
void pushBinaryLocalDSS(location, double, location, double, location);
void pushBinaryLocalDSD(location, double, location, double, location);
void pushBinaryLocalDDS(location, double, location, double, location);
void pushBinaryLocalDDD(location, double, location, double, location);
}


#endif
