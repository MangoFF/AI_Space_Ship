#coding=utf-8

#导入pygame库
import pygame,random,sys,time   #sys模块中的exit用于退出
from pygame.locals import *
from automative import DataGen, OperationSet
import math
from train_panel import TrainSystem
import numpy as np



#定义导弹类
class Bullet(object):
    """Bullet"""
    def __init__(self, planeName,x,y):
        if planeName == 'enemy':        #敌机导弹向下打
            self.imageName = 'Resources/bullet-3.png'
            self.direction = 'down'
        elif planeName == 'hero':       #英雄飞机导弹向上打
            self.imageName = 'Resources/bullet-1.png'
            self.direction = 'up'
        self.image = pygame.image.load(self.imageName).convert()
        self.x = x
        self.y = y

    def draw(self,screen):
        if self.direction == 'down':
            self.y += 8
        elif self.direction == 'up':
            self.y -= 8
        screen.blit(self.image,(self.x,self.y))
    
#定义一个飞机基类		
class Plane(object):
    """Plane"""
    def __init__(self):
        #导弹间隔发射时间1s
        self.bulletSleepTime = 0.3
        self.lastShootTime = time.time()
        #存储导弹列表
        self.bulletList = []

    #描绘飞机
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))

    def shoot(self):
        if time.time()-self.lastShootTime>self.bulletSleepTime:
            self.bulletList.append(Bullet(self.planeName,self.x+36,self.y))
            self.lastShootTime = time.time()

#玩家飞机类，继承基类
class Hero(Plane):
    """Hero"""
    def __init__(self, img='Resources/hero.png', x = 200, y = 600):
        Plane.__init__(self)
        planeImageName = img
        self.image = pygame.image.load(planeImageName).convert()
        #玩家原始位置
        self.width = 70
        self.height = 70
        self.x = x 
        self.y = y
        self.step_length = 25
        self.planeName = 'hero'



    def keepInBound(self):
        if self.x > ScreenWidth - self.width: self.x = ScreenWidth - self.width
        if self.x < 0: self.x = 0
        if self.y > ScreenHeight - self.height: self.y = ScreenHeight - self.height
        if self.y < 0: self.y = 0

    #键盘控制自己飞机
    def keyHandle(self,keyValue):
        if keyValue == 'left':
            self.x -= self.step_length
        elif keyValue == 'right':
            self.x += self.step_length
        elif keyValue == 'up':
            self.y -= self.step_length
        elif keyValue == 'down':
            self.y += self.step_length
        self.keepInBound()
    
    def moveTowards(self, tx, ty):
        force = self.step_length
        if tx != self.x and ty != self.y:
            force /= 2
        dx = 1 if tx > self.x else -1
        dy = 1 if ty > self.y else -1
        if tx != self.x:
            self.x += dx * force
        if ty != self.y:
            self.y += dy * force
        self.keepInBound()

#定义敌人飞机类
class Enemy(Plane):
    """docstring for Enemy"""
    def __init__(self,speed, x = random.randint(20, 400), y = 0):
        super(Enemy, self).__init__()
        randomImageNum = random.randint(1,3)
        planeImageName = 'Resources/enemy-' + str(randomImageNum) + '.png'
        self.image = pygame.image.load(planeImageName).convert()
        #敌人飞机原始位置
        self.x = random.randint(20,400)    #敌机出现的位置任意
        self.y = 0
        self.planeName = 'enemy'
        self.direction = 'down'     #用英文表示
        self.speed = speed          #移动速度,这个参数现在需要传入


    def move(self):
        if self.direction == 'down':
            self.y += self.speed     #飞机不断往下掉


