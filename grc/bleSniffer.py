# https://nabeelvalley.co.za/docs/iot/bluetooth-intro/
from scapy.all import *
import asyncio
from bleak import BleakScanner, BleakClient
import chardet
from deep_translator import GoogleTranslator

from construct import Array, Byte, Const, Int8sl, Int16ub, Struct
from construct.core import ConstError

from uuid import UUID
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

ibeacon_format = Struct(
    "type_length" / Const(b"\x02\x15"),
    "uuid" / Array(16, Byte),
    "major" / Int16ub,
    "minor" / Int16ub,
    "power" / Int8sl,
)

def device_found(
    device: BLEDevice, advertisement_data: AdvertisementData
):
    """Decode iBeacon."""
    try:
        apple_data = advertisement_data.manufacturer_data[0x004C]
        ibeacon = ibeacon_format.parse(apple_data)
        uuid = UUID(bytes=bytes(ibeacon.uuid))
        print(f"UUID     : {uuid}")
        print(f"Major    : {ibeacon.major}")
        print(f"Minor    : {ibeacon.minor}")
        print(f"TX power : {ibeacon.power} dBm")
        print(f"RSSI     : {device.rssi} dBm")
        print(47 * "-")
    except KeyError:
        # Apple company ID (0x004c) not found
        pass
    except ConstError:
        # No iBeacon (type 0x02 and length 0x15)
        pass

yandex = GoogleTranslator(source='auto', target='fr')

async def pair(client):
    try:
        await client.pair()
    except NotImplementedError:
        # This is expected on Mac
        pass

async def bleScan():
    pwtx, rssi, man, services, suid, uuid='', '', '', '', '', ''
    cpt = 0
    arr = []

    devices = await BleakScanner.discover()
    for d in devices:
        try:
            t=dict(d.details)
            client = BleakClient(d)
            if (t['props']['RSSI']>-80 and (t['props']['TxPower']<10) and cpt<3):
                
                await client.connect()
                #await pair(client)
                cpt+=1

            rssi=t['props']['RSSI'] if 'RSSI' in t['props'] else None
            pwtx=t['props']['TxPower'] if 'TxPower' in t['props'] else None
            uuid=t['props']['UUIDs'] if 'UUIDs' in t['props'] else []
            
            if (len(uuid)): 
                k=t['props']['ManufacturerData'].keys() if 'ManufacturerData' in t['props'] else []
                for v,i in enumerate(k):
                    detection = chardet.detect(t['props']['ManufacturerData'][i])
                    encoding = detection["encoding"] if detection["encoding"] else 'utf-8'
                    if isinstance(t['props']['ManufacturerData'][i], bytearray):
                        man=t['props']['ManufacturerData'][i].decode(encoding, 'ignore')
                        man=man.encode('big5', 'ignore').decode('utf-16be', 'ignore')
                        man=yandex.translate(man).encode('utf-16be', 'ignore').decode('utf-8', 'ignore').replace('\x00', '')

                k=t['props']['ServiceData'].keys() if 'ServiceData' in t['props'] else []
                for v,i in enumerate(k):
                    suid=i
                    detection = chardet.detect(t['props']['ServiceData'][i])
                    encoding = detection["encoding"] if detection["encoding"] else 'utf-8'
                    if isinstance(t['props']['ServiceData'][i], bytearray):
                        man=t['props']['ServiceData'][i].decode(encoding, 'ignore')
                        man=man.encode('big5', 'ignore').decode('utf-16be', 'ignore')
                        services=yandex.translate(man).encode('utf-16be', 'ignore').decode('utf-8', 'ignore').replace('\x00', '')

                addr=t['props']['Address'] if 'Address' in t['props'] else ''
                arr.append({ "rssi": rssi, "pwtx": pwtx, "manufact": man, "suid": suid, "services": services, "uuid": uuid, "addr": addr })
                
                print(man)
                print(services)

        except Exception as e:
            print(e)
            pass

    return arr
