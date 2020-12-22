## Python backend

## Imports
import numpy as np ## array manipulations
import scipy.sparse ## scipy's SparseMatrix
from tqdm import tqdm ## for progress bar

def type_cast(array:np.array, type:str) -> np.array:
  '''
  casts numpy arrays into different type. If desired type not implementing, then original array is returned
  Parameters:
    - array: array to cast [numpy.array]
    - type: dtype to cast in. Implemented dtypes are [String]
      - int: Integer
      - float: Floats
      - double: Doubles
  '''
  if type == "int":
    return array.astype(np.int32)
  if type == "float":
    return array.astype(np.float)
  if type == "double":
    return array.astype(np.double)
  return array

def load_sparse_matrix(data_dir:str, name:str) -> (np.array, np.array, np.array, np.array):
  '''
  load data from given directory
  Parameters:
    - data_dir: path to folder with data [String]
    - name: start of filename [String]
  Returns:
    - data: array with values of SparseMatrix [numpy.array]
    - indices: array with indices of SparseMatrix [numpy.array]
    - indptr: array with index pointers of SparseMatrix [numpy.array]
    - shape: shape of SparseMatrix [numpy.array]
  '''
  indptr = np.load(f"{data_dir}/{name}_indptr.npy")
  indices = np.load(f"{data_dir}/{name}_indices.npy")
  data = np.load(f"{data_dir}/{name}_data.npy")
  shape = np.load(f"{data_dir}/{name}_shape.npy")
  indptr, indices, data = type_cast(indptr, "int"), type_cast(indices, "int"), type_cast(data, "double")
  return data, indices, indptr, shape

def to_sparse_matrix(data:np.array, indices:np.array, indptr:np.array, shape:np.array) -> object:
  '''
  makes SparseMatrix from given parameters
  Parameters:
    - data: array with values of SparseMatrix [numpy.array]
    - indices: array with indices of SparseMatrix [numpy.array]
    - indptr: array with index pointers of SparseMatrix [numpy.array]
    - shape: shape of SparseMatrix [numpy.array]
  Returns:
    - SparseMatrix: scipy.SparseMatrix [object]
  '''
  # Eigen provides a similar why to create a CSR view of these arrays, take a look at Eigen::Map< CSR Matrix >(...)
  return scipy.sparse.csr_matrix((data, indices, indptr), shape=shape, dtype=data.dtype)

def state_to_tuple(state:int, n_stars:int) -> (int, int, int):
  '''
  casts state to tuple with fuel, goal star and current star
  Parameters:
    - x: current state [Integer]
    - n_stars: number of stars [Integer]
  Returns:
    - f: fuel left [Integer]
    - g: goal star [Integer]
    - i: current star [Integer]
  '''
  f = state // (n_stars * n_stars)
  g = state % (n_stars * n_stars) // n_stars
  i = state % (n_stars * n_stars) % n_stars

  return f, g, i

def one_step_cost(state:int, control:int, n_stars:int) -> float:
  '''
  calculates cost for given state and action (=control)
  Parameters:
    - state: current state [Integer]
    - control: desired action to take [Integer]
    - n_stars: number of stars given [Integer]
  Returns:
    - cost: respective cost [Float]
  '''
  ## calculate fuel, goal star and current star from state
  f, g, i = state_to_tuple(state, n_stars)
  ## in goal and no jump
  if g == i and control == 0:
    return -100.0
  ## out of fuel
  if f == 0:
    return 100.0
  ## avoid unnecessary jumps
  if control > 0:
    return 5.0
  ## else no cost
  return 0.0

def one_step_lookahead(probabilities:object, state:int, V:np.array, nA:int, n_stars:int, alpha:float = 0.99) -> np.array:
  """
  Helper function to calculate the value for all action in a given state
  Parameters:
    - probabilities: SparseMatrix with all probabilities for all states and actions [object]
    - state: current state [Integer]
    - V: current values [numpy.array]
    - nA: number of theoretical possible actions [Integer]
    - n_stars: number of stars [Integer]
    - alpha: discount factor - between 0 and 1, close to 1 [Float]
  Returns:
    - A: cost array for all actions for this state [numpy.array]
  """
  ## init A as zero-array as long as actual possible actions for current state
  A = np.zeros(probabilities[state*nA : (state+1)*nA].nonzero()[0].__len__())
  ## go through all (action, next_state) pairs
  for action, next_state in zip(*probabilities[state*nA : (state+1)*nA].nonzero()):
    ## calculate reward
    reward = one_step_cost(state, action, n_stars)
    ## add respective costs to respective action
    A[action] += probabilities[state*nA+action, next_state] * (reward + alpha * V[next_state])
  return A

def async_vi(V:np.array, PI:np.array, values:np.array, indices:np.array, indptr:np.array, shape:np.array, n_stars:int, nS:int, nA:int, data_dir:str, recalc:bool = False) -> (np.array, np.array):
  """
  Same as in the C++ version, but using python
  Parameters:
    - V: value array [numpy.array]
    - PI: policy array [numpy.array]
    - values: values of SparseMatrix [numpy.array]
    - col_indices: column indices of SparseMatrix [numpy.array]
    - colptr: column pointers of SparseMatrix [numpy.array]
    - shape: shape of SparseMatrix [numpy.array]
    - n_stars: number of stars [Integer]
    - nS: number of states [Integer]
    - nA: number of actions [Integer]
    - data_dir: directory of data [String]
    - recalc: whether to calculate (=True) or laod (=False, default) policy and values [Boolean]
  Returns:
    - V: calculated values [numpy.array]
    - PI: calculated policy [numpy.array]
  """
  ## only do if results shall not be loaded but be recalculated
  if recalc:
    ## load probability SparseMatrix
    probabilities = to_sparse_matrix(values, indices, indptr, shape)
    ## init a tolerance (break if differences per iteration are below)
    tolerance = 1e-6
    ## init number of epochs to do
    epochs = int(1e3)
    ## init progress bar
    pbar = tqdm(total = epochs)
    for _ in range(epochs):
      ## reinit delta new for every epoch
      delta = 0
      ## go through all states
      for state in range(nS):
        ## calculate costs for this state
        A = one_step_lookahead(probabilities, state, V, nA, n_stars)
        ## calculate delta of new value for this state with existing one
        delta = max(delta, np.abs(np.min(A) - V[state]))
        ## set value and policy new
        V[state] = np.min(A)
        PI[state] = np.argmin(A)
      ## update progress bar
      pbar.set_description(f'Epoch: {_+1}; delta: {delta}')
      pbar.update(1)
      ## check if tolerance was already reached
      if delta <= tolerance:
        break
  ## load given results
  else:
      V = np.load(f"{data_dir}J_star_alpha_0_99_iter_1000.npy")  # Reference solution
      PI = np.load(f"{data_dir}pi_star_alpha_0_99_iter_1000.npy")  # Corresponding optimal policy

  return (V, PI)
