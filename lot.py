#Lot - a crude imagegrabber for crude images
#
# TODO:
# - Threading
# - More readable printout
#

from bs4 import BeautifulSoup
import urllib
import requests
import argparse
import sys
import random
import configparser
from sys import stdout
import os
import common

#
# Config and argument parsing
#
config = configparser.ConfigParser()
configpath = os.path.dirname(os.path.abspath(__file__)) + '/lot.cfg'
config.read(configpath)

directory = config.get('Paths', 'downloaddirectory')
minsize = int(config.get('Limits', 'minsize')) * 1000
maxsize = int(config.get('Limits', 'maxsize')) * 1000
minmax = [minsize, maxsize]
os.chdir(directory)

parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()

#
# Selecting module from URL
#
if "motherless" in args.echo:
    import mother as dl
elif "fuskator" in args.echo:
    import fusk as dl
else:
    exit()

#URL Handling if necessary - switching to right url if known from supplied

#
# Download html, convert to traverseable BS
#
src = requests.get(args.echo)
soup = BeautifulSoup(src.text, "html.parser")

#
# Fetch and filter title
#
title = dl.title(soup)
print("Downloading {}".format(title.strip()))

#
# Expand base url into list of grabbable files- taversing pages if necessary.
#
to_get = dl.filelist(soup)
stdout.write("\rfound {} images\n".format(len(to_get)))
stdout.flush()

#
# Create a folder based on title and download those files
#
common.dir_handling(title, directory)
dl.down(to_get, minmax)
