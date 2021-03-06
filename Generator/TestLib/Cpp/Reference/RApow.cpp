// This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
#include <iostream>
#include <cstdlib>
#include <cmath>
#include "RApow.hpp"

RAfloatD pow(const RAfloatD& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RApowAA.ipp"
  return r;
}

RAfloatD pow(const RAfloatD& a, const double& b) {
  RAfloatD r;
  double recip;
  RAfloatD s;
  RAfloatD t;
  int j;
  float expDiff;
  #include "RApowAP.ipp"
  return r;
}

RAfloatD pow(const double& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RApowPA.ipp"
  return r;
}

