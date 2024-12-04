from pprint import pprint
import json
import xmltodict
from lxml import etree

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
	root = etree.XML(xml_data)

xslt_file = "xml/transform.xslt"
with open(xslt_file, "r", encoding="utf-8") as file:
	xslt_data = file.read().encode("utf-8")
	xslt_root = etree.XML(xslt_data)
	transform = etree.XSLT(xslt_root)

result_tree = transform(root)

transformed_xml_file = "xml/transformed_report_example_auto.xml"
with open(transformed_xml_file, "w", encoding="utf-8") as file:
	file.write(etree.tostring(result_tree, pretty_print=True).decode("utf-8"))