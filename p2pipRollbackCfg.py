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
  
  ## spine switch 정리
  p = re.compile(spinePrefix)
  if (p.match(str(switch[spineCol]))):
    spine = switch[spineCol]
    if not spine in portMap:
      portMap.setdefault(
        spine,  {
          "INTERFACES": [{ "ETHERNET": switch[spinePortCol], "IP": switch[spineIpCol] }]
        }
      )
    else:
      portMap[spine]["INTERFACES"].append({ "ETHERNET": switch[spinePortCol], "IP": switch[spineIpCol] })
      
  ## leaf switch 정리
  p = re.compile(leafPrefix)
  if (p.match(str(switch[leafCol]))):
    leaf = switch[leafCol]
    if not leaf in portMap:
      portMap.setdefault(
        leaf,  {
          "INTERFACES": [{ "ETHERNET": switch[leafPortCol], "IP": switch[leafIpCol] }]
        }
      )
    else:
      portMap[leaf]["INTERFACES"].append({ "ETHERNET": switch[leafPortCol], "IP": switch[leafIpCol] })

## Switch별 cfg 파일 생성
with open('./templates/config/p2pipRollback.j2') as f:
  template = Template(f.read())
  f.close()

for switch in portMap:
  hostname = switch  
  with open("./inventory/intended/configs/" + hostname + ".cfg", "w", encoding='utf8') as reqs:
    reqs.write(template.render(SWITCH=portMap[switch]))
    reqs.close() 