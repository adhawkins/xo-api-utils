#!/usr/bin/env python3

import argparse
from quantiphy import Quantity
import sys

from xoAPI.xoAPI import xoAPI
import authentication


def getDescriptionString(sr, pools):
    return f"{sr['name_label']} on {pools[sr['$poolId']]}"


parser = argparse.ArgumentParser(description='Dump SR usage')

parser.add_argument('xo-url', help='The URL of the XO server')

args = parser.parse_args()

api = xoAPI(getattr(args, 'xo-url'), authentication.TOKEN)

pools = {}

poolData = api.makeRequest("pools?fields=uuid,name_label")

for pool in poolData:
    pools[pool['uuid']] = pool['name_label']

srs = api.makeRequest("srs?fields=size,physical_usage,name_label,$poolId")

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

        print(
            f"{descriptionString:{maxLength}} {usage:>10.2b} {size:>10.2b} {usage/size*100:9.2f}%")
