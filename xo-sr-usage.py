#!/usr/bin/env python3

import argparse
from quantiphy import Quantity
import sys

from xoAPI.xoAPI import xoAPI
import authentication

parser = argparse.ArgumentParser(description = 'Dump SR usage')

parser.add_argument('--xo-url', type=str, help='The URL of the XO server', required=True)

args = parser.parse_args()

api = xoAPI(args.xo_url, authentication.TOKEN)

def getDescriptionString(sr, pools):
	return f"{sr['name_label']} on {pools[sr['$poolId']]}"

pools={}

poolUUIDs = api.makeRequest("pools")

for poolUUID in poolUUIDs:
	poolParams = api.makeRequest(poolUUID)
	pools[poolParams['uuid']] = poolParams['name_label']

srs=[]

srUUIDs = api.makeRequest("srs")

for srUUID in srUUIDs:
	srParams = api.makeRequest(srUUID)
	srs.append(srParams)

maxLength = 0

for sr in srs:
	size = sr['size']

	if size > 0:
		descriptionString = getDescriptionString(sr, pools)
		if len(descriptionString) > maxLength:
			maxLength = len(descriptionString)

srTitle = "SR"
usedTitle = "Used"
totalTitle = "Total"
percentTitle = "Percentage"
underLine = "="
print(f"{srTitle:^{maxLength}s}  {usedTitle:^10s} {totalTitle:^10s} {percentTitle:^6s}")
print(f"{underLine * maxLength}=={underLine * 10}={underLine * 10}={underLine * 10}")


for sr in srs:
	size = Quantity(sr['size'], 'B')

	if size > 0:
		usage = Quantity(sr['physical_usage'], 'B')

		descriptionString = getDescriptionString(sr, pools)

		print(f"{descriptionString:{maxLength}} {usage:>10.2b} {size:>10.2b} {usage/size*100:9.2f}%")

