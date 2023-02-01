from zk import ZK, const
import mysqldatabase
import datetime
import os
import requests
import schedule
import time
import _thread

conn = None
# create ZK instance
zk = ZK(os.getenv('ATTENDANCE_HOST'), port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
HEAD_OFFICE = 0

def makeDataAttendance(attendance):
    return {'office': HEAD_OFFICE, 'fingerprint_machine_id': attendance.user_id, 'datetime_string': attendance.timestamp.strftime("%Y-%m-%d %H:%M:%S")}

def send_users(conn):
    print('start send_users')
    url = format(os.getenv('APP_API'))+'/okr/store-multiple-users'
    results = []
    a_users = conn.get_users()
    for user in a_users:
        results.append({'office': HEAD_OFFICE, 'fingerprint_machine_id': user.uid, 'name': user.name})
    x = requests.post(url, json = results)
    print ("send_users : {}".format(x))

def send_attendances(conn, date_str = None):
    print('start send_attendances')
    url = format(os.getenv('APP_API'))+'/okr/store-multiple-attendance'
    results = []
    date_check = date_str
    if date_str is None:
        date_check = datetime.datetime.now().strftime("%Y-%m-%d")
    attendances = conn.get_attendance()
    for attendance in attendances:
        #if attendance.timestamp.strftime("%Y-%m-%d") == date_check:
        results.append(makeDataAttendance(attendance))
    x = requests.post(url, json = results)
    print ("send_attendances : {}".format(x))

def send_realtime_attendance(attendance):
    url = format(os.getenv('APP_API'))+'/okr/store-attendance'
    myobj = makeDataAttendance(attendance)
    x = requests.post(url, json = myobj)

def start_connect(conn):
    send_users(conn)
    send_attendances(conn)

def run_schedule(conn):
    print('run schedule')
    schedule.every().day.at("12:00").do(send_users, conn)
    schedule.every(1).minutes.do(send_users, conn)
    schedule.every().day.at("23:30").do(send_attendances, conn)
    while True:
        schedule.run_pending()
        time.sleep(1)

def send_telegram(body):
    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    r = requests.post("https://api.telegram.org/bot"+format(os.getenv('TELEGRAM_BOT_TOKEN'))+"/sendMessage?text=" + body + "&chat_id="+format(os.getenv('TELEGRAM_GROUP_ID'))+"&parse_mode=Markdown", headers=headers)
    print(body)

def live_capture(conn):
    print('start live_capture')
    for attendance in conn.live_capture():
        if attendance is None:
            # implement here timeout logic
            pass
        else:
            send_realtime_attendance(attendance)

try:
    # connect to device
    conn = zk.connect()
    start_connect(conn)
    live_capture(conn)
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
        body="Server disconnected at: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_telegram(body)