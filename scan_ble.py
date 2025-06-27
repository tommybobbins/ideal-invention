import sys

sys.path.append("")

from micropython import const

import asyncio
import aioble
import bluetooth
import binascii

import random
import struct
import array
import numpy as np

devlist= []
known_devices = [  '56:c2:0f:2c:8d:db',
                   '45:6e:7c:ab:67:8b',
                   '41:6a:8d:90:7a:08',
                   'c2:33:6e:40:4d:aa',
                ]

async def scan_devices():
    
  
    async with aioble.scan(3000, interval_us=30000, window_us=30000, active=True) as scanner:
        devlist = []
        async for result in scanner:
            #if result.name():
            #    print(result, '::', binascii.hexlify(result.device.addr,':'), '::', result.name(), '::', result.rssi, '::')
            
            xx = [ binascii.hexlify(result.device.addr,':') , result.name() ]
            devlist.append(xx)
    return devlist


async def main():
    devices = await scan_devices()
    new_devices = list(np.array(devices) - np.array(known_devices))
    for dev in devices:
        print(dev)
    for dev in new_devices:
        print(f, 'New device {dev}')
   
asyncio.run(main())
