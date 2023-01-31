import datetime
import schedule
import time
import _thread

conn = 1

def send_users(conn):
    print('send_users'.format(conn))

def send_attendances(conn):
    print('send_attendances'.format(conn))

def job1(conn):
    print('start new thread')
    schedule.every(1).minutes.do(send_users, conn)
    schedule.every(1).minutes.do(send_attendances, conn)
    while True:
        if datetime.datetime.now().strftime("%M:%S") == '12:00':
            print('time at'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(1)
job1(conn)
while True:
    if datetime.datetime.now().strftime("%S") == '00':
        print('time at'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)
    else:
        pass