#!/usr/bin/env python3.5
#runn ass sudo
import usb.core
import usb.util
print(usb.core.show_devices())
divice= usb.core.find(find_all=True)
for I in divice:
  print(I.product + "  ", end="")
  try:
    print(I.manufacturer)
  except Exception:
    pass
def test():
  print("bella")