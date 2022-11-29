#!/usr/bin/env python3

import argparse
import sys
from datetime import datetime
from operator import itemgetter

from quantiphy import Quantity

import authentication
from xoAPI.xoAPI import xoAPI

parser = argparse.ArgumentParser(description='View VM snapshot info')

parser.add_argument('--xo-url', type=str,
                    help='The URL of the XO server', required=True)

args = parser.parse_args()

api = xoAPI(args.xo_url, authentication.TOKEN)
now = datetime.now()

info = {}

vms = api.makeRequest("vms")

for vm in vms:
    vmUUID = vm.split('/')[-1]

    vmInfo = api.makeRequest(vm)
    vmName = vmInfo['name_label']

    vmSnapshots = api.makeRequest(
        f"vm-snapshots?filter=%24snapshot_of:{vmUUID}")

    vmSnapshotInfo = []

    for vmSnapshot in vmSnapshots:
        snapshotInfo = api.makeRequest(vmSnapshot)

        snapshotData = {
            'name': snapshotInfo['name_label'],
            'time': snapshotInfo['snapshot_time'],
        }

        vmSnapshotInfo.append(snapshotData)

    info[vmName] = sorted(vmSnapshotInfo, key=itemgetter('time'))

for vm in sorted(info.keys()):
    print(f"{vm}:")

    for snapshot in info[vm]:
        snapshotTime = datetime.fromtimestamp(snapshot['time'])
        snapshotAge = now - snapshotTime
        if snapshotAge.days:
            print(f"\t{snapshot['name']}: {snapshotAge.days} days ago")
        elif snapshotAge.seconds//3600:
            print(
                f"\t{snapshot['name']}: {snapshotAge.seconds//3600} hours ago")
        else:
            print(f"\t{snapshot['name']}: Recently")

    print()
