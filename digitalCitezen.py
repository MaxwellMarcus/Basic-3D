try:
    from tkinter import *
except:
    from Tkinter import *
root = Tk()
canvas = Canvas(root,height=600,width=1000)
canvas.pack()

class Game:
    def __init__(self):
        self.game = True
        self.keys = []
        self.squares = []
        self.text = []
        root.bind('<KeyPress>',self.keyPressed)
        root.bind('<KeyRelease>',self.KeyReleased)
        root.bind('<Button-1>',self.mousePress)
    def keyPressed(self,event):
        self.keys.append(event.keysym)
        print(event.keysym)
        if not len(event.keysym) > 1:
            self.text += [str(event.keysym)]
        if event.keysym == 'BackSpace' and len(self.text) > 0:
            self.text.remove(self.text[len(self.text)-1])
        if event.keysym == 'space':
            self.text.append(' ')
    def KeyReleased(self,event):
        for event.keysym in self.keys:
            self.keys.remove(event.keysym)
    def mousePress(self,event):
        self.squares.append([canvas.create_rectangle(event.x-50,event.y-50,event.x+50,event.y+50,fill='Blue'),event.x,event.y])
    def update(self):
        if 'Escape' in self.keys:
            self.game = False
        for i in self.squares:
            i[0] = canvas.create_rectangle(i[1]-50,i[2]-50,i[1]+50,i[2]+50,fill='Blue')
        text = ''
        for i in self.text:
            text += i
        canvas.create_text(500,300,text=text,font=('TkTextFont',100))

game = Game()
while game.game:
    canvas.delete(ALL)
    game.update()
    root.update()
