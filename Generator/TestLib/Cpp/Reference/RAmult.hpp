// This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
#ifndef _RAmult_INCLUDE_
#define _RAmult_INCLUDE_
  #include "RAprec.hpp"
  #include "RAtypes.hpp"
  RAfloatS operator *(const RAfloatS& a, const RAfloatS& b);
  RAfloatD operator *(const RAfloatS& a, const RAfloatD& b);
  RAfloatD operator *(const RAfloatD& a, const RAfloatS& b);
  RAfloatD operator *(const RAfloatD& a, const RAfloatD& b);
  RAfloatS operator *(const RAfloatS& a, const int& b);
  RAfloatS operator *(const RAfloatS& a, const float& b);
  RAfloatD operator *(const RAfloatS& a, const double& b);
  RAfloatD operator *(const RAfloatD& a, const int& b);
  RAfloatD operator *(const RAfloatD& a, const float& b);
  RAfloatD operator *(const RAfloatD& a, const double& b);
  RAfloatS operator *(const int& a, const RAfloatS& b);
  RAfloatD operator *(const int& a, const RAfloatD& b);
  RAfloatS operator *(const float& a, const RAfloatS& b);
  RAfloatD operator *(const float& a, const RAfloatD& b);
  RAfloatD operator *(const double& a, const RAfloatS& b);
  RAfloatD operator *(const double& a, const RAfloatD& b);
#endif
