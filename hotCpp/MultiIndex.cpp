//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#include <cassert>
#include <iostream>
#include <iomanip>
#include "MultiIndex.hpp"

#ifdef RA_DEBUG
  #define CHECKCOMPAT(a,b) assert ((a).myN == (b).myN)
  #define CHECKINDEX(a,i) assert ((a).myNumberOfIndices >= (i) && (i)!=0 )
#else
  #define CHECKCOMPAT(a,b) 
  #define CHECKINDEX(a,i) 
#endif


MultiIndex::MultiIndex() :
  myN(0),
  myD(0),
  myNumberOfIndices(0),
  myIndices(0,0),
  myStartPosition(0) { 
} 

MultiIndex::MultiIndex(unsigned short indexElements, 
		       unsigned short highestDegree,
		       unsigned int startPosition) :
  myN(indexElements),
  myD(highestDegree),
  myNumberOfIndices(computeIndexCount(myN,myD)),
  myIndices(myN,myNumberOfIndices),
  myStartPosition(startPosition) { 
  makeIndices();
} 

unsigned short MultiIndex::getNumberOfIndexElements() const { 
  return myN; 
} 

unsigned short MultiIndex::getDegree() const { 
  return myD; 
} 

unsigned int MultiIndex::getPosition(unsigned int i) const { 
  return myStartPosition+i-1;
} 

unsigned int MultiIndex::getIndexCount() const { 
  return myNumberOfIndices; 
} 

const Matrix<unsigned int>& MultiIndex::getIndices() const { 
  return myIndices;
} 


void MultiIndex::makeIndices() { 
  // we pick the Indexes each with d_i, i=1,.,myN
  // such that the sum over all d_i equals myD
  if (myN==1) { 
    myIndices[0][0]=myD;
  }
  else { 
    unsigned int currDir=1;
    for (unsigned int i=0; i<=myD; i++) { 
      for (unsigned int j=currDir;j<=currDir+computeIndexCount(myN-1,myD-i)-1;j++) { 
	myIndices[0][j-1]=i;
      }
      setLeadingDimension(myN-1,myD-i,currDir,2);
    }
  }
}

void MultiIndex::setLeadingDimension(unsigned short n,     // (current) number of index elements
				     unsigned short d,     // (current) highest  degree
				     unsigned int& currDir, // the current Index
				     unsigned short startRow ) { 
  if (n>1) { 
    for(unsigned int i=0;i<=d;i++){ 
      for (unsigned int j=currDir; j<=currDir+computeIndexCount(n-1,d-i)-1; j++) { 
	myIndices[startRow-1][j-1]=i;
      }
      setLeadingDimension(n-1,d-i,currDir,startRow+1);
    }
  }
  else { 
    myIndices[startRow-1][currDir-1]=d;
    currDir++;
  }
}
       
unsigned int MultiIndex::binomial(unsigned short a,
		      unsigned short b){ 
  unsigned int result=1;
  for (int i=1;i<=b;i++) { 
    result = (result *(a-i+1))/i; 
  }
  return result; 
}

double MultiIndex::binomial(unsigned short a,
			    double s,
			    unsigned short b) { 
  double sa=s*a;
  double result=1.0; 
  for (unsigned short i=1; i<=b; i++) { 
    result = (result *(sa-i+1))/i; 
  }
  return result; 
}

unsigned int MultiIndex::binomial(const MultiIndex& aMultiI1, 
				  unsigned int index1, 
				  const MultiIndex& aMultiI2, 
				  unsigned int index2) { 
  CHECKCOMPAT(aMultiI1,aMultiI2);
  CHECKINDEX(aMultiI1,index1);
  CHECKINDEX(aMultiI2,index2);
  unsigned int result=1;
  for (unsigned short i=1;i<=aMultiI1.myN; i++) { 
    result = result*binomial(aMultiI1.myIndices[i-1][index1-1],aMultiI2.myIndices[i-1][index2-1]);
  }
  return result; 
} 

double MultiIndex::binomial(const MultiIndex& aMultiI1, 
			    unsigned int index1, 
			    double s, 
			    const MultiIndex& aMultiI2, 
			    unsigned int index2) { 
  CHECKCOMPAT(aMultiI1,aMultiI2);
  CHECKINDEX(aMultiI1,index1);
  CHECKINDEX(aMultiI2,index2);
  double result=1.0;
  for (unsigned int i=1;i<=aMultiI1.myN; i++) { 
    result = result*binomial(aMultiI1.myIndices[i-1][index1-1],s,aMultiI2.myIndices[i-1][index2-1]);
  }
  return result; 
} 


unsigned int MultiIndex::L1_Norm(unsigned int index) const { 
  CHECKINDEX(*this,index);
  unsigned int result = 0;
  for(int i=1; i<=myN; i++) { 
    result = result + myIndices[i-1][index-1];
  }
  return result; 
}
  
unsigned int MultiIndex::L1_NormOfDifference(const MultiIndex& aMultiI1, 
				unsigned int  index1, 
				const MultiIndex& aMultiI2, 
				 unsigned int index2)  { 
  CHECKCOMPAT(aMultiI1,aMultiI2);
  CHECKINDEX(aMultiI1,index1);
  CHECKINDEX(aMultiI2,index2);
  unsigned int result=0;
  for(unsigned int i=1; i<=aMultiI1.myN; i++) { 
    result = result + aMultiI1.myIndices[i-1][index1-1]-aMultiI2.myIndices[i-1][index2-1];
  }
  return result; 
}
  
unsigned int MultiIndex::computeIndexCount(unsigned short indexElements, 
					     unsigned short highestDegree) { 
  return binomial(indexElements+highestDegree-1,highestDegree);
}

bool MultiIndex::lessThanOrEqual(const MultiIndex& aMultiI1, 
				 unsigned int  index1, 
				 const MultiIndex& aMultiI2, 
				 unsigned int index2) { 
  CHECKCOMPAT(aMultiI1,aMultiI2);
  CHECKINDEX(aMultiI1,index1);
  CHECKINDEX(aMultiI2,index2);
  for(unsigned short i=1; i<=aMultiI1.myN; i++) { 
    if (aMultiI1.myIndices[i-1][index1-1]>aMultiI2.myIndices[i-1][index2-1]) 
      return false;
  }
  return true; 
}
