from pydantic import BaseModel, Field
from datetime import datetime
import xmltodict
from pprint import pprint
from typing import List, Optional, Union

hide_metadata = True

class Terminology_id_wrapper(BaseModel):
	terminology_id: "Value"
	code_string: str

class Value(BaseModel):
	xsi_type: Optional[str] = Field(None, alias="@xsi:type", exclude=hide_metadata)

	terminology_id: Optional[Terminology_id_wrapper] = Field(None, exclude=hide_metadata)
	defining_code: Optional[Terminology_id_wrapper] = Field(None, exclude=hide_metadata)
	
	value: Optional[Union[str, datetime]] = None
	magnitude: Optional[str] = None
	units: Optional[str] = None
	symbol: Optional["Value"]


class Uid(BaseModel):
	xsi_type: str = Field(None, alias="@xsi:type", exclude=hide_metadata)
	value: str

class Archetype_details(BaseModel):
	archetype_id: Value
	template_id: Value
	rm_version: str

class Category(BaseModel):
	value: Optional[str] = None
	defining_code: Optional[Terminology_id_wrapper] = None

class Composer(BaseModel):
	xsi_type: str = Field(None, alias="@xsi:type", exclude=hide_metadata)
	name: str 

class Other_context(BaseModel):
	xsi_type: str = Field(None, alias="@xsi:type", exclude=hide_metadata)
	archetype_node_id: str = Field(None, alias="@archetype_node_id", exclude=hide_metadata)
	name: Value

class Context(BaseModel):
	start_time: Value
	end_time: Optional[Value]
	setting: Category = Field(exclude=hide_metadata)
	other_context: Other_context = Field(exclude=hide_metadata)

class Subject(BaseModel):
	xsi_type: str = Field(None, alias="@xsi:type", exclude=hide_metadata)

class Items(BaseModel):
	xsi_type: str = Field(None, alias="@xsi:type", exclude=hide_metadata)
	archetype_node_id: str = Field(None, alias="@archetype_node_id", exclude=hide_metadata)

	name: Value
	archetype_details: Optional[Archetype_details] = Field(None, exclude=hide_metadata)
	language: Optional[Terminology_id_wrapper] = Field(None, exclude=hide_metadata)
	encoding: Optional[Terminology_id_wrapper] = Field(None, exclude=hide_metadata)

	items: Optional[Union[List["Items"], "Items"]] = None

	subject: Optional[Subject] = Field(None, exclude=hide_metadata)
	protocol: Optional["Protocol"] = None
	data: Optional["Data"] = None

	value: Optional[Value] = None

class Protocol(BaseModel):
	xsi_type: str = Field(None, alias="@xsi:type", exclude=hide_metadata)
	archetype_node_id: str = Field(None, alias="@archetype_node_id", exclude=hide_metadata)

	name: Value 
	items: Items 

class Data(BaseModel):
	xsi_type: str = Field(None, alias="@xsi:type", exclude=hide_metadata)
	archetype_node_id: str = Field(None, alias="@archetype_node_id", exclude=hide_metadata)

	language: Optional[Terminology_id_wrapper] = Field(None, exclude=hide_metadata)
	encoding: Optional[Terminology_id_wrapper] = Field(None, exclude=hide_metadata)

	name: Value 
	items: Optional[Union[List[Items], Items]] = None

	origin: Optional[Value] = None
	events: Optional["Events"] = None

class Events(BaseModel):
	xsi_type: str = Field(None, alias="@xsi:type", exclude=hide_metadata)
	archetype_node_id: str = Field(None, alias="@archetype_node_id", exclude=hide_metadata)	

	name: Value
	time: Value
	data: Data

class Content(BaseModel):
	xsi_type: str = Field(None, alias="@xsi:type", exclude=hide_metadata)
	archetype_node_id: str = Field(None, alias="@archetype_node_id", exclude=hide_metadata)

	name: Value 
	archetype_details: Archetype_details = Field(exclude=hide_metadata)
	items: Optional[List[Items]] = None
	data: Optional[Data] = None

class Composition(BaseModel):
	p1_type: str = Field(None, alias="@p1:type")
	archetype_node_id: str = Field(None, alias="@archetype_node_id", exclude=hide_metadata)

	name: Value
	uid: Uid = Field(exclude=hide_metadata)
	archetype_details: Archetype_details = Field(exclude=hide_metadata)
	language: Terminology_id_wrapper = Field(exclude=hide_metadata)
	territory: Terminology_id_wrapper = Field(exclude=hide_metadata)
	category: Category
	composer: Composer
	context: Context
	content: List[Content]

xml_file ='xml/report_example_auto.xml'

Terminology_id_wrapper.update_forward_refs()
Value.update_forward_refs()
Items.update_forward_refs()
Data.update_forward_refs()
Composition.update_forward_refs()
# Composition.model_validate()