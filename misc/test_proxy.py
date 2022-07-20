import urllib
import urllib2

#urllib2.install_opener(
#    urllib2.build_opener(
#        urllib2.ProxyHandler({'http': '<proxy_url>'})
#    )
#)
response = urllib2.urlopen('service_url')
for line in response:
	print line
response.close()
