#!/usr/bin/env python3

#Program Inżynierki Wojciecha Surówki.

from mine import createGuiWindow
try:
  with open('defValues.txt','r') as file:
    defaultTable = [ val.strip('\n') for val in file ]
    if len(defaultTable) > 8:
      defaultTable = defaultTable[0:8]
except Exception:
  defaultTable = [int(4000/7 * i) for i in range(8)]
createGuiWindow(defaultTable)
