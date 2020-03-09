from datetime import datetime, timedelta, time
import calendar
import csv
import re
import argparse

rest = []
find_lunch = argparse.ArgumentParser(description='Generate a list of open restaurants')
group = find_lunch.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--day', help='day restaurants are  open')
find_lunch.add_argument('-t', '--time', help='hour to test against')
group.add_argument('-n', '--now', help='get open restaurants at this hour', action='store_true')
myargs = find_lunch.parse_args()

# add arguments to variables
if myargs.now:
    input_now = datetime.now()
else:
    input_now = myargs.day


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


def get_rest_params(name, timestring):
    opent, closet = parse_start_and_close(timestring)
    return rest.append({'name': name, 'start_time': opent, 'end_time': closet, 'open_days': days_open(timestring)})


def compose_rest_dict():
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
                            for timecomma in timecommas:
                                # initially was:
                                # opentime, closetime = parse_start_and_close(timecomma)
                                # rest.append({'name': row[0], 'start_time': opentime, 'end_time': closetime, 'open_days': days_open(timecomma)})
                                get_rest_params(row[0], timecomma)
                        else:
                            get_rest_params(row[0], timecommas[0])
                    elif re.search(r'([a-zA-Z]{3},)', timerange):
                        # this particular case does not exist in the csv, for ex: Mon-Fri 10 am - 10 pm / Sat,Sun 11 am - 10 pm
                        timecommas = [r.strip() for r in timerange.split(',')]
                        if len(timecommas) == 2:
                            timecommas[0] = f'{timecommas[0]}{re.split(r"([a-zA-Z]{3})", timecommas[1])[2]}'
                            for timecomma in timecommas:
                                get_rest_params(row[0], timecomma)
                        else:
                            get_rest_params(row[0], timecommas[0])
            else:
                timecommas = [r.strip() for r in row[1].split(',')]
                if len(timecommas) >= 2:
                    timecommas[0] = f'{timecommas[0]}{re.split(r"([a-zA-Z]{3}-[a-zA-Z]{3})", timecommas[1])[2]}'
                    for timecomma in timecommas:
                        get_rest_params(row[0], timecomma)
                else:
                    get_rest_params(row[0], row[1])
    return rest


def get_open_rest():
    i = 0
    open_rest = []
    for r in compose_rest_dict():
        while r['open_days'] >= 0:
            day = r['start_time'] + timedelta(days=i)
            if datetime.strftime(input_now, '%a') in datetime.strftime(day, '%a'):
                if time(7, 1) <= datetime.time(r['end_time']) <= time(23, 59) and datetime.time(r['start_time']) <= datetime.time(input_now) <= datetime.time(r['end_time']):
                    open_rest.append(r['name'])
                elif time(0) <= datetime.time(r['end_time']) <= time(7) and time(0) <= datetime.time(input_now) <= datetime.time(r['end_time']):
                    open_rest.append(r['name'])
            r['open_days'] -= 1
            i += 1
    open_rest = list(set(open_rest))
    return open_rest


print(get_open_rest())
