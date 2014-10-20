//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#include <iostream>
#include <cmath>

#include "RAinclude.ipp"


int main(void){
  int rc=0;
  const int directions=2;
  const int order=10;

  int testCase;
  bool done, dumpedTestLine;
  double xCoeff[directions][order],yCoeff[directions][order];
  RAfloatD  x,y;
  double xp,yp, myEps=1.E-13;
  const char* testLine;
  int i,j;
  
  // the point at which we test
  xp=0.3;
  
  // keep the coefficient values for comparison
  for( i=0;i<directions;i++) { 
    for( j=0;j<order; j++) { 
      xCoeff[i][j]=0.0;
    }
    xCoeff[i][1]=i*0.3;
  }
 
  // initialize the active input
  x=xp;
  for( i=0;i<directions;i++) { 
    for( j=0;j<order; j++) { 
      x.set(i+1,j+1,xCoeff[i][j]);
    }
  } 

  // populate the coefficients
  // with something nontrivial
  x=asin(x);

  done=false;
  testCase=0;

  
  // run the identities
  while (!done) { 
    switch(testCase) { 
    case 0:
      y=x;
      testLine="y=x";
      break;
    case 1: 
      y=x+x-x;
      testLine="y=x+x-x";
      break;
    case 2:
      y=-2+(2+((x+2)-2));
      testLine="y=-2+(2+((x+2)-2))";
      break;
    case 3:
      y=(2*x)/2;
      testLine="y=(2*x)/2";
      break;
    case 4:
      y=(x*x)/x;
      testLine="y=(x*x)/x";
      break;
    case 5:
      y=sqrt(x*x);
      testLine="y=sqrt(x*x)";
      break;
    case 6:
      y=sqrt(pow(x,2));
      testLine="y=sqrt(pow(x,2))";
      break;
    case 7:
      y=log(exp(x));
      testLine="y=log(exp(x))";
      break;
    case 8:
      y=pow(pow(x,2),.5);
      testLine="y=pow(pow(x,2),.5)";
      break;
    case 9:
      y=pow(pow(x,3),1.0/3.0);
      testLine="y=pow(pow(x,3),1.0/3.0)";
      break;
    case 10:
      y=atan(tan(x));
      testLine="y=atan(tan(x))";
      break;
    case 11:
      y=(-x)*(-1.0);
      testLine="y=(-x)*(-1.0);";
      break;
    case 12:
      y=0.0;
      y+=2*x;
      y-=x;
      testLine="y+=2*x;y-=x";
      break;
    case 13:
      y=0.0;
      y+=x;
      y*=x;
      y/=x;
      testLine="y+=x;y*=x;y/=x";
      break;
    default:
      done=true;
      break;
    }
    if (!done) { 
      y=sin(y);
      dumpedTestLine=false;
      // test the value: 
      if (fabs(y.v-xp)>myEps) { 
	if (!dumpedTestLine) {
	  std::cout << "deviation for " <<  testLine << std::endl; 
	  dumpedTestLine=true;
	}
	std::cout << " y.v=" << y.v << " x.v=" << xp << " diff: " <<  fabs(y.v-xp) << std::endl;
        rc=1; 
      }
      // test the coefficients
      for( i=0;i<directions;i++) { 
	for( j=0;j<order; j++) { 
	  yCoeff[i][j]=y.get(i+1,j+1);
	  if (fabs(yCoeff[i][j]-xCoeff[i][j])>myEps) { 
	    if (!dumpedTestLine) {
	      std::cout << "deviation for " <<  testLine << std::endl; 
	      dumpedTestLine=true;
	    }
	    std::cout << " y[" << i << "][" << j << "]=" << yCoeff[i][j] << " x[" << i << "][" << j << "]=" << xCoeff[i][j] << " diff: " << fabs(yCoeff[i][j]-xCoeff[i][j]) << std::endl; 
            rc=1;
	  }
	}
      }
      if (!dumpedTestLine) {
	std::cout << "test " << testLine << " ok" << std::endl; 
      }
    }
    testCase=testCase+1;
  }
  return rc;
}
