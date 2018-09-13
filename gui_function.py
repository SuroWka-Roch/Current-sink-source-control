#!/usr/bin/env python3.5
from serialInfo import serial_ports
from tkinter import *
from tkinter import ttk


def ConnectButtonFunction(string,state,usbList):
  if string == "reset":
    resetListTemp=serial_ports()
    if not resetListTemp:
       resetListTemp.append('none found')
    resetListTemp.append('reset')
    usbList['values']=tuple(resetListTemp)
    usbList.set(usbList['values'][0])
  if string == "none found":
    state.set("Try clicing reset")

if __name__ == '__main__':
  pass
