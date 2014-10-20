#ifndef _RA_ADACC_H_
#define _RA_ADACC_H_
extern "C" {
int findTapLoc(location,int);
bool inActiveSource(location);
void pushTapeToGlobal(location,int);
int getSourceType(int);
void eliminateResiduals(location,location);
void eliminateResidual(location);
}
#endif
