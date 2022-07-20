import urllib
import urllib2
import pyslet.http.client as http
import untangle
from xml.dom import minidom
import xml.etree.ElementTree as ET


urllib2.install_opener(
    urllib2.build_opener(
        urllib2.ProxyHandler({'http': '<proxy_url>'})
    )
)

response = urllib2.urlopen('<URL>/API/v1_0/Products/Processors()?$top=10&api_key=<key>') # -> to get xml
#xmldoc = minidom.parse(response)
root = ET.fromstring(response)
print root.findall(".")


#root = tree.getroot()
#for child in root:
#	print child.tag, child.attrib

#for GraphicsDeviceId in root.iter('neighbor'):
#	print GraphicsDeviceId.attrib
#print xmldoc.toxml().encode('utf-8')

