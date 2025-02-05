from rich import print

def simplify_dict(d):
	"""Recursively simplify and flatten a nested dictionary and lists."""
	if isinstance(d, dict):
		# Keywords to elevate or flatten
		keywords = [
			"value",
			"Tree",
			"Item tree",
			"List",
			"events",
			"Uspesifisert hendelse"
		]

		# Elevate values if the dictionary only contains a specific keyword
		for k in keywords:
			if k in d and len(d) == 1:
				return simplify_dict(d[k])

		# Flatten the content of specific keywords into the current level
		#keywords.append("items")
		flattened = {}
		for k, v in d.items():
			if k in keywords:
				# Simplify the content under the keyword
				inner = simplify_dict(v)
				if isinstance(inner, dict):
					# Merge dictionaries into the current level
					for inner_key, inner_value in inner.items():
						if inner_key not in flattened:
							flattened[inner_key] = inner_value
						else:
							# Combine conflicting keys into a list
							if not isinstance(flattened[inner_key], list):
								flattened[inner_key] = [flattened[inner_key]]
							flattened[inner_key].append(inner_value)
				elif isinstance(inner, list):
					# Handle lists under keywords
					flattened[k] = inner
				else:
					# Add non-dict, non-list values
					flattened[k] = inner
			else:
				# Process other keys as usual
				flattened[k] = simplify_dict(v)

		return flattened

	elif isinstance(d, list):
		# Recurse into each element of the list
		simplified_list = [simplify_dict(item) for item in d]

		# If the list contains only dictionaries, keep it as a list of dictionaries
		return simplified_list

	else:
		# Return non-dict, non-list items as is
		return d


def remove_name_tree(d):
	"""Recursively remove all occurrences of 'name': 'Tree'."""
	if isinstance(d, dict):
		# Remove 'name': 'Tree' pairs from the dictionary
		return {k: remove_name_tree(v) for k, v in d.items() if not (k == "name" and v in ["Tree", "*Tree(en)", "Item tree"])}
	
	elif isinstance(d, list):
		# Recursively process each element in the list
		return [remove_name_tree(item) for item in d]
	
	else:
		# Return non-dict, non-list items as is
		return d	

def transform_to_header_structure(d):
	"""Transform the dictionary to the form {header: {[name: value]}}, preserving 'origin' and 'time'."""
	if isinstance(d, dict):
		if "name" in d and ("items" in d or "data" in d):
			# If it's a header, recursively simplify its content
			header_name = d["name"]
			if isinstance(header_name, list):
				header_name = "_".join(header_name)

			content = d.get("items", d.get("data", {}))
			simplified_content = transform_to_header_structure(content)

			# Include 'origin' and 'time' if they exist
			additional_info = {k: v for k, v in d.items() if k in {"origin", "time"}}
			if isinstance(simplified_content, dict):
				simplified_content.update(additional_info)
			elif isinstance(simplified_content, list):
				simplified_content.append(additional_info)

			return {header_name: simplified_content}
		elif "name" in d and "value" in d and len(d) == 2:
			# If it's a variable, return it as a {name: value} pair
			return {d["name"]: d["value"]}
		elif "name" in d and "value" in d and "symbol" in d and len(d) == 3:
			return {d["name"]: d["value"], "symbol": d["symbol"]}
		elif "name" in d and "magnitude" in d and len(d) == 2:
			return {d["name"]: d["magnitude"]}
		elif "name" in d and "magnitude" in d and "units" in d and len(d) == 3:
			return {d["name"]: d["magnitude"], "units": d["units"]}
		else:
			# Otherwise, recurse into each value
			return {k: transform_to_header_structure(v) for k, v in d.items()}
	elif isinstance(d, list):
		# If it's a list, process each element
		simplified_list = [transform_to_header_structure(item) for item in d]
		# Combine dictionaries into one if they're simple {name: value} pairs
		combined_dict = {}
		for item in simplified_list:
			if isinstance(item, dict) and len(item) == 1:
				combined_dict.update(item)
			else:
				# If not all are {name: value}, return as a list
				return simplified_list
		return combined_dict
	else:
		# Return non-dict, non-list items as is
		return d

def flatten_middle_nodes(d):
	"""Recursively flatten nested dictionaries, removing middle nodes."""
	if isinstance(d, dict):
		flattened_dict = {}
		for key, value in d.items():
			keys_to_test = ["items", "List", "_Uspesifi", "structure"]
			key_test = False
			for k in keys_to_test:
				if isinstance(value, dict) and len(value) and k in list(value.keys())[0]:
					key_test = True
					break
					
			if key_test:
				# If the value is a dictionary with exactly one key, "lift" the inner key-value pair
				inner_key, inner_value = list(value.items())[0]
				flattened_dict[key] = inner_value
			else:
				# Otherwise, keep the original key-value pair
				flattened_dict[key] = flatten_middle_nodes(value)
		return flattened_dict
	
	elif isinstance(d, list):
		# Process each item in the list
		return [flatten_middle_nodes(item) for item in d]
	
	else:
		# Return non-dict, non-list items as is
		return d

def flatten_dicts_in_list(data):
	"""
	Recursively traverses a dictionary, flattens any lists containing dictionaries into a single dictionary.

	Args:
		data (dict): Input dictionary.

	Returns:
		dict: Processed dictionary with lists of dictionaries flattened.
	"""
	if isinstance(data, dict):
		new_data = {}
		for key, value in data.items():
			if isinstance(value, list) and all(isinstance(item, dict) for item in value):
				# Merge all dictionaries in the list into a single dictionary
				flattened = {}
				for item in value:
					flattened.update(flatten_dicts_in_list(item))  # Recursively flatten nested dicts
				new_data[key] = flattened
			else:
				# Recursively process the value
				new_data[key] = flatten_dicts_in_list(value)
		return new_data
	elif isinstance(data, list):
		# Recursively process list elements
		return [flatten_dicts_in_list(item) for item in data]
	else:
		# Return the value as-is if it's not a list or dictionary
		return data