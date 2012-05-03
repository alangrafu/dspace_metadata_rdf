#!/usr/bin/python
from rdflib.graph import Graph
from rdflib.term import URIRef, Literal, BNode
from rdflib.namespace import Namespace, RDF, XSD
import csv
import sys
import re


class Ds2rdf:
  def __init__(self, csvFile):
    try:
      self.source = csvFile
      self.reader = csv.reader(open(csvFile, 'rb'), delimiter=',')
    except IOError as (errno, strerror):
      print >> sys,stderr, "I/O error({0}): {2} {1}".format(errno, strerror, csvFile)
      exit(1)
      

  def convert(self):
    store = Graph()
    store.bind("dc", "http://purl.org/dc/elements/1.1/")
    store.bind("data", "http://data.rpi.edu/vocab/")
    store.bind("owl", "http://www.w3.org/2002/07/owl#")
    store.bind("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
    store.bind("foaf", "http://xmlns.com/foaf/0.1/")
    store.bind("void", "http://rdfs.org/ns/void#")
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    OWL = Namespace("http://www.w3.org/2002/07/owl#")
    DATA = Namespace("http://data.rpi.edu/vocab/")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    VOID = Namespace("http://rdfs.org/ns/void#")
    header = self.reader.next()   #Skip header  
    minSize = len(header)
    #print header
    for row in self.reader:
      if len(row) != minSize:
        print >> sys.stderr,  "Number of columns different than header ({0} vs. {1}). Skipping".format(len(row), minSize)
        exit(1) #continue
      print >> sys.stderr, "Processing "+row[19]
      datasetUri = URIRef(row[14])
      if re.search("^http", row[3]):
        creator = URIRef(row[3])
        names = None
      else:
        if len(row[2]) > 0:
          people = row[2].split("||")
        else:
          del people[:]
          people.append(row[3])
          print >> sys.stderr, people
        for i in people:
          names = i.split(', ')
          token = ""
          if len(names) > 1:
            token = "id/"+names[1].capitalize().replace(" ", "_")+names[0].capitalize().replace(" ", "_")
            creator=URIRef("http://data.rpi.edu/"+token)
            store.add((creator, FOAF['firstName'], Literal(names[1])))
            store.add((creator, FOAF['lastName'], Literal(names[0])))
          else:
            if names != None:
              token = "id/"+names[0].capitalize().replace(" ", "_").replace(".", "")
              creator=URIRef("http://data.rpi.edu/"+token)
              store.add((creator, FOAF['name'], Literal(names[0])))
              store.add((creator, DC['title'], Literal(names[0])))
      store.add((datasetUri, DC['contributor'], creator))
      store.add((datasetUri, RDF['type'], VOID['Dataset']))
      if len(row[15]) > 0:
        store.add((datasetUri, OWL['sameAs'], URIRef(row[15])))
        store.add((datasetUri, RDFS['seeAlso'], URIRef(row[15])))
      if len(row[9]) > 0:
        store.add((datasetUri, RDFS['comments'], Literal(row[9])))
        store.add((datasetUri, DC['description'], Literal(row[9])))      
      if len(row[17]) > 0:
        subjects = row[17].split("||")
        backwardsCompatibleSubject = ", ".join(subjects)
        store.add((datasetUri, DC['subject'], Literal(backwardsCompatibleSubject)))
        for subject in subjects:
          store.add((datasetUri, DC['subject'], Literal(subject)))          
      if len(row[8]) > 0:
        store.add((datasetUri, DC['modified'], Literal(row[8],datatype=XSD.dateTime)))
      if len(row[7]) > 0:
        store.add((datasetUri, DC['issued'], Literal(row[7],datatype=XSD.date)))
      store.add((datasetUri, DC['title'], Literal(row[19])))
      store.add((datasetUri, RDFS['label'], Literal(row[19])))
    print(store.serialize(format="pretty-xml"))
    
d = Ds2rdf(sys.argv[1])
d.convert()
