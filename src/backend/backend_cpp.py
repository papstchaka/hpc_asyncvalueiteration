## C++ backend

## Imports
import numpy as np ## array manipulations
import os, logging ## operating system operations, logging
## init logger
_logger = logging.getLogger(__name__)

#######################
# Ugly Interface Part #
#######################

def _find_compile_output():
  """
  Returns all the files that belong to the compiled interface
  """
  def should_include(bar):
    """
    checks whether cpp_interface.cpp, cpp_interface.---.so and cpp_interface.o exist
    """
    return bar.startswith("cpp_interface") and bar.endswith((".cpp", ".o", ".so"))

  return [foo for foo in os.listdir(os.path.dirname(__file__)) if should_include(foo)]

def _compile_output_complete():
  """
  checks if exactly the desired 3 files exist
  """
  return len(_find_compile_output()) == 3

## if some compile issues occured
if not _compile_output_complete():
  ## give warning
  _logger.warning("Only parts of the expected compilation output are present. Trying to compile the c++ backend now.")
  ## this is the folder in which backend_cpp.py is located
  the_dir = os.path.dirname(__file__)
  ## these are created during the 'make install' step
  inc_dir = os.path.join(the_dir, 'inc')
  lib_dir = os.path.join(the_dir, 'lib')
  ## if one of the needed parts is missing or is empty
  if not os.path.exists(inc_dir) or not os.path.exists(lib_dir) or len(os.listdir(inc_dir)) == 0 or len(os.listdir(lib_dir)) == 0:
    raise ImportError("The include and/or library folder is not existing or empty, did you run 'make install'?")
  ## import compile_interface
  from .compile_interface import compile_interface
  ## we must change into the folder with the compile script, otherwise the include folder is at the wrong location
  ## use the location of this python script as "robust" change directory instruction
  os.chdir(the_dir)
  ## compile the interface
  compile_interface(verbose=True)
  ## now go back to the parent folder to not affect the remaining script
  ## since the working directory is now known it is enough to go one level up
  os.chdir("..")

## if some errors issues occured
if not _compile_output_complete():
  _logger.error("The expected compilation output is incomplete, stopping here!")
  raise ImportError("The compilation of the c++ python interface was not successful.")

try:
  ## this is the name we set in set_source(...), i.e. the first argument
  from . import cpp_interface
  from cffi import FFI

except (ModuleNotFoundError, ImportError) as e:
  _logger.error(f"Compiled interface is present, yet importing failed.\nReason:\n\n{e}\n\n")
  raise

## for casting the pointers
_ffi = FFI()

##########################################
# Now just the wrappers for the c++ code #
##########################################

def async_vi(V:np.array, PI:np.array, values:np.array, indices:np.array, indptr:np.array, shape:np.array, n_stars:int, nS:int, nA:int, data_dir:str) -> (np.array, np.array):
  """
  Same as in the python version, but using the C++ library
  Parameters:
    - V: value array [numpy.array]
    - PI: policy array [numpy.array]
    - values: values of SparseMatrix [numpy.array]
    - indices: column indices of SparseMatrix [numpy.array]
    - indptr: column pointers of SparseMatrix [numpy.array]
    - shape: shape of SparseMatrix [numpy.array]
    - n_stars: number of stars [Integer]
    - nS: number of states [Integer]
    - nA: number of actions [Integer]
    - data_dir: directory of data [String] - unused, only exists that call of python backend and cpp backend is the same!
  Returns:
    - V: calculated values [numpy.array]
    - PI: calculated policy [numpy.array]
  """
  ## these are the memory addresses of the numpy matrices
  ## yes, C-pointer in python! Print them to the console if you like ;)

  ## check dtypes of values, indptr and indices
  if values.dtype != np.double:
    raise TypeError("Datatype missmatch for values of probability matrix.")
  if indptr.dtype != indices.dtype != np.int:
    raise TypeError("Datatype missmatch for indptr and indices of probability matrix.")

  ## cast V, PI, values, indptr and indices to C pointers
  V_ptr = _ffi.cast("double*", V.ctypes.data)
  PI_ptr = _ffi.cast("double*", PI.ctypes.data)
  values_ptr = _ffi.cast("double*", values.ctypes.data)
  indices_ptr = _ffi.cast("int*", indices.ctypes.data)
  indptr_ptr = _ffi.cast("int*", indptr.ctypes.data)

  ## set rows and cols of SparseMatrix
  rows, cols = shape
  ## get number of non zeros in SparseMatrix
  nnz = values.__len__()
  ## run code
  cpp_interface.lib.cffi_async_vi(V_ptr, PI_ptr, values_ptr, indices_ptr, indptr_ptr, nnz, cols, rows, n_stars, nS, nA)
  return V, PI
