from re import T
from module.register_datamodel import (
	Metadata,
	Demographics,
	Social,
	Stimulantia,
	FunctionStatus,
	Comorbidity,
	PrimaryDiagnosis,
	Staging,
	Metastasis,
	Histology,
	Genetics,
	PreviousCancerItem,
	PreviousCancer,
	TreatmentRadiotherapy,
	TreatmentSurgery,
	TreatmentSystemic,
	TreatmentSummary,
	BiologicalSample,
	Biomarker,
	CTCAE,
	VitalStatus,
	TumorEvent,
	Consent,
	ClinicalStudy,
	Course
)

def find_end(d):
	if isinstance(d, dict):
		for key, value in d.items():
			if isinstance(value, (dict, list)):
				return find_end(value)
			else:
				return value

def find(d, target_key):
	"""Retrieve the end node value from a dictionary given a higher-level key."""
	if isinstance(d, dict):
		# Traverse each key-value pair in the dictionary
		for key, value in d.items():
			# If the current key matches the target key, and the value is not a dictionary/list, return it
			if key == target_key:
				if isinstance(value, (dict, list)):
					# Recursively traverse further if value is a nested structure
					return find_end(value)
				else:
					return value
			else:
				# Continue recursively if the key does not match
				result = find(value, target_key)
				if result is not None:
					return result
	
	elif isinstance(d, list):
		# Process each item in the list if the input is a list
		for item in d:
			result = find(item, target_key)
			if result is not None:
				return result
	
	return None  # Return None if no match is found

# TODO: Klarer vi å putte alle hardkodede paths under inn i en configfil?


