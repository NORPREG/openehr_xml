from lxml import etree
from pprint import pprint
import xmltodict, json



xml_file = "xml/report_example_auto.xml"
parse_document(xml_file)

pprint(xml_dict)
