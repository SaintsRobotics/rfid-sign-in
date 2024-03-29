### arduino_running_code
*The code uploaded to the arduino, to be in use the majority of the time*

* Outputs the (custom) UUID to Serial as cards are scanned
* Double beep -> error

### write_tags
*A utility to write UUIDs (integer, 0-2^32) to RFID tags*

* User enters an initial ID number (ie 42) and the arduino writes identifiers in single increments from that as tags are scanned (first tag -> 42, second -> 43, etc)
* Writing "saints" to a sector alongside those is a WIP

### main.py [intended to be put on a raspi and ran on boot]
*Reads ids from arduino as scanned and processes them*

* Reads the hex UUIDs outputted by `arduino_running_code.ino` in Serial, and writes the scan time (and associated id) to a csv
* Contains logic for distinguishing sign-ins and sign-outs
* correlates UUIDs to names, student ids, emails, etc and puts that in a "final" csv, to be sent off to the requisite target(s)

### time.py [intented to be put on a raspi and ran on boot]
*Sends a request to a time API and sets the raspi local time*

* Intended for a network which blocks port 123 (used for NTP)
* Sends a request to the World Time API to get the current time
* Sets raspi time to the current time so that sign in times can be accurate

### upload.py [intente to be put on a raspi and ran perioically]
*Sends an email with the attendance csv attached*

* Sends it to a single secified recipient
* Automates sending of the csv

### web_server.py and HTML files [meant to be put on a raspi and ran on boot]
*Runs a local web server (using Flask) which can be used to input attendance if someone forgets their RFID tag*

* Stores attendance in the same file as the scanner code
* Can be used interchangebly with the RFID scanner
* The days attendance is viewable through another port on the raspi
* http:// (raspi ip adress):8000
* /admin shows attendance for the day
* /form is where you log in

### Probably out of scope ideas
* Automate sending of csvs (will be using google drive api)
* Purchase and use a small screen attached to the pi to veriy that the process worked
* Have the pi host a small web server so that people without RFID tags can still sign in
