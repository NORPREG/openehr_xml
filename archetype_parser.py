from _pytest.monkeypatch import V
from lxml import etree
from pprint import pprint

import xmltodict, json

def read_metadata(xml, ns):
	d = dict()

	name = xml.xpath(".//x:name/value/text()", namespaces=ns)
	uid = xml.xpath(".//x:uid/value/text()", namespaces=ns)

	archetype_details = {
		"archetype_id": xml.xpath(".//x:archetype_details/value/text()", namespaces=ns),
		"template_id": xml.xpath(".//x:template_id/value/text()", namespaces=ns),
		"rm_version": xml.xpath(".//x:rm_version/text()", namespaces=ns)
	}

def parse_document(xml_file):
	def first(s):
		return len(s) and s[0] or None

	root = etree.parse(xml_file)

	ns1 = {
		"xsi": "http://www.w3.org/2001/XMLSchema-instance",
		"p1": "http://www.w3.org/2001/XMLSchema-instance",
		"x": "http://schemas.openehr.org/v1" # def. x her, er i default i filen
	}

	# composition 
	#	metadata
	#	content (section; evaluation; observation)
	#		metadata
	#		subject
	#		data
	#			items cluster
	#				name
	#				items element

	compositions = root.xpath("//x:composition", namespaces=ns1)
	for composition in compositions:
		metadata = read_metadata(composition, ns1)

xml_file = "xml/report_example_auto.xml"
parse_document(xml_file)

xml_string = open(xml_file, "r", encoding="utf-8").read()
xml_dict = xmltodict.parse(xml_string)
pprint(xml_dict)
