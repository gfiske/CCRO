#gfiske
#November 2016
#CCRO project

# import the modules
try:
    import urllib
    import gspread
    from oauth2client.client import SignedJwtAssertionCredentials
    import json
    import base64
    import ConfigParser
except:
    print "Cannot import one or more module"
    import sys
    sys.exit(1)


###############################################################
config = ConfigParser.RawConfigParser()
config.read('/home/gfiske/Data/python_scripts/gfiske.cfg')
db_user = config.get('section1', 'db_user')
db_passwd = config.get('section1', 'db_passwd')
g_user = config.get('section1', 'g_user')
g_passwd = config.get('section1', 'g_passwd')
db_user = db_user.decode('base64','strict')
db_passwd = db_passwd.strip("'")
email = g_user.decode('base64','strict')
password = g_passwd.decode('base64','strict')[0:15]
chdb_user = config.get('section1', 'chdb_user')
chdb_user = chdb_user.strip("'")
chdb_passwd = config.get('section1', 'chdb_passwd')
chdb_passwd = chdb_passwd.strip("'")

###############################################################


#########################################
#       PULL FROM CASCADE DEVICE        #
#########################################

url = "https://www.dropbox.com/s/24cmcg6zsakxn8w/Quashnet-001?dl=1"
u = urllib.urlopen(url)
data = u.read()
u.close()

date, time, temp = data.split()
dateTime = date + " " + time
#convert temp to decimal value
temp = int(temp) * 0.001 




#print "date: " + date
#print "time: " + time
#print "temperature: " + str(temp)
#print "dateTime"

#########################################
#            Update Sheet               #
#########################################


try:
    #enter the data into the google spreadsheet
    rowToAdd = (date, time, str(temp), dateTime, str(temp))
    json_key = json.load(open('/home/gfiske/Data/python_scripts/raspPi-e0a08639ebab.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    g = gspread.authorize(credentials)
    worksheet = g.open('Quashnet_temperature').get_worksheet(0)
    worksheet.append_row(rowToAdd)
except:
    print "update spreadsheet failed"



