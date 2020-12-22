# `cpp_backend`

holds complete `C++` backend, including <a href='main.cpp' target='_blank'>`main.cpp`</a> that can be used for testing the `C++` code (independently from `Python` or the `CFFI Interface`)

<br/><br/>

-------

## <a href='lib/' target='_blank'>`lib/`</a>

folder containing all libraries that are used by this backend

<br/><br/>

-------

## <a href='CMakeLists.txt' target='_blank'>`CMakeLists.txt`</a>

respective `cmake` file that gets called during compilation process in <a href='Makefile' target='_blank'>`Makefile`</a>. Needs no change for other tasks

Given functionality:
- sets all parameters for the `compiler` to run

<br/><br/>

-------

## <a href='main.cpp' target='_blank'>`main.cpp`</a>

Testing script, to check workwise of implemented `Async VI`. Uses <a href='../data/data_debug/' target='_blank'>`data_debug/`</a> dataset (hard coded). Needs complete change for other tasks

Given functionality:
- hard coded initialization of `values`, `row_pointer`, `rows`, `nnz`, `cols` and `rows` of `probability matrix`. Hard coded initialization of `v`, `pi`, `n_stars`, `nS` and `nA`
- runs <a href='lib/src/Async_VI.cpp' target='_blank'>`backend's asnyc_vi`</a> and compares the result with (hard coded) `ground truth` of `PI`

<br/><br/>

-------

## <a href='Makefile' target='_blank'>`Makefile`</a>

Makefile for this folder. Needs no change for other tasks

Given functionality:
- `make clean` - cleans project folder by removing old executables, `tar`-archives and further folders, calls `remove_pycache` and `remove_srcfiles`. Calls `make clean` in <a href='lib/' target='_blank'>`lib/`</a>
- `remove_clion_build` - removes the clion build folders [`cmake-build-debug/` and `.idea/`]
- `remove_build_directories` - removes all build folders and files [`build/`, `debug/`, `release/` and `CMakeLists.txt.user`]
- `remove_vs_folder` - removes Visual Studio folder [`.vs/`]
- `make compile` - deletes old build directories and recompiles full project. Builds `build/` folder, runs `cmake`, `make` and `make install` in there