'''
    uchiwa-papirus.py A script to check uchiwa for events and send this data to
    a raspberry pi with a papirus hat
    Copyright (C) 2018 Rowan Wookey <admin@rwky.net>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import socket
import urllib.request
import json
import os
from papirus import PapirusTextPos
from datetime import datetime

url = os.environ['URL']
user = os.environ['AUTH_USER']
passwd = os.environ['AUTH_PASSWD']
realm = os.environ['AUTH_REALM']

authHandler = urllib.request.HTTPBasicAuthHandler()
authHandler.add_password(realm=realm, uri=url, user=user, passwd=passwd)

text = PapirusTextPos(False, rotation=180)
warn = 0
critical = 0
unknown = 0

def writeStatus(txt, x_offset, y_offset, size):
    text.AddText(txt, x_offset, y_offset, size=size)

    # add the current time, means I can check at a glance if it's working
    text.AddText(str(datetime.now().time()), 0, 0, size=20)

    # I keep forgetting the IP get it and display it
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('192.168.1.1', 80))
    text.AddText(str(s.getsockname()[0]), 0, 20, size=20)

    text.WriteAll()

try:
    opener = urllib.request.build_opener(authHandler)
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(url).read()
    data = json.loads(response.decode('utf-8'))

    for item in data:
        if item['check']['status'] > 2:
            unknown += 1
        elif item['check']['status'] == 2:
            critical += 1
        elif item['check']['status'] == 1:
            warn += 1
    if warn == 0 and critical == 0 and unknown == 0:
        writeStatus('OK', 0, 20, size=180)
    else:
        writeStatus('%d CRIT\n%d WARN\n%d UNKN' % (critical, warn, unknown), 0, 35, size=45)
except Exception as e:
    writeStatus('ERR', 0, 20, size=140)
    raise e
