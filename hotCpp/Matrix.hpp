//*********************************************************
// This file is part of Rapsodia released under the LGPL. *
// The full COPYRIGHT notice can be found in the top      *
// level directory of the Rapsodia distribution           *
//*********************************************************
#include <vector>

// very simple matrix template
template <class T> class Matrix : public std::vector<std::vector<T> > {
public: 
  Matrix(unsigned int r,
	 unsigned int c) : 
    std::vector<std::vector<T> >(r,std::vector<T>(c)),
    myR(r),
    myC(c) { 
  };

  Matrix(unsigned int r,
	 unsigned int c,
	 T v) : 
    std::vector<std::vector<T> >(r,std::vector<T>(c,v)) ,
    myR(r),
    myC(c) {
  };

  unsigned int r() const {return myR;}; 
  unsigned int c() const {return myC;}; 
  
private: 
  unsigned int myR;
  unsigned int myC;

};
