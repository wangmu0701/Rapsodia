// This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
#include <iostream>
#include <cstdlib>
#include <cmath>
#include "RAtan.hpp"

RAfloatS tan(const RAfloatS& a) {
  RAfloatS r;
  #include "RAtan.ipp"
  return r;
}

RAfloatD tan(const RAfloatD& a) {
  RAfloatD r;
  #include "RAtan.ipp"
  return r;
}
