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
with open("./generators/excelEnvriment.json", "r", encoding='utf8') as f:
  excelVar = json.load(f)
  f.close()
  
info = {}
for item in excelVar["all"]:
  v = getExcelSheetValue(workbook, excelVar["all"][item])
  info[excelVar["all"][item]["mapping"]] = v


## Switch ID 확인
sheetName = excelVar["pd"]["switchIpInfo"]["sheetName"]
headerRow = excelVar["pd"]["switchIpInfo"]["header"]
hostNameCol = excelVar["pd"]["switchIpInfo"]["hostName"]
loop1Col = excelVar["pd"]["switchIpInfo"]["loopback1"]

## Switch 정보 로드
switches = pd.read_excel(inventory_file, header=headerRow, sheet_name=sheetName)[[hostNameCol, loop1Col]].fillna("")

portMap = {}
## Switch별 cfg 파일 생성
for idx, switch in switches.iterrows():
  hostname = switch[hostNameCol] 
  
  if switch[loop1Col] != "":
    loopback1 = str(switch[loop1Col]) + "/32"  if switch[loop1Col] != "" else ""
    ip = str(ipaddress.IPv4Interface(str(switch[loop1Col]) + "/24").network)
  else:
    loopback1 = ""
    ip = ""
    
  portMap.setdefault(
    hostname, {
      "LOOPBACK1": loopback1,
      "PERMIT_IP": ip
    }
  )

# print(portMap)

## Switch별 cfg 파일 생성
with open('./templates/config/vxlan.j2') as f:
  template = Template(f.read())
  f.close()


for switch in portMap:
  # print(switch)
  hostname = switch  
  with open("./inventory/intended/configs/" + hostname + ".cfg", "w", encoding='utf8') as reqs:
    reqs.write(template.render(**portMap[switch]))
    reqs.close()