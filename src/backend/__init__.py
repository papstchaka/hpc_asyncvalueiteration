from . import backend_py

## second name, which can be the cpp code whenever possible, but falls back to python if needed
backend = backend_py

## try to load C++ backend
try:
  ## hide python backend by overwriting the variable
  from . import backend_cpp as backend
  ## import python backend with original name (just in case it is still required)
  from . import backend_py
## if fails, only load python backend
except (ModuleNotFoundError, ImportError) as e:
  import logging
  _logger = logging.getLogger(__name__)
  ## give warning
  _logger.warning(f"The c++ backend could not be imported, falling back to python!\nReason:\n\n{e}\n\n")

  ## might be handy to kill the program if this step fails ...
  # print(f"Reason - {type(e)}:", e)
  # import sys
  # sys.exit(1)

## only import important stuff with 'from backend import *'
__all__ = ["backend", "backend_py"]
