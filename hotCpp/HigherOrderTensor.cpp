//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#include <iostream>
#include <cmath>
#include <cassert>
#include "HigherOrderTensor.hpp"

HigherOrderTensor::HigherOrderTensor(unsigned short indepCount,
				     unsigned short highestDegree) : 
  myN(indepCount),
  myD(highestDegree),
  myNumberOfDirections(MultiIndex::computeIndexCount(myN,myD)),
  myTaylorCoefficients(myD,myNumberOfDirections),
  myInterpolationCoefficients(totalIndexCount(myN,myD),myNumberOfDirections){
  makeMultiIndices();
  makeInterpolationCoefficients();
}

unsigned int HigherOrderTensor::totalIndexCount(unsigned short indepCount,
						unsigned short highestDegree) { 
  unsigned int result=0;
  for (unsigned short i=1; i<=highestDegree; i++) 
    result+=MultiIndex::computeIndexCount(indepCount,i);
  return result;
}

unsigned short HigherOrderTensor::getNumberOfIndependents()const { 
  return myN; 
} 

unsigned short HigherOrderTensor::getHighestDerivativeDegree() const {
  return myD; 
}

void HigherOrderTensor::setTaylorCoefficients(const Matrix<double>& taylorCoefficients) {
  if (myD!=taylorCoefficients.size()) { 
    std::cerr << "HigherOrderTensor::setTaylorCoefficients: expect " << myD << " rows in taylorCoefficients" << std::endl; 
    assert(0);
  }
  if (myD && taylorCoefficients[0].size()!=myNumberOfDirections) {
    std::cerr << "HigherOrderTensor::setTaylorCoefficients: expect " << myNumberOfDirections << " columns in taylorCoefficients" << std::endl; 
    assert(0);
  }
  for (unsigned int i=1; i<=myD; i++ ) { 
    std::vector<double>& target=myTaylorCoefficients[i-1];
    const std::vector<double>& source=taylorCoefficients[i-1];
    for (unsigned int j=1; j<=myNumberOfDirections; j++ ) { 
      target[j-1]=source[j-1];
    }
  }
} 

std::vector<double> HigherOrderTensor::getCompressedTensor(unsigned short tensorOrder) const { 
  std::vector<double> compressedTensor(myMultiIndices[tensorOrder-1].getIndexCount());
  for (unsigned int i=1;i<=myMultiIndices[tensorOrder-1].getIndexCount(); i++) { 
    compressedTensor[i-1]=0.0;
    for (unsigned int j=1;j<=myMultiIndices[myD-1].getIndexCount();j++) { 
      compressedTensor[i-1]+=
	myTaylorCoefficients[tensorOrder-1][j-1] * 
	myInterpolationCoefficients[myMultiIndices[tensorOrder-1].getPosition(i)-1][j-1];
    }
  }
  return compressedTensor;
} 

Matrix<unsigned int> HigherOrderTensor::getSeedMatrix() const { 
  return myMultiIndices[myD-1].getIndices();
}

void HigherOrderTensor::makeMultiIndices() { 
  myIndexCounter=1;
  // we pick the directions each with d_i, i=1,.n
  // such that the sum over all d_i equals d
  for (unsigned short i=1; i<=myD; i++ ) { 
    myMultiIndices.push_back(MultiIndex(myN,i,myIndexCounter));
    myIndexCounter+=myMultiIndices[i-1].getIndexCount();
  }
}

void HigherOrderTensor::makeInterpolationCoefficients() { 
  float factor;
  unsigned int l1Ofk;
  double coefficient;
  for(unsigned short id=1; id<=myD; id++) { 
    for(unsigned short in=1;in<=myMultiIndices[id-1].getIndexCount(); in++) { 
      for(unsigned short j=1; j<=myMultiIndices[myD-1].getIndexCount(); j++) { 
	// now do the loop for the sum where
	// we need to find all the kd/kn indices smaller than the id/in index
	coefficient=0.0;
	for(unsigned short kd=1; kd<=id; kd++) { 
	  for(unsigned short kn=1; kn<=myMultiIndices[kd-1].getIndexCount(); kn ++) { 
	    // obviously we still need to check <=
	    if (MultiIndex::lessThanOrEqual(myMultiIndices[kd-1],kn,myMultiIndices[id-1],in)) {
	      l1Ofk=myMultiIndices[kd-1].L1_Norm(kn);
	      if (MultiIndex::L1_NormOfDifference(myMultiIndices[id-1],
						  in,
						  myMultiIndices[kd-1],
						  kn)
		  %2==0) { 
		factor=1.0;
	      }
	      else { 
		factor=-1.0;
	      }
              int l1=myMultiIndices[id-1].L1_Norm(in);
	      coefficient+= (factor *  // need to avoid the unsigned vs signed overflow mess
		MultiIndex::binomial(myMultiIndices[id-1],in,
				     myMultiIndices[kd-1],kn))* 
		MultiIndex::binomial(myMultiIndices[kd-1],kn,
				     ((myD*1.0)/(l1Ofk*1.0)),
				     myMultiIndices[myD-1],j) * 
		pow(((l1Ofk*1.0)/(myD*1.0)),l1);
	    }
	  }
	}
	myInterpolationCoefficients[myMultiIndices[id-1].getPosition(in)-1][j-1]=coefficient;
      }
    }
  }
}
       
unsigned int HigherOrderTensor::getDirectionCount() const { 
  return myNumberOfDirections;
}

const std::vector<MultiIndex>& HigherOrderTensor::getMultiIndices() const { 
  return myMultiIndices;
}

const Matrix<double>& HigherOrderTensor::getInterpolationCoefficients() const { 
  return myInterpolationCoefficients;
}
