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
typeCol = excelVar["pd"]["switchIpInfo"]["type"]
idCol = excelVar["pd"]["switchIpInfo"]["id"]
p2pSubnet = info["p2p_subnet"]

## Switch 정보 로드
switches = pd.read_excel(inventory_file, header=headerRow, sheet_name=sheetName)[[hostNameCol, typeCol, idCol]]

switchInfo = {}
## Switch별 cfg 파일 생성
for idx, switch in switches.iterrows():
  hostname = switch[hostNameCol] 
  
  switchInfo.setdefault(
    hostname, {
      "ID": switch[idCol]
    }
  )

sheetName = excelVar["pd"]["portMap"]["sheetName"]
headerRow = excelVar["pd"]["portMap"]["header"]
spineCol = excelVar["pd"]["portMap"]["spine"]
spinePortCol = excelVar["pd"]["portMap"]["spinePort"]
spineIpCol = excelVar["pd"]["portMap"]["spineIp"]
leafCol = excelVar["pd"]["portMap"]["leaf"]
leafPortCol = excelVar["pd"]["portMap"]["leafPort"]
leafIpCol = excelVar["pd"]["portMap"]["leafIp"]

spinePrefix = excelVar["spine"]["prefix"]
leafPrefix = excelVar["leaf"]["prefix"]

## Switch 정보 로드
switches = pd.read_excel(inventory_file, header=headerRow, sheet_name=sheetName)[[spineCol, spinePortCol, spineIpCol, leafCol, leafPortCol, leafIpCol]].dropna(axis=0)

portMap = {}

for idx, switch in switches.iterrows():
  
  ## port channell
  p = re.compile(leafPrefix)
  # print(switch[spineCol], switch[leafCol])
  if (p.match(str(switch[leafCol])) and p.match(str(switch[spineCol]))):
    leaf = switch[leafCol]
    if not leaf in portMap:
      ip = ipaddress.ip_network(switch[leafIpCol])[switchInfo[leaf]["ID"]]
      portMap.setdefault(
        leaf,  {
          "IP": str(ip) + "/" + str(p2pSubnet),
          "ID": switchInfo[leaf]["ID"],
          "INTERFACES": [{ "ETHERNET": switch[leafPortCol] }]
        }
      )
    else:
      portMap[leaf]["INTERFACES"].append({ "ETHERNET": switch[leafPortCol] })

    leaf = switch[spineCol]
    if not leaf in portMap:
      ip = ipaddress.ip_network(switch[spineIpCol])[switchInfo[leaf]["ID"]]
      portMap.setdefault(
        leaf,  {
          "IP": str(ip) + "/" + str(p2pSubnet),
          "ID": switchInfo[leaf]["ID"],
          "INTERFACES": [{ "ETHERNET": switch[spinePortCol] }]
        }
      )
    else:
      portMap[leaf]["INTERFACES"].append({ "ETHERNET": switch[spinePortCol]})

## Switch별 cfg 파일 생성
with open('./templates/config/etcport.j2') as f:
  template = Template(f.read())
  f.close()

switchInfo.update(portMap)
for switch in switchInfo:
  # print(switch)
  hostname = switch  
  with open("./inventory/intended/configs/" + hostname + ".cfg", "w", encoding='utf8') as reqs:
    reqs.write(template.render(SWITCH=switchInfo[switch]))
    reqs.close()