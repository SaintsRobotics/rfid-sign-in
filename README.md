### arduino_running_code
*The code uploaded to the arduino, to be in use the majority of the time*

* Outputs the (custom) UUID to Serial as cards are scanned
* Double beep -> error

### write_tags
*A utility to write UUIDs (integer, 0-2^32) to rfid tags*

* User enters an initial ID number (ie 42) and the arduino writes identifiers in single increments from that as tags are scanned (first tag -> 42, second -> 43, etc)
* Writing "saints" to a sector alongside those is a WIP

### main.py [intended to be put on a raspi]
*Reads ids from arduino as scanned and processes them*

* Reads the hex UUIDs outputted by `arduino_running_code.ino` in Serial, and writes the scan time (and associated id) to a csv
* Contains logic for distinguishing sign-ins and sign-outs
* correlates UUIDs to names, student ids, emails, etc and puts that in a "final" csv, to be sent off to the requisite target(s)

### Probably out of scope ideas
* Automate sending of csvs
