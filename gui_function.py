#!/usr/bin/env python3.5
from serialInfo import serial_ports
from tkinter import *
from tkinter import ttk
import serial
import time

#Constants
HANSHAKE_CONFIRM_REQUEST_CODE = b'4'
HANSHAKE_CONFIRMATION_CODE = b'2'
COMAND_VOLTAGE_CHANGE = b'v'
VOLTAGE_CHANGE_DONE = b'd'


def HandShake(Portname, state):
  try:
    #open port and make shure my program is running on the arduino
    with serial.Serial(Portname, 9600, timeout=3) as ser:
      time.sleep(2)
      ser.write(HANSHAKE_CONFIRM_REQUEST_CODE)
      ser.flush()

      #handle no information resived problem
      received = ser.read(1)
      counter = 0
      while received == b'':
        received = ser.read(1)
        time.sleep(0.1)
        counter = counter+1
        if counter == 20:
          break

      if received == HANSHAKE_CONFIRMATION_CODE:
        return True
      else:
        print(str(received))
        return False
  except Exception as e:
    print(str(e))
    state.set(str(e))
    return False


def ConnectButtonFunction(string,state,usbList):
  """funktion that handles bonnect buttom outcome depends on the combobox value selected"""
  if string == "reset":
    #restarting the list of combobox
    resetListTemp=serial_ports()
    if not resetListTemp:
       resetListTemp.append('none found')
    resetListTemp.append('reset')
    usbList['values'] = tuple(resetListTemp)
    usbList.set(usbList['values'][0])
    state.set("Wybierz port")

  elif string == "none found":
    state.set("Try clicing reset")

  else:
    #connect to device and confirm functionality
    if HandShake(string, state):
      state.set('Device is conected and the code is loaded.')
    else:
      state.set("Arduino sided conection problem")

def SendButtonFunction(VoltTable,port):
  try:
    with serial.Serial(port, 9600, timeout=3) as ser:
      informationString = ''
      for i in range(8):
        informationString += chr(i+97)
        tempStr = VoltTable[i].get()
        if len(tempStr) > 4:
          raise ValueError('Volt value is out of range')
        for i in range(4-len(VoltTable[i].get())):
          tempStr = '0'+ tempStr
        informationString += tempStr
      print(informationString)
      if len(informationString)>40:
        raise ValueError('The string is to long')
      informationString += '\0'
      time.sleep(2)
      ser.write(COMAND_VOLTAGE_CHANGE)
      ser.flush()
      time.sleep(0.5)
      ser.write(informationString.encode('utf-8'))
      ser.flush()
      while ser.inWaiting() == 0:
        time.sleep(0.5)
      if ser.read()==VOLTAGE_CHANGE_DONE:
        print('done')
  except Exception as e:
    print(str(e))
if __name__ == '__main__':
  pass
