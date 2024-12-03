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


def extract_datamodel(dips):
	data_model = dict()
	d = dips["content"]["Sosialanamnese_generell"]

	arb = d.get("Arbeidsstatus", {})

	sosialt = {
		"Høyeste fullførte utdanningsnivå": find(d, "Høyeste fullførte utdanningsnivå"),
		"Arbeidsstatus": find(d, "Arbeidsstatus"),
		"Yrke tittel/rolle": find(d, "Tittel/rolle"),
		"Yrkeskategori": find(d, "Yrkeskategori"),
		"Sykemelding startdato": find(arb.get("Sykemelding", {}), "Startdato"),
		"Sykemelding varighet": find(arb.get("Sykemelding", {}), "Varighet"),
		"Juridisk sivilstatus": find(d, "Juridisk sivilstand"),
		"Samlivsstatus": find(d, "Samlivsstatus"),
		"Hvilken samlivsform har pasienten?": find(d, "Hvilken samlivsform har pasienten?"),
		"Samlivsform, tilstede?": find(d, "Tilstede?")
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

	komorbiditet = {
		"Har pasienten kjent komorbiditet?": find(d, "Har pasient kjent komorbiditet?"),
		# Legg til flere når jeg ser hvordan det er modellert
	}

	seneffekter = list()
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

		seneffekter.append(ctcae)

	p = d.get("Problem/diagnose (inkl TNM)", {})
	pTNM = p.get("TNM-klassifikasjon klinisk", {})
	cTNM = p.get("TNM-klassifikasjon pataologi", {})

	primaer_diagnose = {
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
		"Patologisk T": find(cTNM, "Primærtumor (pT)"),
		"Patologisk N": find(cTNM, "Regionale lymfeknuter (pN)"),
		"Patologisk M": find(cTNM, "Fjernmetastase (pM)"),
		"Patologisk residiv": find(cTNM, "Residiv (r)"),
		"Patologisk TNM-vurdering": find(cTNM, "pTNM-vurdering"),
		"Patologisk TNM-utgave": find(cTNM, "TNM-utgave"),
	}

	utr = d.get("Lymfeknutemetastase", {}).get("Utredningsmetode regionale lymfeknutemetastaser", {})
	lymfeknutemetastase = {
		"Regional lymfeknutemetastase": find(d, "Regional lymfeknutemetastase"),
		"Metode": [v for k,v in utr.items() if "Metode" in k],
		"Funn": find(utr, "Funn")
	}

	data_model["sosialt"] = sosialt
	data_model["stimulantia"] = stimulantia
	data_model["komorbiditet"] = komorbiditet
	data_model["seneffekter"] = seneffekter
	data_model["primærdiagnose"] = primaer_diagnose


	sa = data_model["Sosialanamnese_generell"] = dict()
	d = dips["content"]["Sosialanamnese_generell"]
	for k,v in d.items():
		if k == "Barn under 18":
			keys = [
				"Omsorgsperson for barn under 18 år",
				"Omsorgsperson for personer over 18 år"
			]
			for key in keys:
				sa[key] = find(d, key)
		elif "items" in v:
			for kk, vv in v["items"].items():
				sa[kk] = vv
		else:
			sa[k] = v

	sa["Fritekst relatert til sosial anamnese"] = find(sa["Fritekst relatert til sosial anamnese"], "items")
	sa["Hvilken samlivsform har pasienten?"] = find(sa["Samlivsform"], "Hvilken samlivsform har pasienten?")
	sa["Samlivsform, tilstede?"] = find(sa["Samlivsform"], "Tilstede?")
	del sa["Samlivsform"]

	data_model["Stimulantia"] = dict()
	st = data_model["Stimulantia"] = dict()
	d = dips["content"]["Stimulantia"]

	for k,v in d.items():
		st[k] = v

	return data_model

