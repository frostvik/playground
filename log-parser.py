# Script for parsing log files
#  and appends VM hostname and date to filename
import datetime
import os

# olddate = datetime.date.today()
# if needed, range for digits regex: \d{4,7}
path = 'put path here'
basefn = 'put base name here'

# Function to change date format
def createdate(l):
    datefromfile = l.split()[0].split('[')[1].__str__()
    # map the var to a date type and tell it the format
    thedate = datetime.datetime.strptime(datefromfile, '%Y-%m-%d').date()
    # convert it to a string in a different format
    newdate = datetime.date.strftime(thedate, '%Y%m%d')

    return newdate


# Function to update base naming
def basename(l):
    basefn = ''
    if 'Starting pre-provisioning workflow' in l:
        basefn = 'log_0_preprov_workflow'
    elif 'Starting post-provisioning workflow' in l:
        basefn = 'log_1_postprov_workflow'
    elif 'Starting decommissioning workflow' in l:
        basefn = 'log_2_decomm_workflow'
    elif 'Fetching a work item' in l:
        basefn = 'log_gugent'
    return basefn


found = False
for logfile in os.listdir(path):
    if logfile.startswith(basen):
        found = True
if not found:
    print 'No log file found!'

count = 0
for logfile in os.listdir(path):
    if logfile.startswith(basen):
        os.chdir(path)
        logname = ''
        for logline in open(logfile):
            if basename(logline):
                logname = basename(logline)
                break
        for logline in open(logfile):
            # if 'Hostname' in logline:
            if 'Found property Hostname' in logline:
                # host = logline.split()[5]
                host = logline.split()[7]
                mydate = createdate(logline)
                os.rename(logfile, logname + '_' + mydate + '_' + host + '.log')
                count += 1
                break
count = count.__str__()
print count + ' files modified.'
