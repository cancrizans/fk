#stop sneaking!
#this is not for you


import json
from pathlib import Path
import xml.etree.cElementTree as ET
import os.path
import subprocess

LOCATION = "https://cancrizans.github.io/fk/"


# crop thumb
def cropThumb(src_im,dest_im):
	print("cropping thumb %s into %s"%(src_im,dest_im),flush=True)
	cmd = "magick convert %s[0] -crop 940x700+0+0 -filter Cosine -resize 1000 -quality 90 %s"%(src_im,dest_im)
	subprocess.run(cmd,shell=True)


# Compile static pages

def compileStaticPages():

	print("compiling static pages")

	PREWARNING = "<!-- AUTO-GENERATED FILE -- DO NOT EDIT!! -->\n"

	with open('src/template.html','r') as tf:
		temp = tf.read()



	def compilePage(source,dest):
		print(source + " > " + dest)

		with open(source,'r') as f:
			src = f.read()

		page = PREWARNING + temp.replace("$CONTENT$",src) 

		with open(dest,'w') as f:
			f.write(page)

	compilePage("src/index.htm","index.html")
	compilePage("src/cast.htm","cast.html")
	compilePage("src/clongs.htm","clongs.html")

# Compile c/ folder

def compileCFolder():

	print("compiling c/ folder")

	with open('fleshkernel.json') as f:
		data = json.load(f)


	comics = list(filter(lambda e : (not 'type' in e), data['entries']))



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
	tree.write('feed.rss',encoding="utf-8",xml_declaration=True)





	with open('c/template.html','r') as f:
		template = f.read()


	#ABSOLUTEIMGPATH = LOCATION + 'pic/'

	for c in list(comics):

		
		directory = "c/"+c['code']
		
		Path(directory).mkdir(exist_ok=True)

		if(not 'comment' in c):
			c['comment'] = "A psychedelic sci-fi webcomic."

		
		image_source_name = c['prefix'] + c['img'][0]
		image_source = "pic/"+image_source_name

		image_dest = 'thumbs/'+c['code']+".jpg"
		if(not Path(image_dest).exists()):
			cropThumb(image_source,image_dest)
			
		image = LOCATION + image_dest

		page = template.replace("$TITLE$",c['title']).replace("$QCODE$","c="+c['code']).replace("$DESCRIPTION$",c['comment']).replace("$IMAGE$",image)
		
		with open(directory + "/index.html",'w') as ff:
			ff.write(page)




compileStaticPages()
compileCFolder()

