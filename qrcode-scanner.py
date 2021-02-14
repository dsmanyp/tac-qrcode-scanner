import time
from datetime import datetime

import imutils
import requests
from beepy import beep
from imutils.video import VideoStream
from pyzbar import pyzbar

import config

vs = VideoStream().start()
time.sleep(2.0)

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        data = {
            'scanner_uuid': config.SCANNER_UUID,
            'data': barcode.data.decode("utf-8"),
            'type': config.SCAN_TYPE,
            'scan_time': '{}Z'.format(datetime.utcnow().isoformat())
        }

        response = requests.post('{}{}'.format(config.DOMAIN, config.URL), data)

        if response.status_code == 201 or response.status_code == 200:
            beep(sound='coin')
            print(barcode.data.decode("utf-8"))
        else:
            beep(sound='error')

    time.sleep(3)
