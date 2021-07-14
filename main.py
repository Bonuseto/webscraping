from User import User

import requests

from bs4 import BeautifulSoup as BS

file1 = open("cases.txt", "r+")
lines = file1.readlines()
for line in lines:
    line = line.split(",")

    data = {
        'ioff_application_number': line[2],
        'ioff_application_number_fake': line[3],
        'ioff_application_code': line[4],
        'ioff_application_year': line[5],
        'form_id': 'ioff_application_status_form',
        'honeypot_time': '1626245458|hhSKJ7eadYjR87usUrLNOpNH539nIqSqqwnH_52KkjI',

    }
    url = 'https://frs.gov.cz/en/ioff/application-status'
    html = requests.post(url, data)
    soup = BS(html.text, 'html.parser')
    result = ''
    warn = soup.findAll('span', {'class': 'alert alert-warning'})
    if warn:
        result = warn
    dang = soup.findAll('span', {'class': 'alert alert-danger'})
    if dang:
        result = dang
    sucs = soup.findAll('span', {'class': 'alert alert-success'})
    if sucs:
        result = sucs

    user = User(line[0], line[1], line[2], line[3], line[4], line[5], result[0].text)

    f = open("results.txt", "a")
    f.write(
        user.firstname + ',' + user.lastname + ',' + user.appnum + ',' + user.type + ',' + user.year + ',' + user.status + '\n')
    f.close()
file1.close()
