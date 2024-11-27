from pprint import pprint
import json
import xmltodict

from module.dataclass import Composition
from module.utils import (
	simplify_dict, 
	transform_to_header_structure, 
	extract_datamodel,
	remove_name_tree,
	convert_to_list,
	remove_comments,
	flatten_middle_nodes
)

xml_file = "xml/report_example_auto.xml"
with open(xml_file, 'r', encoding="utf-8") as file:
	xml_data = file.read().encode("utf-8")
	data =  xmltodict.parse(xml_data, encoding="utf-8")

# c = Composition.model_validate(data["composition"])
dips = Composition.parse_obj(data["composition"])

#datamodel = extract_datamodel(dips)

# model_dump_dict = dips.model_dump(exclude_none=True)

model_dump_dict = dips.dict(exclude_none=True)

model_dump_dict = simplify_dict(model_dump_dict)
model_dump_dict = remove_name_tree(model_dump_dict)
#model_dump_dict = convert_to_list(model_dump_dict)

model_dump_dict = transform_to_header_structure(model_dump_dict)
model_dump_dict = remove_comments(model_dump_dict)
model_dump_dict = flatten_middle_nodes(model_dump_dict)
model_dump_dict = flatten_middle_nodes(model_dump_dict)

model_dump_string = json.dumps(model_dump_dict, indent=2, ensure_ascii=False)
with open("output/parsed_data.json", "w", encoding="utf-8") as out:
	out.write(model_dump_string)

data_model = extract_datamodel(model_dump_dict)
data_model_string = json.dumps(data_model, indent=2, ensure_ascii=False)
with open("output/data_model.json", "w", encoding="utf-8") as out:
	out.write(data_model_string)