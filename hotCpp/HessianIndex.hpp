// A utility class to specially deal with sparse Hessian Computation.
// The idea is to first compute the entries along the diagnoal of the Hessian
// And then only computes the off-diag non-zero entries.
#include <vector>
#include <Matrix.hpp>

class HessianIndex {
 public:
  // The default ctor, will construction a full-Hessian
  HessianIndex(int dim);

  // Initialize the HessianIndex with the given sparsity pattern
  HessianIndex(int dim, int nnz, unsigned int* rind, unsigned int* cind);

  // Get Direction Count
  unsigned int getDirectionCount();

  // Get Seed Matrix
  Matrix<unsigned int> getSeedMatrix();

  // Set Taylor Coefficients
  void setTaylorCoefficients(const Matrix<double>& taylorCoefficients);

  std::vector<unsigned int> getRind();
  std::vector<unsigned int> getCind();

  // Get Gradient
  std::vector<double> getGradient();

  // Get Hessian
  std::vector<double> getHessian();

 private:
  void AppendDiagonal();
  void Append(unsigned int r, unsigned int c);

  int n;                             // The dim of the Hessian
  int offnnz;                        // # of non-zeros off-diagonal
  std::vector<unsigned int> rind;
  std::vector<unsigned int> cind;
  std::vector<double> taylorGradient;
  std::vector<double> taylorHessian;
};
