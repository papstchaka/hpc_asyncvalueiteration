# `backend`

holds all files that are responsible for the `Python/C++` interface from python side

<br/><br/>

-------

## <a href='__init__.py' target='_blank'>`__init__.py`</a>

responsible to correctly import `backend_cpp.py` and `backend_py.py`

Given functionality:
- tries to import both, `backend_py.py` and `backend_cpp.py`. Raises a warning if unsuccesfull

<br/><br/>

-------

## <a href='backend_cpp.py' target='_blank'>`backend_cpp.py`</a>

C++ backend. Responsible to load the - by CFFI provided - C++ functionality. Until line 75 - meaning anything else then the last function, here `async_vi()` - no changes are needed (no matter the respective task)

Given functionality:
- `_find_compile_output()` - returns all files that belong to the compiled interface
    * `should_include()` - checks whether cpp_interface.cpp, cpp_interface.---.so and cpp_interface.o exist
- `_compile_output_complete()`- checks if exactly the desired 3 files exist
- check if compile issues occured --> if yes, tries to recompile. If then still errors occur, throws error and stops
- tries to import the `cpp_interface`, throws error if it fails
- `async_vi()` [! only function that needs to be changed for other tasks!] - same as in the python version, but using the C++ library --> performs the aynchronous value iteration, after checking types of the input parameters and casting respective ones to `C pointers`

<br/><br/>

-------

## <a href='backend_py.py' target='_blank'>`backend_py.py`</a>

Python backend. Needs complete change for other tasks than `Async VI`. 

Given functionality:
- `type_cast()` - casts numpy arrays into different type. If desired type not implementing, then original array is returned
- `load_sparse_matrix()` - load sparse matrix data from given directory
- `to_sparse_matrix()` - makes scipy.sparse.csr_matrix from given parameters
- `state_to_tuple()` - casts state to tuple with fuel, goal star and current star
- `one_step_cost` - calculates cost for given state and action (=control)
- `one_step_lookahead()` - Helper function to calculate the value for all action in a given state
- `async_vi()` - same as in the C++ version, but using the python --> performs the aynchronous value iteration or loads the given data arrays from the data directory (depending on the `recalc` parameter)

<br/><br/>

-------

## <a href='compile_interface.py' target='_blank'>`compile_interface.py`</a>

Interface python code for CFFI. Only needs slight changes when implementing different task!

Given functionality:
- `compile_interface()` - Use API mode of cffi to get speed of access and proper errors. Compiles the interface (C++ code). [!only line that needs to be changed for other tasks is line 23 (respective all lines starting with `ffi.cdef(""" ...`), here `ffi.cdef("""void cffi_async_vi(double* ...);""")`]

<br/><br/>

-------

## <a href='Makefile' target='_blank'>`Makefile`</a>

Makefile for this folder.

Given functionality:
- `make clean` - cleans the folder by deleting all compilation files, listed below, calls `remove_interface`, `remove_backend` and `remove_pycache`
- `remove_interface` - removes the interface files [`cpp_interface.cpp`, `cpp_interface.cpython-*.so` and `cpp_interface.o`]
- `remove_backend` - removes the backend folders [`inc/` and `lib/`]
- `remove_pycache` - removes pycache folder [`__pycache__/`]