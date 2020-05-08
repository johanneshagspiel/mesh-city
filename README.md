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
Now you can run the following to check your code for formatting and linting issues:
```
(mesh-city) $ python setup.py check
```
and the following to automatically fix the formatting:
```
(mesh-city) $ python setup.py fix
```
and this to run all the tests with coverage:
```
(mesh-city) $ python setup.py test
```
The coverage report can then be found in `build/coverage` in HTML format. For more tasks
see the `cmdclass` section in `setup.py`.
