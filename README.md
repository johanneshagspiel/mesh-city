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
Then install the dependencies:
```
$ pipenv sync --dev
```
Then start a shell inside the virtual environment:
```
$ pipenv shell
```
Then install the dependencies that don't work with Pipenv:
```
(mesh-city) $ pip install -r requirements.txt
```
Then install the dependencies that don't work with Pipenv:
```
(mesh-city) $ pip install libs/rasterio-1.1.4-cp37-cp37m-win_amd64.whl libs/GDAL-3.0.4-cp37-cp37m-win_amd64.whl 
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