def extract_datamodel(dips):
	data_model = dict()
	d = dips["content"]

	soc = d.get("Sosialanamnese_generell")
	arb = soc.get("Arbeidsstatus", {})
	social = {
		"Høyeste fullførte utdanningsnivå": find(soc, "Høyeste fullførte utdanningsnivå"),
		"Arbeidsstatus": find(soc, "Arbeidsstatus"),
		"Yrke tittel/rolle": find(soc, "Tittel/rolle"),
		"Yrkeskategori": find(soc, "Yrkeskategori"),
		"Sykemelding startdato": find(arb.get("Sykemelding", {}), "Startdato"),
		"Sykemelding varighet": find(arb.get("Sykemelding", {}), "Varighet"),
		"Juridisk sivilstatus": find(soc, "Juridisk sivilstand"),
		"Samlivsstatus": find(soc, "Samlivsstatus"),
		"Hvilken samlivsform har pasienten?": find(soc, "Hvilken samlivsform har pasienten?"),
		"Samlivsform, tilstede?": find(soc, "Tilstede?")
	}
	
	stimulantia = {
		"Alkoholanamnese status": find(d.get("Stimulantia", {}).get("Alkoholanamnese"), "Overordnet status"),
		"Alkoholanamnese typisk bruk verdi": find(d.get("Stimulantia", {}).get("Alkoholanamnese"), "magnitude"),
		"Alkoholanamnese typisk bruk enhet": find(d.get("Stimulantia", {}).get("Alkoholanamnese"), "units"),
		"Røykeanamnese status": find(d.get("Stimulantia", {}).get("Røykeanamnese"), "Overordnet status"),
		"Røykeanamnese typisk bruk verdi": find(d.get("Stimulantia", {}).get("Røykeanamnese"), "magnitude"),
		"Røykeanamnese typisk bruk enhet": find(d.get("Stimulantia", {}).get("Røykeanamnese"), "name"),
		"Røykfri tobakkanamnese status": find(d.get("Stimulantia", {}).get("Røykfri tobakkanamnese"), "Overordnet status")	
	}

	comorb_keys = [k for k in d.get("Komorbiditet_utredning", {}) if "Forholdsregel" in k]

	kom = d.get("Komorbiditet_utredning", {})
	comorbidity = {
		"Har pasienten kjent komorbiditet?": find(d, "Har pasient kjent komorbiditet?"),

		# Denne er ikke god. I UI skilles det mellom kategori (ICD10 kapittel) og tilstand (ICD10 kode)
		# Hver av dem har en kommentar ("detaljer") til seg som ikke bør lagres?
		
		# Alle items må parses slik at de grupperes i videre behandling

		"items": [
			{
				"Sykdomskategori": v.get("Sykdomskategori"), 
				"Sykdomstilstand": v.get("Tilstand"),	
			} for k,v in kom.items() if "Forholdsregel" in k
		],

		"ICD10 symbol": [v.get("Tilstand") for k,v in kom.get("ICD10", {}).items() if "Forholdsregel" in k],
	}

	cci = {"items": []}

	for item in kom.get("Charlson Comorbidity Index (CCI)", {}).get("items", []):
		new_dict = dict()
		new_dict["Kategori"] = item["name"]
		if "value" in item:
			new_dict["Verdi"] = item["value"]
		if "symbol" in item:
			new_dict["Symbol"] = item["symbol"]
		if "magnitude" in item:
			assert "value" not in item
			new_dict["Verdi"] = item["magnitude"]
		if "units" in item:
			new_dict["Enhet"] = item["units"]
		cci["items"].append(new_dict)

	late_effects = list()
	for k,v in d.get("Problem/diagnose", {}).items():
		if not "CTCAE" in k:
			continue

		ctcae = {
			"Kategori": find(v, "Kategori"),
			"Term": find(v, "Term"),
			"Grad": find(v, "value"),
			"Grad symbol": find(v, "symbol"),
			"Beskrivelse av grad": find(v, "Beskrivelse av grad"),
			"CTCAE versjon": find(v, "CTCAE- versjon")
		}

		late_effects.append(ctcae)

	p = d.get("Problem/diagnose (inkl TNM)", {})
	cTNM = p.get("TNM-klassifikasjon klinisk", {})
	pTNM = p.get("TNM-klassifikasjon patologi", {})

	primary_diagnosis = {
		"diagnose": find(p, "Problem/diagnosenavn"),
		"Anatomisk lokalisering": find(p, "Anatomisk lokalisering"),
		"Dato/tid for klinisk bekreftelse": find(p, "Dato/tid for klinisk bekreftelse"),
		"Multiple primærtumorer": find(p, "Multiple primærtumorer"),
		"Klinisk T": find(cTNM, "Primærtumor (T)"),
		"Klinisk N": find(cTNM, "Regionale lymfeknuter (N)"),
		"Klinisk M": find(cTNM, "Fjernmetastase (M)"),
		"Klinisk residiv": find(cTNM, "Residiv (r)"),
		"Klinisk TNM-vurdering": find(cTNM, "TNM-vurdering"),
		"Klinisk TNM-utgave": find(cTNM, "TNM-utgave"),
		"Patologisk T": find(pTNM, "Primærtumor (pT)"),
		"Patologisk N": find(pTNM, "Regionale lymfeknuter (pN)"),
		"Patologisk M": find(pTNM, "Fjernmetastase (pM)"),
		"Patologisk residiv": find(pTNM, "Residiv (r)"),
		"Patologisk TNM-vurdering": find(pTNM, "pTNM-vurdering"),
		"Patologisk TNM-utgave": find(pTNM, "TNM-utgave"),
	}

	utr = d.get("Lymfeknutemetastase", {}).get("Utredningsmetode regionale lymfeknutemetastaser", {})
	lymph_node_metastases = {
		"Regional lymfeknutemetastase": find(d, "Regional lymfeknutemetastase"),
		"Metode": [v for k,v in utr.items() if "Metode" in k],
		"Funn": find(utr, "Funn")
	}

	utr = d.get("Fjernmetastaser", {}).get("Utredningsmetode fjernmetastaser", {})
	distant_metastases = {
		"Fjernmetastaser": find(d, "Fjernmetastaser"),
		"Funn": find(utr, "Funn"),
		"Metode": [v for k,v in utr.items() if "Metode" in k],
		"Anatomisk lokalisasjon": [v.get("Navn på kroppssted") for k,v in utr.items() if "anatomisk lokalisajson" in k],
	}

	ecog = {
		"ECOG verdi": find(d.get("ECOG funksjonsstatus", {}), "value"),
		"ECOG symbol": find(d.get("ECOG funksjonsstatus", {}), "symbol"),
		"ECOG tidspunkt": find(d.get("ECOG funksjonsstatus", {}), "time"),
	}

	data_model["sosialt"] = social
	data_model["stimulantia"] = stimulantia
	data_model["komorbiditet"] = comorbidity
	data_model["CCI"] = cci
	data_model["seneffekter"] = late_effects
	data_model["primærdiagnose"] = primary_diagnosis
	data_model["lymeknutemetastase"] = lymph_node_metastases
	data_model["fjernmetastaser"] = distant_metastases
	data_model["ECOG"] = ecog

	return data_model


