import random
import csv

from SPARQLWrapper import JSON, SPARQLWrapper
from collections import defaultdict


WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")


prefix = """
	PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wds: <http://www.wikidata.org/entity/statement/>
    PREFIX wdv: <http://www.wikidata.org/value/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

test_num = 100

def write_csv(fname, data):
	with open(fname, 'w') as f:
		write = csv.writer(f)    
		write.writerows(data)

def query_sparql(query):
	sparql.setQuery(prefix+query)
	sparql.setReturnFormat(JSON)

	results = sparql.query().convert()

	return results



def print_examples(training_data, test):
	num = 2
	print("training_data_example")
	for x in range(num):
		print(training_data[x])

	print()	
	print("test_data_example")
	for x in range(num):
		print(test[x])

def getPronouns(gender, val_type="subj"):
	if gender == "female":
		if val_type == "subj":
			return "she"
		elif val_type == "poss" or val_type == "obj":
			return "her"
	elif gender == "male":
		if val_type == "subj":
			return "he"
		elif val_type == "poss":
			return "his"
		elif val_type == "obj":
			return "him"
	else:
		if val_type == "subj":
			return "they"
		elif val_type == "poss":
			return "their"
		elif val_type == "obj":
			return "them"
	return "they"