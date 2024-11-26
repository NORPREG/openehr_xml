from asyncio.events import BaseDefaultEventLoopPolicy
from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, attr, computed_attr, computed_element, element
from datetime import datetime

from typing import Dict, List, Literal, Optional, Set, Tuple

ns = {
	"xsi": "http://www.w3.org/2001/XMLSchema-instance",
	"p1": "http://www.w3.org/2001/XMLSchema-instance",
	"": "http://schemas.openehr.org/v1" # def. x her, er i default i filen
}

class Value(BaseXmlModel, nsmap=ns):
	value: str

class ValueDT(BaseXmlModel, nsmap=ns):
	value: datetime

class Terminology_id_wrapper(BaseXmlModel, nsmap=ns):
	terminology_id: Value
	code_string: str

class ValueType(BaseXmlModel, nsmap=ns):
	xsi_type: str = attr(name="type", ns="xsi")
	value: str
	terminology_id: Optional[Terminology_id_wrapper]

class Uid(BaseXmlModel, nsmap=ns):
	xsi_type: str = attr(name="type", ns="xsi")
	value: str

class Archetype_details(BaseXmlModel, nsmap=ns):
	archetype_id: Value 
	template_id: Value
	rm_version: str

class Category(BaseXmlModel, nsmap=ns):
	value: Optional[str] = None
	defining_code: Optional[Terminology_id_wrapper] = None

class Composer(BaseXmlModel, nsmap=ns):
	xsi_type: str = attr(name="type", ns="xsi")
	name: str 

class Other_context(BaseXmlModel, nsmap=ns):
	xsi_type: str = attr(name="type", ns="xsi")
	archetype_node_id: str = attr()
	name: Value

class Context(BaseXmlModel, nsmap=ns):
	start_time: Value
	end_time: Value
	setting: Category
	other_context: Other_context

class Subject(BaseXmlModel, nsmap=ns):
	xsi_type: str = attr(name="type", ns="xsi")

class Items(BaseXmlModel, nsmap=ns):
	xsi_type: str = attr(name="type", ns="xsi")
	archetype_node_id: str = attr()

	name: Value
	value: ValueType

class Protocol(BaseXmlModel, nsmap=ns):
	xsi_type: Optional[str] = attr(name="type", ns="xsi")
	archetype_node_id: str = attr()

	name: Value 
	items: Items 

class Data(BaseXmlModel, nsmap=ns):
	xsi_type: str = attr(name="type", ns="xsi")
	archetype_node_id: str = attr()

	name: Value 
	items: Optional[List[Items]] = None

class Events(BaseXmlModel, nsmap=ns):
	name: Value 
	time: ValueDT 
	data: Data 

class DataEvent(BaseXmlModel, nsmap=ns):
	archetype_node_id: str = attr()

	name: Value 
	origin: Optional[ValueDT] 
	events: Optional[Events] 

class Items_entry(BaseXmlModel, nsmap=ns):
	xsi_type: str = attr(name="type", ns="xsi")
	archetype_node_id: str = attr()
	
	name: Value 
	archetype_details: Archetype_details 
	language: Terminology_id_wrapper 
	encoding: Terminology_id_wrapper 

	subject: Subject 
	data: Data 

class Items_Evaluation(BaseXmlModel, nsmap=ns):
	xsi_type: str = attr(name="type", ns="xsi")
	archetype_node_id: str = attr()
	
	name: Value 
	archetype_details: Archetype_details 
	language: Terminology_id_wrapper 
	encoding: Terminology_id_wrapper 

	subject: Subject 
	protocol: Protocol 
	data: Data 

class Content(BaseXmlModel, nsmap=ns):
	xsi_type: str = attr(name="type", ns="xsi")
	archetype_node_id: str = attr()

	name: Value 
	archetype_details: Archetype_details 
	items: Items 
	data: Optional[Data] = None

class composition(BaseXmlModel, nsmap=ns):
	p1_type: str = attr(name="type", ns="p1")
	archetype_node_id: str = attr()

	name: Value
	uid: Uid
	archetype_details: Archetype_details
	language: Terminology_id_wrapper
	territory: Terminology_id_wrapper
	category: Category
	composer: Composer
	context: Context
	content: Content

xml_file ='xml/report_example_auto_first_items.xml'


from lxml import objectify

with open(xml_file, 'r', encoding="utf-8") as file:
	xml_data = file.read().encode("utf-8")

print(xml_data.decode("utf-8"))

c = composition.from_xml_tree(xml_data)