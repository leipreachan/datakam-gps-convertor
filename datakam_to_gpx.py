#!/usr/bin/python

from xml import etree
import xml.etree.cElementTree as ET

filename = '2015-09-03.log'

with open(filename) as f:
	content = f.read().splitlines()

for i, var in enumerate(content):
	content[i] = var.split('\t')
	
root = ET.Element('gpx')
trk = ET.SubElement(root, 'trk')

name = ET.SubElement(trk, 'name')
name.text = "datakam track " + filename

for i, v in enumerate(content):
	if len(v) > 1:
		pt = ET.SubElement(trk, 'wpt')
		pt.set('lat', v[1])
		pt.set('lon', v[2])
		ET.SubElement(pt, 'time').text = v[0]
		ET.SubElement(pt, 'ele').text= v[3]


tree = ET.ElementTree(root)
tree.write(filename + '.gpx')
