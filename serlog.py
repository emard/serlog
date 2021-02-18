#!/usr/bin/env python3

# Serial Logger

import serial, time, datetime

ser = serial.Serial()
ser.baudrate = 115200
ser.timeout = 10
ser.port = '/dev/ttyUSB0'
#ser.rtscts = False
#ser.dsrdtr = False
#ser.open()

def reopen_serial():
  global ser
  ser.close()
  ser.open()

def datenow():
  return str(datetime.datetime.today()).split()[0] # yyyy-mm-dd every day
  #return str(datetime.datetime.today()).split()[1][0:5] # hh:mm every minute

def filenow():
  return "/tmp/wt-"+datenow()+".log"

def open_file():
  global current_filename, current_file
  if current_file:
    return
  current_file = open(current_filename, "a+")
  print("new log file", current_filename)

current_filename = filenow()
current_file = False

# update current filename according to current date
# if file is open and date has changed, close file
# create new file name for new date
def rotatelog():
  global current_filename, current_file
  if current_filename != filenow():
    if(current_file):
      current_file.close()
      current_file = False
    current_filename = filenow()

while True:
  r=""
  try:
    r=ser.readline().decode("utf-8").strip()+"\n"
  except:
    print("trying to reopen", ser.port)
    time.sleep(5)
    try:
      reopen_serial()
    except:
      print("can't reopen yet")
  if(len(r)):
    open_file()
    current_file.write(r)
    current_file.flush()
    rotatelog()
    #print(r)
