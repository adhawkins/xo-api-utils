#!/usr/bin/env python3

import argparse
import sys
from datetime import datetime
from operator import itemgetter

import authentication
from xoAPI.xoAPI import xoAPI

parser = argparse.ArgumentParser(description='View VM snapshot info')

parser.add_argument('xo-url', help='The URL of the XO server')

args = parser.parse_args()

api = xoAPI(getattr(args, 'xo-url'), authentication.TOKEN)
now = datetime.now()

info = {}

vms = api.makeRequest("vms?fields=name_label,id")

for vm in vms:
    vmName = vm['name_label']
    vmUUID = vm['id']

    vmSnapshots = api.makeRequest(
        f"vm-snapshots?filter=%24snapshot_of:{vmUUID}&fields=name_label,snapshot_time")

    vmSnapshotInfo = []

    for vmSnapshot in vmSnapshots:
        snapshotData = {
            'name': vmSnapshot['name_label'],
            'time': vmSnapshot['snapshot_time'],
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
