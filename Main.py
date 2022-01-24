import serial
import time
import sqlite3

ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)
print("CONNECTED")


def sign_in(id):
    pass


con = sqlite3.connect('sign_ins.db')
cur = con.cursor()
cur.execute('''CREATE TABLE signins
               (date tex, trans text, symbol text, qty real, price real)''')

# Insert a row of data
cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()

while True:
    resp = ser.read_until("\n").decode("utf-8")
    if resp:
        resp = resp.replace("0x", "").replace(" ", "").rstrip()
        print(resp)
        sign_in(resp)


for i in range(5):
    time.sleep(1)
    ser.write(s.encode('utf-8'))
