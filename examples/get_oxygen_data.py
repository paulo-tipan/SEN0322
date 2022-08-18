import time
from SEN0322 import *

COLLECT_NUMBER   = 10              # collect number, the collection range is 1-100

'''
  The first  parameter is to select iic0 or iic1
  The second parameter is the iic device address
  The default address for iic is ADDRESS_3
  ADDR_0                 = 0x70
  ADDR_1                 = 0x71
  ADDR_2                 = 0x72
  ADDR_3                 = 0x73
'''
oxygen = SEN0322(ADDR_3)
def loop():
  oxygen_data = oxygen.get_oxygen_data(COLLECT_NUMBER)
  print("oxygen concentration is %4.2f %%vol"%oxygen_data)
  time.sleep(1)

if __name__ == "__main__":
  while True:
    loop()