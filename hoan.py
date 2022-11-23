from zk import ZK, const
import mysql.connector
import datetime

conn = None
# create ZK instance
zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

try:
   # connect to device
   conn = zk.connect()
   # disable device, this method ensures no activity on the device while the process is run
   conn.disable_device()
   # live capture! (timeout at 10s)
   getLiveCapture()
   conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()

def getLiveCapture():
    for attendance in conn.live_capture():
        if attendance is None:
            # implement here timeout logic
            pass
        else:
            insertToDatabase(attendance)

def insertToDatabase(attendance):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="api-edutalk"
    )
    mycursor = mydb.cursor()
    print (vars(attendance)) # Attendance object
    sql = "INSERT INTO fingerprint_attendances (fingerprint_attendance_id, date_time, created_at, updated_at) VALUES (%s, %s, %s, %s)"
    val = (attendance.user_id, attendance.timestamp.strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
