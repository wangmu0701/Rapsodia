// This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
#include <iostream>
#include <cstdlib>
#include <cmath>
#include "RAsqrt.hpp"

RAfloatS sqrt(const RAfloatS& a) {
  RAfloatS r;
  float recip;
  #include "RAsqrt.ipp"
  return r;
}

RAfloatD sqrt(const RAfloatD& a) {
  RAfloatD r;
  double recip;
  #include "RAsqrt.ipp"
  return r;
}
