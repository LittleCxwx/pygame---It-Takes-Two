import pygame
import random
from pygame.sprite import Sprite
from spritesheet import SpriteSheet
from enemy_bullet import EnemyBullet


class Enemy(Sprite):
    def __init__(self, game):
        # 初始化基类
        super().__init__()

        # 获取游戏窗口屏幕
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置敌方飞船图片
        self.img = "img/enemy01-Sheet.png"
        self.all_frames = self.load_frames_from_sheet()
        self.rect = self.all_frames.get("idle")[0].get_rect()

        # 设置敌方飞船的初始位置
        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = -self.rect.height

        # 存储飞船坐标
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 设置移动速度
        self.enemy_speed_x = 0
        self.enemy_speed_y = 2

        # 改变速度的间隔时间
        self.chenge_speed_cd = 2000
        self.last_speed_update = 0

        # 设置飞船改变速度的值
        self.enemy_change_speed_x = 0.7
        self.enemy_change_speed_y = 0.2

        # 设置飞船动画速度
        self.enemy_frame_speed = 100

        # 设置帧数
        self.current_frame = 0
        self.frames = []
        self.last_updated = 0

        # 初始化当前图片
        self.current_image = self.all_frames.get("idle")[0]
        self.image = self.current_image

        # 设置初始状态
        self.state = "idle"

        # 设置敌方子弹的编组
        self.enemy_bullets = pygame.sprite.Group()

        # 设置敌方子弹发射冷却时间
        self.enemy_fire_cd = 2000
        self.enemy_fire_last_updated = 0

        # 设置敌方血量
        self.enemy_life = 30

        # 设置boss标识符
        self.is_boss = False
        self.is_boss_component = False
        self.invincible_identifier = False

    def update(self):
        self.y += self.enemy_speed_y
        self.x += self.enemy_speed_x
        self.rect.y = self.y
        self.rect.x = self.x
        # print("x:", self.rect.x, "y:", self.rect.y)

        # 更新x、y速度改变方向
        # self.change_speed()

        # 更新状态
        self.handle_state()

        # 更新动画
        self.animate()

        # 当敌方移至边缘则消除
        if self.rect.top >= self.screen_rect.bottom or \
                self.rect.left >= self.screen_rect.right or \
                self.rect.right <= self.screen_rect.left:
            self.kill()
            # print("已消除")

        # 敌方发射子弹
        self.enemy_fire()

        # 绘制敌方子弹
        # self.enemy_bullets.draw(self.screen)

        # 更新敌方子弹
        # self.enemy_bullets.update()

    def enemy_fire(self):
        now = pygame.time.get_ticks()
        if now - self.enemy_fire_last_updated > self.enemy_fire_cd:
            self.enemy_fire_last_updated = now
            new_enemy_bullet = EnemyBullet(self.game)
            new_enemy_bullet.rect.midbottom = self.rect.midbottom

            self.game.enemy_bullets.add(new_enemy_bullet)

    def load_frames_from_sheet(self):
        my_sprite_sheet = SpriteSheet(self.img)
        idle_frames = [my_sprite_sheet.parse_sprite(f"idle{i}") for i in range(0, 2)]
        all_frames = {
            "idle": idle_frames
        }
        return all_frames

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > self.enemy_frame_speed:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.current_image = self.frames[self.current_frame]
            self.image = self.current_image

    def handle_state(self):
        if self.state == "idle":
            self.frames = self.all_frames.get("idle")

    def change_speed(self):
        now = pygame.time.get_ticks()
        if now - self.last_speed_update > self.chenge_speed_cd:
            self.last_speed_update = now
            self.enemy_speed_x += self.enemy_change_speed_x
            self.enemy_speed_y -= self.enemy_change_speed_y
            # print("change")
