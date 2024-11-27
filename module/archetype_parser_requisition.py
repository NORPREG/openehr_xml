from lxml import etree
import re
from pprint import pprint

def parse_outer_document(modified_wrapper):
	root = etree.fromstring(modified_wrapper)

	ns0 = {
		"i": "http://www.w3.org/2001/XMLSchema-instance",
		"a": "http://schemas.datacontract.org/2004/07/Service.Dips_Rekvisisjon",
		"x": "http://ihelse.net/wcf/2015/09"
	}

	req_list = root.xpath("//a:Rekvisisjon", namespaces=ns0)

	keys = [
		"avdeling",
		"avd_reshid",
		"dokumentformat",
		"dokumenttype",
		"dokumenttypeid",
		"dokumentversjon",
		"foedselsnr",
		"foretak",
		"forfatter",
		"forfatterkode",
		"forfatter_hprnr",
		"forrigeid",
		"godkjentav",
		"godkjenttid",
		"henvisningid",
		"hfkortnavn",
		"journalid",
		"nprid",
		"recordtype",
		"setid",
		"sistendrettid",
		"skjema"
	]

	results = list()

	for req in req_list:
		req_dict = dict()
		for key in keys:
			res = req.xpath(f".//a:{key.upper()}/text()", namespaces=ns0)
			res_parsed = len(res) and res[0] or None
			req_dict[key] = res_parsed
		results.append(req_dict)

def parse_inner_document(inner_document):
	def p(s):
		return len(s) and s[0] or None

	root = etree.fromstring(inner_document)

	ns1 = {
		"xsi": "http://www.w3.org/2001/XMLSchema-instance",
		"p1": "http://www.w3.org/2001/XMLSchema-instance",
		"x": "http://schemas.openehr.org/v1" # def. x her, er i default i filen
	}

	contents = root.xpath("//x:content", namespaces=ns1)

	results = list()

	for content in contents:
		name = p(content.xpath(".//x:name/x:value/text()", namespaces=ns1))
		at = p(content.xpath(".//x:archetype_details/x:archetype_id/x:value/text()", namespaces=ns1))

		content_dict = dict(
			content_name=name,
			archetype_name=at
		)

		element_items = content.xpath(".//x:items[@xsi:type='ELEMENT']", namespaces=ns1)
		for element_item in element_items:
			name = p(element_item.xpath(".//x:name/x:value/text()", namespaces=ns1))
			value = p(element_item.xpath(".//x:value/x:value/text()", namespaces=ns1))

			content_dict[name] = value
		
		cluster_items = content.xpath(".//x:items[@xsi:type='CLUSTER']", namespaces=ns1)
		for cluster_item in cluster_items:
			element_items = cluster_item.xpath(".//x:items[@xsi:type='ELEMENT']", namespaces=ns1)
			for element_item in element_items:
				name = p(element_item.xpath(".//x:name/x:value/text()", namespaces=ns1))
				value = p(element_item.xpath(".//x:value/x:value/text()", namespaces=ns1))
				
				content_dict[name] = value

		results.append(content_dict)

	return results

def split_document(xml_file):
	with open(xml_file, "r", encoding="utf-8") as f:
		wrapper_xml = f.read()
		inner_documents = dict()

		pattern = r"<a:SKJEMA[^>]*>(.*?)</a:SKJEMA>"

		def replace_with_placeholder(match):
			index = len(inner_documents)
			placeholder = f"SKJEMA_CONTENTS_{index}"
			inner_documents[placeholder] = match.group(1).strip().replace(' encoding="utf-8"', "")
			return f"<a:SKJEMA>{placeholder}</a:SKJEMA>"

		modified_wrapper = re.sub(pattern, replace_with_placeholder, wrapper_xml, flags=re.DOTALL)
		
		return modified_wrapper, inner_documents


xml_file = "xml/rt_requisition.xml"

modified_wrapper, inner_documents = split_document(xml_file)
parse_outer_document(modified_wrapper)

parsed_inner_document = dict()
for name, inner_document in inner_documents.items():
	parsed_inner_document[name] = parse_inner_document(inner_document)