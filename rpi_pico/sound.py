import machine
import time
import _thread
class note:
    def __init__(self,frequency,duration,pause):
        self.frequency = frequency
        self.duration = duration
        self.pause = pause

class sound:
    def __init__(self):
        self.onboard_led=machine.Pin(25,machine.Pin.OUT)
        self.sound_pin=machine.PWM(machine.Pin(9,machine.Pin.OUT))
        self.tune=[]
        # Rounded musical note frequencies
        # 'S' is used in place of # (sharp) as that has a special meaning in python
        # DS2_Eb2 is D#2 / Eb2 
        self.C0=16
        self.CS0_Db0=17
        self.D0=18
        self.DS0_Eb0=19
        self.E0=21
        self.F0=22
        self.FS0_Gb0=23
        self.G0=25
        self.GS0_Ab0=26
        self.A0=28
        self.AS0_Bb0=29
        self.B0=31
        self.C1=33
        self.CS1_Db1=35
        self.D1=37
        self.DS1_Eb1=39
        self.E1=41
        self.F1=44
        self.FS1_Gb1=46
        self.G1=49
        self.GS1_Ab1=52
        self.A1=55
        self.AS1_Bb1=58
        self.B1=62
        self.C2=65
        self.CS2_Db2=69
        self.D2=73
        self.DS2_Eb2=78
        self.E2=82
        self.F2=87
        self.FS2_Gb2=93
        self.G2=98
        self.GS2_Ab2=104
        self.A2=110
        self.AS2_Bb2=117
        self.B2=123
        self.C3=131
        self.CS3_Db3=139
        self.D3=147
        self.DS3_Eb3=156
        self.E3=165
        self.F3=175
        self.FS3_Gb3=185
        self.G3=196
        self.GS3_Ab3=208
        self.A3=220
        self.AS3_Bb3=233
        self.B3=247
        self.C4=262
        self.CS4_Db4=277
        self.D4=294
        self.DS4_Eb4=311
        self.E4=330
        self.F4=349
        self.FS4_Gb4=370
        self.G4=392
        self.GS4_Ab4=415
        self.A4=440
        self.AS4_Bb4=466
        self.B4=494
        self.C5=523
        self.CS5_Db5=554
        self.D5=587
        self.DS5_Eb5=622
        self.E5=659
        self.F5=698
        self.FS5_Gb5=740
        self.G5=784
        self.GS5_Ab5=831
        self.A5=880
        self.AS5_Bb5=932
        self.B5=988
        self.C6=1047
        self.CS6_Db6=109
        self.D6=1175
        self.DS6_Eb6=1245
        self.E6=1319
        self.F6=1397
        self.FS6_Gb6=1480
        self.G6=1568
        self.GS6_Ab6=1661
        self.A6=1760
        self.AS6_Bb6=1865
        self.B6=1976
        self.C7=2093
        self.CS7_Db7=2217
        self.D7=2349
        self.DS7_Eb7=2489
        self.E7=2637
        self.F7=2794
        self.FS7_Gb7=2960
        self.G7=3136
        self.GS7_Ab7=3322
        self.A7=3520
        self.AS7_Bb7=3729
        self.B7=3951
        self.C8=4186
        self.CS8_Db8=4435
        self.D8=4699
        self.DS8_Eb8=4978
        self.E8=5274
        self.F8=5588
        self.FS8_Gb8=5920
        self.G8=6272
        self.GS8_Ab8=6645
        self.A8=7040
        self.AS8_Bb8=7459
        self.B8=7902
        _thread.start_new_thread(self.run,())
        
    def run(self):
        while(1):
            self.onboard_led.value(1)
            if (len(self.tune)):
                for tone in self.tune:
                    self.sound_pin.freq(tone.frequency)
                    self.sound_pin.duty_u16(20000)
                    time.sleep_ms(tone.duration)
                    self.sound_pin.duty_u16(0)
                    time.sleep_ms(tone.pause)
                self.tune=[]
            self.onboard_led.value(0)
            
            