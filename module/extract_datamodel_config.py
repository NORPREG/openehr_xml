from re import T
import json
from functools import reduce
from operator import getitem

class DictionaryMapper:
	def __init__(self, b_config_path):
		with open(b_config_path) as f:
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
	
	def _handle_list_pattern(self, keys, a_data):
		"""Handle paths ending with '##' to extract list items."""
		if isinstance(keys[-1], str) and keys[-1].endswith("##"):
			base_key = keys[-1][:-2]  # Remove '##' from the end
			parent_keys = keys[:-1]
			parent_data = self.get_from_a(a_data, parent_keys, {})
			
			if isinstance(parent_data, dict):
				# Collect all keys matching the pattern (e.g., Name#1, Name#2)
				list_items = []
				i = 1
				while f"{base_key}#{i}" in parent_data:
					list_items.append(parent_data[f"{base_key}#{i}"])
					i += 1
				return list_items
		return None
	
	def map(self, a_data):
		"""Recursively map dictionary A to dictionary B using the config."""
		def _map_recursive(config_node, b_key=None):
			if isinstance(config_node, dict):
                return {k: _map_recursive(v, k) for k, v in config_node.items()}
			elif isinstance(config_node, list):
				# Handle dynamic key replacement
                config_node = self._handle_dynamic_key(config_node, a_data, b_key)
				
				# Handle list pattern extraction
				list_items = self._handle_list_pattern(config_node, a_data)
				if list_items is not None:
					return list_items
				
				# Default behavior: retrieve nested value
				return self.get_from_a(a_data, config_node)
			else:
				raise ValueError("Invalid config node")
		
		return _map_recursive(self.config)

def extract_datamodel(dips):
	mapper = DictionaryMapper("config/v12.json")
	b_data = mapper.map(dips)
	print(b_data)