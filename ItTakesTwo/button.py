import pygame


class Button:
    def __init__(self, game):
        # 获取屏幕窗口大小
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # 获取游戏
        self.game = game


class PauseButton(Button):
    def __init__(self, game):
        # 获取屏幕窗口大小
        super().__init__(game)

        # 获取暂停按钮图片并初始化位置
        self.image = pygame.image.load("img/pause.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_rect.width - self.rect.width - 5
        self.rect.y = self.screen_rect.y + 20

    def blit_pause_button(self):
        self.screen.blit(self.image, self.rect)


class StartButton(Button):
    def __init__(self, game):
        # 初始化
        super().__init__(game)

        # 获取图片
        self.pause_start_button_image = pygame.image.load("img/start_button.png").convert_alpha()
        self.pause_start_button_image_rect = self.pause_start_button_image.get_rect()
        self.pause_start_button_image_rect.x = 84
        self.pause_start_button_image_rect.y = 323

    def blit_start_button(self):
        self.screen.blit(self.pause_start_button_image, self.pause_start_button_image_rect)


class HomeButton(Button):
    def __init__(self, game):
        # 初始化
        super().__init__(game)

        # 获取图片
        self.pause_home_button_image = pygame.image.load("img/home_button.png").convert_alpha()
        self.pause_home_button_image_rect = self.pause_home_button_image.get_rect()
        self.pause_home_button_image_rect.x = 212
        self.pause_home_button_image_rect.y = 323

    def blit_home_button(self):
        self.screen.blit(self.pause_home_button_image, self.pause_home_button_image_rect)


class BackButton(Button):
    def __init__(self, game):
        # 初始化
        super().__init__(game)

        # 获取图片
        self.back_button_image = pygame.image.load("img/back_button.png").convert_alpha()
        self.back_button_image_rect = self.back_button_image.get_rect()
        self.back_button_image_rect.x = 84
        self.back_button_image_rect.y = 323

    def blit_back_button(self):
        self.screen.blit(self.back_button_image, self.back_button_image_rect)

class StartGameButton(Button):
    def __init__(self, game):
        # 初始化
        super().__init__(game)

        # 获取图片
        self.start_game_button_image = pygame.image.load("img/start_game.png").convert_alpha()
        self.start_game_button_rect = self.start_game_button_image.get_rect()
        self.start_game_button_rect.x = 105
        self.start_game_button_rect.y = 370

    def blit_start_game_button(self):
        self.screen.blit(self.start_game_button_image, self.start_game_button_rect)



class ExitGameButton(Button):
    def __init__(self, game):
        # 初始化
        super().__init__(game)

        # 获取图片
        self.exit_game_button_image = pygame.image.load("img/exit_game.png").convert_alpha()
        self.exit_game_button_rect = self.exit_game_button_image.get_rect()
        self.exit_game_button_rect.x = 105
        self.exit_game_button_rect.y = 470

    def blit_exit_game_button(self):
        self.screen.blit(self.exit_game_button_image, self.exit_game_button_rect)
