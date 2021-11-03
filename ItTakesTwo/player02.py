from player import Player


class Player02(Player):
    def __init__(self, game):
        super().__init__(game)

        # 设置飞船的图片
        self.img = "img/Airship02-Sheet.png"
        self.all_frames = self.load_frames_from_sheet()
        self.rect = self.all_frames.get("idle")[0].get_rect()

        # 设置飞船的初始位置
        self.rect.centerx = self.screen_rect.centerx + self.rect.width * 2
        self.rect.bottom = self.screen_rect.bottom

    def reset_player(self):
        self.rect.centerx = self.screen_rect.centerx + self.rect.width * 2
        self.rect.bottom = self.screen_rect.bottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.player_life = 100
        self.is_survival = True
