import pygame
from button import StartGameButton, ExitGameButton


class Background:
    def __init__(self, game):
        # 获取游戏窗口屏幕
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # 获取游戏
        self.game = game

        # 加载图片并初始化图片的坐标
        self.image1 = pygame.image.load("img/bg.png").convert()
        self.image2 = pygame.image.load("img/bg2.png").convert()
        self.image3 = pygame.image.load("img/bg2.png").convert()
        self.image_rect1 = self.image1.get_rect()
        self.image_rect1.midbottom = self.screen_rect.midbottom
        self.image_rect2 = self.image2.get_rect()
        self.image_rect2.y = self.screen_rect.height - self.image_rect1.height
        self.image_rect3 = self.image3.get_rect()
        self.image_rect3.y = self.image_rect2.y - self.image_rect3.height

        # 设置image3翻转
        self.image3 = pygame.transform.flip(self.image3, True, False)

        # 设置背景移动的速度
        self.image_speed = 1

        # 设置y存储图片位置
        self.y1 = float(self.image_rect1.y)
        self.y2 = float(self.image_rect2.y)
        self.y3 = float(self.image_rect3.y)

        # 设置主菜单的图片并设置其初始位置
        self.main_bg_image01 = pygame.image.load("img/space_bg02.png").convert()
        self.main_bg_image02 = pygame.image.load("img/space_bg03.png").convert()
        self.main_bg_image01_rect = self.main_bg_image01.get_rect()
        self.main_bg_image02_rect = self.main_bg_image02.get_rect()
        self.main_bg_image01_rect.x = 0
        self.main_bg_image01_rect.y = 0
        self.main_bg_image02_rect.x = 0
        self.main_bg_image02_rect.y = self.main_bg_image01_rect.y - \
                                      self.main_bg_image01_rect.height

        # 存储主菜单页面的背景
        self.main_bg_image01_y = float(self.main_bg_image01_rect.y)
        self.main_bg_image02_y = float(self.main_bg_image02_rect.y)

        # 设置主菜单的标题
        self.main_bg_title_image = pygame.image.load("img/title.png").convert_alpha()
        self.main_bg_title_image_rect = self.main_bg_title_image.get_rect()
        self.main_bg_title_image_rect.centerx = self.screen_rect.centerx
        self.main_bg_title_image_rect.y = self.screen_rect.centery - self.main_bg_title_image_rect.height * 3

        # 初始化按钮
        self.start_game_button = StartGameButton(self.game)
        self.exit_game_button = ExitGameButton(self.game)
        self.start_game_button.start_game_button_rect.centerx = self.screen_rect.centerx
        self.start_game_button.start_game_button_rect.y = self.screen_rect.centery + \
                                                          self.start_game_button.start_game_button_rect.height
        self.exit_game_button.exit_game_button_rect.centerx = self.screen_rect.centerx
        self.exit_game_button.exit_game_button_rect.y = self.screen_rect.centery + \
                                                        self.exit_game_button.exit_game_button_rect.height * 3
        # print("start_game_button_x:", self.start_game_button.start_game_button_rect.x)
        # print("start_game_button_y:", self.start_game_button.start_game_button_rect.y)
        # print("exit_game_button_x:", self.exit_game_button.exit_game_button_rect.x)
        # print("exit_game_button_y:", self.exit_game_button.exit_game_button_rect.y)

        # 初始化太空背景
        self.space_image01 = pygame.image.load("img/space_bg01.png").convert()
        self.space_image02 = pygame.image.load("img/space_bg02.png").convert()
        self.space_image03 = pygame.image.load("img/space_bg03.png").convert()
        self.space_image01_rect = self.space_image01.get_rect()
        self.space_image02_rect = self.space_image02.get_rect()
        self.space_image03_rect = self.space_image03.get_rect()
        self.space_image01_rect.center = self.screen_rect.center
        self.space_image02_rect.centerx = self.screen_rect.centerx
        self.space_image02_rect.y = self.space_image01_rect.y - self.space_image02_rect.height
        self.space_image03_rect.centerx = self.screen_rect.centerx
        self.space_image03_rect.y = self.space_image02_rect.y - self.space_image03_rect.height

        # 存储y位置
        self.space_image01_y = float(self.space_image01_rect.y)
        self.space_image02_y = float(self.space_image02_rect.y)
        self.space_image03_y = float(self.space_image03_rect.y)

    # 绘制背景
    def blit_bg(self):
        if self.game.stats.game_active == "start_game" and self.game.stats.fly_distance < 3000:
            self.screen.blit(self.image1, self.image_rect1)
            self.screen.blit(self.image2, self.image_rect2)
            self.screen.blit(self.image3, self.image_rect3)
        if self.game.stats.game_active == "start_game" and self.game.stats.fly_distance >= 3000:
            self.screen.blit(self.space_image01, self.space_image01_rect)
            self.screen.blit(self.space_image02, self.space_image02_rect)
            self.screen.blit(self.space_image03, self.space_image03_rect)
        if self.game.stats.game_active == "main_menu":
            self.screen.blit(self.main_bg_image01, self.main_bg_image01_rect)
            self.screen.blit(self.main_bg_image02, self.main_bg_image02_rect)
            self.screen.blit(self.main_bg_title_image, self.main_bg_title_image_rect)
            self.start_game_button.blit_start_game_button()
            self.exit_game_button.blit_exit_game_button()

    # 更新背景并绘制背景
    def update(self):
        if self.game.stats.game_active == "start_game" and self.game.stats.fly_distance < 3000:
            self.y1 += self.image_speed
            self.image_rect1.y = self.y1
            self.y2 += self.image_speed
            self.image_rect2.y = self.y2
            self.y3 += self.image_speed
            self.image_rect3.y = self.y3
            if self.image_rect2.top >= self.screen_rect.bottom:
                self.y2 = -self.screen_rect.height
            if self.image_rect3.top >= self.screen_rect.bottom:
                self.y3 = -self.screen_rect.height
            # print(self.game.stats.game_active)
            # 飞行距离持续增加
            self.game.stats.fly_distance += 0.5

        if self.game.stats.game_active == "start_game" and self.game.stats.fly_distance >= 3000:
            self.space_image01_y += self.image_speed
            self.space_image01_rect.y = self.space_image01_y
            self.space_image02_y += self.image_speed
            self.space_image02_rect.y = self.space_image02_y
            self.space_image03_y += self.image_speed
            self.space_image03_rect.y = self.space_image03_y
            if self.space_image02_rect.top >= self.screen_rect.bottom:
                self.space_image02_y = -self.screen_rect.height
            if self.space_image03_rect.top >= self.screen_rect.bottom:
                self.space_image03_y = -self.screen_rect.height
            # 飞行距离持续增加
            self.game.stats.fly_distance += 0.5

        if self.game.stats.game_active == "main_menu":
            self.main_bg_image01_y += self.image_speed
            self.main_bg_image01_rect.y = self.main_bg_image01_y
            self.main_bg_image02_y += self.image_speed
            self.main_bg_image02_rect.y = self.main_bg_image02_y
            if self.main_bg_image01_rect.top >= self.screen_rect.bottom:
                self.main_bg_image01_y = -self.screen_rect.height
            if self.main_bg_image02_rect.top >= self.screen_rect.bottom:
                self.main_bg_image02_y = -self.screen_rect.height

        # 绘制背景
        self.blit_bg()
