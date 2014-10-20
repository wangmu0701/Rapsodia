//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#include "Matrix.hpp"

class MultiIndex { 

public: 
  
  MultiIndex(); 

  MultiIndex(unsigned short indexElements, 
	     unsigned short highestDegree,
	     unsigned int startPosition); 

  unsigned short getNumberOfIndexElements() const;
  unsigned short getDegree() const; 

  /**
   * gives the position in the vector of 
   * all MultiIndex instances
   */
  unsigned int getPosition(unsigned int i) const;
  unsigned int getIndexCount() const;

  typedef Matrix<unsigned int> IndexMatrix;

  /**
   * for regression testing only 
   */
  const IndexMatrix& getIndices() const; 

  static unsigned int binomial(unsigned short a,
			       unsigned short b);
  static double binomial(unsigned short a,
			 double s,
			 unsigned short b); 
  static unsigned int binomial(const MultiIndex& aMultiI1, 
			       unsigned int index1, 
			       const MultiIndex& aMultiI2, 
			       unsigned int index2);
  static double binomial(const MultiIndex& aMultiI1, 
			 unsigned int index1, 
			 double s, 
			 const MultiIndex& aMultiI2, 
			 unsigned int index2); 
  static unsigned int computeIndexCount(unsigned short indexElements, 
					unsigned short highestDegree);
  unsigned int L1_Norm(unsigned int index) const; 

  static unsigned int L1_NormOfDifference(const MultiIndex& aMultiI1, 
					  unsigned int  index1, 
					  const MultiIndex& aMultiI2, 
					  unsigned int index2);
  
  static bool lessThanOrEqual(const MultiIndex& aMultiI1, 
			      unsigned int  index1, 
			      const MultiIndex& aMultiI2, 
			      unsigned int index2); 
  
private: 
  // number of index elements
  unsigned short myN;
  // highest  index degree
  unsigned short myD;
  // number of Indices,
  // this is set when we make the indices
  unsigned int myNumberOfIndices;
  // index matrix (myN,myNumberOfIndices)
  IndexMatrix myIndices;
  // index starting position from which we get the position
  unsigned int myStartPosition;

  
  void makeIndices();
 
  void setLeadingDimension(unsigned short n,
			   unsigned short d,
			   unsigned int& currDir,
			   unsigned short startRow);
  
  bool mydebugFlag;

};
