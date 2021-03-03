import logging
import sys
import time
from datetime import date
from datetime import datetime

import imutils
import requests
from beepy import beep
from imutils.video import VideoStream
from pyzbar import pyzbar

import config
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(filename='{}/logs/{}.log'.format(ROOT_DIR, date.today().strftime("%Y_%m_%d")), level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s][%(filename)s][%(funcName)s][%(lineno)d]:%(message)s')

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logger = logging.getLogger()


def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))


sys.excepthook = my_handler

vs = VideoStream().start()
time.sleep(2.0)

logging.info('{}: STARTED SCANNING...'.format(datetime.now().isoformat()))

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
            logging.info(
                '{}: SCAN SUCCESSFUL (UUID: {})'.format(datetime.now().isoformat(), barcode.data.decode("utf-8")))
        elif 400 <= response.status_code <= 499:
            beep(sound='error')
            logging.error(
                '{}: BAD REQUEST {}'.format(datetime.now().isoformat(), response.content))
        elif response.status_code <= 500:
            beep(sound='error')
            logging.error(
                '{}: SERVER ERROR {})'.format(datetime.now().isoformat(), response.content))
        else:
            beep(sound='error')
            logging.error(
                '{}: SOMETHING WENT WRONG {}'.format(datetime.now().isoformat(), response.content))

    time.sleep(3)
