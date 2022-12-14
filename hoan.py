from zk import ZK, const
import mysqldatabase
import datetime
import os

conn = None
# create ZK instance
zk = ZK(os.getenv('ATTENDANCE_HOST'), port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

try:
   # connect to device
   conn = zk.connect()
   # disable device, this method ensures no activity on the device while the process is run
   # live capture! (timeout at 10s)
   for attendance in conn.live_capture():
       if attendance is None:
           # implement here timeout logic
           pass
       else:
           print (vars(attendance)) # Attendance object
           sql = "INSERT INTO fingerprint_attendance1s (fingerprint_attendance_id, date_time, created_at, updated_at) VALUES (%s, %s, %s, %s)"
           val = (attendance.user_id, attendance.timestamp.strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
           mysqldatabase.insert(sql, val)
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()

