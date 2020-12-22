import pickle
import logging

logger = logging.getLogger(__name__)

import numpy as np
import scipy.sparse
from matplotlib import pyplot as plt

import graphsearch

#---------------------------------------------------------------------------------------

def state_to_tuple(x, n_stars):
  # Fuel f, goal star g and current node in graph i
  f = x // (n_stars * n_stars)
  g = x % (n_stars * n_stars) // n_stars
  i = x % (n_stars * n_stars) % n_stars

  return f, g, i

def state_from_tuple(f, g, i, n_stars):
  """ Fuel f, goal star g and current node in graph i """
  return f * n_stars * n_stars + g * n_stars + i

def jump(x, u, P, max_u):
  targets = P[x * max_u + u].nonzero()[1]

  if targets.size == 0:
    raise ValueError(f"Control {u} is not allowed in state {x}")

  disturbance = np.random.randint(0, targets.size)

  return targets[disturbance]

def travel(state, P, policy, n_stars, max_u, max_len=250):
  f, g, i = state_to_tuple(state, n_stars)

  path = [i]
  cur = state
  goal_reached = False

  while not goal_reached and len(path) < max_len:
    cur = jump(cur, policy[cur], P, max_u)

    _, _, i = state_to_tuple(cur, n_stars)

    goal_reached = i == g

    path.append(i)

  return path

def path_to_coor(path, stars):
  return np.array([stars[node, :] for node in path])

def plot_full_graph(adjacency, coordinates, star_types, *paths):

  connections_from = []
  connections_to = []

  for i, j in zip(*adjacency.nonzero()):
    connections_from.append(coordinates[i, :])
    connections_to.append(coordinates[j, :] - coordinates[i, :])

  connections_from = np.array(connections_from)
  connections_to = np.array(connections_to)

  plt.figure()

  plt.quiver(connections_from[:, 0], connections_from[:, 1], connections_to[:, 0], connections_to[:, 1],
             color='grey', headwidth=1, headlength=0, linewidth=0.5, width=0.001,
             scale_units='xy', scale=1.0, angles='xy')


  for i, path_col in enumerate(paths):

    if type(path_col) == tuple:
      path, color = path_col
    else:
      path, color = path_col, "orange"

    if path is None:
      print("Skipping invalid path -> no connection from start to goal")
      continue

    start = path[0]
    goal = path[-1]
    path_coor = path_to_coor(path, coordinates)

    plt.plot(coordinates[start, 0], coordinates[start, 1], 'x', color=color)
    plt.plot(coordinates[goal, 0], coordinates[goal, 1], 'x', color=color)
    plt.plot(path_coor[:, 0], path_coor[:, 1], '-o', linewidth=3.0, color=color)

    plt.annotate(f"start {i}",
                 xy=coordinates[start, :], xycoords='data',
                 xytext=(10, 10), textcoords='offset points',
                 color="k",
                 arrowprops={'arrowstyle': '->', 'color': "k"})
    plt.annotate(f"end {i}",
                 xy=coordinates[goal, :], xycoords='data',
                 xytext=(10, 10), textcoords='offset points',
                 color="k",
                 arrowprops={'arrowstyle': '->', 'color': "k"})

  fuel_stars = coordinates[np.argwhere(star_types > 0).squeeze()]
  normal_stars = coordinates[np.argwhere(star_types < 1).squeeze()]

  plt.plot(fuel_stars[:, 0], fuel_stars[:, 1], 'o', color="purple")
  plt.plot(normal_stars[:, 0], normal_stars[:, 1], '.', color="blue")

  plt.grid()
  plt.xlabel("x")
  plt.ylabel("y")

  return

def load_sparse_matrix(data_dir, name):
  indptr = np.load(f"{data_dir}/{name}_indptr.npy")
  indices = np.load(f"{data_dir}/{name}_indices.npy")
  data = np.load(f"{data_dir}/{name}_data.npy")
  shape = np.load(f"{data_dir}/{name}_shape.npy")
  return data, indices, indptr, shape

def to_sparse_matrix(data, indices, indptr, shape):
  # Eigen provides a similar why to create a CSR view of these arrays, take a look at Eigen::Map< CSR Matrix >(...)
  return scipy.sparse.csr_matrix((data, indices, indptr), shape=shape, dtype=data.dtype)