import pygame
from pygame.sprite import Sprite


class EnemyBullet(Sprite):
    def __init__(self, game):
        # 初始化基类
        super().__init__()

        # 获取游戏屏幕窗口
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # 加载图片并初始化图片位置
        self.image = pygame.image.load("img/enemy_bullet.png")
        self.rect = self.image.get_rect()

        # x、y存储位置
        # self.x = float(self.rect.x)
        # self.y = float(self.rect.y)

        # 设置子弹速度
        self.bullet_speed = 5

    def update(self):
        # 设置子弹垂直向下飞行
        self.rect.y += self.bullet_speed

        # 判断子弹是否到达底部
        self.check_bullet_edge()

    def check_bullet_edge(self):
        if self.rect.top > self.screen_rect.bottom:
            self.kill()
            # print("已删除")
