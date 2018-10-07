#!/usr/bin/env python3.5
from serialInfo import serial_ports
from tkinter import *
from tkinter import ttk
import serial
import time

#Constants
HANSHAKE_CONFIRM_REQUEST_CODE = b'4'
HANSHAKE_CONFIRMATION_CODE = b'2'


def HandShake(Portname, state):
  try:

    with serial.Serial(Portname, 9600, timeout=3) as ser:
      time.sleep(3)
      print(ser.write(HANSHAKE_CONFIRM_REQUEST_CODE))
      ser.flush()
      received = ser.read(1)
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

  elif string == "none found":
    state.set("Try clicing reset")

  else:
    #connect to device and confirm functionality
    if HandShake(string, state):
      state.set('Device is conected and the code is loaded.')
    else:
      state.set("Arduino sided conection problem")


if __name__ == '__main__':
  pass
