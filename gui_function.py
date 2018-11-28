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
#wartość rezystorów w układzie pomniejszona o 1E3
REZISTOR_VALUES = (83.333,13.888,62.5,8.333,62.5,41.666,50,41.666)

def HandShake(Portname):
  """"Sends one Bite code to arduino and returns True if confirmation is resived
  returns false on any another occasion"""
  try:
    #open port and make sure my program is running on the Arduino
    with serial.Serial(Portname, 9600, timeout=3) as ser:
      time.sleep(2)
      ser.write(HANSHAKE_CONFIRM_REQUEST_CODE)
      ser.flush()

      #handle no information relived problem
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
    return False


def ConnectButtonFunction(string,state,usbList):
  """funktion that handles bonnect buttom outcome depends on the combobox value selected"""
  if string == "reset":
    #restarting the list of combobox
    resetListTemp=serial_ports()
    if not resetListTemp:
       resetListTemp.append('brak')
    resetListTemp.append('reset')
    usbList['values'] = tuple(resetListTemp)
    usbList.set(usbList['values'][0])
    state.set("Wybierz port")

  elif string == "brak":
    state.set("Wybierz reset")

  else:
    #Connect to device and confirm functionality
    if HandShake(string):
      state.set('Kontroler jest podłączony i sprawny')
    else:
      state.set("Problem po stronie Arduino")


def Calculate12ByteVoltValue(courent,portNumber):
  """Calculate int reprezentation of Volt value for defined courent value
    returns:
      Value as string
    rises:
      Value error if string is too long
  """
  courent = float(courent)
  value = courent * REZISTOR_VALUES[portNumber] * 1000 * 2
  assert value < 4096 and value > 0, "Calculation error or range extended"
  value = str(round(value, 0))
  if len(value) > 4:
    raise ValueError('Volt value is out of range in port ' + portNumber)
  return value


def SendButtonFunction(VoltTable,port):
  """Connects to arduino and sends formated information."""
  try:
    with serial.Serial(port, 9600, timeout=3) as ser:
      informationString = ''
      for i in range(8):
        tempStr = VoltTable[i].get()
        if tempStr == '~':
          continue
        informationString += chr(i+97)
        tempStr = Calculate12ByteVoltValue(tempStr, i)
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
      resived = ser.read()
      if resived == VOLTAGE_CHANGE_DONE:
        print('done')
      else:
          print(resived)
          raise Exception("Voltage change not confirmed")
  except Exception as e:
    print(str(e))
if __name__ == '__main__':
  pass
