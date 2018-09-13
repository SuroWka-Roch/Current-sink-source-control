#!/usr/bin/env python3.5
#sprawdz odnajdywanie usb maszynek i wsadz je do tego wejścia
from tkinter import *
from tkinter import ttk
from serialInfo import serial_ports
import gui_function
#import USB
#USB.test()



# Base window creation.

root = Tk()
root.title("Inżynierka")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set frame to add widgets to.

mainframe = ttk.Frame(root, padding="6 6 6 6")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

# Handle streathing
for i in range(8):
  mainframe.rowconfigure(i, weight=1)
for i in range(6):
  mainframe.columnconfigure(i,weight=1)

# Window valuables.
state = StringVar()
state.set("Do i wonna know if..")
portValues = [StringVar for _ in range(8)]

# Constants
padingx = 5

# Legend line.

ttk.Label(mainframe, text="Long and confusing what this is and what this is not \nexplanation").grid(column=0, row=0, columnspan=6, sticky=(N, W, E, S), pady=5, padx=3)
ttk.Label(mainframe, text="Port name").grid(column=0, row=1, sticky=W, padx=padingx)
ttk.Label(mainframe, text="Value").grid(column=1, row=1, sticky=( W, E), padx=padingx)
ttk.Label(mainframe, text="Unit").grid(column=2, row=1, sticky=E, padx=padingx)
ttk.Label(mainframe, text="Port name").grid(column=3, row=1, sticky=W, padx=padingx)
ttk.Label(mainframe, text="Value").grid(column=4, row=1, sticky=( W, E), padx=padingx)
ttk.Label(mainframe, text="Unit").grid(column=5, row=1, sticky=E, padx=padingx)

# Port name line

ttk.Label(mainframe, text="1").grid(column=0, row=2, sticky=W, padx=padingx)
ttk.Label(mainframe, text="2").grid(column=0, row=3, sticky=W, padx=padingx)
ttk.Label(mainframe, text="3").grid(column=0, row=4, sticky=W, padx=padingx)
ttk.Label(mainframe, text="4").grid(column=3, row=2, sticky=W, padx=padingx)
ttk.Label(mainframe, text="5").grid(column=3, row=3, sticky=W, padx=padingx)
ttk.Label(mainframe, text="6").grid(column=3, row=4, sticky=W, padx=padingx)
ttk.Label(mainframe, text="7").grid(column=0, row=5, sticky=W, padx=padingx)
ttk.Label(mainframe, text="8").grid(column=3, row=5, sticky=W, padx=padingx)

# imput line.
entryList = []
for i in range(8):
  entryList.append(Entry(mainframe, width=10, textvariable=portValues[i]))
  entryList[i].grid(column=1 if i < 4 else 4, row=i+2 if i < 4 else i-2)

# Unit line.
ttk.Label(mainframe, text="µA").grid(column=2, row=2, sticky=E, padx=padingx)
ttk.Label(mainframe, text="µA").grid(column=2, row=3, sticky=E, padx=padingx)
ttk.Label(mainframe, text="µA").grid(column=2, row=4, sticky=E, padx=padingx)
ttk.Label(mainframe, text="µA").grid(column=2, row=5, sticky=E, padx=padingx)

ttk.Label(mainframe, text="µA").grid(column=5, row=2, sticky=E, padx=padingx)
ttk.Label(mainframe, text="µA").grid(column=5, row=3, sticky=E, padx=padingx)
ttk.Label(mainframe, text="µA").grid(column=5, row=4, sticky=E, padx=padingx)
ttk.Label(mainframe, text="µA").grid(column=5, row=5, sticky=E, padx=padingx)

# status and conection
usbList = serial_ports()
if not usbList:
  usbList=['none found']
usbList.append("reset")

ttk.Label(mainframe, textvariable=state).grid(column=0, row=6, columnspan=2)
ttk.Label(mainframe, text='port').grid(column=2, row=6,sticky=E)
usbPortUsersChose = StringVar()
comboBox = ttk.Combobox(mainframe, textvariable=usbPortUsersChose,values=usbList)
comboBox.grid(column=3, row=6, columnspan=2)
comboBox.set(usbList[0])
ttk.Button(mainframe, text='connect', command=lambda: gui_function.ConnectButtonFunction(usbPortUsersChose.get(),state,comboBox)).grid(column=5, row=6)

#send buttom

ttk.Button(mainframe, text='send').grid(column=4, row=7, columnspan=2, sticky= (W,E))

root.mainloop()
