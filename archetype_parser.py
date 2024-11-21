from lxml import etree
import re

def parse_contents_tree(xml_input):
	tree = etree.parse(xml_input)
	root = tree.getroot()

	ns = {
		"xsi": "http://www.w3.org/2001/XMLSchema-instance",
		"p1": "http://www.w3.org/2001/XMLSchema-instance",
		"x": "http://schemas.openehr.org/v1" # def. x her, er i default i filen
	}
	
	# Find all contents
	contents = root.xpath("//x:content", namespaces=ns)
	print(f"found {len(contents)} items in contents")

	for content in contents:
		name = content.xpath(".//x:name/x:value/text()", namespaces=ns)[0]
		at = content.xpath(".//x:archetype_details/x:archetype_id/x:value/text()", namespaces=ns)[0]
		print(f"Currently working with content = '{name}' using archetype '{at}'.")
		cluster_items = content.xpath(".//x:items[@xsi:type='CLUSTER']", namespaces=ns)

		for cluster_item in cluster_items:
			element_items = content.xpath(".//x:items[@xsi:type='ELEMENT']", namespaces=ns)
			for element_item in element_items:
				name = element_item.xpath(".//x:name/x:value/text()", namespaces=ns)[0]
				value = element_item.xpath(".//x:value/x:value/text()", namespaces=ns)[0]
				print(f" * '{name}' = '{value}'") 

			cluster_name = cluster_item.xpath(".//x:name/x:value/text()", namespaces=ns)[0]
			cluster_value = cluster_item.xpath(".//x:value/x:value/text()", namespaces=ns)[0]
			print(f" ** '{cluster_name}' = '{cluster_value}' **")

			element_items = cluster_item.xpath(".//x:items[@xsi:type='ELEMENT']", namespaces=ns)
			for element_item in element_items:
				name = element_item.xpath(".//x:name/x:value/text()", namespaces=ns)[0]
				value = element_item.xpath(".//x:value/x:value/text()", namespaces=ns)[0]
				print(f" *** '{name}' = '{value}'")

		print()

def parse_archetype_tree(xml_input, input_file = False):
	if input_file:
		tree = etree.parse(xml_input)
		root = tree.getroot()
	else:
		root = etree.fromstring(xml_input)

	ns = {
		"xsi": "http://www.w3.org/2001/XMLSchema-instance",
		"p1": "http://www.w3.org/2001/XMLSchema-instance",
		"x": "http://schemas.openehr.org/v1" # def. x her, er i default i filen
	}

	# Find previous RT treatment
	at_list = root.xpath("//x:content", namespaces=ns)
	for at in at_list:
		archetype_node_id = at.xpath("@archetype_node_id")
		if archetype_node_id[0] == "openEHR-EHR-OBSERVATION.procedure_screening.v1":
			tidl_rt_list = at.xpath("//x:events//*[@archetype_node_id='at0022']/x:name/x:value/text()", namespaces=ns)
			print(tidl_rt_list[0])

	# Here at0022 refers to "Specific procedure"

	# Find kartleggingsformal
	x = root.xpath("//*[@archetype_node_id='at0034']/x:name/x:value/text()", namespaces=ns)[0]
	y = root.xpath("//*[@archetype_node_id='at0034']/x:value/x:value/text()", namespaces=ns)[0]
	z = root.xpath("//*[@archetype_node_id='at0034']/x:value/x:defining_code/x:code_string/text()", namespaces=ns)[0]
	print(x, "er", y, "med SNOMED-CT kode", z)
	
def remove_dips_frame(xml_file):
	with open(xml_file, "r") as f:
		text = "".join(f.readlines())

		pattern = r"<a:SKJEMA[^>]*>(.*?)</a:SKJEMA>"
		skjemas = re.findall(pattern, text, re.DOTALL)

	return skjemas

xml_file = "xml/rt_requisition_clean.xml"
xml_string_list = remove_dips_frame(xml_file)

"""
for xml_string in xml_string_list:
	result = parse_archetype_tree(xml_string.encode("utf-8"))
"""

parse_contents_tree(xml_file)