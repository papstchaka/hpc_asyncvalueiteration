// Interface C code for CFFI ...

// Imports
#include "Async_VI.h"

extern "C"
{
  extern void cffi_async_vi(float* V, int* PI, float* values, int* row_indices, int* rowptr, const unsigned int nnz, const unsigned int cols, const unsigned int rows, const unsigned int n_stars, const unsigned int nS, const unsigned int nA)
  {
    // No C++ in here, but namespaces work in external C linkage
    // But only from C++ -> C direction, don't try to define new namespaces inside this C realm
    Backend::async_vi(V, PI, values, row_indices, rowptr, nnz, cols, rows, n_stars, nS, nA);
  }
}
