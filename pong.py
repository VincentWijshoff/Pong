import pandas
import pygame as pg
import time as t
import random as rndm

class Ball:

    def __init__(self, size, screen_width, screen_height, wallsize, vel):
        self.BALLSIZE = size
        pg.draw.rect(screen, pg.Color("black"), pg.Rect((screen_width // 2, screen_height // 2), (self.BALLSIZE, self.BALLSIZE)))
        pg.display.flip()
        self.maxvel = vel
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.xvel = 0
        self.yvel = 0
        while self.xvel == 0 or self.yvel == 0:
            self.xvel = rndm.uniform(0.5, self.maxvel)
            self.yvel = rndm.uniform(-self.maxvel, self.maxvel)
        self.white = pg.Color("white")
        self.black = pg.Color("black")
        self.scrn_wdth = screen_width
        self.scrn_hght = screen_height
        self.wall_sze = wallsize

    def paddles(self, padle):
        if self.x <= padle.x + padle.width and self.x + self.BALLSIZE >= padle.x and self.y <= padle.y + padle.height and self.y + self.BALLSIZE >= padle.y:
            self.xvel *= -1
            if rndm.random() >= 0.4:
                self.yvel *= -1

    def move(self, padle1, padle2):
        #first remove old ball
        pg.draw.rect(screen, self.white, pg.Rect((int(self.x), int(self.y)), (self.BALLSIZE, self.BALLSIZE)))
        #then calculate the new values
        self.x = self.x + self.xvel
        self.y = self.y + self.yvel
        #if the ball is touching any off the surfaces the velocity should change
        if self.x <= self.wall_sze:
            self.reset()
        if self.x + self.BALLSIZE >= self.scrn_wdth - self.wall_sze:
            self.reset()
        if self.y <= self.wall_sze:
            self.yvel *= -1
        if self.y + self.BALLSIZE >= self.scrn_hght - self.wall_sze:
            self.yvel *= -1
        self.paddles(padle1)
        self.paddles(padle2)
        #redraw the bal
        pg.draw.rect(screen, self.black, pg.Rect((int(self.x), int(self.y)), (self.BALLSIZE, self.BALLSIZE)))

    def reset(self):
        t.sleep(0.2)
        self.x = self.scrn_wdth//2
        self.y = self.scrn_hght//2
        self.xvel = 0
        self.yvel = 0
        while self.xvel == 0 or self.yvel == 0:
            self.xvel = rndm.uniform(-self.maxvel, self.maxvel)
            self.yvel = rndm.uniform(-self.maxvel, self.maxvel)


class Padle:

    def __init__(self, height, x, screen_height, wallsize):
        self.height = height
        self.scrn_hgth = screen_height
        self.wall_sze = wallsize
        self.black = pg.Color("black")
        self.white = pg.Color("white")
        self.x = x
        self.y = self.scrn_hgth//2
        self.width = wallsize
        pg.draw.rect(screen, self.black, pg.Rect((self.x, self.scrn_hgth//2), (self.wall_sze, self.height)))

    def move(self, y):
        pg.draw.rect(screen, self.white, pg.Rect((self.x, int(self.y)), (self.wall_sze, self.height)))
        self.y = y - self.height//2
        if self.y + self.height + self.wall_sze >= self.scrn_hgth:
            self.y = self.scrn_hgth - self.wall_sze - self.height
        if self.y - self.wall_sze <= 0:
            self.y = self.wall_sze
        pg.draw.rect(screen, self.black, pg.Rect((self.x, int(self.y)), (self.wall_sze, self.height)))


def drawWalls(color, screen_width, screen_height, BORDER):
    pg.draw.rect(screen, color, pg.Rect((0, 0), (screen_width, BORDER)))
    pg.draw.rect(screen, color, pg.Rect((0, 0), (BORDER, screen_height)))
    pg.draw.rect(screen, color, pg.Rect((0, screen_height - BORDER), (screen_width, BORDER)))
    pg.draw.rect(screen, color, pg.Rect((screen_width - BORDER, 0), (BORDER, screen_height)))


#init
canv = pg.init()
screen_width = 900
screen_height = 600
screen = pg.display.set_mode([screen_width, screen_height])
pg.draw.rect(screen, pg.Color("white"), pg.Rect((0,0), (screen_width, screen_height)))
pg.display.flip()
#borders
BORDER = 20
drawWalls(pg.Color("black"), screen_width, screen_height, BORDER)
pg.display.flip()
#ball + controllers
bal = Ball(20, screen_width, screen_height, BORDER, 1)
padle1 = Padle(screen_height//6, 2*BORDER, screen_height, BORDER)
padle2 = Padle(screen_height//6, screen_width-3*BORDER, screen_height, BORDER)
pg.display.flip()

#padleLeft = open("rightPadleData.csv", "w")

#padleLeft.truncate()

#print("x,y,xvel,yvel,padle.y", file= padleLeft)

# pongLeft = pandas.read_csv("leftPadleData.csv")
# pongLeft = pongLeft.drop_duplicates()
# pongRight = pandas.read_csv("rightPadleData.csv")
# pongRight = pongRight.drop_duplicates()
#
# Lx = pongLeft.drop(columns = "padle.y")
# Ly = pongLeft['padle.y']
# Rx = pongRight.drop(columns = "padle.y")
# Ry = pongRight['padle.y']

# from sklearn.neighbors import KNeighborsRegressor
#
# clfL = KNeighborsRegressor(n_neighbors=3)
# clfR = KNeighborsRegressor(n_neighbors=3)
#
# clfL.fit(Lx,Ly)
# clfR.fit(Rx,Ry)
#
# dflL = pandas.DataFrame(columns=['x','y','xvel','yvel'])
# dflR = pandas.DataFrame(columns=['x','y','xvel','yvel'])
#game
while True:
    e = pg.event.poll()
    if e.type == pg.QUIT:
        break
    bal.move(padle1, padle2)
    # toPredictLeft = dflL.append({'x':bal.x, 'y':bal.y, 'xvel':bal.xvel, 'yvel':bal.yvel}, ignore_index=True)
    # moveL = clfL.predict(toPredictLeft)
    # toPredictRight = dflR.append({'x': bal.x, 'y': bal.y, 'xvel': bal.xvel, 'yvel': bal.yvel}, ignore_index=True)
    # moveR = clfR.predict(toPredictRight)
    padle1.move(bal.y)
    padle2.move(bal.y)
    drawWalls(pg.Color("black"), screen_width, screen_height, BORDER)
    pg.display.flip()
    #print("{},{},{},{},{}".format(bal.x, bal.y, bal.xvel, bal.yvel, padle2.y), file= padleLeft)

pg.quit()