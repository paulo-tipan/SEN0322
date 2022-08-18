import time
from SEN0322 import *

OXYGEN_CONECTRATION = 20.9        # The current concentration of oxygen in the air.
OXYGEN_MV           = 0           # The value marked on the sensor, Do not use must be assigned to 0.

def setup():
  '''
    The default address for iic is ADDRESS_3
    ADDRESS_0                 = 0x70
    ADDRESS_1                 = 0x71
    ADDRESS_2                 = 0x72
    ADDRESS_3                 = 0x73 
  '''
  oxygen = SEN0322(ADDRESS_3)
  oxygen.calibrate(OXYGEN_CONECTRATION ,OXYGEN_MV)
  print("oxygen calibrate success")
  time.sleep(1)

if __name__ == "__main__":
  setup()