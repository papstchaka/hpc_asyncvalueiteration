# `inc`

contains all `include` files (Header) for project. Maybe needs a change for other tasks, depending on the needed `C++` libraries

<br/><br/>

-------

## <a href='Eigen/' target='_blank'>`Eigen/`</a>

contains all files that this version of <a href='http://eigen.tuxfamily.org/index.php?title=Main_Page' target='_blank'>`Eigen`</a> needs to work properly

<br/><br/>

-------

## <a href='Async_VI.h' target='_blank'>`Async_VI.h`</a>

Header of <a href='../src/Async_VI.cpp' target='_blank'>`Async_VI.cpp`</a>. Needs complete change for other task

<br/><br/>

-------

## <a href='Interface.h' target='_blank'>`Interface.h`</a>

Header file for the Interface. Logic is same as in <a href='../../../backend/compile_interface.py' target='_blank'>`compile_interface.py`</a> but in `C++` code. Needs same changes as `compile_interface.py`

Given functionality:
- `extern void cffi_async__vi()` - provides a pipeline of the `C++` code into `Python` Interface