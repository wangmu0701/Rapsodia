// This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
#include <iostream>
#include <cstdlib>
#include <cmath>
#include "RAacos.hpp"

RAfloatS acos(const RAfloatS& a) {
  RAfloatS r;
  RAfloatS h;
  RAfloatS t;
  #include "RAacos.ipp"
  return r;
}

RAfloatD acos(const RAfloatD& a) {
  RAfloatD r;
  RAfloatD h;
  RAfloatD t;
  #include "RAacos.ipp"
  return r;
}
