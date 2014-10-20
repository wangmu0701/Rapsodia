// This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
#include <iostream>
#include <cstdlib>
#include <cmath>
#include "RAsub.hpp"

RAfloatS operator -(const RAfloatS& a, const RAfloatS& b) {
  RAfloatS r;
  #include "RAsubAA.ipp"
  return r;
}

RAfloatD operator -(const RAfloatS& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RAsubAA.ipp"
  return r;
}

RAfloatD operator -(const RAfloatD& a, const RAfloatS& b) {
  RAfloatD r;
  #include "RAsubAA.ipp"
  return r;
}

RAfloatD operator -(const RAfloatD& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RAsubAA.ipp"
  return r;
}

RAfloatS operator -(const RAfloatS& a, const int& b) {
  RAfloatS r;
  #include "RAsubAP.ipp"
  return r;
}

RAfloatS operator -(const RAfloatS& a, const float& b) {
  RAfloatS r;
  #include "RAsubAP.ipp"
  return r;
}

RAfloatD operator -(const RAfloatS& a, const double& b) {
  RAfloatD r;
  #include "RAsubAP.ipp"
  return r;
}

RAfloatD operator -(const RAfloatD& a, const int& b) {
  RAfloatD r;
  #include "RAsubAP.ipp"
  return r;
}

RAfloatD operator -(const RAfloatD& a, const float& b) {
  RAfloatD r;
  #include "RAsubAP.ipp"
  return r;
}

RAfloatD operator -(const RAfloatD& a, const double& b) {
  RAfloatD r;
  #include "RAsubAP.ipp"
  return r;
}

RAfloatS operator -(const int& a, const RAfloatS& b) {
  RAfloatS r;
  #include "RAsubPA.ipp"
  return r;
}

RAfloatD operator -(const int& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RAsubPA.ipp"
  return r;
}

RAfloatS operator -(const float& a, const RAfloatS& b) {
  RAfloatS r;
  #include "RAsubPA.ipp"
  return r;
}

RAfloatD operator -(const float& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RAsubPA.ipp"
  return r;
}

RAfloatD operator -(const double& a, const RAfloatS& b) {
  RAfloatD r;
  #include "RAsubPA.ipp"
  return r;
}

RAfloatD operator -(const double& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RAsubPA.ipp"
  return r;
}
