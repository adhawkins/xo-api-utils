#!/usr/bin/env python3

import argparse
from quantiphy import Quantity

import authentication
from xoAPI.xoAPI import xoAPI

def transform(val):
	return {d['id']: d for d in val}

def hostsInPool(hosts, poolId):
	ret = {}
	for host in hosts.values():
		if host['$poolId']==poolId:
			ret[host['id']]=host

	return ret

def vmsInPool(vms, poolId):
	ret = {}
	for vm in vms.values():
		if vm['$container']==poolId:
			ret[vm['id']]=vm

	return ret

def vmsOnHost(vms, hostId):
	ret = {}
	for vm in vms.values():
		if vm['$container']==hostId:
			ret[vm['id']]=vm

	return ret

def printVM(vm, indent):
	tab = '\t'
	RAM = Quantity(vm['memory']['size'], 'B')
	print(f"{tab * indent}VM: '{vm['name_label']}' - CPUs: {vm['CPUs']['number']}, RAM: {RAM:b}")
	for vbd in vm['$VBDs']:
		if vbd in vdis:
			vdi = vdis[vbd]
			size = Quantity(vdi['size'], 'B')
			print(f"{tab * (indent + 1)}VDI: '{vdi['name_label']}' - {size:b}")

parser = argparse.ArgumentParser(description='View VM snapshot info')

parser.add_argument('xo-url', help='The URL of the XO server')

args = parser.parse_args()

api = xoAPI(getattr(args, 'xo-url'), authentication.TOKEN)

pools = transform(api.makeRequest("pools?fields=id,name_label,name_description"))
hosts = transform(api.makeRequest("hosts?fields=id,$poolId,cpus,hostname,memory,name_label,name_description,power_state,version"))
vms = transform(api.makeRequest("vms?fields=id,$VBDs,$pool,$container,CPUs,memory,name_label,name_description"))

vdis={}
rawvdis = api.makeRequest("vdis?fields=$VBDs,$id,size,name_label,name_description,usage")
for vdi in rawvdis:
	if vdi['$VBDs']:
		vdis[vdi['$VBDs'][0]] = vdi

for pool in pools.values():
	print(f"Pool: {pool['name_label']}")

	for vm in vmsInPool(vms, pool['id']).values():
		printVM(vm, 1)

	for host in hostsInPool(hosts, pool['id']).values():
		RAM = Quantity(host['memory']['size'], 'B')
		print(f"\tHost: {host['name_label']}, CPUs: {host['cpus']['cores']} cores, {host['cpus']['sockets']} sockets, RAM: {RAM:b}")

		for vm in vmsOnHost(vms, host['id']).values():
			printVM(vm, 2)
