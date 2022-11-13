from time import sleep
import serial
from datetime import datetime, timedelta
import os
import csv

sleep(60) # So that when script is run on startup, it will have the pi systems fully enabled

TIMESTAMP_FORMAT = "%m/%d/%Y %H:%M:%S"

STUDENTS_FILEPATH = 'students.csv'  # this is the CSV file where student names and IDs are stored.  Do not write to this file
STUDENTS_FILEPATH = '/home/admin/rfid-sign-in/students.csv'
STUDENTS_HEADER = ["FIRST_NAME", "LAST_NAME", "STUDENT_ID", "RFID_TAG_NUMBER"]

ATTENDANCE_LOG_FILEPATH = '/home/admin/rfid-sign-in/attendance/attendance-' + str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + \
    '.csv'  # this is the CSV file that the sign ins and outs are logged
ATTENDANCE_LOG_HEADER = ["TIMESTAMP", "IN_OR_OUT"] + STUDENTS_HEADER

######## CONNECTING TO SERIAL BUS ########
"""Comment out the appropriate lines below depending on which operating system this is running on."""
ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)
# ser = serial.Serial("COM8", baudrate=115200, timeout=1)

print("CONNECTED")
# TODO add more checks in the arduino code and here to make sure there aren't any hardware issues.
# This includes adding a handshake on startup.



def get_student_info(rfidTagNumber: int):
    """Looks up the user's first and last name and student ID number in the database.
    Returns a dictionary of the student's """
    with open(STUDENTS_FILEPATH, 'r') as file:
        for row in csv.DictReader(file):
            if int(row["RFID_TAG_NUMBER"]) == rfidTagNumber:
                return row
        file.close()
    print("STUDENT NOT FOUND.  RFID TAG #", rfidTagNumber)
    # TODO: make a better interface for this
    return {}


def log_user(rfidTagNumber: int):
    """
    Logs the user sign in/out in the CSV file.
    uid: the number that the user's rfid tag was assigned.  we started at 1, and just counted up from there
    """

    row = {}  # the data that gets written to the csv

    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    row["TIMESTAMP"] = timestamp

    row["RFID_TAG_NUMBER"] = rfidTagNumber

    student_info = get_student_info(rfidTagNumber)
    if student_info:  # only writes to the attendance log if the RFID tag number is valid
        row.update(student_info)

        #### MAKING SURE THE CSV FILE EXISTS and creating it if it doesn't ####
        ATTENDANCE_LOG_FILEPATH = '/home/admin/rfid-sign-in/attendance/attendance-' + str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + '.csv'
        if not os.path.exists(ATTENDANCE_LOG_FILEPATH):
            with open(ATTENDANCE_LOG_FILEPATH, 'w') as file:
                csv.DictWriter(file, fieldnames=ATTENDANCE_LOG_HEADER, quoting=csv.QUOTE_ALL).writeheader()
            file.close()

        row["IN_OR_OUT"] = "SIGN_IN"
        with open(ATTENDANCE_LOG_FILEPATH, "r") as readFile:
            for line in csv.DictReader(readFile):
                if int(line["RFID_TAG_NUMBER"]) == int(row["RFID_TAG_NUMBER"]) and line["IN_OR_OUT"] == "SIGN_IN":
                    row["IN_OR_OUT"] = "SIGN_OUT"
                elif int(line["RFID_TAG_NUMBER"]) == int(row["RFID_TAG_NUMBER"]):
                    row["IN_OR_OUT"] = "SIGN_IN"
        readFile.close()

        with open(ATTENDANCE_LOG_FILEPATH, "a+") as writeFile:
            csv.DictWriter(writeFile, fieldnames=ATTENDANCE_LOG_HEADER, quoting=csv.QUOTE_ALL).writerow(row)
        writeFile.close()
        
        print(row["FIRST_NAME"], row["LAST_NAME"], row["IN_OR_OUT"])


while True:
    arduinoResponse = ser.read_until("\n").decode("utf-8")

    if arduinoResponse:
        arduinoResponse = int(''.join([chr(int(i, 16)) for i in arduinoResponse.replace("0x", "").rstrip().split(" ")]).replace('\x00', ''))
        log_user(arduinoResponse)
