#
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
import os
from sys import stdout

directory = "/Users/roald/Documents/pron/"
os.chdir(directory)
print(os.getcwd())

subsequentpages = []
scrapepage = []
to_download = []
imageprogress = 0

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
		subsequentpages.append("http://www.motherless.com" + link.get("href"))

def getallmetas(alist):
	for thing in alist:
		src = BeautifulSoup(requests.get(thing).text, "html.parser")
		containers = src.findAll(class_ = "img-container")
		for container in containers:
			scrapepage.append("http://www.motherless.com" + container.get("href"))
		print("found {} things".format(len(scrapepage)))

def download(url, filename):
	r = requests.get(url)
	with open(filename, "wb") as code:
		code.write(r.content)

for e in meta:
	scrapepage.append("http://www.motherless.com" + e.get("href"))

print("Downloading {}".format(title.strip()))

getallmetas(subsequentpages)

print("found {} images.".format(len(scrapepage)))
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
	#print("downloading image {} of {}".format(imageprogress, len(scrapepage)))
	stdout.write("\rdownloading image {} of {}".format(imageprogress, len(scrapepage)))
	stdout.flush()
	try:
		download(e, filename[0])

	except:
		pass