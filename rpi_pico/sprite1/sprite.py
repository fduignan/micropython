
class sprite:
    def __init__(self,x,y,w,h,image,display):
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.image=image
        self.visible=0
        self.display=display
        self.horiz=1 # default orientation left to right
        self.vert=1  # default orientation top to bottom
    def show(self):
        self.display.putImage(self.x,self.y,self.width,self.height,self.image,self.horiz,self.vert)
        self.visible=1
    def hide(self):
        self.display.fillRectangle(self.x,self.y,self.width,self.height,0)
        self.visible=0
    def move(self,newx, newy):
        if (self.visible==1):
            self.hide()
        self.x = newx
        self.y = newy
        self.show()
    def setOrientation(self, horiz, vert):
        self.horiz = horiz
        self.vert = vert