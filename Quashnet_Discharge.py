#!/usr/bin/python
#Quashnet_Discharge.py
# accesses the USGS live discharge for the Quashnet river
# posts to google spreadsheet every hour
#Greg Fiske 
# March 2017

import xml.etree.ElementTree as ET # for XML parsing
import json
import urllib
import time
import gspread
import base64
import ConfigParser
from oauth2client.client import SignedJwtAssertionCredentials

###############################################################
config = ConfigParser.RawConfigParser()
config.read('/home/gfiske/Data/python_scripts/gfiske.cfg')
g_user = config.get('section1', 'g_user')
g_passwd = config.get('section1', 'g_passwd')
email = g_user.decode('base64','strict')
password = g_passwd.decode('base64','strict')[0:15]
###############################################################

# Get XML from waterdata.usgs.gov
url = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=011058837&parameterCd=00060"

# Parse the discharge results
tree = ET.parse(urllib.urlopen(url)).getroot()
discharge = tree[1][2][0].text


#print discharge
timestamp = time.strftime('%m/%d/%Y') + "_" + time.strftime('%H:%M:%S')
#print timestamp

## Update the spreadsheet
try:
        rowToAdd = (timestamp,discharge)
        json_key = json.load(open('/home/gfiske/Data/python_scripts/raspPi-e0a08639ebab.json'))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
        g = gspread.authorize(credentials)
        worksheet = g.open('QuashnetDischarge').get_worksheet(0)
        worksheet.append_row(rowToAdd)
except:
        print "cannot update spreadsheet"
        pass