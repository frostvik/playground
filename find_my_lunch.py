from datetime import datetime, timedelta, time
import calendar
import csv
import re
import argparse

find_lunch = argparse.ArgumentParser(description='Generate a list of open restaurants')
find_lunch.add_argument('-d', '--day', help='day restaurants are  open')
find_lunch.add_argument('-t', '--time', help='hour to test against')
find_lunch.add_argument('-n', '--now', help='get open restaurants at this hour', action='store_true')
myargs = find_lunch.parse_args()

# add arguments to variables
input_day = myargs.day
input_hour = myargs.time
if myargs.now:
    input_now = datetime.now()

rest = []
# a = "Kushi Tsuru,Mon-Sun 11:30 am - 9 pm"
# a = 'Restaurant Lulu,"Mon-Thu, Sun 11:30 am - 9 pm  / Fri-Sat 11:30 am - 10 pm"'
# a = "The Cheesecake Factory,Mon-Thu 11 am - 11 pm  / Fri-Sat 11 am - 12:30 am  / Sun 10 am - 11 pm"

# https://strftime.org for strftime/strptime formatting


def match_starttime(timestring):
    return re.search(r'([0-9]{1,2} [a-z]{2} -|[0-9]{1,2}:[0-9]{2} [a-z]{2} -)', timestring).group(0).split('-')[0].strip()


def match_endtime(timestring):
    return re.search(r'(- [0-9]{1,2} [a-z]{2}|- [0-9]{1,2}:[0-9]{2} [a-z]{2})', timestring).group(0).split('-')[1].strip()


def compose_day(daystring):
    firstday = datetime.strptime('Mon 17/02/20', '%a %d/%m/%y')
    weekdays = list(calendar.day_abbr)
    weekdayint = weekdays.index(daystring)
    return firstday + timedelta(days=weekdayint)


def after_midnight(timestring):
    if datetime.strptime('12 am', '%I %p') <= timestring <= datetime.strptime('5 am', '%I %p'):
        # timestring = timestring + timedelta(days=1)
        return True


def add_day(timestring, day):
    if after_midnight(timestring):
        return day + timedelta(days=1)
    else:
        return day


def days_open(dayrange):
    # parse a range of days returning number of days in the range
    dayrange = dayrange.split()[0]
    weekdays = list(calendar.day_abbr)
    if '-' in dayrange:
        start_day = weekdays.index(dayrange.split('-')[0])
        end_day = weekdays.index(dayrange.split('-')[1])
        return end_day - start_day + 1
    else:
        return 1


def parse_start_and_close(timestring):
    openday = datetime.strptime(timestring.split()[0].split('-')[0], '%a')
    weekdays = list(calendar.day_abbr)
    weekdayint = weekdays.index(timestring.split()[0].split('-')[0])
    openday = openday + timedelta(days=weekdayint)
    try:
        time1 = datetime.strptime(match_starttime(timestring), '%I:%M %p').time()
        opentime = datetime.combine(openday, time1)
        try:
            time2 = datetime.strptime(match_endtime(timestring), '%I:%M %p')
            closetime = datetime.combine(add_day(time2, openday), time2.time())
            return opentime, closetime
        except ValueError:
            time2 = datetime.strptime(match_endtime(timestring), '%I %p')
            closetime = datetime.combine(add_day(time2, openday), time2.time())
            return opentime, closetime
    except ValueError:
        time1 = datetime.strptime(match_starttime(timestring), '%I %p').time()
        opentime = datetime.combine(openday, time1)
        try:
            time2 = datetime.strptime(match_endtime(timestring), '%I:%M %p')
            closetime = datetime.combine(add_day(time2, openday), time2.time())
            return opentime, closetime
        except ValueError:
            time2 = datetime.strptime(match_endtime(timestring), '%I %p')
            closetime = datetime.combine(add_day(time2, openday), time2.time())
            return opentime, closetime


with open('restaurants.csv') as csvfile:
    csvread = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvread:
        if '/' in row[1]:
            timeranges = [r.strip() for r in row[1].split('/')]
            for timerange in timeranges:
                if re.search(r'([a-zA-Z]{3})-([a-zA-Z]{3})', timerange):
                    timecommas = [r.strip() for r in timerange.split(',')]
                    if len(timecommas) >= 2:
                        timecommas[0] = f'{timecommas[0]}{re.split(r"([a-zA-Z]{3})", timecommas[1])[2]}'
                        # don't know how to comprehend
                        for timecomma in timecommas:
                            opentime, closetime = parse_start_and_close(timecomma)
                            # print(f"{opentime.strftime('%A %H:%M')} {closetime.strftime('%A %H:%M')} {row[0]}")
                            rest.append({'name': row[0], 'start_time': opentime, 'end_time': closetime, 'open_days': days_open(timecomma)})
                    else:
                        opentime, closetime = parse_start_and_close(timecommas[0])
                        # print(f"{opentime.strftime('%A %H:%M')} {closetime.strftime('%A %H:%M')} {row[0]}")
                        rest.append({'name': row[0], 'start_time': opentime, 'end_time': closetime, 'open_days': days_open(timecommas[0])})
                elif re.search(r'([a-zA-Z]{3})', timerange):
                    # this particular case does not exist in the csv, for ex: Sat 11 am - 11 pm, Sun 11 am - 10 pm
                    timecommas = [r.strip() for r in timerange.split(',')]
                    if len(timecommas) == 2:
                        timecommas[0] = f'{timecommas[0]}{re.split(r"([a-zA-Z]{3})", timecommas[1])[2]}'
                        for timecomma in timecommas:
                            opentime, closetime = parse_start_and_close(timecomma)
                            # print(f"{opentime.strftime('%A %H:%M')} {closetime.strftime('%A %H:%M')} {row[0]}")
                            rest.append({'name': row[0], 'start_time': opentime, 'end_time': closetime, 'open_days': days_open(timecomma)})
                    else:
                        opentime, closetime = parse_start_and_close(timecommas[0])
                        # print(f"{opentime.strftime('%A %H:%M')} {closetime.strftime('%A %H:%M')} {row[0]}")
                        rest.append({'name': row[0], 'start_time': opentime, 'end_time': closetime, 'open_days': days_open(timecommas[0])})
        else:
            timecommas = [r.strip() for r in row[1].split(',')]
            if len(timecommas) >= 2:
                timecommas[0] = f'{timecommas[0]}{re.split(r"([a-zA-Z]{3}-[a-zA-Z]{3})", timecommas[1])[2]}'
                for timecomma in timecommas:
                    opentime, closetime = parse_start_and_close(timecomma)
                    # print(f"{opentime.strftime('%A %H:%M')} {closetime.strftime('%A %H:%M')} {row[0]}")
                    rest.append({'name': row[0], 'start_time': opentime, 'end_time': closetime, 'open_days': days_open(timecomma)})

            else:
                opentime, closetime = parse_start_and_close(row[1])
                # print(f"{opentime.strftime('%A %H:%M')} {closetime.strftime('%A %H:%M')} {row[0]}")
                rest.append({'name': row[0], 'start_time': opentime, 'end_time': closetime, 'open_days': days_open(row[1])})
print(rest)
