import pygame
import json


class SpriteSheet():
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.meta_data = self.filename.replace('png', 'json').replace('img', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        # 创建一个图片对象
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    # 分析精灵表
    def parse_sprite(self, name):
        sprite = self.data["frames"][name]["frame"]
        x, y, w, h = int(sprite["x"]), int(sprite["y"]), int(sprite["w"]), int(sprite["h"])
        image = self.get_sprite(x, y, w, h)
        return image
