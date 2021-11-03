import pygame

from enemy import Enemy
from enemy_bullet import EnemyBullet


class Enemy02(Enemy):
    def __init__(self, game):
        super().__init__(game)

        # 设置敌方飞船图片
        self.img = "img/enemy02-Sheet.png"
        self.all_frames = self.load_frames_from_sheet()
        self.rect = self.all_frames.get("idle")[0].get_rect()
        
        # 设置敌方血量
        self.enemy_life = 50

        # 设置敌方分数
        self.enemy_score = 100

    def enemy_fire(self):
        now = pygame.time.get_ticks()
        if now - self.enemy_fire_last_updated > self.enemy_fire_cd:
            self.enemy_fire_last_updated = now
            new_enemy_bullet = EnemyBullet(self.game)
            new_enemy_bullet.rect.y = self.rect.bottom - 16
            new_enemy_bullet.rect.x = self.rect.centerx - 17
            self.game.enemy_bullets.add(new_enemy_bullet)
            new_enemy_bullet = EnemyBullet(self.game)
            new_enemy_bullet.rect.y = self.rect.bottom - 16
            new_enemy_bullet.rect.x = self.rect.centerx + 14
            self.game.enemy_bullets.add(new_enemy_bullet)
