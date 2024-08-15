import time, network
from Maix import GPIO
from fpioa_manager import fm

class wifi():
    nic = None
    def reset(force=False, reply=5, is_hard=True):
        if force == False and __class__.nic != None:
            return True
        try:
            # IO map for ESP32 on Maixduino
            fm.register(25,fm.fpioa.GPIOHS10)#cs
            fm.register(8,fm.fpioa.GPIOHS11)#rst
            fm.register(9,fm.fpioa.GPIOHS12)#rdy

            if is_hard:
                # print("Use Hareware SPI for other maixduino")
                fm.register(28,fm.fpioa.SPI1_D0, force=True)#mosi
                fm.register(26,fm.fpioa.SPI1_D1, force=True)#miso
                fm.register(27,fm.fpioa.SPI1_SCLK, force=True)#sclk
                __class__.nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10, rst=fm.fpioa.GPIOHS11, rdy=fm.fpioa.GPIOHS12, spi=1)
                # print("ESP32_SPI firmware version:", __class__.nic.version())
            else:
                # Running within 3 seconds of power-up can cause an SD load error
                # print("Use Software SPI for other hardware")
                fm.register(28,fm.fpioa.GPIOHS13, force=True)#mosi
                fm.register(26,fm.fpioa.GPIOHS14, force=True)#miso
                fm.register(27,fm.fpioa.GPIOHS15, force=True)#sclk
                __class__.nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10, rst=fm.fpioa.GPIOHS11, rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13, miso=fm.fpioa.GPIOHS14, sclk=fm.fpioa.GPIOHS15)
                # print("ESP32_SPI firmware version:", __class__.nic.version())d

            # time.sleep_ms(500) # wait at ready to connect
        except Exception as e:
            print(e)
            __class__.nic = None
            return False
        return True

    def adc():
        __class__.reset()
        if __class__.nic != None:
            return __class__.nic.adc()
    
    def ping(host):
        __class__.reset()
        if __class__.nic != None:
            return __class__.nic.ping(host)

    def scan():
        __class__.reset()
        if __class__.nic != None:
            return __class__.nic.scan()

    def connect(ssid="wifi_name", pasw="pass_word"):
        __class__.reset()
        if __class__.nic != None:
            return __class__.nic.connect(ssid, pasw)

    def disconnect():
        __class__.reset()
        if __class__.nic != None:
            return __class__.nic.disconnect()

    def ifconfig(): # should check ip != 0.0.0.0
        __class__.reset()
        if __class__.nic != None:
            return __class__.nic.ifconfig()

    def isconnected():
        __class__.reset()
        if __class__.nic != None:
            return __class__.nic.isconnected()
        return False
    

