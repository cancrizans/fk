#stop sneaking!
#this is not for you


import json

with open('fleshkernel.json') as f:
	data = json.load(f)


comics = list(filter(lambda e : (not 'type' in e), data['entries']))

import xml.etree.cElementTree as ET
LOCATION = "https://cancrizans.github.io/fk/"



def parseComic(e):
	item = ET.Element('item')

	
	ET.SubElement(item,'title').text = e['title']
	ET.SubElement(item,'link').text = LOCATION  + "?c="+e['code']

	if('comment' in e):
		ET.SubElement(item,'description').text = e['comment']
	return item



rssEntries = map(parseComic,comics)



rss = ET.Element('rss')
rss.set('version',"2.0")



channel = ET.SubElement(rss,'channel')
ET.SubElement(channel,'title').text = "Flesh Kernel Webcomic"
ET.SubElement(channel,'description').text = "A psychedelic sci-fi webcomic"
ET.SubElement(channel,'link').text = LOCATION



for item in rssEntries:
	channel.append(item)




tree = ET.ElementTree(rss)
tree.write('feed.rss',encoding="unicode",xml_declaration=True)




from pathlib import Path

with open('c/template.html','r') as f:
	template = f.read()


for c in list(comics):

	
	directory = "c/"+c['code']
	
	Path(directory).mkdir(exist_ok=True)

	
	page = template.replace("$TITLE$",c['title']).replace("$QCODE$","c="+c['code'])
	
	with open(directory + "/index.html",'w') as ff:
		ff.write(page)







