#!/usr/bin/env python3
from serialInfo import serial_ports
from tkinter import *
from tkinter import ttk
import serial
import time
import random

#Constants
HANSHAKE_CONFIRM_REQUEST_CODE = b'4'
HANSHAKE_CONFIRMATION_CODE = b'2'
COMAND_VOLTAGE_CHANGE = b'v'
VOLTAGE_CHANGE_DONE = b'd'
#wartość rezystorów w układzie pomniejszona o 1E3 każda z wartości jest krotką pierwsza wartość to rezystancja druga to
#wartość bool mówiąca czy to układ sink=0 czy source=1
REZISTOR_VALUES = ((83.333,1),(13.888,1),(62.5,1),(8.333,0),(62.5,0),(41.666,1),(50,1),(41.666,0))
Vcc_VALUE = 3.3
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


def Calculate12ByteVoltValue(current, portNumber):
  """Calculate int reprezentation of Volt value for defined current value
    returns:
      Value as string
    rises:
      Value error if string is too long or out of 12 bit range
  """
  current = float(current)
  print(current)
  value = 0
  if REZISTOR_VALUES[portNumber][1] == 0: #odnalezienie portów sink
    value = current * REZISTOR_VALUES[portNumber][0] *1E3 # wzor plus przeliczenie z koloohmow do omow
    value = value/1E6 #z mikro do amperow
    value = value/3.0*4095 #mapowanie do 12 bitow
  else:
    value = Vcc_VALUE - current/1E6 * REZISTOR_VALUES[portNumber][0] * 1E3
    value = value/3.0*4095
  if value > 4095 or value < 0:
    raise ValueError('Mapping error value out of range for 12 bit  port name ' + str(portNumber) +" value "+ str(value))
  value = str(int(round(value, 0)))
  if len(value) > 4:
    raise ValueError('Volt value is out of range in port ' + str(portNumber) +"value " + str(value))
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