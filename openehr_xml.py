from pprint import pprint
import json
import xmltodict
from rich import print
import pandas as pd

from module.dataclass import Composition
from module.utils import (
	simplify_dict, 
	transform_to_header_structure,
	transform_to_header_structure2,
	remove_name_tree,
	convert_to_list,
	remove_comments,
	flatten_middle_nodes
)

from module.extract_datamodel import extract_datamodel

xml_file = "xml/report_example_auto.xml"
with open(xml_file, 'r', encoding="utf-8") as file:
	xml_data = file.read().encode("utf-8")
	data =  xmltodict.parse(xml_data, encoding="utf-8")

dips = Composition.model_validate(data["composition"])


model_dump_dict = dips.model_dump(exclude_none=True)
model_dump_dict = simplify_dict(model_dump_dict)
model_dump_dict = remove_name_tree(model_dump_dict)

model_dump_dict = transform_to_header_structure2(model_dump_dict)

model_dump_dict = remove_comments(model_dump_dict)
model_dump_dict = flatten_middle_nodes(model_dump_dict)

model_dump_string = json.dumps(model_dump_dict, indent=2, ensure_ascii=False)
with open("output/parsed_data.json", "w", encoding="utf-8") as out:
	out.write(model_dump_string)

data_model = extract_datamodel(model_dump_dict)
data_model_string = json.dumps(data_model, indent=2, ensure_ascii=False)
with open("output/data_model.json", "w", encoding="utf-8") as out:
	out.write(data_model_string)

pd_input = {
	"category": list(),
	"parameter": list(),
	"idx": list(),
	"value": list(),
}

for category, values in data_model.items():
	if isinstance(values, list):
		for values_item in values:
			for key, value in values_item.items():
				if not isinstance(value, list):
					value = [value]

				for idx, value_item in enumerate(value):
					if len(value_item) > 100:
						# Remove lorem ipsum noise
						value_item = value_item[:25] + "...."

					pd_input["category"].append(category)
					pd_input["parameter"].append(key)
					pd_input["value"].append(value_item)
					pd_input["idx"].append(idx+1)
	else:
		for key, value in values.items():
			if not isinstance(value, list):
				value = [value]

			for idx, value_item in enumerate(value):
				if len(value_item) > 100:
					# Remove lorem ipsum noise
					value_item = value_item[:25] + "...."
					 
				pd_input["category"].append(category)
				pd_input["parameter"].append(key)
				pd_input["value"].append(value_item)
				pd_input["idx"].append(idx+1)

df = pd.DataFrame(pd_input)
df.to_excel("output/data_model.xlsx", index=False)