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
      self.store = None
      self.source = csvFile
      self.reader = csv.reader(open(csvFile, 'rb'), delimiter=',')
    except IOError as (errno, strerror):
      print >> sys.stderr, "I/O error({0}): {2} {1}".format(errno, strerror, csvFile)
      exit(1)
      

  def subjectProcessor(self, root, value):
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    a = value.split("||")
    for i in a:
     self.store.add((root, DC['subject'], Literal(i)))

  def convert(self):
    self.store = Graph()
    processors = {}
    processors['subject'] = self.subjectProcessor
    self.store.bind("dc", "http://purl.org/dc/elements/1.1/")
    self.store.bind("data", "http://data.rpi.edu/vocab/")
    self.store.bind("owl", "http://www.w3.org/2002/07/owl#")
    self.store.bind("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
    self.store.bind("foaf", "http://xmlns.com/foaf/0.1/")
    self.store.bind("void", "http://rdfs.org/ns/void#")
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    OWL = Namespace("http://www.w3.org/2002/07/owl#")
    DATA = Namespace("http://data.rpi.edu/vocab/")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    VOID = Namespace("http://rdfs.org/ns/void#")
    header = self.reader.next()   #Skip header  
    minSize = len(header)
    semanticHeaders = [None]* len(header)
    headerCounter = 0
    for i in header:
      #Take only DC terms
      if re.match("^(dc\.)", i) != None:
        normalizedHeader = re.sub("\[\w+\]$", "", i)
        normalizedHeader = re.sub("^dc\.", "", normalizedHeader)
        semanticHeaders[headerCounter] = normalizedHeader
        currentList = semanticHeaders[headerCounter]
        currentList = normalizedHeader
      headerCounter += 1

    for row in self.reader:
      print >> sys.stderr, "Processing "+row[19]
      if len(row) != minSize:
        print >> sys.stderr,  "Number of columns different than header ({0} vs. {1}). Skipping".format(len(row), minSize)
        exit(1) #continue
      datasetUri = URIRef(row[semanticHeaders.index("identifier.uri")])
      for index, cell in enumerate(row):
        if semanticHeaders[index] in processors:
          aux = processors[semanticHeaders[index]]
          aux(datasetUri, cell)
        #else:
        #  self.store.add((datasetUri, DC[str(semanticHeaders[index])], Literal(cell)))
        print semanticHeaders[index]," ->", cell
    print(self.store.serialize(format="pretty-xml"))
    
if len(sys.argv) < 2:
  print >> sys.stderr, "No file selected"
  exit(0)
d = Ds2rdf(sys.argv[1])
d.convert()
