#!/bin/bash
suda apt-get update
sudo apt-get install libatlas-base-dev

git clone https://github.com/dsmanyp/tac-qrcode-scanner.git /home/pi/Desktop/qrcode-scanner
sudo chmod +x /home/pi/Desktop/qrcode-scanner/start.sh

python3 -m venv qrcode-scanner-venv
source /home/pi/Desktop/qrcode-scanner-venv/bin/activate

pip3 install -r /home/pi/Desktop/qrcode-scanner/requirements.txt
