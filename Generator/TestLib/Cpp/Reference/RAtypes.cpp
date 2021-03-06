// This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
#include <iostream>
#include <cstdlib>
#include <cmath>
#include "RAtypes.hpp"

const unsigned int RAfloatS::arrSz;
RAfloatS::RAfloatS() {
  RAfloatS& l = *this;
  const float r = 0.0F;
  #include "RAasgnP.ipp"
}

void RAfloatS::set(const int& direction, const int& degree, const float& passive) {
  #include "RAset.ipp"
}

float RAfloatS::get(const int& direction, const int& degree) {
  float passive;
  #include "RAget.ipp"
  return passive;
}

const RAfloatS& RAfloatS::operator =(const int& r) {
  const RAfloatS& ret = *this;
  RAfloatS& l = *this;
  #include "RAasgnP.ipp"
  return ret;
}

const RAfloatS& RAfloatS::operator =(const float& r) {
  const RAfloatS& ret = *this;
  RAfloatS& l = *this;
  #include "RAasgnP.ipp"
  return ret;
}

RAfloatS::RAfloatS(const int& r) {
  const RAfloatS& ret = *this;
  RAfloatS& l = *this;
  #include "RAasgnP.ipp"
}

RAfloatS::RAfloatS(const float& r) {
  const RAfloatS& ret = *this;
  RAfloatS& l = *this;
  #include "RAasgnP.ipp"
}

void RAfloatS::toArray(float arr[RAfloatS::arrSz]) {
  RAfloatS& l = *this;
  arr[0] = l.v;
  #include "RAtoArray.ipp"
}

void RAfloatS::fromArray(float arr[RAfloatS::arrSz]) {
  RAfloatS& l = *this;
  l.v = arr[0];
  #include "RAfromArray.ipp"
}

const unsigned int RAfloatD::arrSz;
RAfloatD::RAfloatD() {
  RAfloatD& l = *this;
  const double r = 0.0;
  #include "RAasgnP.ipp"
}

void RAfloatD::set(const int& direction, const int& degree, const double& passive) {
  #include "RAset.ipp"
}

double RAfloatD::get(const int& direction, const int& degree) {
  double passive;
  #include "RAget.ipp"
  return passive;
}

const RAfloatD& RAfloatD::operator =(const RAfloatS& r) {
  const RAfloatD& ret = *this;
  RAfloatD& l = *this;
  #include "RAasgnA.ipp"
  return ret;
}

const RAfloatD& RAfloatD::operator =(const int& r) {
  const RAfloatD& ret = *this;
  RAfloatD& l = *this;
  #include "RAasgnP.ipp"
  return ret;
}

const RAfloatD& RAfloatD::operator =(const float& r) {
  const RAfloatD& ret = *this;
  RAfloatD& l = *this;
  #include "RAasgnP.ipp"
  return ret;
}

const RAfloatD& RAfloatD::operator =(const double& r) {
  const RAfloatD& ret = *this;
  RAfloatD& l = *this;
  #include "RAasgnP.ipp"
  return ret;
}

RAfloatD::RAfloatD(const RAfloatS& r) {
  const RAfloatD& ret = *this;
  RAfloatD& l = *this;
  #include "RAasgnA.ipp"
}

RAfloatD::RAfloatD(const int& r) {
  const RAfloatD& ret = *this;
  RAfloatD& l = *this;
  #include "RAasgnP.ipp"
}

RAfloatD::RAfloatD(const float& r) {
  const RAfloatD& ret = *this;
  RAfloatD& l = *this;
  #include "RAasgnP.ipp"
}

RAfloatD::RAfloatD(const double& r) {
  const RAfloatD& ret = *this;
  RAfloatD& l = *this;
  #include "RAasgnP.ipp"
}

void RAfloatD::toArray(double arr[RAfloatD::arrSz]) {
  RAfloatD& l = *this;
  arr[0] = l.v;
  #include "RAtoArray.ipp"
}

void RAfloatD::fromArray(double arr[RAfloatD::arrSz]) {
  RAfloatD& l = *this;
  l.v = arr[0];
  #include "RAfromArray.ipp"
}

float makeFPE(const float& n, const float& d) {
  float r;
  r = n / d;
  return r;
}

