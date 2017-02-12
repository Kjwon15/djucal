import datetime
import re

import fake_useragent
import flask
import icalendar
import lxml.html
import requests


app = flask.Flask(__name__)


@app.route('/djucal.ical')
def djucal():
    cal = make_ical()
    return cal.to_ical().decode('utf-8')


def extract_schedule(year, schedule):
    pattern = re.compile(
        r'(?P<from>\d{1,2}/\d{1,2})'
        r'(?: ~(?P<to>\d{1,2}/\d{1,2}))?'
        r' (?P<content>.*)')

    event = icalendar.Event()
    matched = pattern.match(schedule)

    from_date = matched.group('from')
    to_date = matched.group('to')
    content = matched.group('content')

    event.add('dtstart', datetime.date(year, *map(int, from_date.split('/'))))
    if to_date:
        event.add('dtend', datetime.date(year, *map(int, to_date.split('/'))))

    event.add('summary', content)

    return event


def make_ical():
    ua = fake_useragent.UserAgent()
    session = requests.session()
    session.headers['User-Agent'] = ua.Chrome

    current_year = datetime.date.today().year

    cal = icalendar.Calendar()

    for year in [current_year-1, current_year]:
        resp = session.get('http://www.dju.ac.kr/kor/html/subp.htm', params={
            'page_code': '01040100',
            'listYear': year,
        })

        tree = lxml.html.fromstring(resp.content.decode('cp949'))

        for month in tree.xpath('//*[@class="sch-box"]'):
            year_month = month.find('*/*[@class="year"]').text_content()
            year = int(year_month.split('/')[0])
            for schedule in month.findall('*[@class="schList-box"]/ul/li'):
                t = schedule.text_content()
                event = extract_schedule(year, t)
                cal.add_component(event)

    return cal
