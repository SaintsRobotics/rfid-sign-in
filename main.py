import serial
from datetime import datetime, timedelta
import os
import csv

TIMESTAMP_FORMAT = "%Y/%m/%d %H:%M:%S"

STUDENTS_FILEPATH = 'students.csv'  # this is the CSV file where student names and IDs are stored.  Do not write to this file
STUDENTS_HEADER = ["FIRST_NAME", "LAST_NAME", "STUDENT_ID", "RFID_TAG_NUMBER"]

ATTENDANCE_LOG_FILEPATH = 'attendance.csv'  # this is the CSV file that the sign ins and outs are logged
ATTENDANCE_LOG_HEADER = ["TIMESTAMP"] + STUDENTS_HEADER

######## CONNECTING TO SERIAL BUS ########
"""Comment out the appropriate lines below depending on which operating system this is running on."""
ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)
# ser = serial.Serial("COM8", baudrate=115200, timeout=1)

print("CONNECTED")
# TODO add more checks in the arduino code and here to make sure there aren't any hardware issues.
# This includes adding a handshake on startup.

#### MAKING SURE THE CSV FILE EXISTS and creating it if it doesn't ####
if not os.path.exists(ATTENDANCE_LOG_FILEPATH):
    with open(ATTENDANCE_LOG_FILEPATH, 'w') as file:
        csv.DictWriter(file, fieldnames=ATTENDANCE_LOG_FILEPATH, quoting=csv.QUOTE_NONNUMERIC).writeheader()
        file.close()


def get_student_info(rfidTagNumber):
    """Looks up the user's first and last name and student ID number in the database.
    Returns a dictionary of the student's """
    with open(STUDENTS_FILEPATH, 'r') as file:
        for row in csv.DictReader(STUDENTS_FILEPATH):
            # print(type(row), row)
            if row["RFID_TAG_NUMBER"] == rfidTagNumber:
                return row
        file.close()
    return {}


def log_user(rfidTagNumber):
    """
    Loggs the user sign in/out in the CSV file.
    uid: the number that the user's rfid tag was assigned.  we started at 1, and just counted up from there
    """

    row = {}  # the data that gets written to the csv

    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    row["TIMESTAMP"] = timestamp

    row["RFID_TAG_NUMBER"] = rfidTagNumber

    studentInfo = get_student_info(rfidTagNumber)

    row["FIRST_NAME"] = studentInfo["FIRST_NAME"]
    row["LAST_NAME"] = studentInfo["LAST_NAME"]
    row["STUDENT_ID"] = studentInfo["STUDENT_ID"]

    with open(ATTENDANCE_LOG_FILEPATH, "a+") as file:
        csv.DictWriter(file, fieldnames=ATTENDANCE_LOG_HEADER, quoting=csv.QUOTE_NONNUMERIC).writerow(row)


while True:
    arduinoResponse = ser.read_until("\n").decode("utf-8")

    if arduinoResponse:
        arduinoResponse = arduinoResponse.replace("0x", "").replace(" ", "").rstrip()

        log_user(int(arduinoResponse, 16))
