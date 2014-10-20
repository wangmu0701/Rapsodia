//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************

/**
 *  \mainpage Rapsodia (hotCpp)
 *  \author Isabelle Charpentier and Jean Utke
 *    
 *  \section intro Introduction
 *  
 * Rapsodia = <b>rap</b>ide <b>s</b>urcharge d'<b>o</b>p&eacute;rateur pour la <b>di</b>ff&eacute;rentiation <b>a</b>utomatique.
 *
 * hotCpp   = <b>h</b>igher-<b>o</b>rder <b>t</b>ensor interpolation implemented in <b>C++</b>
 *
 * hotF90   = <b>h</b>igher-<b>o</b>rder <b>t</b>ensor interpolation implemented in <b>F90</b>
 * 
 * Rapsodia is a tool for the efficient computation of higher order derivative tensors. 
 * It consists of two parts. 
 * <ol>
 * <li> A Python-based generator producing C++ or Fortran code for the forward propagation  of univariate Taylor polynomials.
 * This code yields efficiency gains via explcitly unrolled loops for a fixed derivative order and number of directions.
 *
 * <li> Implementations of the algorithm to interpolate derivative tensor entries from univariate 
 * Taylor coefficients in C++ and Fortran  
 * </ol> 
 * This part of the documentation covers the C++ implementation of the higher-order tensor interpolation.
 */

#include <vector>
#include "MultiIndex.hpp"

  /** 
   *  top level class for higher-order tensor interpolation
   */
class HigherOrderTensor { 

public : 

  /** 
   * create a class instance for 
   * \param indepCount to initialize HigherOrderTensor::myN
   * \param highestDegree to initialize HigherOrderTensor::myD
   */
  HigherOrderTensor(unsigned short indepCount,
		    unsigned short highestDegree); 

  /**
   * returns HigherOrderTensor::myN
   */
  unsigned short getNumberOfIndependents() const; 

  /**
   * returns HigherOrderTensor::myD
   */
  unsigned short getHighestDerivativeDegree() const; 

  /** 
   * get the number of columns in the  seed matrix 
   * for HigherOrderTensor::myN inputs and HigherOrderTensor::myD degree
   */
  unsigned int getDirectionCount() const; 

  /** 
   * get the seed matrix for HigherOrderTensor::myN inputs and HigherOrderTensor::myD degree
   */
  Matrix<unsigned int> getSeedMatrix() const; 

  /** 
   * supply the computed output coefficients to the interpolation 
   * \param taylorCoefficients the output coefficients are to be ordered 
   * as a matrix that has HigherOrderTensor::myNumberOfDirections columns 
   * and HigherOrderTensor::myD rows
   */
  void setTaylorCoefficients(const Matrix<double>& taylorCoefficients); 

  /**
   * the interpolated entries 
   * \param tensorOrder the given order (less than or equal to HigherOrderTensor::myD)
   * compressed into a vector
   * each vector element has an index corresponding to 
   * a column index in the seed matrix made for the given tensorOrder 
   */
  std::vector<double> getCompressedTensor(unsigned short tensorOrder) const; 

  /** 
   * the number of indices over all derivative degrees up tp HigherOrderTensor::myD
   */
  static unsigned int totalIndexCount(unsigned short indepCount,
				      unsigned short highestDegree); 

  const std::vector<MultiIndex>& getMultiIndices() const; 

  const Matrix<double>& getInterpolationCoefficients() const;

 
private: 

  void makeMultiIndices();
  void makeInterpolationCoefficients();

  /** 
   * indep number
   */
  unsigned short myN;

  /** 
   * highest derivative degree
   */
  unsigned short myD; 

  /** 
   * number of directions
   */
  unsigned int myNumberOfDirections;

  /** 
   * all the multiIndices up to degree HigherOrderTensor::myD
   */
  std::vector<MultiIndex>  myMultiIndices;

  /** 
   * taylor coefficients computed by the user
   * first dimension is HigherOrderTensor::myD
   * second dimension is HigherOrderTensor::myNumberOfDirections
   */
  Matrix<double> myTaylorCoefficients;

  /** 
   *interpolation coefficients (computed once by HigherOrderTensor::makeInterpolationCoefficients)
   */
  Matrix<double> myInterpolationCoefficients;

  /** 
   * total index counter
   */
  unsigned int myIndexCounter;

};
