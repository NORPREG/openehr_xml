from lxml import etree
import re

def parse_archetype_tree(xml_input, input_file = False):
	if input_file:
		tree = etree.parse(xml_input)
		root = tree.getroot()
	else:
		root = etree.fromstring(xml_input)

	nsmap = {
		"xsi": "http://www.w3.org/2001/XMLSchema-instance",
		"p1": "http://www.w3.org/2001/XMLSchema-instance",
		# None: "http://schemas.openehr.org/v1"
	}	

	# innholdet er i root

	comp_list = root.xpath(".//*[local-name()='composition']")
	at_dict = dict()

	for comp in comp_list:
		at_details = comp.xpath("//*[local-name()='archetype_details']")
	
		for at in at_details:
			at_name = at.xpath(".//*[local-name()='archetype_id']/*[local-name()='value']/text()")
			if at_name:
				at_name = at_name[0]

			items = at.xpath(".//*[local-name()='template_id']")
			item_list = list()

			for item in items:
				at_node_id = item.attrib.get("archetype_node_id")
				name_element = item.xpath(".//*[local-name()='value']/text()")
				name_content = name_element[0] if name_element else None

				if at_node_id and name_content:
					item_list.append({
						"archetype_node_id": at_node_id,
						"name": name_content
					})

				if item_list:
					at_dict[at_name] = item_list

	return at_dict

def remove_dips_frame(xml_file):
	with open(xml_file, "r") as f:
		text = "".join(f.readlines())

		pattern = r"<a:SKJEMA[^>]*>(.*?)</a:SKJEMA>"
		skjemas = re.findall(pattern, text, re.DOTALL)

	return skjemas



"""
xml_string_list = remove_dips_frame(xml_file)

for xml_string in xml_string_list:
	result = parse_archetype_tree(xml_string.encode("utf-8"))
	print(result)

"""

xml_file = "xml/rt_requisition_clean.xml"

result = parse_archetype_tree(xml_file, input_file = True)
print(result)