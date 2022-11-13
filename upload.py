# Import smtplib for the actual sending function
import csv
import smtplib

# Import the email modules
from email.mime.text import MIMEText

from datetime import datetime

ATTENDANCE_LOG_FILEPATH = '/home/admin/rfid-sign-in/attendance/attendance-' + str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().year) + \
    '.csv'  # this is the CSV file that the sign ins and outs are logged

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

msg = MIMEMultipart()
body_part = MIMEText("Attached to this email is the attenance for today. \n \n Thanks!", 'plain')
msg['Subject'] = "Attendance for " + str(datetime.date(datetime.now()))
msg['From'] = "attendance@saintsrobotics.com"
msg['To'] = "anay.nagar@saintsrobotics.com"
msg.attach(body_part)

input_file = open(ATTENDANCE_LOG_FILEPATH, "r+")
reader_file = csv.reader(input_file)
file_length = len(list(reader_file))
input_file.close()

if file_length > 1:
    fp = open(ATTENDANCE_LOG_FILEPATH, "rb")
    attachment = MIMEBase("text", "plain")
    attachment.set_payload(fp.read())
    fp.close()
    attachment.add_header("Content-Disposition", "attachment", filename=ATTENDANCE_LOG_FILEPATH)
    msg.attach(attachment)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login("attendance@saintsrobotics.com", "sr1899attendance")
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

    print("Email successully sent to:", msg["To"])
else:
    print("No file found or file has no attendance values")