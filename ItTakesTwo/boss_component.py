import pygame
import random

from pygame.sprite import Sprite

from boss import Boss
from spritesheet import SpriteSheet
from enemy_bullet import EnemyBullet


class BossComponent(Sprite):
    def __init__(self, game):
        super().__init__()

        self.game = game
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.boss = Boss(self.game)

        # 设置敌方飞船图片
        self.img = "img/boss_component-Sheet.png"
        self.all_frames = self.load_frames_from_sheet()
        self.rect = self.all_frames.get("idle")[0].get_rect()
        self.rect.x = random.randint(1, self.screen_rect.width - self.rect.width)
        self.rect.y = -self.rect.height

        # 方向
        number = random.randint(1, 3)
        if number == 1:
            self.direction = 1
        else:
            self.direction = -1

        # 速度
        self.enemy_speed_x = random.randint(1, 11) / 10
        self.enemy_speed_y = 0.2

        # 存储飞船坐标
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 设置敌方子弹发射冷却时间
        self.enemy_fire_cd = 1000
        self.enemy_fire_last_updated = 0

        # 设置飞船动画速度
        self.enemy_frame_speed = 100
        # 初始化当前图片
        self.current_image = self.all_frames.get("idle")[0]
        self.image = self.current_image

        # 设置初始状态
        self.state = "idle"

        # 设置敌方子弹的编组
        self.enemy_bullets = pygame.sprite.Group()

        # 设置敌方血量
        self.enemy_life = 2000

        # 设置敌方分数
        self.enemy_score = 500

        # 设置帧数
        self.current_frame = 0
        self.frames = []
        self.last_updated = 0

        # 开火标识符
        self.fire_identifier = True

        # 无敌标识符
        self.invincible_identifier = True

        # 设置boss标识符
        self.is_boss = True
        self.is_boss_component = True

    def enemy_fire(self):
        if self.fire_identifier:
            now = pygame.time.get_ticks()
            if now - self.enemy_fire_last_updated > self.enemy_fire_cd:
                self.enemy_fire_last_updated = now
                new_enemy_bullet = EnemyBullet(self.game)
                new_enemy_bullet.rect.midbottom = self.rect.midbottom
                self.game.enemy_bullets.add(new_enemy_bullet)

    def load_frames_from_sheet(self):
        my_sprite_sheet = SpriteSheet(self.img)
        # print(my_sprite_sheet.data)
        idle_frames = [my_sprite_sheet.parse_sprite(f"idle{i}") for i in range(0, 5)]
        all_frames = {
            "idle": idle_frames
        }
        return all_frames

    def update(self):
        if self.rect.y < self.boss.rect.height:
            self.y += self.enemy_speed_y
            self.rect.y = self.y
        else:
            self.fire_identifier = True
            self.invincible_identifier = False
        self.x += self.enemy_speed_x * self.direction
        self.rect.x = self.x
        # print("x:", self.rect.x, "y:", self.rect.y)

        # 更新x、y速度改变方向
        # self.change_speed()

        # 更新状态
        self.handle_state()

        # 更新动画
        self.animate()

        # 当敌方移至边缘则消除
        if self.rect.right >= self.screen_rect.right or \
                self.rect.left <= self.screen_rect.left:
            self.direction = -self.direction
            # print("已消除")

        # 敌方发射子弹
        self.enemy_fire()

    def handle_state(self):
        if self.state == "idle":
            self.frames = self.all_frames.get("idle")

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > self.enemy_frame_speed:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.current_image = self.frames[self.current_frame]
            self.image = self.current_image
