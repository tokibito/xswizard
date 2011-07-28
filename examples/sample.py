"""
>python sample.py
<xswizard.api.API: url=http://192.168.11.100/, username=root>
[<VM: debian01-sandbox>, <VM: debian04-php>, <VM: debian02-py>, <VM: ubuntu03-py>, <VM: Control domain on host: xenserver01>]
<VM: test_snapshot_1299773422>
"""
import time
from xswizard.api import API

URL = 'https://192.168.11.100/'
USERNAME = 'root'
PASSWORD = ''

api = API(URL, USERNAME, PASSWORD)
print api
vms = api.get_hosts()[0].residentVMs
print vms
vm = vms[1].snapshot('test_snapshot_%s' % int(time.time()))
print vm
#vm.export_as_file('test.xva')
