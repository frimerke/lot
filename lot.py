#Lot - a crude imagegrabber for crude images
#
# TODO:
# - Threading
# - More readable printout
# - Option to skip small or big files
#

from bs4 import BeautifulSoup
import urllib
import requests
import argparse
import sys
import ConfigParser
from sys import stdout
import os


config = ConfigParser.ConfigParser()
configpath = os.path.dirname(os.path.abspath(__file__)) + '/lot.cfg'
config.read(configpath)


directory = config.get('Paths', 'downloaddirectory')
minsize = int(config.get('Limits', 'minsize')) * 1000
maxsize = int(config.get('Limits', 'maxsize')) * 1000
os.chdir(directory)

subsequentpages = []
scrapepage = []
to_download = []
imageprogress = 0
skippedfiles = 0

parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()

src = requests.get(args.echo)

soup = BeautifulSoup(src.text, "html.parser")

title = soup.find(class_="content-title").string
meta = soup.findAll(class_="img-container")
pages = soup.findAll(class_="pagination_link")

for page in pages:
	for link in page.findAll('a'):
		try:
			subsequentpages.append("http://www.motherless.com" + link.get("href"))
		except:
			pass
		

def getallmetas(alist):
	for thing in alist:
		src = BeautifulSoup(requests.get(thing).text, "html.parser")
		containers = src.findAll(class_ = "img-container")
		for container in containers:
			scrapepage.append("http://www.motherless.com" + container.get("href"))
		#print("found {} things".format(len(scrapepage)))
		stdout.write("\rfound {} images".format(len(scrapepage)))
		stdout.flush()

def download(url, filename):
	h = requests.head(url)
	size = h.headers['content-length']
	if (int(size) < minsize) or (int(size) > maxsize):
		pass
		skippedfiles += 1
	else:
		r = requests.get(url)
		with open(filename, "wb") as code:
			code.write(r.content)

for e in meta:
	try:
		scrapepage.append("http://www.motherless.com" + e.get("href"))
	except:
		pass

print("Downloading {}".format(title.strip()))

getallmetas(subsequentpages)

stdout.write("\rfound {} images\n".format(len(scrapepage)))
stdout.flush()

try:
	os.mkdir(directory + title.strip())
except:
	pass
os.chdir(directory + title.strip())

for image in scrapepage:
	imageprogress += 1
	try:
		page = requests.get(image)
	except:
		pass
	suppe = BeautifulSoup(page.text, "html.parser")
	elem = suppe.find(rel="image_src")
	e = elem["href"]
	filename = e.split("/")
	filename = filename[-1].split("?")
	procent = (imageprogress / len(scrapepage))
	stdout.write("\rdownloading {} of {} | {} files skipped".format(imageprogress, len(scrapepage), skippedfiles))
	stdout.flush()
	try:
		download(e, filename[0])

	except:
		pass