#!/usr/bin/env python3.5
#contakt usb z kompem
from tkinter import *
from tkinter import ttk
from serialInfo import serial_ports
import gui_function
def createGuiWindow(defaultTable):
  """make the gui"""

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
  state.set("Miejsce informacji")
  portValues = [StringVar() for _ in range(8)]

  # Constants
  padingx = 5

  # Legend line.
  explanationString = '''Program ten jest częścią pracy inżynierskiej Wojciecha Surówki. 
Użycie:
  Na rozsuwanym menu wybierz port do którego jest połączony moduł Arduino.
  Następnie wciśnij "Połącz" w celu sprawdzenia poprawności załadowanego kodu. 
  Po wypełnieniu okienek wartości napięć użyj klawisza "Wyślij" żeby załadować wartości napięcia do układu\n'''

  ttk.Label(mainframe, text=explanationString).grid(column=0, row=0, columnspan=6, sticky=(N, W, E, S), pady=5, padx=3)
  ttk.Label(mainframe, text="Port name").grid(column=0, row=1, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="Value").grid(column=1, row=1, sticky=( W, E), padx=padingx)
  ttk.Label(mainframe, text="Unit").grid(column=2, row=1, sticky=E, padx=padingx)
  ttk.Label(mainframe, text="Port name").grid(column=3, row=1, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="Value").grid(column=4, row=1, sticky=( W, E), padx=padingx)
  ttk.Label(mainframe, text="Unit").grid(column=5, row=1, sticky=E, padx=padingx)

  # Port name line

  ttk.Label(mainframe, text="0").grid(column=0, row=2, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="1").grid(column=0, row=3, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="2").grid(column=0, row=4, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="3").grid(column=0, row=5, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="4").grid(column=3, row=2, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="5").grid(column=3, row=3, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="6").grid(column=3, row=4, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="7").grid(column=3, row=5, sticky=W, padx=padingx)

  entryList = []
  for i in range(8):
    entryList.append(Entry(mainframe, width=10, textvariable=portValues[i]))
    entryList[i].grid(column=1 if i < 4 else 4, row=i+2 if i < 4 else i-2)
    portValues[i].set(defaultTable[i])

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
    usbList=['Nie odnaleziono']
    state.set("Sprawdz połączenie Arduino")
  usbList.append("reset")

  ttk.Label(mainframe, textvariable=state).grid(column=0, row=6, columnspan=2)
  ttk.Label(mainframe, text='port').grid(column=2, row=6,sticky=E)
  usbPortUsersChose = StringVar()
  comboBox = ttk.Combobox(mainframe, textvariable=usbPortUsersChose,values=usbList)
  comboBox.grid(column=3, row=6, columnspan=2)
  comboBox.set(usbList[0])
  ttk.Button(mainframe, text='Połącz', command=lambda: gui_function.ConnectButtonFunction(usbPortUsersChose.get(),state,comboBox)).grid(column=5, row=6)

  #send buttom

  ttk.Button(mainframe, text='Wyślij', command=lambda: gui_function.SendButtonFunction(portValues,usbPortUsersChose.get())).grid(column=4, row=7, columnspan=2, sticky= (W,E))

  root.mainloop()

if __name__ == '__main__':
  import main

