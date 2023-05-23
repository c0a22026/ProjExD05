import pygame as pg
import time
import sys

WIDTH = 1600
HEIGHT = 900

class Tower(pg.sprite.Sprite):
    def __init__(self, life, bool):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("ex05/fig/tower.png"), 0, 0.5)
        self.life = life
        self.rect = self.image.get_rect()
        self.bool = bool
        if self.bool:
            self.rect.centerx = WIDTH - 50
        else:
            self.rect.centerx = 50
        self.rect.centery = HEIGHT / 5 * 3
    
    def winlose(self):
        if self.life <= 0 and self.bool:
            print("win")
            return
        elif self.life <= 0 and self.bool == False:
            print("lose")
            return 
    def update(self):
        self.winlose()
            

class Chara(pg.sprite.Sprite):
    def __init__(self, life, bool, speed):
        super().__init__()
        self.image = pg.image.load("ex05/fig/3.png")
        self.life = life
        self.collision = 0
        self.speed = speed
        self.rect = self.image.get_rect()
        self.bool = bool
        if self.bool:
            self.image = pg.image.load("ex05/fig/3.png")
            self.rect.centerx = 1540
        else:
            self.image = pg.transform.flip(pg.image.load("ex05/fig/3.png"), True, False) 
            self.rect.centerx = 60
        self.rect.centery = HEIGHT / 5 * 3.6
    def update(self):
        if WIDTH <= self.rect.centerx or self.rect.centerx <= 0:
            self.kill()
        if self.collision == 0:
            self.rect.centerx += self.speed
        if self.life <= 0:
            self.kill()



def main():
    tmr = 0
    temp = 0
    flag = True
    speed = 5
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex04/fig/pg_bg.jpg")
    enemys = pg.sprite.Group()
    clock = pg.time.Clock()
    allis = pg.sprite.Group()
    towers = pg.sprite.Group()
    towers.add(Tower(50, True))
    towers.add(Tower(50, False))
    while True:
        if tmr - temp >= 30:
            flag = True
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():#キーに関する判定
            if event.type == pg.QUIT:
                return 0
            if event.type == pg.KEYDOWN and event.key == pg.K_1 and flag:#こうかとん出撃に関する判定
                allis.add(Chara(60, False, speed))
                flag = False
                temp = tmr
        if tmr % 100 == 0:
            enemys.add(Chara(60, True, -speed))
        #当たり判定記述
        for emy in pg.sprite.groupcollide(enemys, allis, False, False):#こうかとんどうしの当たり判定
            for ally in pg.sprite.groupcollide(allis, enemys, False, False):
                emy.speed = 0
                emy.life -= 1
                ally.speed = 0
                ally.life -= 1
                if emy.life <= 0:
                    ally.speed = speed
                if ally.life <= 0:
                    emy.speed = -speed
        for emy in pg.sprite.groupcollide(enemys, towers, False, False):#こうかとんとタワーの当たり判定
            for tower in pg.sprite.groupcollide(towers, enemys, False, False):
                if tower.bool == False:
                    emy.life -= 1
                    emy.speed = 0
                    tower.life -= 1

        for ally in pg.sprite.groupcollide(allis, towers, False, False):
            for tower in pg.sprite.groupcollide(towers, allis, False, False):
                if tower.bool:
                    ally.life -= 1
                    ally.speed = 0
                    tower.life -= 1


        screen.blit(bg_img, [0, 0])
        towers.draw(screen)
        towers.update()
        enemys.draw(screen)
        enemys.update()
        allis.draw(screen)
        allis.update()
        pg.display.update()
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

