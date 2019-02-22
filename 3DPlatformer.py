import render3D

camera = render3D._3D(500)
class Game:
    def __init__(self):
        self.game = True
        for i in range(100):
            camera.createCube(i*20,50,100,10)
    def render(self):
        camera.clearScreen()
        for i in camera.visible(camera.objects):
            i = camera.project(i)
            face = camera.visibleFace(i)
            camera.draw_faces(i,face)
        player.render()
        camera.updateScreen()
class Player:
    def __init__(self):
        self.player = camera.returnCube(0,40,110,5)
        self.coords = self.player[0]

    def render(self):
        i = self.player
        i = camera.project(i)
        face = camera.visibleFace(i)
        camera.draw_faces(i,face)


game = Game()
player = Player()
while game.game:
    game.render()
