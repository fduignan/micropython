from machine import Pin, Timer,SPI, PWM
import urandom
import time
import st7735
import sprite
import sprites
import controller
import santa
import brici
import sound
display=st7735.st7735()
display.clear()
gamepad=controller.controller()
display.clear()
urandom.seed()
display.setOrientation(0,1)
snd=sound.sound()

x = 0
y = 0
moved = 0
count=0
colour=0
while(1):
    display.clear()
    display.print("Main Menu",0,10,display.RGBToWord(255,255,255),0)
    display.print("Left for Brici",0,20,display.RGBToWord(255,255,0),0)
    display.print("Right for Santa",0,30,display.RGBToWord(255,64,64),0)
    
    while(gamepad.buttonPressed()==0):
        pass
    if (gamepad.leftPressed()==1):
        BriciGame=brici.brici(display,gamepad,snd)
        BriciGame.play()
    if (gamepad.rightPressed()==1):
        SantaGame=santa.santa(display,gamepad,snd)
        SantaGame.play()
        

