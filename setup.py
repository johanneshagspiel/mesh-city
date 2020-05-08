from abc import ABC
from distutils.cmd import Command
from subprocess import CalledProcessError, check_call
from sys import stdout
from typing import List

import pipfile
from pipfile import Pipfile
from setuptools import find_packages, setup


def get_pipfile_dependencies(category: str) -> List[str]:
	project_pipfile: Pipfile = pipfile.load("Pipfile")
	dependencies: List[str] = []
	for name, version in project_pipfile.data[category].items():
		if version == "*":
			version = ""
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
		check_call(args="pylint -j 0 --rcfile=../.pylintrc mesh_city", cwd="src", shell=True)
		check_call(args="pylint -j 0 --rcfile=../.pylintrc test_mesh_city", cwd="src", shell=True)


class CoverageTestCommand(CommandAdapter):
	def run(self) -> None:
		check_call(args="coverage run --branch --source=src/mesh_city --module unittest discover src", shell=True, stderr=stdout)


class CoverageCheckCommand(CommandAdapter):
	def run(self) -> None:
		check_call(args="coverage report --fail-under 70 --skip-empty --show-missing", shell=True)


class CoverageReportCommand(CommandAdapter):
	def run(self) -> None:
		check_call(args="coverage html --directory=build/coverage", shell=True)


class YapfCheckCommand(CommandAdapter):
	def run(self) -> None:
		check_call(args="yapf --diff --parallel --recursive src", shell=True)


class YapfFixCommand(CommandAdapter):
	def run(self) -> None:
		check_call(args="yapf --in-place --parallel --recursive src", shell=True)


class IsortCheckCommand(CommandAdapter):
	def run(self) -> None:
		check_call(args="isort --check-only --diff --recursive src", shell=True)


class IsortFixCommand(CommandAdapter):
	def run(self) -> None:
		check_call(args="isort --recursive src", shell=True)


class FixCommand(CommandAdapter):
	def run(self) -> None:
		self.run_command("imports_fix")
		self.run_command("format_fix")


try:
	setup(
		name="mesh-city",
		version="0.1.0",
		url="https://gitlab.ewi.tudelft.nl/cse2000-software-project/2019-2020-q4/cluster-3/mesh-city/mesh-city",
		package_dir={"": "src"},
		packages=find_packages(where="src"),
		python_requires=">=3.7",
		install_requires=get_pipfile_dependencies("default"),
		extras_require={"dev": get_pipfile_dependencies("develop")},
		cmdclass={
			"coverage_check": CoverageCheckCommand,
			"coverage_report": CoverageReportCommand,
			"fix": FixCommand,
			"format_check": YapfCheckCommand,
			"format_fix": YapfFixCommand,
			"imports_check": IsortCheckCommand,
			"imports_fix": IsortFixCommand,
			"lint": PylintCommand,
			"test": CoverageTestCommand,
		},
	)
except CalledProcessError as cpe:
	print("\nTask failed")
	exit(1)
