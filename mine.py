#!/usr/bin/env python3
#contakt usb z kompem
from tkinter import *
from tkinter import ttk
from serialInfo import serial_ports
import gui_function
def createGuiWindow(defaultTable):
  """make the gui"""

  # Base window creation.

  root = Tk()
  root.title("Program kontroli prądów polaryzacyjnych")
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
  Po wypełnieniu okienek wartości prądów użyj klawisza "Wyślij" żeby załadować wartości natężeń do układu
  Użyj symbolu "~" żeby nie zmieniać aktualnej wartości natężenia\n'''

  ttk.Label(mainframe, text=explanationString).grid(column=0, row=0, columnspan=6, sticky=(N, W, E, S), pady=5, padx=3)
  ttk.Label(mainframe, text="Nazwa portu").grid(column=0, row=1, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="Wartość").grid(column=1, row=1, sticky=( W, E), padx=padingx)
  ttk.Label(mainframe, text="Jednostka").grid(column=2, row=1, sticky=E, padx=padingx)
  ttk.Label(mainframe, text="Nazwa portu").grid(column=3, row=1, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="Wartość").grid(column=4, row=1, sticky=( W, E), padx=padingx)
  ttk.Label(mainframe, text="Jednostka").grid(column=5, row=1, sticky=E, padx=padingx)

  # Port name line

  ttk.Label(mainframe, text="RESx25").grid(column=0, row=2, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="CAS").grid(column=0, row=3, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="COMP").grid(column=0, row=4, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="B").grid(column=0, row=5, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="STD").grid(column=3, row=2, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="SH").grid(column=3, row=3, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="PDH").grid(column=3, row=4, sticky=W, padx=padingx)
  ttk.Label(mainframe, text="AMP").grid(column=3, row=5, sticky=W, padx=padingx)

  entryList = []
  for i in range(8):
    entryList.append(Entry(mainframe, width=10, textvariable=portValues[i]))
    entryList[i].grid(column=1 if i < 4 else 4, row=i+2 if i < 4 else i-2,sticky=W)
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
    usbList=['brak']
    state.set("Sprawdz połączenie Arduino")
  usbList.append("reset")

  ttk.Label(mainframe, textvariable=state).grid(column=0, row=6, columnspan=2)
  ttk.Label(mainframe, text='port').grid(column=2, row=6,sticky=E)
  usbPortUsersChose = StringVar()
  comboBox = ttk.Combobox(mainframe, textvariable=usbPortUsersChose,values=usbList)
  comboBox.grid(column=3, row=6, columnspan=2)
  comboBox.set(usbList[0])
  ttk.Button(mainframe, text='Połącz', command=lambda: gui_function.ConnectButtonFunction(usbPortUsersChose.get(),state,comboBox)).grid(column=5, row=6,sticky = E)

  #send buttom

  ttk.Button(mainframe, text='Wyślij', command=lambda: gui_function.SendButtonFunction(portValues,usbPortUsersChose.get(),state)).grid(column=4, row=7, columnspan=2, sticky= (W,E))
  root.mainloop()
if __name__ == '__main__':
  import main

