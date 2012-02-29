#!/usr/bin/python
from rdflib.graph import Graph
from rdflib.term import URIRef, Literal, BNode
from rdflib.namespace import Namespace, RDF
import csv
import sys
import re


class Ds2rdf:
  def __init__(self, csvFile):
    try:
      self.source = csvFile
      self.reader = csv.reader(open(csvFile, 'rb'), delimiter=',')
#      for row in self.reader:
#        print ', '.join(row)
    except IOError as (errno, strerror):
      print "I/O error({0}): {2} {1}".format(errno, strerror, csvFile)
      exit(0)
  def convert(self):
    store = Graph()
    store.bind("dc", "http://purl.org/dc/elements/1.1/")
    store.bind("data", "http://data.rpi.edu/vocab/")
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    DATA = Namespace("http://data.rpi.edu/vocab/")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    header = self.reader.next()   #Skip header  
    minSize = len(header)
    #print header
    for row in self.reader:
      if len(row) != minSize:
        print "Number of columns different than header ({0} vs. {1}). Skipping".format(len(row), minSize)
        continue
      store.add((row[8], DC['identifier'], Literal(row[0])))
      names = row[2].split(", ")
      creator=URIRef("http://data.rpi.edu/people/"+names[0].capitalize()+names[1].capitalize())
      store.add((row[8], DC['creator'], creator))
      store.add((creator, FOAF['firstName'], names[0]))
      store.add((creator, DC['family_name'], names[1]))
      store.add((row[8], DC['dateAccepted'], Literal(row[5])))
      store.add((row[8], RDFS['comments'], Literal(row[6])))
      store.add((row[8], DC['description'], Literal(row[6])))
      store.add((row[8], DC['bibliographicCitation'], Literal(row[7])))
      store.add((row[8], DC['title'], Literal(row[10])))
      store.add((row[8], RDFS['label'], Literal(row[10])))
      store.add((row[8], DC['subject'], URIRef(DATA+re.sub("\s", "_", row[9]))))
    print(store.serialize(format="pretty-xml"))
    
d = Ds2rdf(sys.argv[1])
d.convert()
