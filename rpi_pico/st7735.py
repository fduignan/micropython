from machine import Pin, Timer,SPI
import time
import array
import font5x7
class st7735:
    def __init__(self):
        self.screen_width=128
        self.screen_height=160
        # configure pins for output
        self.reset=Pin(21,Pin.OUT)
        self.cs=Pin(22,Pin.OUT)
        self.a0=Pin(20,Pin.OUT)
        self.spi=SPI(0,baudrate=40000000,polarity=1,phase=1,bits=8,firstbit=SPI.MSB,sck=Pin(18),mosi=Pin(19))        
        self.cs.value(1)
        self.reset.value(1)
        time.sleep_ms(10)
        
        self.reset.value(0)
        time.sleep_ms(200)
        
        self.reset.value(1)
        time.sleep_ms(200)
        self.cs.value(200)
        time.sleep_ms(200)
        
        self.cs.value(0)
        time.sleep_ms(20)
        
        self.command(1) # software reset
        time.sleep_ms(100)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0x11)
        time.sleep_ms(120)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)        
        time.sleep_ms(1)
        
        self.command(0xb1)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c);
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0xb2)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c);        
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0xb3)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c)
        self.data(0x05)
        self.data(0x3c)
        self.data(0x3c)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0xb4)
        self.data(0x03)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0x36)
        self.data(0xc8)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0x3a)
        self.data(0x05)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0x29)
        time.sleep_ms(100)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
        
        self.command(0x2c)          
        self.fillRectangle(0,0,128,160,0)
        
    def command(self,cmd):
        self.a0.value(0)
        self.spi_write(cmd)
        #msg=bytearray()
        #msg.append(cmd)
        #self.spi.write(msg)        
    def data(self,data):
        self.a0.value(1)
        self.spi_write(data)
        #msg=bytearray()
        #msg.append(cmd)
        #self.spi.write(msg)        
    def openAperture(self,x1,y1,x2,y2):
        self.command(0x2a)
        self.data(x1 >> 8)
        self.data(x1 & 0xff)
        self.data(x2 >> 8)
        self.data(x2 & 0xff)
        self.command(0x2b)
        self.data(y1 >> 8)
        self.data(y1 & 0xff)
        self.data(y2 >> 8)
        self.data(y2 & 0xff)        
        self.command(0x2c)
    
    def putPixel(self,x,y,colour):
        self.command(0x2a)
        self.data(x >> 8)
        self.data(x & 0xff)
        self.data(x+1 >> 8)
        self.data(x+1 & 0xff)
        self.command(0x2b)
        self.data(y >> 8)
        self.data(y & 0xff)
        self.data(y+1 >> 8)
        self.data(y+1 & 0xff)        
        self.command(0x2c)      
        self.a0.value(1)
        self.fill_block(colour,1)
        
    def putPixelPy(self,x,y,colour):
        self.openAperture(x,y,x+1,y+1)        
        self.a0.value(1)
        msg=bytearray()
        msg.append(colour >> 8)
        msg.append(colour & 0xff)
        self.spi.write(msg)    
    def drawLine(self,x0,y0,x1,y1,colour):
        if (x0==x1):
            # vertical line so use fill rectanlge (faster)
            self.fillRectangle(x0,y0,1,y1-y0,colour)
            return
        if (y0==y1):
            # vertical line so use fill rectanlge (faster)
            self.fillRectangle(x0,y0,x1-x0,1,colour)
            return
        if ( (abs(y1-y0) < abs(x1-x0))):
             if (x0 > x1):
                 self.drawLineLowSlope(x1,y1,x0,y0,colour)
             else:
                 self.drawLineLowSlope(x0,y0,x1,y1,colour)
        else:
            if (y0 > y1):
                self.drawLineHighSlope(x1,y1,x0,y0,colour)
            else:
                self.drawLineHighSlope(x0,y0,x1,y1,colour)
             
    def drawLineLowSlope(self,x0,y0,x1,y1,colour):
        # Reference : https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm    
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if (dy < 0):
            yi = -1
            dy = -dy
        D = 2*dy - dx
        y = y0
        for x in range(x0,x1+1):
            self.putPixel(x,y,colour)
            if (D > 0):
                y = y + yi
                D = D - 2*dx
            D=D + 2*dy
    def drawLineHighSlope(self,x0,y0,x1,y1,colour):
        # Reference : https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm    
        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if (dx < 0):
            xi = -1
            dx = -dx
        D = 2*dx - dy
        x = x0
        for y in range(y0,y1+1):
            self.putPixel(x,y,colour)
            if (D > 0):
                x = x + xi
                D = D - 2*dy
            D=D + 2*dx        
    def fillRectangle(self,x1,y1,w,h,colour):
        self.openAperture(x1,y1,x1+w-1,y1+h-1)        
        pixelcount=h*w
        self.command(0x2c)
        self.a0.value(1)
        self.fill_block(colour,pixelcount)        
    def fillRectanglePy(self,x1,y1,w,h,colour):
        self.openAperture(x1,y1,x1+w-1,y1+h-1)        
        pixelcount=h*w
        self.command(0x2c)
        self.a0.value(1)        
        msg=bytearray()
        while(pixelcount >0):
            pixelcount = pixelcount-1          
            msg.append(colour >> 8)
            msg.append(colour & 0xff)
        self.spi.write(msg)
    @micropython.asm_thumb
    def fill_block(r0,r1,r2):
        # pointer to self passed in r0
        # r1 contains the 16 bit data to be written
        # r2 countains count
        # Going to use SPI0.
        # Base address = 0x4003c000
        # SSPCR0 Register OFFSET 0
        # SSPCR1 Register OFFSET 4
        # SSPDR Register OFFSET 8
        # SSPSR Register OFFSET c
        push({r1,r2,r3,r4,r7})
        # Convoluted load of a 32 bit value into r7
        mov(r7,0x40)
        lsl(r7,r7,8)
        add(r7,0x03)
        lsl(r7,r7,8)
        add(r7,0xc0)
        lsl(r7,r7,8)
        add(r7,0x00)
        mov(r4,2)        
        label(fill_block_loop_start)
        cmp(r2,0)
        beq(fill_block_exit)        
        mov(r3,r1) # read next byte from colour (there is an endian-ness change)
        strb(r3,[r7,8]) # write to SPI
        label(fill_block_spi_wait1)        
        ldr(r3,[r7,0xc]) # read status
        and_(r3,r4) # mask for busy flags
        beq(fill_block_spi_wait1) # if busy go back and wait
        
        mov(r3,r1) # read next byte from colour (there is an endian-ness change)
        lsr(r3,r3,8) 
        strb(r3,[r7,8]) # write to SPI        
        sub(r2,r2,1) # decrement count                
        label(fill_block_spi_wait2)        
        ldr(r3,[r7,0xc]) # read status
        and_(r3,r4) # mask for busy flags
        beq(fill_block_spi_wait2) # if busy go back and wait
        b(fill_block_loop_start)
        label(fill_block_exit)
        pop ({r1,r2,r3,r4,r7})
        
   
    @micropython.asm_thumb
    def spi_write(r0,r1):
        # on entry r0 points to self
        # r1 contains value to write to SPI bus
        mov(r2,0x40)
        lsl(r2,r2,8)
        add(r2,0x03)
        lsl(r2,r2,8)
        add(r2,0xc0)
        lsl(r2,r2,8)
        add(r2,0x00)
        str(r1,[r2,8])
        
    def drawRectangle(self,x1,y1,w,h,Colour):
        self.drawLine(x1,y1,x1+w,y1,Colour)
        self.drawLine(x1,y1,x1,y1+h,Colour)
        self.drawLine(x1+w,y1,x1+w,y1+h,Colour)
        self.drawLine(x1,y1+h,x1+w,y1+h,Colour)
    def clear(self):
        self.fillRectangle(0,0,128,160,0)
    def putImage(self,x,y,w,h,img,horiz,vert):
        # assumption: img is a bytearray object
        if (vert == 0):
            y=self.screen_height-y-h
        if (horiz == 0):
            x=self.screen_width-x-w
        self.setOrientation(horiz,vert)
        self.openAperture(x,y,x+w-1,y+h-1)
        pixelcount=w*h
        self.command(0x2c)
        self.a0.value(1)
        self.spi.write(img)
        self.setOrientation(1,1)
    def setOrientation(self,h,v):
        # 1,1 = left to right scanning moving vertically downwards
        # 1,0 = left to right scanning moving vertically upwards
        # 0,1 = right to left scanning moving vertically downwards
        # 0,0 = right to left scanning moving vertically upwards
        # Note : if using this to transform a sprite or tile you also
        # need to adjust the start co-ordinates.
        self.command(0x36)
        mode = (v << 7)+(h << 6) + 0x08
        self.data(mode)
        self.cs.value(1)
        time.sleep_ms(1)
        self.cs.value(0)
        time.sleep_ms(1)
    def print(self, text, x, y, forecolour, backcolour):
        index=0
        row=0
        col=0
        textBox=array.array('h',[0]*font5x7.width*font5x7.height)        
        for index in range(0,len(text)):
            font_table_index=font5x7.width*(ord(text[index])-32)
            col=0
            while(col < font5x7.width):
                row=0
                while (row < font5x7.height):                 
                    if (font5x7.font[font_table_index+col]&(1<<row)):
                        textBox[(row*font5x7.width)+col]=forecolour
                    else:
                        textBox[(row*font5x7.width)+col]=backcolour
                    row=row+1
                col = col+1
            self.putImage(x+10,y+10,font5x7.width, font5x7.height,textBox,1,1)
            x=x+font5x7.width+2
    def RGBToWord(self,r,g,b):
        rvalue=0
        rvalue = rvalue + (g >> 5)
        rvalue = rvalue + ((g & (0b111)) << 13)
        rvalue = rvalue + ((r >> 3) << 8)
        rvalue = rvalue + ((b >> 3) << 3)
        #b1=rvalue & 0xff;
        #b2=rvalue >> 8;
        #rvalue = (b1<<8)+b2
        return rvalue
    def drawCircle(self,x0,y0,radius,colour):
        # Reference : https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
        x = radius - 1
        y = 0
        dx = 1
        dy = 1
        err = dx - (radius << 1)
        if (radius > x0):
            return # don't draw partially off-screen circles
        if (radius > y0):
            return # don't draw partially off-screen circles
        if ((x0+radius) > self.screen_width):
            return # don't draw partially off-screen circles
        if ((y0+radius) > self.screen_height):
            return # don't draw partially off-screen circles
        while (x >= y):
            self.putPixel(x0 + x, y0 + y, colour)
            self.putPixel(x0 + y, y0 + x, colour)
            self.putPixel(x0 - y, y0 + x, colour)
            self.putPixel(x0 - x, y0 + y, colour)
            self.putPixel(x0 - x, y0 - y, colour)
            self.putPixel(x0 - y, y0 - x, colour)
            self.putPixel(x0 + y, y0 - x, colour)
            self.putPixel(x0 + x, y0 - y, colour)
            if (err <=0):
                y = y + 1
                err = err + dy
                dy = dy + 2
            if (err > 0):
                x = x - 1
                dx = dx + 2
                err = err + dx - (radius << 1)
    def fillCircle(self,x0,y0,radius,colour):
        # Reference : https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
        x = radius - 1
        y = 0
        dx = 1
        dy = 1
        err = dx - (radius << 1)
        if (radius > x0):
            return # don't draw partially off-screen circles
        if (radius > y0):
            return # don't draw partially off-screen circles
        if ((x0+radius) > self.screen_width):
            return # don't draw partially off-screen circles
        if ((y0+radius) > self.screen_height):
            return # don't draw partially off-screen circles
        while (x >= y):
            self.drawLine(x0-x,y0+y,x0+x,y0+y,colour)
            self.drawLine(x0-y,y0+x,x0+y,y0+x,colour)
            self.drawLine(x0-x,y0-y,x0+x,y0-y,colour)
            self.drawLine(x0-y,y0-x,x0+y,y0-x,colour)
            if (err <=0):
                y = y + 1
                err = err + dy
                dy = dy + 2
            if (err > 0):
                x = x - 1
                dx = dx + 2
                err = err + dx - (radius << 1)                