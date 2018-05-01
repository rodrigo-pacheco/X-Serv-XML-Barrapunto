#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from urllib import request

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Title: " + self.theContent + "."
                # To avoid Unicode trouble
                print(str(line.encode('utf-8')))
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                print(" Link: " + str(self.theContent) + ".")
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

if len(sys.argv) < 2:
    print("Usage: python xml-parser-barrapunto.py <document/URL>")
    print()
    print(" <document/URL>: file name of the document or URL  to parse")
    sys.exit(1)

# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
def createOutputFile():
    file = open("parsed.html", "w")
    file.write("<html><body><h1>Parsing result:<br></html></body></h1>")
    file.close
try:
    xmlFile = open(sys.argv[1],"r")
    createOutputFile()
    theParser.parse(xmlFile)
except FileNotFoundError:
    try:
        xmlFile = request.urlopen(sys.argv[1])
        createOutputFile()
        theParser.parse(xmlFile)
    except ValueError:
        print("URL or file not found")
        sys.exit(1)
print("Parse complete")
