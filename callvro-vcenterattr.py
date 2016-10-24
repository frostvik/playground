# Update vCenter attributes for various notes like Owner, DateCreated
# callvro-vcenterattr.py -s vrohost.domain.com -v vmname -p stackname -o owner -d datecreated

# !/usr/bin/python
import argparse
import getpass
import socket
import urllib2
import json

# describe the arguments
callvro = argparse.ArgumentParser(description='This script will call a vRO workflow for configurations.')
callvro.add_argument('-s', '--vROserver', help='vRO host for initiating the workflow', required=True)
callvro.add_argument('-v', '--vmname', help='Name of the VM', required=True)
callvro.add_argument('-p', '--stackname', help='The name of the stack the VM was deployed from', required=True)
callvro.add_argument('-o', '--owner', help='The owner of the VM', required=True)
callvro.add_argument('-d', '--date', help='The date the VM was created', required=True)
myargs = callvro.parse_args()

# add to variables all arguments
vrohost = myargs.vROserver
vrouser = 'admin'
vropassword = getpass.getpass(prompt='Enter vRO user password: ')
# vropassword = 'xxxxxxxxx'
vmname = myargs.vmname
stackname = myargs.stackname
owner = myargs.owner
thedate = myargs.date

# get workflow id for Update-vCenter-attr
print ("\n")
print ("Initiating GET call for retrieving workflow ID")
workpath = '/vco/api/workflows?conditions=name=Update-vCenter-attr'
target = 'https://' + vrohost + ':8281' + workpath
theget = urllib2.Request(target)
theget.add_header('Accept', 'application/json')
theget.add_header('Content-Type', 'application/json; charset=UTF-8')


def testconn():
    s = socket.socket()
    try:
        s.connect((vrohost, 8281))
        return True
    except Exception as e:
        print ("Cannot connect to: "+target+" the error is: %s" % e)
        return False

# Creating a password manager that keeps credentials, using it in a auth handler, that is added to a installed opener
if testconn():
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, target, vrouser, vropassword)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)

    # run the get request and parse the ID
    thegetresp = urllib2.urlopen(theget)
    respbody = thegetresp.read().decode('utf-8')
    respgetbody = thegetresp.getcode().__str__()
    print ("Response: HTTP " + respgetbody)
    workid = respbody.split(',')[0].split('//')[1].split('/')[4]
    print ("The ID were searching for is: " + workid + "\n")

    # POST the embedded json
    print ("Initiating POST call for running workflow")
    updatedtarget = 'https://' + vrohost + ':8281/vco/api/workflows/' + workid + '/executions'

    thepost = urllib2.Request(updatedtarget)
    thepost.add_header('Accept', 'application/json')
    thepost.add_header('Content-Type', 'application/json')

    # add parameters to the json template
    jsonchange = \
        {
            "parameters":
            [
                {
                    "value": {"string": {"value": owner}},
                    "type": "string",
                    "name": "owner",
                    "scope": "local"
                },
                {
                    "value": {"string": {"value": vmname}},
                    "type": "string",
                    "name": "vmname",
                    "scope": "local"
                },
                {
                    "value": {"string": {"value": stackname}},
                    "type": "string",
                    "name": "stackname",
                    "scope": "local"
                },
                {
                    "value": {"string": {"value": thedate}},
                    "type": "string",
                    "name": "DateCreated",
                    "scope": "local"
                }
            ]
        }

    thepostresp = urllib2.urlopen(thepost, json.dumps(jsonchange))
    resppostbody = thepostresp.getcode().__str__()
    print ("Response: HTTP " + resppostbody)
else:
    print ("Check your connection to the %s" % target)
