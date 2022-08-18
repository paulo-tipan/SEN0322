from machine import I2C, Pin
from time import sleep_us

##Sensor I2C Address, default: 0x73
  
ADDR_0      = 0x70
ADDR_1      = 0x71
ADDR_2      = 0x72
ADDR_3      = 0x73


##Sensor Data registers
#Resgister for o2 data
OXYGEN_DATA_REGISTER    = 0x03
#Register for user to configure key value manually
USER_SET_REGISTER       = 0x08
#Register for auto configuring key value
AUTUAL_SET_REGISTER     = 0x09
#register for key value
GET_KEY_REGISTER        = 0x0A

class SEN0322:
    """
    i2c_port: (scl_pin=GPIO22,sda_pin=GPIO21)
    """
    __key               = 0.0
    __count             = 0
    __txbuf             = [0]
    __oxygendata        = [0]*101

    ##
    def __init__(self,sensor_addr):
        self.i2c=I2C(0,scl=Pin(22),sda=Pin(21))
        self.addr=sensor_addr
        
    def calibrate(self,vol,mv):
        '''!
        @brief Calibrate sensor
        @param vol Oxygen concentration unit vol
        @param mv Calibrated voltage unit mv
        @return None
        '''
        self.__txbuf[0]=int(vol*10)
        if mv<1e-6 and mv>-1e-6:
            self.i2c.writeto_mem(self.addr,USER_SET_REGISTER,bytearray(self.__txbuf))
        else:
            self.__txbuf[0]=int((vol/mv)*1000)
            self.i2c.writeto_mem(self.addr,AUTUAL_SET_REGISTER,bytearray(self.__txbuf))

    def get_key(self):
        data=self.i2c.readfrom_mem(self.addr,GET_KEY_REGISTER,1)
        if data==0:
            self.__key=(20.9/120.0)
        else:
            self.__key=(float(data[0])/1000.0)
        sleep_us(int(1e5))    

    def get_oxygen_data(self,samples):
        '''!
        @brief Get oxygen concentration
        @param collectNum The number of data to be smoothed
        @n     For example, upload 20 and take the average value of the 20 data, then return the concentration data
        @return Oxygen concentration, unit vol
        '''
        self.get_key()
        if samples>0:
            for sample in range(samples,1,-1):
                self.__oxygendata[sample-1]=self.__oxygendata[sample-2]
            data=self.i2c.readfrom_mem(self.addr,OXYGEN_DATA_REGISTER,3)
            self.__oxygendata[0]=self.__key*(float(data[0]) + float(data[1])/10.0 + float(data[2])/100.0)
            if self.__count<samples:
                self.__count+=1
            return self.get_avg_data(self.__oxygendata,self.__count)
        elif (samples>100) or (samples<=0):
            return -1

    def get_avg_data(self,sample_data,samples):
        temp=0.0
        for sample in range(samples):
            temp+=sample_data[sample]
        return (temp/float(samples))


