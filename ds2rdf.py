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
    except IOError as (errno, strerror):
      print >> sys,stderr, "I/O error({0}): {2} {1}".format(errno, strerror, csvFile)
      exit(1)
      

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
        print  "Number of columns different than header ({0} vs. {1}). Skipping".format(len(row), minSize)
        exit(1) #continue
      store.add((row[15], DC['identifier'], Literal(row[0])))
      print >> sys.stderr, "Processing "+row[20]
      if re.search("^http", row[2]):
        creator = row[2]
        names = None
        store.add((row[15], DC['creator'], creator))
      else:
        if len(row[2]) > 0:
          people = row[2].split("||")
        else:
          people = row[3]
        for i in people:
          names = i.split(", ")
          token = ""
          if len(names) > 1:
            token = "id/"+names[1].capitalize().replace(" ", "_")+names[0].capitalize().replace(" ", "_")
            creator=URIRef("http://data.rpi.edu/"+token)
            store.add((creator, FOAF['firstName'], Literal(names[0])))
            store.add((creator, FOAF['lastName'], Literal(names[1])))
          else:
            token = "id/"+names[0].capitalize().replace(" ", "_").replace(".", "")
            creator=URIRef("http://data.rpi.edu/"+token)
            store.add((creator, FOAF['name'], Literal(names[0])))
            store.add((creator, DC['title'], Literal(names[0])))
          store.add((row[15], DC['creator'], creator))

      store.add((row[15], DC['dateAccepted'], Literal(row[5])))
      store.add((row[15], RDFS['comments'], Literal(row[6])))
      store.add((row[15], DC['description'], Literal(row[6])))
      store.add((row[15], DC['bibliographicCitation'], Literal(row[7])))
      store.add((row[15], DC['title'], Literal(row[20])))
      store.add((row[15], RDFS['label'], Literal(row[20])))
      store.add((row[15], DC['subject'], URIRef(DATA+re.sub("\s", "_", row[9]))))
    print(store.serialize(format="pretty-xml"))
    
d = Ds2rdf(sys.argv[1])
d.convert()
