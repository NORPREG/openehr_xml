from unittest.util import strclass
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import date, datetime

class Metadata(BaseModel):
	xml_timestamp: datetime
	xml_version_major: int = 0
	xml_version_minor: int = 3

class Demographics(BaseModel):
	rt_center: str
	referring_hf: str
	birth_year: int
	sex: Literal["mann", "kvinne"]
	weight_at_diagnosis_kg: float
	height_cm: float
	patient_id_fnr: str

class Social(BaseModel):
	education_level: Literal[
		"Ingen utdanning",
		"Grunnskole",
		"Videregående",
		"Universitet/høyskole <4 år",
		"Universitet/høyskole >=4 år",
		"Ukjent"
	]

	martial_status: Literal[
		"Ugift",
		"Gift / Registrert partner",
		"Enke / enkemann / gjenlevende partner",
		"Skilt",
		"Separert",
		"Ukjent"
	]

	living_arrangements: Literal[
		"Ikke i parforhold",
		"Samboer/lever i parforhold",
		"Parforhold, lever ikke sammen / særbo",
		"Ukjent"
	]

	

class Stimulantia(BaseModel):
	smoking_status: Literal[
		"Aldri røykt",
		"Røyker",
		"Tidligere røyker"
	]

	pack_years: int
	month_since_stopping: Optional[int] = None
	non_smoking_tobacco_status: Literal[
		"Aldri brukt",
		"Nåværende bruker",
		"Tidligere bruker"
	]
	
	# Evaluation.Alkoholanamnese_v1 @ CKM
	alcohol_abuse: Literal[
		"Nåværende bruker",
		"TIdligere bruker",
		"Aldri brukt"
	]

class FunctionStatus(BaseModel):
	ecog_grade: Literal[0,1,2,3,4,5]
	ecog_date: date

class Comorbidity(BaseModel):
	comorbidity_name: Optional[str] = None
	comorbidity_code: Optional[str] = None
	comorbidity_term: Optional[str] = None
	comorbidity_terminology_version: Optional[str] = None

	comorbidity_category: Optional[str] = None
	comorbidity_date: date

class PrimaryDiagnosis(BaseModel):
	diagnosis_name: str
	diagnosis_code: str
	diagnosis_term: str
	diagnosis_edition: str
	multiple_primaries: bool
	
#	diagnosis_laterality: Optional[str] = None
	diagnosis_localisation: Optional[str] = None
	diagnosis_date: date
	diagnosis_method: str
#	diagnosis_comment: Optional[str] = None

class Staging(BaseModel):
	tnm_t: str
	tnm_n: str
	tnm_m: str

	tnm_string: str
	tnm_edition: str
	tnm_stage: Optional[str] = None
	
	# Brukes U, yC, yP i Norge?
	tnm_type: Literal["C", "P", "U", "yC", "yP"]
	other_type: Optional[str] = None
	other_grade: Optional[str] = None
	is_relapse: bool
	staging_date: date

class Metastasis(BaseModel):
	metastasis_diagnosed: bool
	metastasis_localisation: Optional[str]

class Histology(BaseModel):
	histological_celltype_code: str
	histological_celltype_description: str
	topographical_mapping_code: str
	topographical_mapping_description: str

class Genetics(BaseModel):
	amino_acid_changes: str

class PreviousCancerItem(BaseModel):
	previous_cancer_icd10_code: str
	previous_cancer_icd10_description: str
	previous_cancer_laterality: Optional[str] = None
	previous_cancer_localisation: Optional[str] = None
	previous_cancer_diagnosis_year: int
	previous_cancer_rt_given: bool
#	previous_cancer_comment: Optional[str] = None

class PreviousCancer(BaseModel):
	is_previous_cancer: bool
	previous_cancer: List[PreviousCancerItem]

class TreatmentRadiotherapy(BaseModel):
	course_id: str
	procedure_nkpk_code: str
	procedure_nkpk_description: str
#	comment: Optional[str] = None

class TreatmentSurgery(BaseModel):
	procedure_nkpk_code: str
	procedure_nkpk_description: str
	surgery_target: Literal[
		"Primærtumor",
		"Lokalt residiv og primærtumor",
		"Metastase"
	]
	surgery_date: date
#	comment: Optional[str] = None

