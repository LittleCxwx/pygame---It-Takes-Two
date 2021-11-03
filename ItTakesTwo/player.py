import pygame
from pygame.sprite import Sprite
from spritesheet import SpriteSheet


class Player(Sprite):
    def __init__(self, game):
        """初始化"""
        super().__init__()

        # 获取游戏窗口的屏幕及高宽
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        '''
        # 加载并优化飞船图片
        self.image = pygame.image.load("img/Airship-Sheet.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        
        # 正常飞船的高宽
        self.ship_width = 48
        self.ship_height = 48
        '''

        # 设置飞船的图片
        self.img = "img/Airship-Sheet.png"
        self.all_frames = self.load_frames_from_sheet()
        self.rect = self.all_frames.get("idle")[0].get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        # 飞船的属性x和y中存储最小值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 设置飞船标识符
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        # 设置飞船移动速度
        self.ship_speed = 5

        # 设置飞船动画速度
        self.ship_frame_speed = 100

        # 初始化当前帧数
        self.current_frame = 0
        self.frames = []
        self.last_updated = 0

        # 初始化当前图片
        self.current_image = self.all_frames.get("idle")[0]

        # 设置初始状态
        self.state = "idle"

        # 设置玩家开火标识符
        self.fire_identifier = False

        # 设置玩家生命值
        self.player_life = 100

        # 设置玩家存活标识符
        self.is_survival = True

    def update(self):
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ship_speed
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ship_speed

        # 更新飞船的rect对象
        self.rect.x = self.x
        self.rect.y = self.y

        # 更新状态
        self.handle_state()

        # 更新动画
        self.animate()

    def blit_me(self):
        self.screen.blit(self.current_image, self.rect)

    def load_frames_from_sheet(self):
        my_sprite_sheet = SpriteSheet(self.img)
        idle_frames = [my_sprite_sheet.parse_sprite(f"idle{i}") for i in range(0, 2)]
        all_frames = {
            "idle": idle_frames
        }
        return all_frames

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > self.ship_frame_speed:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.current_image = self.frames[self.current_frame]

    def handle_state(self):
        if self.state == "idle":
            self.frames = self.all_frames.get("idle")

    def reset_player(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
