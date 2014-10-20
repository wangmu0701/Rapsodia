#ifndef _RA_ADACC_D_H_
#define _RA_ADACC_D_H_
extern "C" {
int findTapLoc(location);
bool inActiveSource(location);
void globalReduction();
void pushTapeToGlobal(location);
void eliminateResiduals(location,location);
void eliminateResidual(location);
}
#endif
