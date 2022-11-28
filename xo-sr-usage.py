#!/usr/bin/env python3

import authentication
import requests

from quantiphy import Quantity

BASE_URL="https://xcp-xo-amd.gently.org.uk:9443"
API_BASE="/rest/v0/"

def getDescriptionString(sr, pools):
	return f"{sr['name_label']} on {pools[sr['$poolId']]}"

def makeRequest(request):
	cookies = {
		"authenticationToken": authentication.TOKEN
	}

	ret = requests.get(request, cookies = cookies)
	ret.raise_for_status()
	return ret.json()

pools={}

poolUUIDs = makeRequest(f"{BASE_URL}{API_BASE}pools")

for poolUUID in poolUUIDs:
	poolParams = makeRequest(f"{BASE_URL}{poolUUID}")
	pools[poolParams['uuid']] = poolParams['name_label']

srs=[]

srUUIDs = makeRequest(f"{BASE_URL}{API_BASE}srs")

for srUUID in srUUIDs:
	srParams = makeRequest(f"{BASE_URL}{srUUID}")
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

		print(f"{descriptionString:{maxLength}}: {usage:>10.2b} {size:>10.2b} {usage/size*100:9.2f}%")

