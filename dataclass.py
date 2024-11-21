from asyncio.events import BaseDefaultEventLoopPolicy
from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, attr, computed_attr, computed_element, element
from datetime import datetime

from typing import Dict, List, Literal, Optional, Set, Tuple

class Value(BaseXmlModel):
	value: str = element()

class ValueDT(BaseXmlModel):
	value: datetime = element()

class Terminology_id_wrapper(BaseXmlModel):
	terminology_id: Value = element()
	code_string: str = element()

class ValueType(BaseXmlModel):
	xsi_type: str = attr(name="xsi:type")
	value: str = element()
	terminology_id: Optional[Terminology_id_wrapper] = element()

class Uid(BaseXmlModel):
	xsi_type: str = attr(name="xsi_type")
	value: str = element()

class Archetype_details(BaseXmlModel):
	archetype_id: Value = element()
	template_id: Value = element()
	rm_version: str = element()

class Category(BaseXmlModel):
	value: str = element()
	defining_code: Terminology_id_wrapper = element()

class Composer(BaseXmlModel):
	xsi_type: str = attr(name="xsi:type")
	name: str = element()

class Other_context(BaseXmlModel):
	xsi_type: str = attr(name="xsi:type")
	archetype_node_id: str = attr()
	name: Value = element()

class Context(BaseXmlModel):
	start_time: Value = element()
	setting: Category = element()
	other_context: Other_context = element()

class Subject(BaseXmlModel):
	xsi_type: str = attr(name="xsi:type")

class Items_element(BaseXmlModel):
	archetype_node_id: str = attr()
	name: Value = element()
	value: ValueType = element()
	
class Items_cluster(BaseXmlModel):
	archetype_details: Archetype_details = element()


class Data(BaseXmlModel):
	xsi_type: Optional[str] = attr(name="xsi:type")
	archetype_node_id: str = attr()

	name: Value = element()
	items: List[Items_cluster] = element()

class Events(BaseXmlModel):
	name: Value = element()
	time: ValueDT = element()
	data: Data = element()

class DataEvent(BaseXmlModel):
	archetype_node_id: str = attr()

	name: Value = element()
	origin: Optional[ValueDT] = element()
	events: Optional[Events] = element()

class Items_entry(BaseXmlModel):
	xsi_type: str = attr(name="xsi:type")
	archetype_node_id: str = attr()
	
	name: Value = element()
	archetype_details: Archetype_details = element()
	language: Terminology_id_wrapper = element()
	encoding: Terminology_id_wrapper = element()

	subject: Subject = element()
	data: Data = element()

class Content(BaseXmlModel):
	xsi_type: str = attr(name="xsi:type")
	archetype_node_id: str = attr()

	name: Value = element()
	archetype_details: Archetype_details = element()
	items: Items_entry = element()
	data: Optional[DataEvent] = element()

class Composition(BaseXmlModel):
	nsmap = {
		"xsi": "http://www.w3.org/2001/XMLSchema-instance",
		"p1": "http://www.w3.org/2001/XMLSchema-instance",
		"": "http://schemas.openehr.org/v1"
	}
	p1_type: str = attr(name="p1:type")
	archetype_node_id: str = attr()

	name: Value = element()
	uid: Uid = element()
	archetype_details: Archetype_details = element()
	language: Terminology_id_wrapper = element()
	territory: Terminology_id_wrapper = element()
	category: Category = element()
	composer: Composer = element()