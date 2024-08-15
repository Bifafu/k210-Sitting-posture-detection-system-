from network_esp32 import wifi
from fpioa_manager import fm
from umqtt import MQTTClient
from board import board_info
from machine import UART
import KPU as kpu
import network
import ntptime
import sensor
import image
import time
import lcd


def camera_init():
  sensor.reset()
  sensor.set_pixformat(sensor.RGB565)
  sensor.set_framesize(sensor.QVGA)
  sensor.skip_frames(10)
  sensor.run(1)

fm.register(board_info.PIN8, fm.fpioa.UART1_TX, force=True)
fm.register(board_info.PIN9, fm.fpioa.UART1_RX, force=True)


wifi.connect("54088", "11111111")
while not (wifi.isconnected()):
  pass
print("wifi ok")
ntptime.settime(8, "time.windows.com")
mqtt = MQTTClient("ievc3zWuCQk.Maixduino|securemode=2,signmethod=hmacsha256,timestamp=1680878297888|","iot-06z00fio9gy0kiu.mqtt.iothub.aliyuncs.com",1883,"Maixduino&ievc3zWuCQk","22b83b32b9e6ef831ddfb0561dfcb94da481d62debe5df2caa168db82dc204b1",30)
try:
  mqtt.connect()
  print('MQTT Connected Successful')
except:
  print('MQTT Connection Failed')
print("Mqtt ok")
lcd.init(freq=15000000, color=31230, invert=0)
camera_init()
sensor.set_vflip(1)
sensor.set_windowing((224, 224))
lcd.rotation(1)
calsses = ["正确坐姿","错误坐姿"]
anchor = ( 2.22,3.25,3.28,2.94,1.75,3.25,3.27,4.36,2.5,3.91)
task = kpu.load("/sd/zzmx.kmodel")
kpu.init_yolo2(task,0.5,0.3,5,anchor)
uart1 = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)
lcd.draw_string(170, 175, str("5"), 0, 65535)
ZhengQueZuoZi = 0
CuoWuZuoZi = 0
time.sleep(2)
while True:
  image = sensor.snapshot()
  lcd.display(image)
  code = kpu.run_yolo2(task,image)
  lcd.draw_string(143, 175, str(code), 0, 65535)
  if bool(code):
    for i in code:
      image = image.draw_rectangle(i.rect(),(0,0,255),2,0)
      lcd.display(image)
      zhonglei = (calsses[i.classid()])
      lcd.draw_string(i.x(), i.y(), str(zhonglei), 248, 65535)
      print(zhonglei)
      if (zhonglei == "错误坐姿"):
        if ((time.localtime()[3] == 8) and ((time.localtime()[4] == 53) and (time.localtime()[5] == 0))):
          CuoWuZuoZi = (CuoWuZuoZi + 1)
          print(CuoWuZuoZi)
          mqtt.publish(str("/sys/ievc3zWuCQk/Maixduino/thing/event/property/post"), str((str((str("{\"id\":12345,\"params\":{\"301false1\":") + str(CuoWuZuoZi))) + str("},\"method\":\"thing.event.property.post\"}"))).encode('utf-8'))
          time.sleep(3)
          print("hi")
        if ((time.localtime()[3] == 9) and ((time.localtime()[4] == 53) and (time.localtime()[5] == 0))):
          CuoWuZuoZi = (CuoWuZuoZi + 1)
          print(CuoWuZuoZi)
          mqtt.publish(str("/sys/ievc3zWuCQk/Maixduino/thing/event/property/post"), str((str((str("{\"id\":12345,\"params\":{\"301false2\":") + str(CuoWuZuoZi))) + str("},\"method\":\"thing.event.property.post\"}"))).encode('utf-8'))
          time.sleep(3)
          print("hi")
if ((time.localtime()[3] == 10) and ((time.localtime()[4] == 53) and (time.localtime()[5] == 0))):
          CuoWuZuoZi = (CuoWuZuoZi + 1)
          print(CuoWuZuoZi)
          mqtt.publish(str("/sys/ievc3zWuCQk/Maixduino/thing/event/property/post"), str((str((str("{\"id\":12345,\"params\":{\"301false3\":") + str(CuoWuZuoZi))) + str("},\"method\":\"thing.event.property.post\"}"))).encode('utf-8'))
          time.sleep((zhonglei == "错误坐姿"))
          print("hi")
        if ((time.localtime()[3] == 11) and ((time.localtime()[4] == 53) and (time.localtime()[5] == 0))):
          CuoWuZuoZi = (CuoWuZuoZi + 1)
          print(CuoWuZuoZi)
          mqtt.publish(str("/sys/ievc3zWuCQk/Maixduino/thing/event/property/post"), str((str((str("{\"id\":12345,\"params\":{\"301false4\":") + str(CuoWuZuoZi))) + str("},\"method\":\"thing.event.property.post\"}"))).encode('utf-8'))
          time.sleep(3)
          print("hi")
        if ((time.localtime()[3] == 14) and ((time.localtime()[4] == 53) and (time.localtime()[5] == 0))):
          CuoWuZuoZi = (CuoWuZuoZi + 1)
          print(CuoWuZuoZi)
          mqtt.publish(str("/sys/ievc3zWuCQk/Maixduino/thing/event/property/post"), str((str((str("{\"id\":12345,\"params\":{\"301false5\":") + str(CuoWuZuoZi))) + str("},\"method\":\"thing.event.property.post\"}"))).encode('utf-8'))
          time.sleep(3)
          print("hi")
        if ((time.localtime()[3] == 15) and ((time.localtime()[4] == 53) and (time.localtime()[5] == 0))):
          CuoWuZuoZi = (CuoWuZuoZi + 1)
          print(CuoWuZuoZi)
          mqtt.publish(str("/sys/ievc3zWuCQk/Maixduino/thing/event/property/post"), str((str((str("{\"id\":12345,\"params\":{\"301false6\":") + str(CuoWuZuoZi))) + str("},\"method\":\"thing.event.property.post\"}"))).encode('utf-8'))
          time.sleep(3)
          print("hi")
if ((time.localtime()[3] == 16) and ((time.localtime()[4] == 53) and (time.localtime()[5] == 0))):
          CuoWuZuoZi = (CuoWuZuoZi + 1)
          print(CuoWuZuoZi)
          mqtt.publish(str("/sys/ievc3zWuCQk/Maixduino/thing/event/property/post"), str((str((str("{\"id\":12345,\"params\":{\"301false7\":") + str(CuoWuZuoZi))) + str("},\"method\":\"thing.event.property.post\"}"))).encode('utf-8'))
          time.sleep(3)
          print("hi")
        if ((time.localtime()[3] == 17) and ((time.localtime()[4] == 53) and (time.localtime()[5] == 0))):
          CuoWuZuoZi = (CuoWuZuoZi + 1)
          print(CuoWuZuoZi)
          mqtt.publish(str("/sys/ievc3zWuCQk/Maixduino/thing/event/property/post"), str((str((str("{\"id\":12345,\"params\":{\"301false8\":") + str(CuoWuZuoZi))) + str("},\"method\":\"thing.event.property.post\"}"))).encode('utf-8'))
          time.sleep(3)
          print("hi")