import xml.dom.minidom
import xpath

a = xml.dom.minidom.parse( "scheme.xml" )

o = xpath.find("//option",a)
print o

m = xpath.find("menu",o[0])
print m
