import pygame
import pygame.font

from boss_component import BossComponent
from button import StartButton, HomeButton, BackButton, PauseButton
from boss import Boss


class GameUI:
    def __init__(self, game):
        # 获取游戏窗口屏幕
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # 获取游戏
        self.game = game

        # 初始化UI
        self.image_ui = pygame.image.load("img/player_ui.png").convert_alpha()
        self.image_ui_rect = self.image_ui.get_rect()
        self.image_ui_rect.x = 5
        self.image_ui_rect.y = 20
        self.image_ui02 = pygame.image.load("img/player_ui02.png").convert_alpha()
        self.image_ui02_rect = self.image_ui02.get_rect()
        self.image_ui02_rect.x = self.image_ui_rect.width + 10
        self.image_ui02_rect.y = 20

        # 获取玩家以及血量
        self.player01_life = self.game.player.player_life
        self.player02_life = self.game.player02.player_life
        self.player01_life_rect = None
        self.player02_life_rect = None
        self.life_color = (176, 19, 19)

        # 获取暂停页面以及按钮并初始化位置
        self.pause_menu_image = pygame.image.load('img/pause_menu_ui.png').convert_alpha()
        self.pause_menu_image_rect = self.pause_menu_image.get_rect()
        self.pause_menu_image_rect.center = self.screen_rect.center

        # 初始化按钮并初始化位置
        self.start_button = StartButton(self.game)
        self.home_button = HomeButton(self.game)
        self.start_button.pause_start_button_image_rect.x = self.pause_menu_image_rect.centerx - \
            self.start_button.pause_start_button_image_rect.height * 1.5
        self.start_button.pause_start_button_image_rect.y = self.pause_menu_image_rect.y + \
            self.pause_menu_image_rect.height - \
            self.start_button.pause_start_button_image_rect.height * 1.5
        self.home_button.pause_home_button_image_rect.x = self.pause_menu_image_rect.centerx + \
            self.home_button.pause_home_button_image_rect.width // 2
        self.home_button.pause_home_button_image_rect.y = self.pause_menu_image_rect.y + \
            self.pause_menu_image_rect.height - \
            self.home_button.pause_home_button_image_rect.height * 1.5

        # print(self.start_button.pause_start_button_image_rect.x)
        # print(self.start_button.pause_start_button_image_rect.y)
        # print(self.home_button.pause_home_button_image_rect.x)
        # print(self.home_button.pause_home_button_image_rect.y)

        # 加载游戏结束UI界面并初始化位置
        self.game_over_image = pygame.image.load("img/game_over_ui.png").convert_alpha()
        self.game_over_image_rect = self.game_over_image.get_rect()
        self.game_over_image_rect.center = self.screen_rect.center

        # 初始化结束UI按钮并初始化位置
        self.back_button = BackButton(self.game)
        self.back_button.back_button_image_rect.x = self.game_over_image_rect.centerx - \
            self.back_button.back_button_image_rect.width * 1.5
        self.back_button.back_button_image_rect.y = self.game_over_image_rect.y + \
            self.game_over_image_rect.height - \
            self.back_button.back_button_image_rect.height * 1.5

        # 初始化文字模块
        pygame.font.init()

        # 初始化游戏的文字
        self.game_font = pygame.font.Font("font/方正像素12.TTF", 12)

        # 设置文字的颜色
        self.text_color = (255, 255, 255)
        self.red_color = (255, 0, 0)

        # 初始化按钮
        self.pause_button = PauseButton(self.game)

        # 初始化分数图片
        self.score_image = None
        self.score_image_rect = None
        self.high_score_image = None
        self.high_score_image_rect = None

        # 初始化文字图片
        self.msg_image = None
        self.msg_image_rect = None

    # 绘制UI
    def blit_ui(self):
        if self.game.stats.game_active == "start_game":
            pygame.draw.rect(self.screen, self.life_color, self.player01_life_rect)
            pygame.draw.rect(self.screen, self.life_color, self.player02_life_rect)
            self.screen.blit(self.image_ui, self.image_ui_rect)
            self.screen.blit(self.image_ui02, self.image_ui02_rect)
            self.prep_score()
            self.prep_high_score()
            self.prep_msg()
            # self.prep_fly_distance()
            # print("绘制")
        if self.game.stats.game_active == "game_over":
            pygame.draw.rect(self.screen, self.life_color, self.player01_life_rect)
            pygame.draw.rect(self.screen, self.life_color, self.player02_life_rect)
            self.screen.blit(self.image_ui, self.image_ui_rect)
            self.screen.blit(self.image_ui02, self.image_ui02_rect)
            self.screen.blit(self.game_over_image, self.game_over_image_rect)
            self.back_button.blit_back_button()
            self.home_button.blit_home_button()
            # print("绘制")
        if self.game.stats.game_active == "pause_game":
            self.screen.blit(self.pause_menu_image, self.pause_menu_image_rect)
            self.start_button.blit_start_button()
            self.home_button.blit_home_button()
            # print("绘制")

    # 更新UI并绘制UI
    def update(self):
        if self.game.stats.game_active == "start_game":
            # 检测玩家血量
            self.player01_life = self.game.player.player_life
            self.player02_life = self.game.player02.player_life

            # 绘制血量
            self.player01_life_rect = pygame.Rect(
                self.image_ui_rect.x + 48,
                self.image_ui_rect.y + 9,
                self.player01_life,
                16
            )
            self.player02_life_rect = pygame.Rect(
                self.image_ui02_rect.x + 48,
                self.image_ui02_rect.y + 9,
                self.player02_life,
                16
            )

        # 绘制UI
        self.blit_ui()

    def prep_score(self):
        """将得分转化被已付渲染的图像"""
        rounded_score = round(self.game.stats.score, -1)
        msg = "分数: "
        score_str = msg + "{:,}".format(rounded_score)
        self.score_image = self.game_font.render(score_str, True, self.text_color)
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 5
        self.score_image_rect.top = self.pause_button.rect.bottom + 20
        self.screen.blit(self.score_image, self.score_image_rect)

    def prep_high_score(self):
        """将得分转化被已付渲染的图像"""
        rounded_high_score = round(self.game.stats.high_score, -1)
        msg = "历史最高分数: "
        score_str = msg + "{:,}".format(rounded_high_score)
        self.high_score_image = self.game_font.render(score_str, True, self.text_color)
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.right = self.screen_rect.right - 5
        self.high_score_image_rect.top = self.score_image_rect.bottom + 20
        if self.game.stats.high_score < self.game.stats.score:
            self.game.stats.high_score = self.game.stats.score
        self.screen.blit(self.high_score_image, self.high_score_image_rect)

    # def prep_fly_distance(self):
    #     """将得分转化被已付渲染的图像"""
    #     rounded_fly_distance = round(self.game.stats.fly_distance)
    #     msg = "飞行距离: "
    #     fly_distance_str = msg + "{:,}".format(rounded_fly_distance)
    #     self.fly_distance_image = self.game_font.render(fly_distance_str, True, self.text_color)
    #     self.fly_distance_image_rect = self.fly_distance_image.get_rect()
    #     self.fly_distance_image_rect.right = self.screen_rect.right - 5
    #     self.fly_distance_image_rect.top = self.high_score_image_rect.bottom + 20
    #     self.screen.blit(self.fly_distance_image, self.fly_distance_image_rect)

    def prep_msg(self):
        msg1 = "你感到一种邪恶的存在注视着你。。。"
        msg2 = "你感觉周围的空气变得寒冷了。。。"
        msg3 = "领域被切换了!"
        rounded_fly_distance = round(self.game.stats.fly_distance)
        # print(rounded_fly_distance)
        # 大概一分钟后显示文字, 持续十秒左右
        if 2000 < rounded_fly_distance < 2200:
            self.blit_msg_image(msg1)
        if 2500 < rounded_fly_distance < 2700:
            self.blit_msg_image(msg2)
        if 3000 < rounded_fly_distance < 3200:
            self.blit_msg_image(msg3)
        if rounded_fly_distance == 3500:
            enemy = Boss(self.game)
            self.game.enemies.add(enemy)
            for i in range(1):
                enemy = BossComponent(self.game)
                self.game.enemies.add(enemy)

    # 绘制文字图片
    def blit_msg_image(self, msg):
        self.msg_image = self.game_font.render(msg, True, self.red_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.right = self.screen_rect.right - 5
        self.msg_image_rect.top = self.high_score_image_rect.bottom + 20
        self.screen.blit(self.msg_image, self.msg_image_rect)
