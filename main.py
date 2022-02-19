import serial
import time
import sqlite3
from datetime import datetime

#ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)
ser = serial.Serial("COM8", baudrate=115200, timeout=1)
print("CONNECTED")

"""con = sqlite3.connect('sign_ins.db')
cur = con.cursor()

# first name last name, in/out, ID, 
def sign_in(id):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS signins ([in] BOOL, [date] INT, [id] INT);")
    cur.execute(
        f"INSERT INTO signins (date, id) VALUES(strftime('%s','now'), {id});")

    # if (SELECT * FROM MyTable WHERE date(datetime(DateColumn / 1000 , 'unixepoch')) = date('now'))

    con.commit()
    print("cURRENT")
    for x in cur.execute("select * from signins;"):
        print(x)

"""

def sign_in(uid):
    now = datetime.now() # current date and time
    now = now.strftime("%Y/%m/%d %H:%M:%S")
    #create the file before running
    #open("sign-ins.csv", "w").write("\"timestamp\", \"uid\"\n")
    with open("sign-ins.csv", "a+") as f:
        f.write(f'\"{now}\", {uid}\n')
        print("wrote: " +  f"{now}, {uid}\n")

while True:
    resp = ser.read_until("\n").decode("utf-8")
    if resp:
        resp = resp.replace("0x", "").replace(" ", "").rstrip()
        try:
            print(int(resp, 16))
        except:
            continue
        sign_in(int(resp, 16))
        time.sleep(2)


# data csv
#sign in csv

con.close()
