from PTG import ptg
from machine import Timer,PWM
from fpioa_manager import *
from Maix import GPIO
from network_esp32 import wifi



class PIN:
  class Struct:
    def __init__(self,pin,obj,mode,tim,detach):
      self.pin = pin ; self.obj = obj ; self.mode = mode
      self.tim = tim ; self.detach = detach
  def __init__(self):
    self.map = []
    self.GPIO = GPIO
  def dw_attach(self, pin):
    gpio=GPIO(ptg.register(pin)-24, GPIO.OUT)
    self.map.append(self.Struct(pin,gpio,0,None,self.dw_detach))
    return self.map[-1]
  def dr_attach(self, pin):
    gpio=GPIO(ptg.register(pin)-24, GPIO.IN)
    self.map.append(self.Struct(pin,gpio,1,None,self.dr_detach))
    return self.map[-1]
  def aw_attach(self, pin, duty, freq, tim):
    tim = Timer(eval('Timer.TIMER'+str(tim//4)), eval('Timer.CHANNEL'+str(tim%4)), mode=Timer.MODE_PWM)
    pwm = PWM(tim, freq=freq, duty=duty, pin=pin)
    self.map.append(self.Struct(pin,pwm,2,tim,self.aw_detach))
    return self.map[-1]
  def ar_attach(self, pin):
    self.map.append(self.Struct(pin,wifi,3,None,self.ar_detach))
    return self.map[-1]
  def irq_attach(self, pin):
    gpio=GPIO(ptg.register(pin)-24, GPIO.IN, GPIO.PULL_NONE)
    self.map.append(self.Struct(pin,gpio,4,None,self.irq_detach))
    return self.map[-1]
  def dw_detach(self, pin, _map):
    ptg.unregister(pin)
  def dr_detach(self, pin, _map):
    ptg.unregister(pin)
  def aw_detach(self, pin, _map):
    del _map.obj
  def ar_detach(self, pin, _map):
    pass
  def irq_detach(self, pin, _map):
    ptg.unregister(pin)
  def checkMap(self, pin, mode):
    for i, _map in enumerate(self.map):
      if _map.pin == pin:
        if _map.mode == mode:
          return _map
        _map.detach(pin, _map)
        del self.map[i]
        break
    return None
  def digital_write(self, pin, level):
    result = self.checkMap(pin, 0)
    if result:
      return result.obj.value(level)
    result = self.dw_attach(pin)
    result.obj.value(level)
  def digital_read(self, pin):
    result = self.checkMap(pin, 1)
    if result:
      return result.obj.value()
    result = self.dr_attach(pin)
    return result.obj.value()
  def pwm_init(self, pin, freq, tim):
    result = self.checkMap(pin, 2)
    if result:
      return
    result = self.aw_attach(pin, 50, freq, tim)
  def pwm_set(self, pin, duty):
    result = self.checkMap(pin, 2)
    if result:
      result.obj.duty(duty)
  def analog_read(self, pin):
    result = self.checkMap(pin, 3)
    if result:
      try:
        result = result.obj.adc()[pin-100]
      except Exception as e:
        result = 0
      return result
    result = self.ar_attach(pin)
    try:
      result = result.obj.adc()[pin-100]
    except Exception as e:
      result = 0
    return result
  def irq(self, pin, callback, mode, wekup, prority):
    result = self.checkMap(pin, 4)
    if result:
      return result.obj.irq(callback, mode, wekup, prority)
    result = self.irq_attach(pin)
    result.obj.irq(callback, mode, wekup, prority)
  def disirq(self, pin):
    result = self.checkMap(pin, 4)
    if result:
      result.obj.disirq()
      self.free(pin)
  def free(self, pin):
    self.checkMap(pin, -1)


  

Pin = PIN()