class TreatmentSystemic(BaseModel):
	"""Legemiddel versus MKB?"""

	systemic_name: str # navn på legemiddel / virkestoff / kur
	category: Literal[
		"Kjemoterapi",
		"Immunterapi",
		"Hormonell behandling",
		"Målrettet terapi / small molecules"
	]

	therapeutic_intent: Literal[
		"Preoperativt",
		"Postoperativt"
	]

	total_dosage_value: float
	total_dosage_unit: str
	dosage_start_date: date
	dosage_stop_date: date
#	comment: Optional[str] = None

class TreatmentSummary(BaseModel):
	treatment_intention: Literal[
		"Kurativt",
		"Ikke kurativt (livsforlengende)",
		"Ikke kurativt (symptomlindrende)",
		"Ikke kurativt (lokalkontroll)"
	]
	treatment_type: Literal[
		"Neoadjuvant", 
		"Konkomitant", 
		"Adjuvant", 
		"Neoadjuvant + konkomitant", 
		"Neoadjuvant + adjuvant", 
		"Konkomitant + adjuvant", 
		"Neoadjuvant + konkomitant + adjuvant"
	]

	treatment_radiotherapy: Optional[TreatmentRadiotherapy] = None
	treatment_systemic: Optional[TreatmentSystemic] = None
	treatment_surgery: Optional[TreatmentSurgery] = None

class BiologicalSample(BaseModel):
	requisition_remissenr: str
	sample_laboratory: Optional[str] = None
	conclusion: str
	sample_date: date
	sample_type: Optional[Literal["Celler (cytologi)", "Vev", "Annet materiale"]] = None
	sample_anatomical_location: Optional[str] = None
	sample_tumorcells_percentage: Optional[float] = None
#	sample_comment: Optional[str] = None

class Biomarker(BaseModel):
	biomarker_name: str
	# biomarker_type: Literal["Diagnose", "Prognose", "Prediksjon"]
	biomarker_value: Optional[float] = None
	biomarker_unit: Optional[str] = None
	biomarker_result: Optional[Literal["Positiv", "Negativ", "Ikke undersøkt"]] = None
	biomarker_method: Optional[str] = None
#	comment: Optional[str] = None

class CTCAE(BaseModel):
	ctcae_date: date
	meddra_category: Optional[str] = None
	meddra_name: Optional[str] = None
	ctcae_grade: Literal[0,1,2,3,4,5]
	ctcae_terminology_version: Optional[str] = None
	meddra_terminology_version: Optional[str] = None
#	comment: Optional[str] = None

class VitalStatus(BaseModel):
	last_followup: Optional[date] = None # siste polikliniske kontakt
	mors_date: Optional[date] = None

class TumorEvent(BaseModel):
	progression_date: date
	progression_type: Literal["Progresjon", "Residiv"]
	progression_identification: Optional[
		Literal[
			"Histologi",
			"Radiologi",
			"Klinikk",
			"Biokjemisk",
			"Ukjent"
		]
	]
	progression_grade: Literal[
		"Lokal progresjon",
		"Regional progresjon",
		"Fjernmetastase"
	]
#	comment: Optional[str] = None
	
class Consent(BaseModel):
	informed_patient_about_rt_registry: bool
	informed_patient_about_broad_consent: bool

class ClinicalStudy(BaseModel):
	study_name: str
	study_contact_person: Optional[str] = None
#	comment: Optional[str] = None


class Course(BaseModel):
	metadata: Metadata
	demographics: Optional[Demographics] = None
	social: Optional[Social] = None
	stimulantia: Optional[Stimulantia] = None
	function_status: Optional[FunctionStatus] = None
	comorbidity: Optional[List[Comorbidity]] = None
	primary_diagnosis: Optional[PrimaryDiagnosis] = None
	staging: Optional[List[Staging]] = None
	metastasis: Optional[Metastasis] = None
	histology: Optional[List[Histology]] = None
	genetics: Optional[List[Genetics]] = None
	previous_cancer: Optional[PreviousCancer] = None
	treatment_summary: Optional[List[TreatmentSummary]] = None
	biological_sample: Optional[List[BiologicalSample]] = None
	biomarker: Optional[List[Biomarker]] = None
	ctcae: Optional[List[CTCAE]] = None
	vital_status: Optional[VitalStatus] = None
	tumor_event: Optional[List[TumorEvent]] = None
	consent: Optional[Consent] = None
	clinical_studies: Optional[List[ClinicalStudy]] = None