# This file gets the time from an api and sets it
# so that the pi does not have to rely on ntp which
# does not work on our WiFi because port 123 (the 
# port ntp uses) is blocked. This file is meant to
# run at startup

import os
from time import sleep
import requests

sleep(60) # So that when script is run on startup, it will have the pi systems fully enabled

try:
    response = requests.get("http://worldtimeapi.org/api/timezone/America/Los_Angeles")
    data = response.json()["unixtime"]

    os.system(f"sudo date -s @{data}")

    print("time set")
except:
    os.system("sudo timedatectl set-ntp true")
    print("ntp enabled")