#
# LOT module for fuskator.com
# handles importing gallery or group image link (i.e. a /GI or /gi/ url).
#

import common
import re
from bs4 import BeautifulSoup
import requests
from sys import stdout

def title(soup):
	try:
		title = soup.find(class_="content-title").string
	except:
		title = soup.find(class_="group-bio-name").a.string
	title = title.strip()
	title = re.sub('[^\w\-_\. ]', '_', title)
	return title


def filelist(soup):
	meta = soup.findAll(class_="img-container")
	pages = soup.findAll(class_="pagination_link")
	scrapepage = []
	subsequentpages = []
	to_download = []

	for e in meta:
		try:
			scrapepage.append("http://www.motherless.com" + e.get("href"))
		except:
			pass

	for page in pages:
		for link in page.findAll('a'):
			try:
				subsequentpages.append("http://www.motherless.com" + link.get("href"))
			except:
				pass

	getallmetas(subsequentpages, scrapepage)

	for image in scrapepage:
		try:
			page = requests.get(image)
		except:
			pass
		suppe = BeautifulSoup(page.text, "html.parser")
		elem = suppe.find(rel="image_src")
		e = elem["href"]
		to_download.append(e)

	return to_download

def getallmetas(alist, scrapepage):
	for thing in alist:
		src = BeautifulSoup(requests.get(thing).text, "html.parser")
		containers = src.findAll(class_ = "img-container")
		for container in containers:
			scrapepage.append("http://www.motherless.com" + container.get("href"))

def down(dl_list, minmax):
	for image in dl_list:
		filename = image.split("/")
		filename = filename[-1].split("?")
		stdout.write("\rdownloading {}".format(filename))
		stdout.flush()
		common.download(image, filename[0], minmax)
