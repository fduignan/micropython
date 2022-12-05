from machine import Pin, Timer,SPI
import time
class controller:
    def __init__(self):
        self.left=Pin(16,Pin.IN, Pin.PULL_UP)
        self.right=Pin(15,Pin.IN, Pin.PULL_UP)
        self.up=Pin(17,Pin.IN, Pin.PULL_UP)
        self.down=Pin(14,Pin.IN, Pin.PULL_UP)
        self.b=Pin(27,Pin.IN, Pin.PULL_UP)
        self.a=Pin(26,Pin.IN, Pin.PULL_UP)
    def leftPressed(self):
        if (self.left.value()==0):
            return 1
        else:
            return 0
    def rightPressed(self):
        if (self.right.value()==0):
            return 1
        else:
            return 0
    def upPressed(self):
        if (self.up.value()==0):
            return 1
        else:
            return 0        
    def downPressed(self):
        if (self.down.value()==0):
            return 1
        else:
            return 0        
    def aPressed(self):
        if (self.a.value()==0):
            return 1
        else:
            return 0
    def bPressed(self):
        if (self.b.value()==0):
            return 1
        else:
            return 0
    def buttonPressed(self):
        # return which button (if any was pressed). Each button is associated with a particular bit
        # this allows for it to return multiple button presses
        returnValue = 0
        if self.leftPressed():
            returnValue = returnValue + 1
        if self.rightPressed():
            returnValue = returnValue + 2
        if self.upPressed():
            returnValue = returnValue + 4
        if self.downPressed():
            returnValue = returnValue + 8
        if self.aPressed():
            returnValue = returnValue + 16
        if self.bPressed():
            returnValue = returnValue + 32
        return returnValue