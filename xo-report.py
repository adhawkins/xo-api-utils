#!/usr/bin/env python3

import argparse
from quantiphy import Quantity

import authentication
from xoAPI.xoAPI import xoAPI

def transform(val):
	return {d['id']: d for d in val}

parser = argparse.ArgumentParser(description='View VM snapshot info')

parser.add_argument('xo-url', help='The URL of the XO server')

args = parser.parse_args()

api = xoAPI(getattr(args, 'xo-url'), authentication.TOKEN)

vms = transform(api.makeRequest("vms?fields=id,$VBDs,$pool,CPUs,memory,name_label,name_description"))

vdis={}
rawvdis = api.makeRequest("vdis?fields=$VBDs,$id,size,name_label,name_description,usage")
for vdi in rawvdis:
	if vdi['$VBDs']:
		vdis[vdi['$VBDs'][0]] = vdi

for vm in vms.values():
	RAM = Quantity(vm['memory']['size'], 'B')
	print(f"VM: '{vm['name_label']}' - CPUs: {vm['CPUs']['number']}, RAM: {RAM:.2b}")
	for vbd in vm['$VBDs']:
		if vbd in vdis:
			vdi = vdis[vbd]
			size = Quantity(vdi['size'], 'B')
			print(f"\tVDI: '{vdi['name_label']}' - {size:.3b}")
