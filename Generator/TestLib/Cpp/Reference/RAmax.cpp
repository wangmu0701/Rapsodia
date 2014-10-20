// This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
#include <iostream>
#include <cstdlib>
#include <cmath>
#include "RAmax.hpp"

RAfloatS max(const RAfloatS& a, const RAfloatS& b) {
  RAfloatS r;
  #include "RAmaxAA.ipp"
  return r;
}

RAfloatD max(const RAfloatS& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RAmaxAA.ipp"
  return r;
}

RAfloatD max(const RAfloatD& a, const RAfloatS& b) {
  RAfloatD r;
  #include "RAmaxAA.ipp"
  return r;
}

RAfloatD max(const RAfloatD& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RAmaxAA.ipp"
  return r;
}

RAfloatS max(const RAfloatS& a, const int& b) {
  RAfloatS r;
  #include "RAmaxAP.ipp"
  return r;
}

RAfloatS max(const RAfloatS& a, const float& b) {
  RAfloatS r;
  #include "RAmaxAP.ipp"
  return r;
}

RAfloatD max(const RAfloatS& a, const double& b) {
  RAfloatD r;
  #include "RAmaxAP.ipp"
  return r;
}

RAfloatD max(const RAfloatD& a, const int& b) {
  RAfloatD r;
  #include "RAmaxAP.ipp"
  return r;
}

RAfloatD max(const RAfloatD& a, const float& b) {
  RAfloatD r;
  #include "RAmaxAP.ipp"
  return r;
}

RAfloatD max(const RAfloatD& a, const double& b) {
  RAfloatD r;
  #include "RAmaxAP.ipp"
  return r;
}

RAfloatS max(const int& a, const RAfloatS& b) {
  RAfloatS r;
  #include "RAmaxPA.ipp"
  return r;
}

RAfloatD max(const int& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RAmaxPA.ipp"
  return r;
}

RAfloatS max(const float& a, const RAfloatS& b) {
  RAfloatS r;
  #include "RAmaxPA.ipp"
  return r;
}

RAfloatD max(const float& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RAmaxPA.ipp"
  return r;
}

RAfloatD max(const double& a, const RAfloatS& b) {
  RAfloatD r;
  #include "RAmaxPA.ipp"
  return r;
}

RAfloatD max(const double& a, const RAfloatD& b) {
  RAfloatD r;
  #include "RAmaxPA.ipp"
  return r;
}
