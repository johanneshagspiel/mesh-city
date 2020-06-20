# Mesh City

## Tools

| Purpose            | Name                    |
|--------------------|-------------------------|
| Language           | Python                  |
| Dependency manager | Pipenv                  |
| Build tool         | setuptools (`setup.py`) |
| GUI library        | TkInter                 |
| Test framework     | unittest                |

## How to run

The following section will detail how to run the project on the command line. For IDEs
the process may be different.

First install Pipenv using your package manager or Pip
(recommended on Windows):
```
$ pip install pipenv
```
Then start a shell inside the virtual environment:
```
$ pipenv shell
```
Now run this command to install pytorch into the newly created virtual environment.
```
(mesh-city) $ pip install -r requirements.txt
```
Some of the dependencies of this project are very hard to install from their source or using typical
tools such as pip. Therefore binary wheels are included for 64-bit Windows that are compatible with Python 3.7, 
which come from Christoph Gohlke's [repository of unofficial Windows binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/).
There are other ways to install these for other configurations, but running the following command from the root of this project folder will install these
on a compatible configuration.
```
(mesh-city) $ pip install libs/rasterio-1.1.4-cp37-cp37m-win_amd64.whl libs/GDAL-3.0.4-cp37-cp37m-win_amd64.whl libs/Shapely-1.7.0-cp37-cp37m-win_amd64.whl libs/Rtree-0.9.4-cp37-cp37m-win_amd64.whl libs/Fiona-1.8.13-cp37-cp37m-win_amd64.whl
```
Next, the remaining dependencies that are specified in the pipfile are installed by running the following command.
```
$ pipenv sync --dev
```
Now you can run the following to check your code for formatting and linting issues:
```
(mesh-city) $ python setup.py check_code
```
and the following to automatically fix the formatting:
```
(mesh-city) $ python setup.py fix
```
and this to run all the tests with coverage:
```
(mesh-city) $ python setup.py test
```
To generate a linting report, run:
```
(mesh-city) $ python setup.py lint_report
```
The coverage report can then be found in `build/coverage` in HTML format. For more tasks
see the `cmdclass` section in `setup.py`.

Finally, to start the application run:
```
(mesh-city) $ python setup.py run
```


