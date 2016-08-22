# Script for parsing log files
#  and appends VM hostname and date to filename
import datetime
import os
# olddate = datetime.date.today()
# if needed, range for digits regex: \d{4,7}
path = 'put path here'
basefn = 'put base name here'

def createdate(line):
    datefromfile = line.split()[0].split('[')[1].__str__()
    # map the var to a date type and tell it the format
    thedate = datetime.datetime.strptime(datefromfile, '%Y-%m-%d').date()
    # convert it to a string in a different format
    newdate = datetime.date.strftime(thedate, '%Y%m%d')

    return newdate

for file in os.listdir(path):
    if file.startswith(basefn):
        os.chdir(path)
        for line in open(file):
            if 'put search string here' in line:
            # if 'Hostname' in line:
                host = line.split()[7]
                # host = line.split()[5]
                mydate = createdate(line)
                os.rename(file, basefn+'_'+mydate+'_'+host+'.log')
                break
        print file
