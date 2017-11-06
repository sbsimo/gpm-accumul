# Installation steps gpm-accumul
Requirements: Python 3, h5py, GDAL and python-gdal

Suggestion: use virtualenv

1. Setup a virtualenv: `python3 -m venv <dirname>`
1. Activate the virtualenv:
    1. `cd <dirname>`
    1. `source bin/activate`
1. Install the code and dependencies: ` pip install -e git+https://github.com/ITHACA-org/gpm-accumul.git@master#egg=ERDS`
1. Install GDAL:
    1. Install gdal-bin python-gdal libgdal-dev with minimum version 2 (take advantage of ubuntugis [PPA](https://wiki.ubuntu.com/UbuntuGIS) )
    1. Install python-gdal in the virtualenv: `pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"`
  
# Run erds.py
From the command line, activate the virtualenv, then cd to src/erds and: `python3 erds.py`
## or
With cron, insert a job. In this case enter the full path to the python3 in the virtual env e.g. `/path/to/virtualenv/bin/python3`
