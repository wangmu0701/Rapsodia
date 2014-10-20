// This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
#include <iostream>
#include <cstdlib>
#include <cmath>
#include "RAexp.hpp"

RAfloatS exp(const RAfloatS& a) {
  RAfloatS r;
  RAfloatS s;
  RAfloatS t;
  #include "RAexp.ipp"
  return r;
}

RAfloatD exp(const RAfloatD& a) {
  RAfloatD r;
  RAfloatD s;
  RAfloatD t;
  #include "RAexp.ipp"
  return r;
}

