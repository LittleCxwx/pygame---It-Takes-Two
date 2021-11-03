import pygame
from pygame.sprite import Sprite
from spritesheet import SpriteSheet


class Prop(Sprite):
    def __init__(self, game):
        super().__init__()

        # 获取游戏屏幕
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置道具图片
        self.img = "img/prop-Sheet.png"
        self.all_frames = self.load_frames_from_sheet()
        self.rect = self.all_frames.get("idle")[0].get_rect()

        # 设置初始位置
        self.rect.x = 0
        self.rect.y = -self.rect.height

        # 存储道具的坐标
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 道具的移动速度
        self.prop_speed_x = 1
        self.prop_speed_y = 0.5

        # 设置道具方向, 向左运动为1, 向右运动为-1
        self.direction = 1

        # 设置动画速度
        self.prop_frame_speed = 100

        # 设置帧数
        self.current_frame = 0
        self.frames = []
        self.last_updated = 0

        # 初始化当前图片
        self.current_image = self.all_frames.get("idle")[0]
        self.image = self.current_image

        # 设置初始状态
        self.state = "idle"

    def update(self):
        self.x += self.direction * self.prop_speed_x
        self.y += self.prop_speed_y
        self.rect.x = self.x
        self.rect.y = self.y

        # 判断道具触碰到边缘(非底部), 若触碰, 则改变方向
        if self.rect.left <= self.screen_rect.left or self.rect.right >= self.screen_rect.right:
            self.direction = -self.direction

        # 当道具触碰到底部, 则消除
        if self.rect.top >= self.screen_rect.bottom:
            self.kill()
            # print("已消除")

        # 更新状态
        self.handle_state()

        # 更新动画
        self.animate()

    def load_frames_from_sheet(self):
        my_sprite_sheet = SpriteSheet(self.img)
        idle_frames = [my_sprite_sheet.parse_sprite(f"idle{i}") for i in range(0, 22)]
        all_frames = {
            "idle": idle_frames
        }
        return all_frames

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > self.prop_frame_speed:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.current_image = self.frames[self.current_frame]
            self.image = self.current_image

    def handle_state(self):
        if self.state == "idle":
            self.frames = self.all_frames.get("idle")
