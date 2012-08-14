#!/usr/bin/python
from rdflib.graph import Graph
from rdflib.term import URIRef, Literal, BNode
from rdflib.namespace import Namespace, RDF, XSD
import csv
import sys
import re
import json


class Ds2rdf:
  def __init__(self, csvFile, root = 'http://data.rpi.edu/'):
    try:
      self.store = None
      self.rootUri = root
      self.source = csvFile
      self.collectionTree = {}
      self.reader = csv.reader(open(csvFile, 'rb'), delimiter=',')
      self.semanticHeaders = [None]* 10
      
      self.readCollectionTree()
    except IOError as (errno, strerror):
      print >> sys.stderr, "I/O error({0}): {2} {1}".format(errno, strerror, csvFile)
      exit(1)
      
  def readCollectionTree(self):
    #Mapping of dspace handles to a more readable URI
    self.collectionTree["10833/30"] = "twc/logd" 
    self.collectionTree["10833/23"] = "chiefinformationofficer/main" 
    self.collectionTree["10833/12"] = "architecture/main" 
    self.collectionTree["10833/20"] = "science/main" 
    self.collectionTree["10833/3"] = "archives/horsford" 
    
  def cleanLiteral(self, literal):
    return literal.title().replace(".", "").replace(" ", "_").lower()
    
  def getDatasetUri(self, row):
    if row[1] in self.collectionTree:
      collection  = self.collectionTree[row[1]]
    else:
      print >> sys.stderr, "Can't find collection string for %s" % row[1]
      exit(0)
    uri = self.rootUri+collection+'/'+self.cleanLiteral( URIRef(row[self.semanticHeaders.index("title")]))
    return uri
  
  def getCollectionUri(self, colId):
    return 'http://hdl.handle.net/'+colId
    
  def subjectProcessor(self, root, value):
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    a = value.split("||")
    for i in a:
     self.store.add((root, DC['subject'], Literal(i)))

  def dateIssuedProcessor(self, root, value):
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    a = value.split("||")
    for i in a:
      self.store.add((root, DC['issued'], Literal(i)))
      
  def authorProcessor(self, root, value):
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    OWL = Namespace("http://www.w3.org/2002/07/owl#")
    a = value.split("||")
    for i in a:
      contrib = None
      if re.match("^(http:\/\/)", i) != None:
        contrib = self.rootUri+'contributor/'+i.replace("http://", "").replace("/", "_")
        self.store.add((URIRef(contrib), RDFS['label'], Literal(i) ))     
        self.store.add((URIRef(contrib), OWL['sameAs'], URIRef(i) ))     
      else:
        aux = i.split(", ")
        if len(aux)>1:
          contrib = self.rootUri+'contributor/'+self.cleanLiteral(aux[1])+self.cleanLiteral(aux[0])
          self.store.add((URIRef(contrib), RDFS['label'], Literal(aux[1]+" "+aux[0]) ))     
        else:                     
          contrib = self.rootUri+'contributor/'+self.cleanLiteral(aux[0])
          self.store.add((URIRef(contrib), RDFS['label'], Literal(aux[0]) ))     
      self.store.add((root, DC['contributor'], URIRef(contrib)))     
      self.store.add((URIRef(contrib), RDF['type'], FOAF['Agent'] ))     

  def creatorProcessor(self, root, value):
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    OWL = Namespace("http://www.w3.org/2002/07/owl#")
    a = value.split("||")
    for i in a:
      contrib = None
      if re.match("^(http:\/\/)", i) != None:
        contrib = self.rootUri+'contributor/'+i.replace("://", "/")
        self.store.add((URIRef(contrib), RDFS['label'], Literal(i) ))     
        self.store.add((URIRef(contrib), OWL['sameAs'], URIRef(i) ))     
      else:
        aux = i.split(", ")
        if len(aux)>1:
          contrib = self.rootUri+'contributor/'+self.cleanLiteral(aux[1])+self.cleanLiteral(aux[0])
          self.store.add((URIRef(contrib), RDFS['label'], Literal(aux[1]+" "+aux[0]) ))     
        else:                     
          contrib = self.rootUri+'contributor/'+self.cleanLiteral(aux[0])
          self.store.add((URIRef(contrib), RDFS['label'], Literal(aux[0]) ))     
      self.store.add((root, DC['creator'], URIRef(contrib)))     
      self.store.add((URIRef(contrib), RDF['type'], FOAF['Agent'] ))   

  def coverageProcessor(self, root, value):
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    a = value.split("||")
    for i in a:
      self.store.add((root, DC['coverage'], Literal(i)))     

  def descriptionProcessor(self, root, value):
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    a = value.split("||")
    for i in a:
      self.store.add((root, DC['description'], Literal(i)))     

  def titleProcessor(self, root, value):
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    DCAT = Namespace("http://www.w3.org/ns/dcat#")
    RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    a = value.split("||")
    for i in a:
      self.store.add((root, DC['title'], Literal(i)))     
      self.store.add((root, RDFS['label'], Literal(i)))     
      self.store.add((root, RDF['type'], DCAT['Dataset']))    


  def identifierProcessor(self, root, value):
    OWL = Namespace("http://www.w3.org/2002/07/owl#")
    self.store.add((URIRef(root), OWL['sameAs'], URIRef(value)))
  
  def convert(self):
    self.store = Graph()
    processors = {}
    processors['subject'] = self.subjectProcessor
    processors['date.issued'] = self.dateIssuedProcessor
    processors['contributor.author'] = self.authorProcessor
    processors['contributor'] = self.authorProcessor
    processors['creator'] = self.creatorProcessor
    processors['coverage.spatial'] = self.coverageProcessor
    processors['description.abstract'] = self.descriptionProcessor
    processors['identifier.uri'] = self.identifierProcessor
    processors['title'] = self.titleProcessor
    self.store.bind("dc", "http://purl.org/dc/elements/1.1/")
    self.store.bind("data", "http://data.rpi.edu/vocab/")
    self.store.bind("owl", "http://www.w3.org/2002/07/owl#")
    self.store.bind("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
    self.store.bind("foaf", "http://xmlns.com/foaf/0.1/")
    self.store.bind("dcat", "http://www.w3.org/ns/dcat#")
    RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    OWL = Namespace("http://www.w3.org/2002/07/owl#")
    DATA = Namespace("http://data.rpi.edu/vocab/")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    DCAT = Namespace("http://www.w3.org/ns/dcat#")
    header = self.reader.next()   #Skip header  
    minSize = len(header)
    self.semanticHeaders = [None]* len(header)
    headerCounter = 0
    for i in header:
      #Take only DC terms
      if re.match("^(dc\.)", i) != None:
        normalizedHeader = re.sub("\[\w*\]$", "", i)
        normalizedHeader = re.sub("^dc\.", "", normalizedHeader)
        self.semanticHeaders[headerCounter] = normalizedHeader
        currentList = self.semanticHeaders[headerCounter]
        currentList = normalizedHeader
      headerCounter += 1
    for row in self.reader:
      if len(row) != minSize:
        print >> sys.stderr,  "Number of columns different than header ({0} vs. {1}). Skipping".format(len(row), minSize)
        exit(1) #continue
      datasetUri = self.getDatasetUri(row)
      collectionUri = self.getCollectionUri(row[1])
      self.store.add((URIRef(collectionUri), DCAT['dataset'], URIRef(datasetUri) ))     
      self.store.add((URIRef(collectionUri), RDF['type'], DCAT['Catalog'] ))     
      for index, cell in enumerate(row):
        if cell != "":
          if self.semanticHeaders[index] in processors:
            aux = processors[self.semanticHeaders[index]]
            aux(datasetUri, cell)
#          else:
#            self.store.add((datasetUri, DC[str(self.semanticHeaders[index])], Literal(cell)))
    print(self.store.serialize(format="pretty-xml"))
    
if len(sys.argv) < 2:
  print >> sys.stderr, "No file selected"
  exit(0)
d = Ds2rdf(sys.argv[1])
d.convert()
