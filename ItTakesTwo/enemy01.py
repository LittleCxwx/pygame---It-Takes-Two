from enemy import Enemy


class Enemy01(Enemy):
    def __init__(self, game):
        super().__init__(game)

        # 设置敌方飞船图片
        self.img = "img/enemy01-Sheet.png"
        self.all_frames = self.load_frames_from_sheet()
        self.rect = self.all_frames.get("idle")[0].get_rect()

        # 设置敌方血量
        self.enemy_life = 30

        # 设置敌方分数
        self.enemy_score = 50
