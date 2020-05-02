from setuptools import setup, find_packages
import pipfile


def get_pipfile_dependencies(category: str):
	project_pipfile = pipfile.load('Pipfile')
	dependencies = []
	for name, version in project_pipfile.data[category].items():
		if version == '*':
			version = ''
		dependencies.append(name + version)
	return dependencies


setup(
	name='mesh-city',
	version='0.1.0',
	url='https://gitlab.ewi.tudelft.nl/cse2000-software-project/2019-2020-q4/cluster-3/mesh-city/mesh-city',
	package_dir={'': 'src'},
	packages=find_packages(where='src'),
	python_requires='>=3.8',
	install_requires=get_pipfile_dependencies('default'),
	extras_require={'dev': get_pipfile_dependencies('develop')},
)
