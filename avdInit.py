import yaml, os, subprocess
from generators.generateInventory import generateInventory, getFabricName
from generators.generateGroupVarsAll import generateGroupVarsAll
from generators.generateGroupVarsFabric import generateGroupVarsFabric
from generators.generateGroupVarsTenants import generateGroupVarsTenants
from generators.generateGroupVarsServers import generateGroupVarsServers
from generators.envirmentVariables import *
from jinja2 import Template
from generators.BlankNone import BlankNone
import bootstrapGen, json

import argparse

def taskPrint(task):
	task = task + " "
	print(task.ljust(100, "*") + "\n")

def main():
    
	taskPrint("TASK [Start]")
	parser = argparse.ArgumentParser(
			description='Creates necessary files to run Arista AVD ansible playbook')
	parser.add_argument('-f', '--file', help="path to Excel file")

	file_location = "./inventory.xlsx"
	if file_location is None:
			print("Please specify a path for the Excel file by using -f. Enter 'python main.py -h' for more details.")
			return

	with open("./generators/excelEnvriment.json", "r") as f:
		excelVar = json.load(f)
		f.close()
  
	fabric_name = getFabricName(file_location, excelVar)
	avd = {
		"inventory": None,
		"group_vars": {
			fabric_name: None,
			fabric_name + "_FABRIC": None,
			fabric_name + "_TENANTS_NETWORKS": None,
			fabric_name + "_SERVERS": None
			},
		"requirements": None,
	}

	taskPrint("TASK [inventory Parsing]")
	avd["inventory"] = generateInventory(file_location, excelVar)

	# # ALL -> fabric_name 으로 변경
	# avd["group_vars"][fabric_name] = generateGroupVarsAll(file_location, excelVar) 

	# taskPrint("TASK [Group Vars Fabric Parsing]")
	# avd["group_vars"][fabric_name + "_FABRIC"] = generateGroupVarsFabric(file_location, excelVar)

	# taskPrint("TASK [Group Vars Tenants Parsing]")
	# avd["group_vars"][fabric_name + "_TENANTS_NETWORKS"] = generateGroupVarsTenants(file_location)

	# taskPrint("TASK [Group Vars Servers Parsing]")
	# avd["group_vars"][fabric_name + "_SERVERS"] = generateGroupVarsServers(file_location)

	#Create inventory file
	# yaml.dump시 sort_keys=False 값을 주지 않으면 키값 기준으로 오름차순으로 정렬되어 적용됨
	# sort_keys=False 실제 적용한 값 순서대로 처리
	taskPrint("TASK [inventory.yml Generate]")
	with BlankNone(), open("./inventory/inventory.yml", "w") as inv:
			inv.write(yaml.dump(avd["inventory"], sort_keys=False))

	taskPrint("TASK [Group Vars *.yml Generate]")
	#Create group_vars files

	# deploy playbook 생성
	taskPrint("TASK [deploy.yml PlayBook Generate]")
	data = { "fabricName" : fabric_name }
	with open('./templates/deploy.j2', encoding='utf8') as f:
		template = Template(f.read())

	with open("./deploy.yml", "w", encoding='utf8') as reqs:
			reqs.write(template.render(**data))

	with open('./templates/config.j2', encoding='utf8') as f:
		template = Template(f.read())

	with open("./config.yml", "w", encoding='utf8') as reqs:
			reqs.write(template.render(**data))

	with open('./templates/design.j2', encoding='utf8') as f:
		template = Template(f.read())

	with open("./design.yml", "w", encoding='utf8') as reqs:
			reqs.write(template.render(**data))

	bootstrapGen.bootstrapFirstBootPythonCreate()

if __name__ == "__main__":
	main()