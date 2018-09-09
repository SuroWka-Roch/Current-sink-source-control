#!/usr/bin/env python3.5
#runn ass sudo
import usb.core
import usb.util
import serial

def test():
  print("bella")
  print("test")
def makeUsbList():
  divice = usb.core.find(find_all=True)
  list= [usb for usb in divice if usb.product]
  return list


lista= makeUsbList()
help(lista[0])
serial.