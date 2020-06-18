"""
See :class:`.ScenarioSchema`
"""
from typing import Any, Sequence, Tuple

from mesh_city.scenario.scenario_pipeline import ScenarioModificationType


class ScenarioSchema:
	"""
	A schema for making scenario's with particular modifications
	"""

	def __init__(
		self, parameterized_modifications: Sequence[Tuple[ScenarioModificationType, Any]] = None
	):
		if parameterized_modifications:
			self.__parameterized_modifications = parameterized_modifications
		else:
			self.__parameterized_modifications = []

	def add_modification(self, modification_type: ScenarioModificationType, parameter: Any):
		"""
		Adds a parameterized scenario modification to this schema.
		:param modification_type: The type of modification to make
		:param parameter: The parameter for this modification
		:return:
		"""
		self.__parameterized_modifications.append((modification_type, parameter))

	def get_parameterized_modifications(self) -> Sequence[Tuple[ScenarioModificationType, Any]]:
		"""
		Returns the list of modifications to make
		:return: The list of parameterized modifications
		"""
		return self.__parameterized_modifications
