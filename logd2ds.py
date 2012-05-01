#!/usr/bin/python
from SPARQLWrapper import SPARQLWrapper, JSON

class Logd2ds:
  def __init__(self, endpoint = "http://logd.tw.rpi.edu/sparql"):
    self.endpoint = endpoint
    self.collection = 18234

  def getMetadata(self):
    sparql = SPARQLWrapper(self.endpoint)
    sparql.setQuery("""
PREFIX foaf:       <http://xmlns.com/foaf/0.1/>
PREFIX dcterms:    <http://purl.org/dc/terms/>
PREFIX conversion: <http://purl.org/twc/vocab/conversion/>
PREFIX catalog:    <http://logd.tw.rpi.edu/source/twc-rpi-edu/dataset/dataset-catalog/vocab/enhancement/1/>
PREFIX ds92:       <http://logd.tw.rpi.edu/source/data-gov/dataset/92/vocab/enhancement/1/>

SELECT DISTINCT
	?dataset
	(MIN(?Dataset_Identifier) AS ?identifier)
	(MAX(?Dataset_Modified) AS ?modified)
	(MIN(?source) AS ?source_name)
	(MIN(?Description) AS ?desc)
	(MIN(?Title) AS ?dataset_title)
	(MIN(?subj) AS ?subject)
WHERE {
	GRAPH <http://logd.tw.rpi.edu/vocab/Dataset> {
		?dataset
			a conversion:Dataset;
			conversion:dataset_identifier ?Dataset_Identifier ;
			void:subset ?version ;
			dcterms:modified ?Dataset_Modified;
			dcterms:contributor ?source .
		?version a conversion:VersionedDataset .
		?version void:subset  ?layer .
	}
	GRAPH <http://purl.org/twc/vocab/conversion/MetaDataset> {
		?dataset dcterms:title ?Title .
		?dataset dcterms:description ?Description.
		?dataset catalog:source_agency [ rdfs:label ?Agency ]
		OPTIONAL { ?dataset catalog:dataset_category ?cat }
		OPTIONAL { ?dataset dcterms:subject ?subj }
		OPTIONAL { ?dataset foaf:homepage ?hp }
		OPTIONAL { ?dataset catalog:reused_source_identifiers ?reused }
	}
#		?contrib rdfs:label ?source .
}
GROUP BY ?dataset
ORDER BY ?dataset
LIMIT 5
""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print """filename,dc.contributor.author,dc.date.accessioned,dc.date.available,dc.date.issued,dc.description.provenance,dc.identifier.citation,dc.identifier.uri,dc.subject,dc.title,dc.type"""
    id=1
    for result in results["results"]["bindings"]:
      da=result["dataset"]["value"]
      t=result["dataset_title"]["value"]
      s=result["source_name"]["value"]
      d=result["modified"]["value"]
      desc=result["desc"]["value"]
      sub=result["subject"]["value"]
      print ',"%s","%s","%s","%s","","","%s","%s","%s","Data"' % (s,d,d,d,da,sub,t)
      #result["dataset"]["value"],result["modified"]["value"])   
      id=id+1
l2d = Logd2ds()
l2d.getMetadata()