class GameInit(object):
    """GameInit"""
    #类属性
    gameLevel = 1       #简单模式
    g_ememyList = []    #前面加上g类似全局变量
    score = 0           #用于统计分数
    hero = object

    @classmethod
    def createEnemy(cls,speed):
        cls.g_ememyList.append(Enemy(speed))

    @classmethod
    def createHero(cls):
        cls.hero = Hero()

    @classmethod
    def gameInit(cls):
        cls.createHero()

    @classmethod
    def heroPlaneKey(cls,keyValue):
        cls.hero.keyHandle(keyValue)

    @classmethod
    def draw(cls,screen):
        delPlaneList = []
        j = 0
        for i in cls.g_ememyList:
            i.draw(screen)   #画出敌机
            #敌机超过屏幕就从列表中删除
            if i.y > ScreenWidth:
                delPlaneList.append(j)
            j += 1
        delPlaneList.reverse()
        for m in delPlaneList:
            if m < len(cls.g_ememyList):
                del cls.g_ememyList[m]


        delBulletList = []
        j = 0
        cls.hero.draw(screen)    #画出英雄飞机位置
        for i in cls.hero.bulletList:
            #描绘英雄飞机的子弹，超出window从列表中删除
            i.draw(screen)
            if i.y < 0:
                delBulletList.append(j)
            j += 1
        #删除加入到delBulletList中的导弹索引,是同步的
        delBulletList.reverse()
        for m in delBulletList:
            del cls.hero.bulletList[m]
    
    #更新敌人飞机位置
    @classmethod
    def setXY(cls):
        for i in cls.g_ememyList:
            i.move()

    #自己飞机发射子弹
    @classmethod
    def shoot(cls):
        cls.hero.shoot()
        #子弹打到敌机让敌机从列表中消失
        ememyIndex = 0
        for i in cls.g_ememyList:
            enemyRect = pygame.Rect(i.image.get_rect())
            enemyRect.left = i.x
            enemyRect.top  = i.y
            bulletIndex = 0
            for j in cls.hero.bulletList:
                bulletRect = pygame.Rect(j.image.get_rect())
                bulletRect.left = j.x
                bulletRect.top  = j.y
                if enemyRect.colliderect(bulletRect):
                    #判断敌机的宽度或者高度，来知道打中哪种类型的敌机
                    if enemyRect.width == 39:
                        cls.score += 1000     #小中大飞机分别100,500,1000分
                    elif enemyRect.width == 60:
                        cls.score += 5000
                    elif enemyRect.width == 78:
                        cls.score += 10000
                    cls.g_ememyList.pop(ememyIndex)        #敌机删除
                    cls.hero.bulletList.pop(bulletIndex)   #打中的子弹删除
                bulletIndex += 1
            ememyIndex += 1

    #判断游戏是否结束
    @classmethod
    def gameover(cls):
        heroRect = pygame.Rect(cls.hero.image.get_rect())
        heroRect.left = cls.hero.x
        heroRect.top  = cls.hero.y
        for i in cls.g_ememyList:
            enemyRect = pygame.Rect(i.image.get_rect())
            enemyRect.left = i.x
            enemyRect.top  = i.y
            if heroRect.colliderect(enemyRect):
                return True
        return False

    #游戏结束后等待玩家按键
    @classmethod
    def waitForKeyPress(cls):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cls.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_RETURN:    #Enter按键
                        return
                    elif event.key == K_t:
                        return

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit(0)

    @staticmethod
    def pause(surface,image):
        surface.blit(image,(0,0))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cls.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        return

    @staticmethod
    def drawText(text,font,surface,x,y):
        #参数1：显示的内容 |参数2：是否开抗锯齿，True平滑一点|参数3：字体颜色|参数4：字体背景颜色
        content = font.render(text,False,(10,100,200))
        contentRect = content.get_rect()
        contentRect.left = x
        contentRect.top  = y
        surface.blit(content,contentRect)    

def ship_labeling(GameInit,screen):
    trainsys = TrainSystem(ScreenWidth, ScreenHeight, 40, 70)
    trainsys.mprint()
    game_labeling(GameInit,screen)
    ## 开始绘制
    testexit = False
    while not testexit:
        screen.blit(background, (0, 0))  # 不断覆盖，否则在背景上的图片会重叠
        enemies = trainsys.genRandomPlanes(4)
        for i in range(1, len(enemies)):
            e = enemies[i]
            GameInit.g_ememyList.append(Enemy(e[0], e[1]))

        GameInit.hero.x, GameInit.hero.y = enemies[0][0], enemies[0][1]
        print("hero loc", GameInit.hero.x, GameInit.hero.y)
        GameInit.hero.draw(screen)
        GameInit.draw(screen)
        pygame.display.update()

        marked = False
        handled = False
        while not handled:
            for event in pygame.event.get():
                # print(event.type)
                if event.type == pygame.QUIT:
                    GameInit.terminate()
                elif event.type == MOUSEBUTTONDOWN and not marked:
                    ## start draw the target point and record it
                    x, y = pygame.mouse.get_pos()
                    print("start draw the target point and record it. Mark at ", x, y)
                    # y = ScreenHeight - y
                    # draw target
                    target = Hero('Resources/hero.png', x, y)
                    target.draw(screen)
                    pygame.display.update()
                    trainsys.recordBestLoc(enemies, x, y)
                    marked = True
                    # handled = True
                    # break
                elif event.type == KEYDOWN and event.key == K_q:
                    print("Key q pressed")
                    testexit = True
                    handled = True
                    break
                elif event.type == KEYDOWN and event.key == K_n:
                    print("key n pressed")
                    handled = True
                    break
        GameInit.g_ememyList.clear()
def load_pic():
    pic_dic={}
    # pic load
    background = pygame.image.load("Resources/bg_01.png").convert()  # 背景图片
    pic_dic["background"]=background

    gameover = pygame.image.load("Resources/gameover.png").convert()  # 游戏结束图片
    pic_dic["gameover"] = gameover

    start = pygame.image.load("Resources/startone.png")  # 游戏开始图片
    pic_dic["start"] = start

    gamePauseIcon = pygame.image.load("Resources/Pause.png")
    pic_dic["gamePauseIcon"] = gamePauseIcon

    gameStartIcon = pygame.image.load("Resources/Start.png")
    pic_dic["gameStartIcon"] = gameStartIcon
    return pic_dic
