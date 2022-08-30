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

sheetName = excelVar["pd"]["switchIpInfo"]["sheetName"]
headerRow = excelVar["pd"]["switchIpInfo"]["header"]
hostNameCol = excelVar["pd"]["switchIpInfo"]["hostName"]
loopback0Col = excelVar["pd"]["switchIpInfo"]["loopback0"]

## Switch 정보 로드
switches = pd.read_excel(inventory_file, header=headerRow, sheet_name=sheetName)[[hostNameCol, loopback0Col]]

## Switch별 cfg 파일 생성
with open('./templates/config/loop0.j2', encoding='utf8') as f:
  template = Template(f.read())
  f.close()

for idx, switch in switches.iterrows():  
  with open("./inventory/intended/configs/" + switch[hostNameCol] + ".cfg", "w", encoding='utf8') as reqs:   
    reqs.write(template.render(**{ "LOOPBACK0": switch[loopback0Col]}))
    reqs.close() 