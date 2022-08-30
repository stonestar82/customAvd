# -*- coding: utf-8 -*-
import json
from pprint import pprint
from generators.BlankNone import *
from generators.generateInventory import *
from openpyxl import load_workbook
from operator import eq
from jinja2 import Template
import pandas as pd

inventory_file = "inventory.xlsx"
workbook = load_workbook(filename=inventory_file, read_only=False, data_only=True)

## 기본변수 로드
with open("./generators/excelEnvriment.json", "r") as f:
  excelVar = json.load(f)
  f.close()
  
info = {}
for item in excelVar["all"]:
  v = getExcelSheetValue(workbook, excelVar["all"][item])
  info[excelVar["all"][item]["mapping"]] = v

mgmtVrf = info["mgmt_interface_vrf"]
macAging = info["mac_aging"]
arpAging = info["arp_aging"]
timeZone = info["time_zone"]
adminName = info["admin_name"]
adminPassword = info["admin_info"]
admin_privilege = info["admin_privilege"]
spanningTreeMode = info["spanning_tree_mode"]
terminalLength = info["terminal_length"]
terminalWidth = info["terminal_width"]
logginBufferedLevel = info["loggin_buffered_level"]

sheetName = excelVar["pd"]["switchIpInfo"]["sheetName"]
headerRow = excelVar["pd"]["switchIpInfo"]["header"]
hostNameCol = excelVar["pd"]["switchIpInfo"]["hostName"]
mgmtCol = excelVar["pd"]["switchIpInfo"]["mgmt"]

## Switch 정보 로드
switches = pd.read_excel(inventory_file, header=headerRow, sheet_name=sheetName)[[hostNameCol, mgmtCol]]

## Switch별 cfg 파일 생성
with open('./templates/config/base.j2', encoding='utf8') as f:
  template = Template(f.read())
  f.close()

data = {
        "TERMINAL_LENGTH": terminalLength,
        "TERMINAL_WIDTH": terminalWidth,
        "LOGGIN_BUFFERED": logginBufferedLevel,
        "SPANNING_TREE_MODE": spanningTreeMode,
        "ADMIN_USER_NAME": adminName,
        "ADMIN_USER_PW": adminPassword,
        "TIMEZONE": timeZone,
        "ARP_AGING": arpAging,
        "MAC_AGING": macAging,
        "MGMT_VRF": mgmtVrf,
        "ADMIN_PRIVILEGE": admin_privilege
      }

for idx, switch in switches.iterrows():  
  with open("./inventory/intended/configs/" + switch[hostNameCol] + ".cfg", "w", encoding='utf8') as reqs:   
    reqs.write(template.render(**data))
    reqs.close() 