class gamecontroller:
    def __init__(self,frame_rate=30,option_rate=1,mode="HANDY",ScreenWidth=460, ScreenHeight=680,caption='飞机大战'):
        # init py game
        pygame.init()

        # recode the time
        self.startTime = time.time()

        # 控制控制速率
        self.op_rate = option_rate
        self.op_duration = 1 / self.op_rate
        self.last_op_time = self.startTime

        # 控制帧率
        self.fram_rate = frame_rate
        self.frame_duration = 1 / self.fram_rate
        self.last_time = self.startTime

        #mode
        self.mode=mode

        self.screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), 0, 32)

        # 参数1：字体类型，例如"arial"  参数2：字体大小
        self.font = pygame.font.SysFont(None, 64)
        self.font1 = pygame.font.SysFont("arial", 24)
        pygame.display.set_caption(caption)

        self.ops = OperationSet("input.in")
        self.datagen = DataGen("data.out")

        # enemy spawn span
        self.easyEnemySleepTime = 1
        self.middleEnemySleepTime = 0.5
        self.hardEnemySleepTime = 0.25
        self.lastEnemyTime = 0

        GameInit.gameInit()
    def update(self):
        pygame.display.update()
    def screen_draw(self,pic,position):
        self.screen.blit(pic, position)

def run_game():

    game_control = gamecontroller(frame_rate=30, mode="Handy")
    pic_dic=load_pic()

    game_control.screen_draw(pic_dic["start"],(0,0))
    game_control.update()
    GameInit.waitForKeyPress()

    GameInit.hero.x = 200
    GameInit.hero.y = 600
    while True:
        # draw background
        game_control.screen_draw(pic_dic["background"], (0, 0))
        # draw start icon
        game_control.screen_draw(pic_dic["gameStartIcon"], (0, 0))
        GameInit.drawText('score:%s' % (GameInit.score), game_control.font1, game_control.screen, 80, 15)
        cur_time = time.time()
        interval = cur_time - game_control.startTime
        if game_control.mode == "AUTO":
            if cur_time - game_control.last_op_time > game_control.op_duration:
                enemies = []
                for e in GameInit.g_ememyList:
                    enemies.append([e.x, e.y])
                op = game_control.ops.getnxt(game_control.datagen.screenshot([GameInit.hero.x, GameInit.hero.y], enemies))[0]
                print(op)
                if op != None:
                    print("op is ", op)
                    GameInit.hero.moveTowards(op[0], op[1])
                game_control.last_op_time = cur_time
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                GameInit.terminate()
            elif event.type == KEYDOWN:
                # control the ship
                if event.key == K_LEFT:
                    GameInit.heroPlaneKey('left')
                elif event.key == K_RIGHT:
                    GameInit.heroPlaneKey('right')
                elif event.key == K_UP:
                    GameInit.heroPlaneKey('up')
                elif event.key == K_DOWN:
                    GameInit.heroPlaneKey('down')
                elif event.key == K_SPACE:
                    GameInit.pause(game_control.screen, pic_dic["gamePauseIcon"])  # 难度选择方面有bug.因为时间一直继续
        # easy模式
        if interval < 10:
            # print("Spawn a easy Enemy")
            if time.time() - game_control.lastEnemyTime >= game_control.easyEnemySleepTime:
                GameInit.createEnemy(1)  # 传入的参数是speed
                game_control.lastEnemyTime = time.time()
        # middle模式
        elif interval >= 10 and interval < 30:
            # print("Spawn a middle Enemy")
            if time.time() - game_control.lastEnemyTime >= game_control.middleEnemySleepTime:
                GameInit.createEnemy(2)
                game_control.lastEnemyTime = time.time()
        # hard模式
        elif interval >= 30:
            # print("Spawn a Hard Enemy")
            if time.time() - game_control.lastEnemyTime >= game_control.hardEnemySleepTime:
                GameInit.createEnemy(3)
                game_control.lastEnemyTime = time.time()

        # frame update
        if game_control.frame_duration <= cur_time - game_control.last_time:
            enemies = []
            for e in GameInit.g_ememyList:
                enemies.append([e.x, e.y])
            game_control.datagen.screenshot([GameInit.hero.x, GameInit.hero.y], enemies)
            GameInit.shoot()
            GameInit.setXY()
            GameInit.draw(game_control.screen)  # 描绘类的位置
            pygame.display.update()  # 不断更新图片
            game_control.last_time = time.time()

        if GameInit.gameover():
            # crash the enemy ,then game over
            time.sleep(1)  # 睡1s时间,让玩家看到与敌机相撞的画面
            game_control.screen_draw(pic_dic["gameover"], (0, 0))
            GameInit.drawText('%s' % (GameInit.score), game_control.font, game_control.screen, 170, 400)
            pygame.display.update()
            GameInit.waitForKeyPress()
            break
        # time.sleep(max(0, frame_duration - (cur_time - last_time)))

#主循环
if __name__ == '__main__':
    ScreenWidth ,ScreenHeight= 460, 680
    run_game()

        

        

    
