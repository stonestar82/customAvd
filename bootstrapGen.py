# -*- coding: utf-8 -*-
#!/usr/bin/env python
from datetime import datetime
from string import Template
import json

def bootstrapFirstBootPythonCreate():
		
	with open("switchInit.json", "r") as f:
		config = json.load(f)

	url = config["url"]
		
	t = """#!/usr/bin/env python
import requests
from EapiClientLib import EapiClient
from string import Template
from datetime import datetime

t = \"\"\"
!
logging buffered 1000
logging console informational
logging monitor informational
logging synchronous level all
!
username $${ansible} secret $${ansible_pw} privilege 15
!
ip routing
!
interface Management1
	description oob_management
	no shutdown
	ip address $${ip}/24
!
ip route 0.0.0.0/0 $${gateway}.1
\"\"\"

b = \"flash:/SWI=$${swiName}\"

switch = EapiClient(disableAaa=True, privLevel=15)

cli_command = "sh version | json"
result = switch.runCmds( 1, [cli_command])
data = result["result"][0]
sysmac = data["systemMacAddress"]
serial = data["serialNumber"]
modelName = data["modelName"]
version = data["version"]

if modelName == "vEOS-lab":
	cli_command = "copy ${requestUrl}/eos/download/vEOS-lab flash:/vEOS-lab-${version}.swi"
	swiName = "vEOS-lab-${version}.swi"
else:
	cli_command = "copy ${requestUrl}/eos/download/EOS flash:/EOS-${version}.swi"
	swiName = "EOS-${version}.swi"

switch.runCmds( 1, [cli_command])


cli_command = "show interfaces | json"
result = switch.runCmds( 1, [cli_command])
data = result["result"][0]
ip = data["interfaces"]["Management1"]["interfaceAddress"][0]["primaryIp"]["address"]



requestUrl = "${requestUrl}/bootstrap/ip/${seq}/" + ip + "/" + sysmac + "/" + serial

response = requests.get(requestUrl)


tmp_ip = ip.split(".")	
gateway = tmp_ip[0] + "." + tmp_ip[1] + "." + tmp_ip[2]

data = { "ansible" : "ansible", "ansible_pw": "ansible", "ip" : ip, "gateway": gateway, "swiName": swiName  }

template = Template(t)

with open("/mnt/flash/startup-config", "w") as reqs:
	reqs.write(template.substitute(data))
	reqs.close

template = Template(b)
with open("/mnt/flash/boot-config", "w") as reqs:
	reqs.write(template.substitute(data))
	reqs.close


	"""
	now = datetime.now()

	now = now.strftime("%Y%m%d%H%M")

	template = Template(t)

	data = { "seq" : now, "requestUrl": url, "version": "4.27.4M" }

	with open("bootstrap", "w") as reqs:
		reqs.write(template.substitute(data))
