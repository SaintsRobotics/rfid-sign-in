from time import sleep
from flask import Flask, render_template, request
from datetime import datetime, timedelta
import os
import csv

# sleep(60) # So that when script is run on startup, it will have the pi systems fully enabled

TIMESTAMP_FORMAT = "%m/%d/%Y %H:%M:%S"

STUDENTS_HEADER = ["FIRST_NAME", "LAST_NAME", "STUDENT_ID", "RFID_TAG_NUMBER"]

ATTENDANCE_LOG_FILEPATH = '/home/admin/rfid-sign-in/attendance/attendance-' + str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + \
    '.csv'  # this is the CSV file that the sign ins and outs are logged
ATTENDANCE_LOG_HEADER = ["TIMESTAMP", "IN_OR_OUT"] + STUDENTS_HEADER

def log_user(first_name: str, last_name: str, student_id: int):
    """
    Logs the user sign in/out in the CSV file.
    uid: the number that the user's rfid tag was assigned.  we started at 1, and just counted up from there
    """

    row = {}  # the data that gets written to the csv

    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    row["TIMESTAMP"] = timestamp

    student_info = {"FIRST_NAME": first_name, "LAST_NAME": last_name, "STUDENT_ID": student_id}

    row["RFID_TAG_NUMBER"] = 8000

    if student_info:  # only writes to the attendance log if the data exists
        row.update(student_info)

        #### MAKING SURE THE CSV FILE EXISTS and creating it if it doesn't ####
        ATTENDANCE_LOG_FILEPATH = '/home/admin/rfid-sign-in/attendance/attendance-' + str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + '.csv'
        print(ATTENDANCE_LOG_FILEPATH)
        if not os.path.exists(ATTENDANCE_LOG_FILEPATH):
            print(os.path.exists(ATTENDANCE_LOG_FILEPATH))
            with open(ATTENDANCE_LOG_FILEPATH, 'w') as file:
                csv.DictWriter(file, fieldnames=ATTENDANCE_LOG_HEADER, quoting=csv.QUOTE_ALL).writeheader()
            file.close()

        row["IN_OR_OUT"] = "SIGN_IN"
        with open(ATTENDANCE_LOG_FILEPATH, "r") as readFile:

            for line in csv.DictReader(readFile): # looks to see whether user is signing in or out
                # print(line["STUDENT_ID"], row["STUDENT_ID"])
                if int(line["STUDENT_ID"]) == int(row["STUDENT_ID"]) and line["IN_OR_OUT"] == "SIGN_IN":
                    row["IN_OR_OUT"] = "SIGN_OUT"
                elif int(line["STUDENT_ID"]) == int(row["STUDENT_ID"]):
                    row["IN_OR_OUT"] = "SIGN_IN"
        readFile.close()

        with open(ATTENDANCE_LOG_FILEPATH, "a+") as writeFile:
            csv.DictWriter(writeFile, fieldnames=ATTENDANCE_LOG_HEADER, quoting=csv.QUOTE_ALL).writerow(row)
        writeFile.close()

    print(row["FIRST_NAME"], row["LAST_NAME"], row["IN_OR_OUT"])

app = Flask(__name__)

# Debug setting set to true
app.debug = True

@app.route('/form')
def form():
    return render_template('index.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        log_user(form_data["First Name"], form_data["Last Name"], form_data["Student ID"])
        return render_template('data.html', form_data = form_data)

# Route for handling the login page logic
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'sr1899':
            error = 'Invalid Credentials. Please try again.'
        else:
            ATTENDANCE_LOG_FILEPATH = '/home/admin/rfid-sign-in/attendance/attendance-' + str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + '.csv'
            with open(ATTENDANCE_LOG_FILEPATH) as file:
                return render_template('admin.html', csv = file)
    return render_template('admin.html', error = error)


app.run(host="0.0.0.0", port="8000")