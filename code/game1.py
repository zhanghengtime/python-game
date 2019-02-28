import pygame
from sys import exit
from pygame.locals import *
import random
from time import *


class Plane:
    def restart(self, x, y):
        self.x = x
        self.y = y
        self.move_x = 0
        self.move_y = 0

    def __init__(self):
        self.restart(180, 500)
        self.image = pygame.image.load('plane.png').convert_alpha()

    def move(self):
        self.x += self.move_x
        if(self.x >= 400):
            self.x = 400
        if (self.x <= -50):
            self.x = -50
        self.y += self.move_y
        if(self.y >= 750):
            self.y = 750
        if (self.y <= -50):
            self.y = -50

class Bullet:
    def __init__(self):
        # 初始化成员变量，x，y，image
        self.x = 0
        self.y = -3
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.active = False

    def move(self):
        # 激活状态下，向上移动
        if self.active:
            self.y -= 1
        # 当飞出屏幕，就设为不激活
        if self.y < 0:
            self.active = False

    def restart(self, X, Y):
        # 处理子弹的运动
        self.x = X - self.image.get_width() / 2
        self.y = Y - self.image.get_height() / 2
        self.active = True

class Bullet_e:
    def __init__(self):
        # 初始化成员变量，x，y，image
        self.x = 0
        self.y = -3
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.active = False

    def move(self):
        # 激活状态下，向上移动
        if self.active:
            self.y += 1
        # 当飞出屏幕，就设为不激活
        #if self.y < 0:
            #self.active = False

    def restart(self, X, Y):
        # 处理子弹的运动
        self.x = X - self.image.get_width() / 2
        self.y = Y - self.image.get_height() / 2
        self.active = True

class Enemy:
    def restart(self):
        #重塑敌机位置和速度
        self.x = random.randint(50, 400)
        self.y = random.randint(-200, -50)
        self.speed = random.random() + 0.1

    def __init__(self):
        #初始化
        self.restart()
        self.image = pygame.image.load('enemy.png').convert_alpha()

    def move(self):
        if self.y < 800:
            #向下移动
            self.y += self.speed
        else:
            #重置
            self.restart()

    def move_e(self):
        if self.y < 800:
            #向下移动
            self.y += 0.1
        else:
            #重置
            self.restart()


def checkHit(enemy, bullet):
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width()) and (bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height()):
        enemy.restart()
        bullet.active = False
        return True
    return False

def checkCrash(enemy, plane):
    if (plane.x + 0.7*plane.image.get_width() > enemy.x) and (plane.x + 0.3*plane.image.get_width() < enemy.x + enemy.image.get_width()) and (plane.y + 0.7*plane.image.get_height() > enemy.y) and (plane.y + 0.3*plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False

def checkHitCrash(plane, bullet):
    if (bullet.x > plane.x and bullet.x < plane.x + plane.image.get_width()) and (bullet.y > plane.y and bullet.y < plane.y + plane.image.get_height()):
        return True
    return False

pygame.init()
screen = pygame.display.set_mode((450, 800), 0, 32)
pygame.display.set_caption("plane")
background = pygame.image.load('back.jpg').convert()
plane = pygame.image.load('plane.png').convert_alpha()
plane = Plane()
bullet_left = Bullet()
bullet_right = Bullet()
enemy = Enemy()
# 创建子弹的list
bullet_left = []
bullet_right = []
bullet_e = []
# 向list中添加5发子弹
for i in range(5):
    bullet_left.append(Bullet())
for i in range(5):
    bullet_right.append(Bullet())
for i in range(5):
    bullet_e.append(Bullet_e())
# 子弹总数
count_lb = len(bullet_left)
count_rb = len(bullet_right)
count_e = len(bullet_e)
# 即将激活的子弹序号
index_lb = 0
index_rb = 0
index_e = 0
# 发射子弹的间隔
interval_lb = 0
interval_rb = 0
interval_e = 0
enemies = []
for i in range(5):
    enemies.append(Enemy())
enemy = Enemy()
gameover = False
score = 0
font = pygame.font.Font(None, 32)

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            # 键盘有按下？
            if event.key == K_LEFT:
                # 按下的是左方向键的话，把x坐标减一
                plane.move_x = -1
            elif event.key == K_RIGHT:
                # 右方向键则加一
                plane.move_x = 1
            elif event.key == K_UP:
                # 类似了
                plane.move_y = -1
            elif event.key == K_DOWN:
                plane.move_y = 1
        elif event.type == KEYUP:
            # 如果用户放开了键盘，图就不要动了
            plane.move_x = 0
            plane.move_y = 0

    # 计算出新的坐标
    plane.move()
    screen.blit(background, (0, 0))
    # 发射间隔递减
    interval_lb -= 1
    interval_rb -= 1
    # 当间隔小于0时，激活一发子弹
    if interval_lb < 0:
        bullet_left[index_lb].restart(plane.x + 18,plane.y + 10)
        # 重置间隔时间
        interval_lb = 100
        # 子弹序号周期性递增
        index_lb = (index_lb + 1) % count_lb
    # 判断每个子弹的状态
    for b in bullet_left:
        # 处于激活状态的子弹，移动位置并绘制
        if b.active:
            for e in enemies:
                if checkHit(e, b):
                    score += 100
            b.move()
            screen.blit(b.image, (b.x, b.y))
    if interval_rb < 0:
        bullet_right[index_rb].restart(plane.x + 70,plane.y+10)
        # 重置间隔时间
        interval_rb = 100
        # 子弹序号周期性递增
        index_rb = (index_rb + 1) % count_rb
    # 判断每个子弹的状态
    for b in bullet_right:
        # 处于激活状态的子弹，移动位置并绘制
        if b.active:
            for e in enemies:
                if checkHit(e, b):
                    score += 100
            b.move()
            screen.blit(b.image, (b.x, b.y))
    screen.blit(plane.image, (plane.x, plane.y))
    for e in enemies:
        # 如果撞上敌机，设gameover为True
        if checkCrash(e, plane):
            gameover = True
        e.move()
        screen.blit(e.image, (e.x, e.y))
    # 把子弹画到屏幕上
    text = font.render("Socre: %d" % score, 1, (0, 0, 0))
    screen.blit(text, (0, 0))
    if (score >= 1000):
        if (score % 100 == 0):
            interval_e -= 1
            if interval_e < 0:
                bullet_e[index_e].restart(enemy.x +30, enemy.y +10)
                # 重置间隔时间
                interval_e = 100
                # 子弹序号周期性递增
                index_e = (index_e + 1) % count_e
            for b in bullet_e:
                # 处于激活状态的子弹，移动位置并绘制
                if b.active:
                    if checkHitCrash(plane, b):
                        gameover = True
                    b.move()
                    screen.blit(b.image, (b.x, b.y))
                    enemy.move_e()
            screen.blit(enemy.image, (enemy.x, enemy.y))
    pygame.display.update()
    sleep(0.000005)
    while (gameover):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.blit(background, (0, 0))
        fontover = pygame.font.Font(None,64)
        text = fontover.render("Socre: %d" % score, 1, (0, 0, 0))
        screen.blit(text, (120,350))
        pygame.display.update()
        if gameover and event.type == pygame.MOUSEBUTTONUP:
            # 重置游戏
            plane.restart(180, 500)
            for e in enemies:
                e.restart()
            for b in bullet_right:
                b.active = False
            for b in bullet_left:
                b.active = False
            score = 0
            gameover = False










