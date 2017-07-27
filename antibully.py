#!/usr/bin/env python3
#
# Bully suppression machine
# -------------------------
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
import requests
from time import sleep
from bs4 import BeautifulSoup
from textwrap import wrap
from random import randint
from sys import argv

base = 'https://news.ycombinator.com/'

bully = 'tptacek'

usage = """
./{} <username> <pw> [bully]

Default bully: {}
Always remember to use a throwaway when fighting bullies!
""".format(argv[0], bully)


if len(argv) < 3 or len(argv) > 4:
    print(usage)
    exit(1)

user = argv[1]
pasw = argv[2]

if len(argv) == 4:
    bully = argv[3]

urls = {
    'login': base + 'login',
    'bully': base + 'threads?id=' + bully,
    'comment': base + 'item?id='
}

print("logging in...", end='')

session = requests.Session()
resp = session.post(urls['login'], {'acct': user, 'pw': pasw})

print(str(resp.status_code))
if resp.status_code is not 200:
    print('antibully machine login failure, check your antibully credentials')
    exit(1)

def comments_since(last, comments):
    if last == 0:
        return [ comments[0] ]
    result = []
    for comment in comments:
        if comment['id'] != last:
            result.append(comment)
        else:
            break
    return result


last_seen_comment = 0

while True:
    r = session.get(urls['bully'])
    soup = BeautifulSoup(r.text, 'html.parser')
    comments = soup.find_all('tr', class_='athing comtr ')

    for comment in comments_since(last_seen_comment, comments):
        vl = comment.find('a', {'id': 'down_' + comment['id']})
        session.get(base + vl['href'])
        text = '>' + '\n>'.join(wrap(comment.find('span', {'class': 'c00'}).text, 80))
        text = text.replace('   reply', '')
        print('\n[bully downvoted]\n{}'.format(text) + '\n')
        sleep(3)

    last_seen_comment = comments[0]['id']

    wait = randint(30, 150)
    print("[sleeping for {}s to avoid antibully detector]".format(wait))
    sleep(wait)
