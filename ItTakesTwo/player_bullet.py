import pygame
from pygame.sprite import Sprite


class PlayerBullet(Sprite):
    def __init__(self, game, player):
        # 初始化Sprite
        super().__init__()

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # 加载图片并设置初始位置为飞船的正上方
        self.image = pygame.image.load('img/player_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.midtop = player.rect.midtop

        # x、y储存子弹位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 设置子弹的速度
        self.bullet_speed = 7

    def update(self):
        # 暂时设置子弹垂直向上飞行
        self.y -= self.bullet_speed
        self.rect.y = self.y
        # 判断子弹是否到达顶部
        self.check_bullet_edge()

    # 判断子弹是否达到顶部
    def check_bullet_edge(self):
        if self.rect.bottom <= self.screen_rect.top:
            self.kill()
            # print("已删除")
