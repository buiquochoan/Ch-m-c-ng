from zk import ZK, const
import mysqldatabase
import datetime
import os
import requests
import schedule
import time

conn = None
# create ZK instance
zk = ZK(os.getenv('ATTENDANCE_HOST'), port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
HEAD_OFFICE = 0

def makeDataAttendance(attendance):
    return {'office': HEAD_OFFICE, 'fingerprint_machine_id': attendance.user_id, 'datetime_string': attendance.timestamp.strftime("%Y-%m-%d %H:%M:%S")}

def send_users(conn):
    url = format(os.getenv('APP_API'))+'/okr/store-multiple-users'
    results = []
    a_users = conn.get_users()
    for user in a_users:
        results.append({'office': HEAD_OFFICE, 'fingerprint_machine_id': user.uid, 'name': user.name})
    x = requests.post(url, json = results)

def send_attendances(conn, date_str = None):
    url = format(os.getenv('APP_API'))+'/okr/store-multiple-attendance'
    results = []
    date_check = date_str
    if date_str is None:
        date_check = datetime.datetime.now().strftime("%Y-%m-%d")
    attendances = conn.get_attendance()
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for attendance in attendances:
        #if attendance.timestamp.strftime("%Y-%m-%d") == date_check:
        results.append(makeDataAttendance(attendance))
    x = requests.post(url, json = results)

def send_realtime_attendance(attendance):
    url = format(os.getenv('APP_API'))+'/okr/store-attendance'
    myobj = makeDataAttendance(attendance)
    x = requests.post(url, json = myobj)

try:
    # connect to device
    conn = zk.connect()
    #live capture! (timeout at 10s)
    for attendance in conn.live_capture():
        if attendance is None:
           # implement here timeout logic
           pass
        else:
           send_realtime_attendance(attendance)
    schedule.every().day.at("12:00").do(send_users(conn))
    schedule.every().day.at("18:00").do(send_users(conn))
    schedule.every().day.at("23:30").do(send_attendances(conn))
    while True:
        schedule.run_pending()
        time.sleep(1)
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()

