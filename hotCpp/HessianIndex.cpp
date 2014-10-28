#include "HessianIndex.hpp"

void HessianIndex::Append(unsigned int r, unsigned int c) {
  rind.push_back(r);
  cind.push_back(c);
}

void HessianIndex::AppendDiagonal() {
  for(unsigned int i = 0; i < n; i++) {
    Append(i,i);
  }
}

HessianIndex::HessianIndex(int dim) {
  n = dim;
  offnnz = (n*(n-1))/2;
  AppendDiagonal();
  for(unsigned int i = 0; i < n; i++) {
    for(unsigned int j = 0; j < i; j++) {
      Append(i,j);
    }
  }
}

HessianIndex::HessianIndex(int dim,
                           int nnz,
                           unsigned int* r,
                           unsigned int* c) {
  n = dim;
  offnnz = 0;
  AppendDiagonal();
  for(int i = 0; i < nnz; i++) {
    if (r[i] != c[i]) {  // Ignore diagonal entries, we'll do them anyway
      offnnz++;
      if (r[i] > c[i]){
        Append(r[i],c[i]);
      } else {
        Append(c[i],r[i]);
      }
    }
  }
}

unsigned int HessianIndex::getDirectionCount() {
  return n + offnnz;
}

Matrix<unsigned int> HessianIndex::getSeedMatrix() {
  Matrix<unsigned int> ret(n, n+offnnz);
  // Assign diagonal
  for(unsigned int i = 0; i < n+offnnz; i++) {
  }
  for(unsigned int i = 0; i < n; i++) {
    ret[i][i] = 1;
  }
  for(unsigned int i = n; i < n + offnnz; i++) {
    ret[rind[i]][i] = 1;
    ret[cind[i]][i] = 1;
  }
  return ret;    
}

void HessianIndex::setTaylorCoefficients(const Matrix<double>& taylorCoefficients) {
// Gradient
  for(unsigned int i = 0; i < n; i++) {
    taylorGradient.push_back(taylorCoefficients[0][i]);
  }
// Hessian
  for(unsigned int i = 0; i < n + offnnz; i++) {
    taylorHessian.push_back(taylorCoefficients[1][i]);
  }
}

std::vector<unsigned int> HessianIndex::getRind() {
  return rind;
}

std::vector<unsigned int> HessianIndex::getCind() {
  return cind;
}

std::vector<double> HessianIndex::getGradient() {
  std::vector<double> ret(taylorGradient);
  return ret;
}

std::vector<double> HessianIndex::getHessian() {
  double value;
  std::vector<double> ret;
  for(unsigned int i = 0; i < n; i++) {
    ret.push_back(taylorHessian[i]*2);
  }
  for(unsigned int i = n; i < n + offnnz; i++) {
    value = taylorHessian[i] - taylorHessian[rind[i]] - taylorHessian[cind[i]];
    ret.push_back(value);
  }
  return ret;
}
