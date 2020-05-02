import subprocess
from abc import ABC
from distutils.cmd import Command
from typing import List

import pipfile
from pipfile import Pipfile
from setuptools import find_packages, setup


def get_pipfile_dependencies(category: str) -> List[str]:
	project_pipfile: Pipfile = pipfile.load('Pipfile')
	dependencies: List[str] = []
	for name, version in project_pipfile.data[category].items():
		if version == '*':
			version = ''
		dependencies.append(name + version)
	return dependencies


class CommandAdapter(Command, ABC):
	user_options = []

	def initialize_options(self) -> None:
		pass

	def finalize_options(self) -> None:
		pass


class PylintCommand(CommandAdapter):
	def run(self) -> None:
		subprocess.check_call(args='pylint capacity', cwd='src', shell=True)


class UnittestCommand(CommandAdapter):
	def run(self) -> None:
		subprocess.check_call(args='python -m unittest discover', cwd='src', shell=True)


setup(
	name='mesh-city',
	version='0.1.0',
	url='https://gitlab.ewi.tudelft.nl/cse2000-software-project/2019-2020-q4/cluster-3/mesh-city/mesh-city',
	package_dir={'': 'src'},
	packages=find_packages(where='src'),
	python_requires='>=3.8',
	install_requires=get_pipfile_dependencies('default'),
	extras_require={'dev': get_pipfile_dependencies('develop')},
	cmdclass={
		'lint': PylintCommand,
		'test': UnittestCommand,
	},
)
