import pygame
import json

class GameStats:
    """统计游戏信息"""

    def __init__(self, game):
        # 获取游戏
        self.game = game

        # 获取设置类
        self.setting = self.game.setting

        # 初始化分数为0
        self.score = 0

        # 获取json文件
        self.json_filename = "json/game_stats.json"
        with open(self.json_filename) as f:
            self.data = json.load(f)
        # 关闭文件
        f.close()

        # 初始化最高分数
        self.high_score = int(self.data["high_score"])

        # 初始化飞机的飞行距离
        self.fly_distance = 0

        # 初始化游戏状态
        self.game_active = "main_menu"

    # 重置游戏数值
    def reset_stats(self):
        self.score = 0
        self.fly_distance = 0
        now = pygame.time.get_ticks()
        self.game.create_enemy_last_updated = self.setting.first_enemy_appear_cd + now
