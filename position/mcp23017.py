#!/usr/bin/python
# -*- coding: utf-8 -*-

import smbus



class mcp23017:
    def __init__(self,i2cbus=1,device=0x20):
        self.device=device
        self.bus = smbus.SMBus(i2cbus)
        self.gpioa = {"register":0x12,"dirreg":0x00,"pureg":0x0c}
        self.gpiob = {"register":0x13,"dirreg":0x01,"pureg":0x0d}


class pin:
    def __init__(self,ioexp,register="gpioa",bit=0):
        self.__ioexp=ioexp
        self.__register=register
        if self.__register=="gpioa":
            self.__ioreg=self.__ioexp.gpioa
        else:
            self.__ioreg=self.__ioexp.gpiob
        self.__register=self.__ioreg["register"]
        self.__dirreg=self.__ioreg["dirreg"]
        self.__pureg=self.__ioreg["pureg"]
        self.__bit=bit
        #default to tri state 
        self.setx()
    def getbit():
        return self.__bit
    def getregister():
        return self.__register
    def getdirreg():
        return self.__dirreg
    def getpureg():
        return self.__pureg
    def setbit(newbit):
        self.__bit=newbit
    def setregister(newregister):
        self.__register=newregister
    def setdirreg(newdirreg):
        self.__dirreg=newdirreg
    def setpureg(newpureg):
        self.__pureg=newpureg
    def enable(self):
        self.disable_bit(self.__dirreg,self.__bit)
        self.enable_bit(self.__register,self.__bit)
        #print self.value
    def disable(self):
        self.disable_bit(self.__dirreg,self.__bit)
        self.disable_bit(self.__register,self.__bit)
    def setinput(self): 
        self.enable_bit(self.__dirreg,self.__bit)
        self.enable_bit(self.__pureg,self.__bit)
    #Tri state mode, input and pullup resistor off
    def setx(self):
        self.enable_bit(self.__dirreg,self.__bit)
        self.disable_bit(self.__pureg,self.__bit)
    def value(self):
        try:
            returnvalue=self.__ioexp.bus.read_byte_data(self.__ioexp.device,self.__register) & 2**self.__bit
        except:
            print("Error reading bus")
            return 3
        if returnvalue==0:
            return 0
        else:
            return 1
    def enable_bit(self,register,bit):
        try:
            value_old =  self.__ioexp.bus.read_byte_data(self.__ioexp.device,register)
            newvalue = value_old | 1<<bit
        except:
            print("Unable to read bus")
        try:
            self.__ioexp.bus.write_byte_data(self.__ioexp.device, register, newvalue)
        except:
            print("Unable to write bus")
    def disable_bit(self,register,bit):
        try:
            value_old =  self.__ioexp.bus.read_byte_data(self.__ioexp.device, register)
            newvalue = value_old & ~(1<<bit)
        except:
            print("Unable to read bus")
        try:
            self.__ioexp.bus.write_byte_data(self.__ioexp.device, register, newvalue)
        except:
            print("Unable to read bus")









