import pyslet.odata2.client as odata

c = odata.Client('http://odata.pyslet.org/weather/')
with c.feeds['DataPoints'].OpenCollection() as collection:
    collection.SetPage(10)
    for d in collection.iterpage():
        print d['TimePoint'].value, d['Temperature'].value
