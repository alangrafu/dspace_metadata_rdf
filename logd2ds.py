#!/usr/bin/python
import sys
import traceback
from SPARQLWrapper import SPARQLWrapper, JSON

class Logd2ds:
  def __init__(self, endpoint = "http://logd.tw.rpi.edu:8890/sparql"):
    self.endpoint = endpoint
    self.collection = 18234


  def getSubjects(self):
    print >> sys.stderr, "Getting datasets' subjects"
    keywords = {}
    sparql = SPARQLWrapper(self.endpoint)
    sparql.setQuery("""
PREFIX foaf:       <http://xmlns.com/foaf/0.1/>
PREFIX dcterms:    <http://purl.org/dc/terms/>
PREFIX conversion: <http://purl.org/twc/vocab/conversion/>
PREFIX catalog:    <http://logd.tw.rpi.edu/source/twc-rpi-edu/dataset/dataset-catalog/vocab/enhancement/1/>
PREFIX ds92:       <http://logd.tw.rpi.edu/source/data-gov/dataset/92/vocab/enhancement/1/>

SELECT DISTINCT
        ?dataset
        ?subject
WHERE { 
        GRAPH <http://logd.tw.rpi.edu/vocab/Dataset> {
                ?dataset
                        a conversion:Dataset
        }
        GRAPH <http://purl.org/twc/vocab/conversion/MetaDataset> {
                ?dataset dcterms:subject ?subject 
        }
}
""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
      d =result['dataset']['value']
      if d in keywords:
        keywords[d] += "||"+result['subject']['value']
      else:
        keywords[d] = result['subject']['value']
    return keywords

  def getMetadata(self):
    keywords = self.getSubjects()
    print >> sys.stderr, "Getting datasets' metadata"
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
        (MIN(?hp) AS ?page)
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
                OPTIONAL { ?dataset foaf:isPrimaryTopicOf ?hp }
	}
	GRAPH <http://purl.org/twc/vocab/conversion/MetaDataset> {
		?dataset dcterms:title ?Title .
		?dataset dcterms:description ?Description.
		?dataset catalog:source_agency [ rdfs:label ?Agency ]
		OPTIONAL { ?dataset catalog:dataset_category ?cat }
		OPTIONAL { ?dataset dcterms:subject ?subj }
		OPTIONAL { ?dataset catalog:reused_source_identifiers ?reused }
	}
#		?contrib rdfs:label ?source .
}
GROUP BY ?dataset
ORDER BY ?dataset
#LIMIT 50
""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print """filename,dc.publisher,dc.contributor,dc.date.accessioned,dc.date.available,dc.date.issued,dc.description.provenance,dc.identifier.citation,dc.identifier.uri,dc.subject,dc.title,dc.description,dc.type"""
    id=1
    for result in results["results"]["bindings"]:
      try:
        da=result["dataset"]["value"]
        p=result["page"]["value"]
        t=result["dataset_title"]["value"]
        s=result["source_name"]["value"]
        d=result["modified"]["value"]
        desc=result["desc"]["value"]
        if "subject" in result:
          sub=keywords[da]
        else:
          sub=""
        print ',"http://logd.tw.rpi.edu","%s","%s","%s","%s","","","%s","%s","%s","%s","Dataset"' % (s,d,d,d,da,sub,t,desc)
      #result["dataset"]["value"],result["modified"]["value"])   
      except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

        exit(10)
      id=id+1


l2d = Logd2ds()
l2d.getMetadata()
