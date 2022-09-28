<img src=src/mesh_city/resources/mvrdv/planet_painter_logo.png alt="Planet Painter Logo" width="250" height="250">

--------------------------------------------------------------------------------
[![Top Language](https://img.shields.io/github/languages/top/johanneshagspiel/planet-painter)](https://github.com/johanneshagspiel/planet-painter)
[![Latest Release](https://img.shields.io/github/v/release/johanneshagspiel/planet-painter)](https://github.com/johanneshagspiel/planet-painter/releases/)

# Planet Painter

"Planet Painter" is a desktop program developed in collaboration with the think tank [The Why Factory](https://www.mvrdv.nl/projects/368/the-why-factory) of the Dutch Architecture firm [MVRDV NEXT](https://www.mvrdv.nl/themes/15/next) aimed at visualizing and quantifying the impact of different kinds of interventions such as replacing cars with trees on the climate. By using satellite imagery, these kinds of scenarios can be generated even for underserved communities for which traditionally not enough data were collected to explore such scenarios.     

## Features

With the "Planet Painter", the user can:

- download satellite images from multiple sources like Google Maps or Mapbox
- automatically detect through neural networks different objects on these satellite images including:
  - trees
  - cars
  - buildings
- visually generate different kinds of scenarios such as:
  - replacing all cars with trees
  - adding greenery to the roof of buildings
- quantify the impact of these scenarios on the climate by determining based on the biome of the area that has been downloaded the amount of CO2 which would be saved and the amount of trees that would be planted

## Tools

| Purpose                      | Name                                                                                       |
|------------------------------|--------------------------------------------------------------------------------------------|
| Programming language         | Python 3.7                                                                                 |
| Dependency manager           | [Pipenv](https://pipenv.pypa.io/en/latest/)                                                |
| Build tool                   | setuptools (`setup.py`)                                                                    |
| GUI library                  | [tkinter](https://docs.python.org/3/library/tkinter.html)                                  |
| Testing framework            | [unittest](https://docs.python.org/3/library/unittest.html)                                |
| Tree detection framework     | [DeepForest](https://deepforest.readthedocs.io/en/latest/)                                 |
| Building detection framework | [xdxd_spacenet4](https://github.com/CosmiQ/solaris/blob/main/solaris/nets/zoo/__init__.py) |
| Car detection framework      | Self-trained [TensorFlow Model](https://www.tensorflow.org/)                               |


## Installation Process

It is assumed that the user has installed an IDE like [PyCharm](https://www.jetbrains.com/pycharm/) and that the operating system is a 64-bit version of Windows.
	
Make sure that you have installed the [64-bit version of Python 3.7](https://www.python.org/downloads/release/python-370/). You can run `py -0p` in the terminal to see all installed Python versions.

In case you have not installed `pipenv` yet, do so with this command:

	pip install pipenv

Open the repository in the terminal and create a virtual environment:    

    pipenv --python 3.7 

Some of the dependencies of this project are very difficult to install from their source or using typical tools such as pip. Therefore [binary wheels](libs) are included for 64-bit Windows that are compatible with Python 3.7, which come from Christoph Gohlke's [repository of unofficial Windows binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/). By running the following command, these dependencies will be installed:

	pip install libs/GDAL-3.0.4-cp37-cp37m-win_amd64.whl libs/rasterio-1.1.4-cp37-cp37m-win_amd64.whl libs/Shapely-1.7.0-cp37-cp37m-win_amd64.whl libs/Rtree-0.9.4-cp37-cp37m-win_amd64.whl libs/Fiona-1.8.13-cp37-cp37m-win_amd64.whl

Then, the remaining dependencies that are specified in the pipfile are installed by running the following command:

	pipenv sync --dev

Lastly, install `PyTorch` and `pytorch` with this command:
	
	pip install torch torchvision

In order to be able to download images from Google Maps an API key is required. A key can be acquired [here](https://developers.google.com/maps/documentation/javascript/get-api-key) and it has to be stored in the [user file](src/mesh_city/resources/user/users.json).

Now, the program can be run with the following command:

	python setup.py run


## Contributors

This app was developed using the [SCRUM methodology](https://www.scrum.org/resources/what-is-scrum) together with:

- [Thom van der Woude](https://github.com/tbvanderwoude)
- [Reinout Meliesie](https://github.com/Zedfrigg)
- [Wouter Maas](https://github.com/wfvmaas)
- [Borna Salarian](https://github.com/Bsalarian)

Additionally, we collaborated with [Leo Stuckhardt](https://www.mvrdv.nl/about/team/51/leo-stuckardt) from The Why Factory.

## License

This repository is for demonstration only. If you want to use the "Planet Painter" for any purpose including but not limited to for educational or commercial reasons, contact [The Why Factor](javier@thewhyfactory.com) directly. 
