How to Install
=================
  
This library does not deploy PyPI at this moment. So please clone and install yourself.  

clone
------

clone from repository
::
    git https://github.com/muilab/mui-display-lib.git
  
  
install Cython and Build module
--------------------------------

library use Cython for make C-object from pyx file.

install  Cython
::
    python3 -m pip install Cython

  
build module  
::
    python3 setup.py build_ext --inplace
  
  
install library
---------------

install library
::
    python3 setup.py install
  
  
