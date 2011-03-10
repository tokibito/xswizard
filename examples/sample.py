"""
>python sample.py
[<VM: debian01-sandbox>, <VM: debian04-php>, <VM: debian02-py>, <VM: ubuntu03-py>, <VM: Control domain on host: xenserver01>]
"""

from xswizard.api import API

URL = 'http://192.168.11.100/'
USERNAME = 'root'
PASSWORD = ''

api = API(URL, USERNAME, PASSWORD)
print api.get_hosts()[0].residentVMs
