import xlrd, re
from operator import *
from generators.envirmentVariables import *
from jinja2 import Template
from openpyxl import load_workbook
from operator import eq
from generators.BlankNone import *

def convertToBoolIfNeeded(variable):
	if type(variable) == str and re.match(r'(?i)(True|False)', variable.strip()):
		variable = True if re.match(r'(?i)true', variable.strip()) else False
	
	return variable

def parseGeneralInfo(inventory_file, excelVar):
	# configuration_variable_mappers = {"CVP IP Addresses": "cvp_instance_ips", "CVP Ingest Auth Key": "cvp_ingestauth_key",
	# "Management Gateway":"mgmt_gateway",  "DNS Servers":"name_servers", "NTP Servers": "ntp_servers",
	# "cvpadmin password sha512 hash":"cvpadmin_pass", "admin password sha512 hash":"admin_pass"}

	workbook = load_workbook(filename=inventory_file, read_only=False, data_only=True)
	info = {}

	for item in excelVar["all"]:
		v = getExcelSheetValue(workbook, excelVar["all"][item])
		info[excelVar["all"][item]["mapping"]] = v
	

	general_info = {}

	##### ansible/admin 계정 세팅 S
	# ansible 계정은 기본 설정
	general_info["local_users"] = {
			"ansible":{
					"privilege": 15,
					"role": "network-admin",
					"sha512_password": info["ansible_info"]
			}
	}

	# admin 계정은 값을 등록했을경우만 변경
	if ne(info["admin_info"], "") and ne(info["admin_name"], ""):
		general_info["local_users"].setdefault(
			info["admin_name"] , {
					"privilege": 15, "role": "network-admin", "sha512_password": info["admin_info"]
				}
		)

	###### ansible/admin 계정 세팅 E
	
	###### management interface 세팅 S
	general_info["mgmt_interface"] = info["mgmt_interface"]
	general_info["mgmt_interface_vrf"] = info["mgmt_interface_vrf"]
	general_info["mgmt_gateway"] = info["mgmt_gateway"]
	###### management interface 세팅 E 

	# general_info["cvp_instance_ips"] = [ip.strip() for ip in info["cvp_instance_ips"].split(",") if ip != ""]

	# general_info["cvp_ingestauth_key"] = info["cvp_ingestauth_key"] if info["cvp_ingestauth_key"] != "" else None
	
	# Name Server 세팅
	general_info["name_servers"] = [ip.strip() for ip in info["name_servers"].split(",") if ip != ""]

	# NTP Server 세팅
	if ne(info["ntp_servers"], "") and ne(info["mgmt_interface_vrf"], ""):
		general_info["custom_structured_configuration_ntp"] = {
				"local_interface" : {
					"name": MGMT_INTERFACE,
					"vrf": MGMT_INTERFACE_VRF
				}
			}
		

		ntpServers = info["ntp_servers"].split(",")
		ntpServersPrefer = info["ntp_servers_prefer"].split(",")

		ntpInfo = []
		for i in range(len(ntpServers)):
			ntp = {
				"name": ntpServers[i],
				"preferred": convertToBoolIfNeeded(ntpServersPrefer[i]),
				"vrf": MGMT_INTERFACE_VRF
			}
			ntpInfo.append(ntp)			

		general_info["custom_structured_configuration_ntp"]["servers"] = ntpInfo

	# Loggin 세팅
	# loggin_buffered_level",
	# 	gc.logginConsole: "loggin_console",
	# 	gc.logginMonitor: "loggin_monitor",
	# 	gc.logginSynchronous: "loggin_sychronous"
	# logging:
  # buffered:
  #   level: 1000
  # console: informational
  # monitor: informational
  # synchronous: all

	loginInfo = []	
	if ne(info["loggin_console"], ""):
		loginInfo.append(["console", info["loggin_console"]])

	if ne(info["loggin_monitor"], ""):
		loginInfo.append(["monitor", info["loggin_monitor"]])

	if loginInfo:
		general_info["logging"] = dict(loginInfo)

	if ne(info["loggin_buffered_level"], ""):
		v = info["loggin_buffered_level"]
		general_info["logging"]["buffered"] = {
			"level": int(v) if type(v) == float else v
		}

	if ne(info["loggin_sychronous"], ""):
		v = info["loggin_sychronous"]
		general_info["logging"]["synchronous"] = {
			"level": info["loggin_sychronous"]
		}

	# Group Vars all.yml 파일 생성
	terminalLength = int(info["terminal_length"]) if type(info["terminal_length"]) == float else info["terminal_length"]
	termninalWidth = int(info["terminal_width"]) if type(info["terminal_width"]) == float else info["terminal_width"]
	bgp_maximum_paths = int(info["bgp_maximum_paths"]) if type(info["bgp_maximum_paths"]) == float else info["bgp_maximum_paths"]
	bgp_ecmp = int(info["bgp_ecmp"]) if type(info["bgp_ecmp"]) == float else info["bgp_ecmp"]
	data = {
		"terminal_length": terminalLength,
		"terminal_width": termninalWidth,
		"spanning_tree_mode": info["spanning_tree_mode"],
		"timezone": info["time_zone"],
		"ip_route": info["ip_route"],
		"default_mgmt": info["mgmt_interface_vrf"],
		"banner_login": info["banner_login"],
		"bgp_maximum_paths": bgp_maximum_paths,
		"bgp_ecmp": bgp_ecmp,
		"p2p_ipv4_pool": info["p2p_ipv4_pool"]
	}
	
	with open('./templates/allyml.j2') as f:
		template = Template(f.read())

	with open("./inventory/group_vars/all.yml", "w") as reqs:
			reqs.write(template.render(**data))
   
	return general_info

def generateGroupVarsAll(inventory_file, excelVar):
    return parseGeneralInfo(inventory_file, excelVar)