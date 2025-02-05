from re import T
import json
from functools import reduce
from operator import getitem

class DictionaryMapper:
	def __init__(self, b_config_path):
		with open(b_config_path, encoding="utf-8") as f:
			self.config = json.load(f)
		
	def get_from_a(self, a_data, keys, default=None):
		try:
			return reduce(getitem, keys, a_data)
		except (KeyError, TypeError):
			return default
	
	def _handle_dynamic_key(self, keys, a_data, b_key):
		"""Replace '//' in the path with the key from the B dictionary."""
		if keys[-1] == "//":
			# Replace '//' with the B key
			keys[-1] = b_key
		return keys
	
	def _handle_list_pattern(self, keys, a_data, b_key):
		"""Handle paths ending with '##' to extract list items."""

		print("keys", keys)

		# Identify keys[idx] where endswith("##")
		expand_idx = -1
		for idx, key in enumerate(keys):
			if isinstance(key, str) and key.endswith("##"):
				expand_idx = idx
				break

		if expand_idx >= 0:
			base_key = keys[idx].replace("##", "")
			extra_keys = list()
			if len(keys) > expand_idx + 1:
				extra_keys = keys[expand_idx+1:]

			parent_keys = keys[:expand_idx]
			parent_data = self.get_from_a(a_data, parent_keys, {})

			if isinstance(parent_data, dict):
				# Collect all keys matching the pattern (e.g., Name#1, Name#2)
				list_items = list()
				i = 1
				s = f"{base_key}#{i}"
				full_path =  [s] + extra_keys
				while s in parent_data:
					list_items.append(reduce(getitem, full_path, parent_data))
					i += 1
					s = f"{base_key}#{i}"
					full_path =  [s] + extra_keys
				return list_items
		return None

	def _expand_variables(self, path, variables):
		"""Expand variables in the path using the provided variable map."""
		expanded_path = list()
		for element in path:
			if element in variables:
				expanded_path.extend(variables[element])
			else:
				expanded_path.append(element)
		
		return expanded_path
	
	def map(self, a_data):
		"""Recursively map dictionary A to B, resolving variables and dynamic keys."""
		def _map_recursive(config_node, variables=None, b_key=None):
			if variables is None:
				variables = {}
			
			if isinstance(config_node, dict):
				# Split variables (keys starting with "_") and other keys
				current_vars = {}
				non_var_items = {}
				for k, v in config_node.items():
					if k.startswith("_"):
						current_vars[k] = v
					else:
						non_var_items[k] = v
				
				# Process non-variable keys with the current variables
				result = {}
				for k, v in non_var_items.items():
					result[k] = _map_recursive(v, variables=current_vars, b_key=k)
				return result
			
			elif isinstance(config_node, list):
				# Expand variables, then handle dynamic keys and list patterns
				expanded_path = self._expand_variables(config_node, variables)
				expanded_path = self._handle_dynamic_key(expanded_path, a_data, b_key)

				list_items = self._handle_list_pattern(expanded_path, a_data, b_key)
					
				if list_items is not None:
					return list_items
				else:
					return self.get_from_a(a_data, expanded_path)
			
			else:
				raise ValueError("Invalid config node")
		
		return _map_recursive(self.config)

def extract_datamodel(dips):
	mapper = DictionaryMapper("config/v13.json")
	b_data = mapper.map(dips)
	return b_data