//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#include <vector>
#include "RAinclude.ipp"

void head(const std::vector<RAfloatD>& x,
	  RAfloatD& y) { 
  y=sin(x[0])*sin(x[1])*sin(x[2]);
}
