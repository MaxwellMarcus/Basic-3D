import render3D

camera = render3D._3D(500)
class Game:
    def __init__(self):
        self.game = True
        self.screen = 1
        for i in range(100):
            camera.createCube(i*20,50,100,10)
    def render(self):
        if self.screen == 2:
            camera.clearScreen()
            for i in camera.visible(camera.objects):
                i = camera.project(i)
                face = camera.visibleFace(i)
                camera.draw_faces(i,face)
            player.render()
            camera.updateScreen()
        elif self.screen == 1:
            camera.clearScreen()
            camera.drawText(camera.screenWidth/2,camera.screenHeight/4,'GAME',50)
            camera.updateScreen()
class Player:
    def __init__(self):
        self.player = camera.returnCube(0,40,110,5)
        self.coords = self.player[0]
    def move(self,x=0,y=0,z=0):
        for i in self.player:
            i[0]+=x
            i[1]+=y
            i[2]+=z
        camera.camPos[0] += -x
    def render(self):
        i = self.player
        i = camera.project(i)
        face = camera.visibleFace(i)
        camera.draw_faces(i,face)


game = Game()
player = Player()
while game.game:
    if 'Escape' in camera.keysPressed:
        if game.screen == 1:
            game.game = False
        else:
            game.screen = 1
            i=0
            while i < camera.keysPressed.count('Escape'):
                camera.keysPressed.remove('Escape')
                i=0

    elif game.screen == 1:
        if len(camera.keysPressed) > 0:
            game.screen = 2
    elif game.screen == 2:
        if 'd' in camera.keysPressed:
            player.move(x=1)
        if 'a' in camera.keysPressed:
            player.move(x=-1)

    game.render()
