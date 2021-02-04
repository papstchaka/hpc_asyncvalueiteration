// C++ header for asynchronous value iteration
#ifndef _ASYNC_VI_H_
#define _ASYNC_VI_H_
#define EIGEN_USE_BLAS
#define EIGEN_USE_LAPACKE
// Imports
#include "Eigen/Sparse" // for SparseMatrix manipulations
#include "Eigen/Dense" // for vector manipulations
#include <omp.h> // for OpenMP (parallelization)

// typedef's to save some time while coding
typedef Eigen::SparseMatrix<float, Eigen::RowMajor> SpMat;
typedef Eigen::VectorXf vecF; // Standard Vector for Floats
typedef Eigen::VectorXi vecI; // Standard Vector for Integers

namespace Backend
{
  /**
   * Helper function to calculate the value for all action in a given state
   * @param probabilities: SparseMatrix with all probabilities for all states and actions [SpMat]
   * @param state: current state [Integer]
   * @param V: current values [vecF]
   * @param nA: number of theoretical possible actions [const unsigned integer]
   * @param n_stars: number of stars [const unsigned integer]
   * @param alpha: discount factor - between 0 and 1, close to 1 [const float]
   * @return A: cost array for all actions for this state [vec]
   */
  vecF one_step_lookahead(SpMat probabilities, int state, vecF V, const unsigned int nA, const unsigned int n_stars, const float alpha);

  /**
   * Same as in the Python version, but using C++
   * @param V: value array [vecF]
   * @param PI: policy array [vecI]
   * @param probabilities: SparseMatrix with all probabilities for all states and actions [SpMat]
   * @param n_stars: number of stars [const unsigned integer]
   * @param nS: number of states [const unsigned integer]
   * @param nA: number of actions [const unsigned integer]
   */
  void async_vi(Eigen::Ref<vecF> V, Eigen::Ref<vecI> PI, const Eigen::Ref<SpMat> probabilities, const int n_stars, const unsigned int nS, const unsigned int nA);

  /**
   * overloads async_vi to initialize the data
   * @param V: float pointer of value array [float*]
   * @param PI: int pointer of policy array [integer*]
   * @param values: float pointer of values of SparseMatrix [float*]
   * @param row_indices: int pointer of column indices of SparseMatrix [int*]
   * @param rowptr: int pointer of column pointers of SparseMatrix [int*]
   * @param nnz: number of non-zero elements of SparseMatrix [const unsigned integer]
   * @param cols: number of cols of SparseMatrix [const unsigned integer]
   * @param rows: number of rows of SparseMatrix [const unsigned integer]
   * @param n_stars: number of stars [const unsigned integer]
   * @param nS: number of states [const unsigned integer]
   * @param nA: number of actions [const unsigned integer]
   *
   * \overload
   */
  void async_vi(float* V, int* PI, float* values, int* row_indices, int* rowptr, const unsigned int nnz, const unsigned int cols, const unsigned int rows, const unsigned int n_stars, const unsigned int nS, const unsigned int nA);
}

#endif
