//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#include <vector>
#include <cmath>
#include <cassert>
#include <iostream>
#include <iomanip>
#include "RAinclude.ipp"
#include "HigherOrderTensor.hpp"

double explicitSinProdTensorEntry(unsigned short n,
				  std::vector<double> x,
				  std::vector<unsigned short> index) { 
  double result=1.0;
  for(unsigned short i=1; i<=n;i++) { 
    switch(index[i-1]%4) { 
    case (0) :
      result*=sin(x[i-1]);
      break; 
    case (1) :  
      result*=cos(x[i-1]);
      break; 
    case (2) :
      result*=(-sin(x[i-1])); 
      break;
    case (3) :
      result*=(-cos(x[i-1]));
      break;
    default : 
      assert(0);
      break;
    }
  }
  return result; 
}

int main() { 
  int rc=0;
  double myEps=1.0E-12;
  unsigned short  n,o;
  n=3;
  o=3;	
  HigherOrderTensor T(n,o); 
  int dirs=T.getDirectionCount();
  int i,j,k;
  // argument values
  std::vector<RAfloatD> x(n);
  std::vector<double> xv(n);
  for(i=1;i<=n;i++) { 
    xv[i-1]=1.0+.1*i;
    x[i-1]=xv[i-1];
  }
  // get the seed matrix
  Matrix<unsigned int> SeedMatrix=T.getSeedMatrix();
  for(i=1;i<=dirs;i++) { 
    for(j=1;j<=n;j++) { 
      x[j-1].set(i,1,SeedMatrix[j-1][i-1]);
    }
  }
  // compute the target function
  extern void head(const std::vector<RAfloatD>& x,
		   RAfloatD& y) ;
  RAfloatD y;
  head(x,y);
  // transfer the taylor coefficients
  Matrix<double> TaylorCoefficients(o,dirs);
  for(i=1;i<=o;i++) { 
    for(j=1;j<=dirs;j++) { 
      TaylorCoefficients[i-1][j-1]=y.get(j,i);
    }
  }
  T.setTaylorCoefficients(TaylorCoefficients);
  // harvest the compressedTensor
  for (k=1; k<=o; k++){ 
    std::cout << "order: " << k << std::endl;
    double entry=0.0;
    std::vector<double> compressedTensor=T.getCompressedTensor(k);
    HigherOrderTensor Helper(n,k); 
    dirs=Helper.getDirectionCount();
    // get the helper seed matrix
    Matrix<unsigned int> HelperSeedMatrix=Helper.getSeedMatrix();
    for(i=1;i<=dirs;i++) {
      std::vector<unsigned short> index(n);
      for(j=1;j<=n;j++) { 
	index[j-1]=HelperSeedMatrix[j-1][i-1];
      }
      entry=explicitSinProdTensorEntry(n,xv,index);
      std::cout << "T";
      for(j=1;j<=n;j++) { 
      std::cout << "[" << std::setw(2) << HelperSeedMatrix[j-1][i-1] << "]";
      }
      std::cout << compressedTensor[i-1] << " ?= " << entry ;
      if (fabs(compressedTensor[i-1]-entry)>myEps) { 
	std::cout << " diff is: " << fabs(compressedTensor[i-1]-entry);
        rc=1;
      } 
      else { 
        std::cout << " ok"; 
      }
      std::cout << std::endl;
    }
  }
  return rc;
}

