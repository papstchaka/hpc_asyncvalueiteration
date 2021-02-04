## Script to calculate the policy via C++ with bigger datasets

## Imports
import numpy as np ## array manipulations
import pickle ## for data loading
import importlib.util ## to be able to load backend package from different folder source
spec = importlib.util.spec_from_file_location("*", "backend/backend_py.py") ## load python backend from backend folder
b = importlib.util.module_from_spec(spec) ## import backend
spec.loader.exec_module(b) ## import backend
from backend import * ## import both backends
from data_demonstration import *

def run():
    '''
    runs the code
    '''
    ## data source folder
    data_dir = "data/data_small/"
    ## load values, indices and indptr of respective data
    values, indices, indptr, shape = b.load_sparse_matrix(data_dir, "P")
    ## load all other parameters
    with open(f"{data_dir}parameters.pickle", "rb") as the_file:
        parameters = pickle.load(the_file)
    ## set number of states, actions and stars
    nS, nA = parameters["NS"], parameters["max_controls"]
    n_stars = parameters["number_stars"]
    ## init Values and Policy
    V = np.zeros(nS).astype(np.float32)
    PI = np.zeros(nS).astype(np.int32)
    ## copy to avoid call by reference issue
    v_py, pi_py = backend_py.async_vi(V.copy(), PI.copy(), values, indices, indptr, shape, n_stars, nS, nA, data_dir)
    v_cpp, pi_cpp = backend.async_vi(V.copy(), PI.copy(), values, indices, indptr, shape, n_stars, nS, nA, data_dir)
    ## print results
    print(f'Comparison of actual policy with calucalted: Difference is: {(pi_py - pi_cpp).sum()}')
    print(f'Comparison of actual values with calucalted: Difference is: {(v_py - v_cpp).sum()}')
    ##########################################
    #           now plot the result          #
    ##########################################
    ## get the rest of requiered parameters
    max_fuel = parameters["fuel_capacity"]
    P = to_sparse_matrix(values, indices, indptr, shape) ## true transition probs
    star_graph = to_sparse_matrix(*load_sparse_matrix(data_dir, "star_graph")) ## the mere radius neighbor graph (sklearn)
    stars = np.load(f"{data_dir}/stars.npy")  ## coordinates of stars
    star_types = np.load(f"{data_dir}/star_types.npy")  ## fuel star or not as lookup table (mostly for rendering)
    ## set a random state / start with max fuel, last star is goal, start with star 0
    random_state = state_from_tuple(max_fuel - 1, n_stars - 1, 0, n_stars)
    ## reconvert to tuple
    fuel, goal_star, cur_star = state_to_tuple(random_state, n_stars)
    ## A* Path + policy through graph
    a_path = graphsearch.a_star(cur_star, goal_star, star_graph, stars)
    pi_path = travel(random_state, P, pi_cpp, n_stars, nA)
    plot_full_graph(star_graph, stars, star_types, (a_path, "orange"), (pi_path, "red"))
    plt.show()

## you can use this python file directly
if __name__ == "__main__":
    run()
