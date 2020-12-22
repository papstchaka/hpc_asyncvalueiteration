## Test program. Tests whether C++ backend is available and whether it is working correctly (same as python backend)

## Imports
import numpy as np ## array manipulations
import pytest, pickle ## for testing / data loading
import importlib.util ## to be able to load backend package from different folder source
spec = importlib.util.spec_from_file_location("*", "backend/backend_py.py") ## load python backend from backend folder
b = importlib.util.module_from_spec(spec) ## import backend
spec.loader.exec_module(b) ## import backend
from backend import * ## import both backends

def test_cpp_backend_active():
  """
  Tests, whether the C++ backend is running
  """
  assert backend is not backend_py, "The C++ Backend is not active, you are testing the functions with themself!"
  return

def test_cpp_implement():
  """
  Tests, whether the async_vi steps matches between Python and C++
  """
  ## data source folder
  data_dir = "data/data_debug/"
  ## load values, indices and indptr of respective data
  values, indices, indptr, shape = b.load_sparse_matrix(data_dir, "P")
  ## load all other parameters
  with open(f"{data_dir}parameters.pickle", "rb") as the_file:
    parameters = pickle.load(the_file)
  ## set number of states, actions and stars
  nS, nA = parameters["NS"], parameters["max_controls"]
  n_stars = parameters["number_stars"]
  ## init Values and Policy
  V = np.zeros(nS)
  PI = np.zeros(nS)
  ## copy to avoid call by reference issue
  v_py, pi_py = backend_py.async_vi(V.copy(), PI.copy(), values, indices, indptr, shape, n_stars, nS, nA, data_dir)
  v_cpp, pi_cpp = backend.async_vi(V.copy(), PI.copy(), values, indices, indptr, shape, n_stars, nS, nA, data_dir)
  ## check if results are matching
  assert (pi_py - pi_cpp).sum() == 0, "policy mismatch"
  assert (v_py - v_cpp).sum() < 100, "value mismatch"

  return
