# `tests`

contains all testfiles that get called by `make test` in <a href='../Makefile' target='_blank'>`Makefile`</a>

<br/><br/>

-------

## <a href='Makefile' target='_blank'>`Makefile`</a>

Makefile for this folder.

Given functionality:
- `make clean` - cleans folder by removing old folders, calls `remove_pycache`
- `remove_pycache` - removes pycache folder [`__pycache__/`]

<br/><br/>

-------

## <a href='test_backend.py' target='_blank'>`test_backend.py`</a>

runs `pytest` in here. Tests whether `cpp_backend` was succesfully compiled and is in use. Furthermore it tests whether the result of `cpp_backend` leads to the same results as provided in the respective `data` folder (in this case <a href='../data/data_debug' target='_blank'>`data_debug/`</a>)

Given functionality:
- `test_cpp_backend_active()` - tests, whether the C++ backend is running
- `test_cpp_implement()` - tests, whether the async_vi steps matches between Python and C++