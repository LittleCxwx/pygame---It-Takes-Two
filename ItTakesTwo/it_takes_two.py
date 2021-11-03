import sys
import pygame
import random
import json

from button import PauseButton, HomeButton, StartButton, BackButton, StartGameButton, ExitGameButton
from player01 import Player01
from player02 import Player02
from background import Background
from player_bullet import PlayerBullet
from enemy01 import Enemy01
from enemy02 import Enemy02
from setting import Setting
from game_stats import GameStats
from game_ui import GameUI
from prop import Prop


class ItTakesTwo:
    def __init__(self):
        # 初始化pygame
        pygame.init()
        pygame.mixer.init()

        # 初始化游戏帧数, 帧数为60帧
        self.clock = pygame.time.Clock()
        self.fps = 60

        # 初始化设置
        self.setting = Setting()

        # 初始化统计数据
        self.stats = GameStats(self)

        # 设置游戏窗口大小
        self.screen = pygame.display.set_mode((360, 640))

        # 设置游戏窗口名称
        pygame.display.set_caption("It Takes Two")

        # 初始化玩家
        self.player = Player01(self)
        self.player02 = Player02(self)

        # 设置新敌人出现的冷却间隔
        self.create_enemy_cd = 5000
        self.create_enemy_last_updated = self.setting.first_enemy_appear_cd

        # 设置存储敌人的编组
        self.enemies = pygame.sprite.Group()

        # 设置存储子弹的编组
        self.player_bullets = pygame.sprite.Group()

        # 设置敌方子弹编组
        self.enemy_bullets = pygame.sprite.Group()

        # 设置道具的编组
        self.props = pygame.sprite.Group()

        # 设子子弹发射间隔
        self.last_fire = 0
        self.last_fire02 = 0
        self.fire_cd = 100

        # 加载背景图片
        self.bg_image = Background(self)

        # 加载UI
        self.ui_image = GameUI(self)

        # 设置游戏背景音乐
        pygame.mixer.music.load("OST/八仙拳.ogg")
        pygame.mixer.music.set_volume(0.08)
        pygame.mixer.music.play(-1)

        # 设置子弹的音效
        self.fire_sound = pygame.mixer.Sound("OST/fight.wav")
        self.fire_sound.set_volume(0.03)

        # 设置boss无敌状态被击打的音效
        self.hit_invincible_boss_sound = pygame.mixer.Sound("OST/金属敲击.wav")
        self.hit_invincible_boss_sound.set_volume(0.05)

        # 初始化暂停按钮
        self.pause_button = PauseButton(self)
        self.start_button = StartButton(self)
        self.home_button = HomeButton(self)
        self.back_button = BackButton(self)
        self.start_game_button = StartGameButton(self)
        self.exit_game_button = ExitGameButton(self)

        # 设置json文件
        self.json_filename = "json/game_stats.json"

    def run_game(self):
        while True:
            # 设置帧率
            self.clock.tick(self.fps)

            # 检查事件
            self._check_events()

            if self.stats.game_active == "start_game":
                # 创建敌人
                self._create_enemy()

                # 更新游戏
                self.game_update()

            if self.stats.game_active == "pause_game":
                # 游戏屏幕更新
                self.game_update()

            # if self.stats.game_active == "game_over":
            #     # 游戏屏幕更新
            #     self.game_over_screen_update()

            if self.stats.game_active == "main_menu":
                # 游戏屏幕更新
                self.game_update()

            # print(self.stats.game_active)

    def _check_events(self):
        # 获取pygame中内定的事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rewrite_json_file()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    self._check_button_events(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

        # 玩家发射子弹事件
        self.fire_event(self.player, self.player02)

    def rewrite_json_file(self):
        with open(self.json_filename) as f:
            data = json.load(f)
        f.close()
        # print(data["high_score"])
        data["high_score"] = str(self.stats.high_score)
        with open(self.json_filename, "w") as f:
            json.dump(data, f)
        f.close()

    def _check_button_events(self, mouse_pos):
        button_clicked_pause = self.pause_button.rect.collidepoint(mouse_pos)
        button_clicked_start = self.start_button.pause_start_button_image_rect.collidepoint(mouse_pos)
        button_clicked_home = self.home_button.pause_home_button_image_rect.collidepoint(mouse_pos)
        button_clicked_back = self.back_button.back_button_image_rect.collidepoint(mouse_pos)
        button_clicked_start_game = self.start_game_button.start_game_button_rect.collidepoint(mouse_pos)
        button_clicked_exit_game = self.exit_game_button.exit_game_button_rect.collidepoint(mouse_pos)
        if button_clicked_pause and self.stats.game_active == "start_game":
            # 音乐暂停
            pygame.mixer.music.pause()
            # 改变游戏状态
            self.stats.game_active = "pause_game"
        if button_clicked_start and self.stats.game_active == "pause_game":
            # 音乐播放(取消暂停)
            pygame.mixer.music.unpause()
            # 改变游戏状态
            self.stats.game_active = "start_game"
        if button_clicked_home and (self.stats.game_active == "pause_game" or self.stats.game_active == "game_over"):
            # 改变音乐
            pygame.mixer.music.load("OST/八仙拳.ogg")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            # 改变游戏状态
            self.stats.game_active = "main_menu"
        if button_clicked_back and self.stats.game_active == "game_over":
            self.reset_game()
            # 修改游戏状态
            self.stats.game_active = "start_game"
        if button_clicked_start_game and self.stats.game_active == "main_menu":
            # 改变音乐
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.load("OST/8 Bit Adventure.ogg")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            self.reset_game()
            # 改变游戏状态
            self.stats.game_active = "start_game"
        if button_clicked_exit_game and self.stats.game_active == "main_menu":
            self.rewrite_json_file()
            sys.exit()

    def _check_keydown_events(self, event):
        if self.stats.game_active == "start_game":
            if self.player.is_survival:
                if event.key == pygame.K_a:
                    self.player.moving_left = True
                if event.key == pygame.K_d:
                    self.player.moving_right = True
                if event.key == pygame.K_w:
                    self.player.moving_up = True
                if event.key == pygame.K_s:
                    self.player.moving_down = True
                if event.key == pygame.K_SPACE:
                    self.player.fire_identifier = True
            if self.player02.is_survival:
                if event.key == pygame.K_LEFT:
                    self.player02.moving_left = True
                if event.key == pygame.K_RIGHT:
                    self.player02.moving_right = True
                if event.key == pygame.K_UP:
                    self.player02.moving_up = True
                if event.key == pygame.K_DOWN:
                    self.player02.moving_down = True
                if event.key == pygame.K_KP0:
                    self.player02.fire_identifier = True
        if self.stats.game_active == "game_over":
            if event.key == pygame.K_p:
                self.reset_game()
                self.stats.game_active = "start_game"

        if self.stats.game_active == "pause_game":
            if event.key == pygame.K_p:
                pygame.mixer.music.unpause()
                self.stats.game_active = "start_game"

    def _check_keyup_events(self, event):
        if self.player.is_survival:
            if event.key == pygame.K_a:
                self.player.moving_left = False
            if event.key == pygame.K_d:
                self.player.moving_right = False
            if event.key == pygame.K_w:
                self.player.moving_up = False
            if event.key == pygame.K_s:
                self.player.moving_down = False
            if event.key == pygame.K_SPACE:
                self.player.fire_identifier = False
        if self.player02.is_survival:
            if event.key == pygame.K_LEFT:
                self.player02.moving_left = False
            if event.key == pygame.K_RIGHT:
                self.player02.moving_right = False
            if event.key == pygame.K_UP:
                self.player02.moving_up = False
            if event.key == pygame.K_DOWN:
                self.player02.moving_down = False
            if event.key == pygame.K_KP0:
                self.player02.fire_identifier = False

    '''子弹发射事件'''

    def fire_event(self, player, player02):
        # print("player01:", player.fire_identifier, "player02:", player02.fire_identifier)
        if player.fire_identifier:
            self.fire_bullet()
        if player02.fire_identifier:
            self.fire_bullet02()

    '''更新游戏'''

    def game_update(self):
        if self.stats.game_active == "start_game":
            # 屏幕更新
            self.__screen_update()

            # 玩家子弹更新
            self.__player_bullets_update()

            # 玩家更新
            self.__player_update()

            # 敌方子弹更新
            self.__enemy_bullets_update()

            # 敌人更新
            self.__enemy_update()

            # 道具更新
            self.__prop_update()

            # UI 更新
            self.__game_ui_update()

        if self.stats.game_active == "main_menu":
            # 屏幕更新
            self.__screen_update()

        if self.stats.game_active == "pause_game":
            # UI 更新
            self.__game_ui_update()

        # 屏幕刷新
        pygame.display.flip()

    def __prop_update(self):
        self.props.update()
        self.props.draw(self.screen)
        self.__check_prop_player_collisions()

    def __check_prop_player_collisions(self):
        global collisions01, collisions02
        if self.player.is_survival:
            collisions01 = pygame.sprite.spritecollide(
                self.player, self.props, True
            )
        if self.player02.is_survival:
            collisions02 = pygame.sprite.spritecollide(
                self.player02, self.props, True
            )
        if collisions01 and self.player.is_survival:
            self.player.player_life += self.setting.prop_treatment_volume
            if self.player.player_life > 100:
                self.player.player_life = 100
        if collisions02 and self.player02.is_survival:
            self.player02.player_life += self.setting.prop_treatment_volume
            if self.player02.player_life > 100:
                self.player02.player_life = 100

    def __game_ui_update(self):
        self.ui_image.update()
        self.pause_button.blit_pause_button()

    def __enemy_bullets_update(self):
        self.enemy_bullets.update()
        self.enemy_bullets.draw(self.screen)
        # 敌方子弹与玩家碰撞检测
        self.__check_enemy_bullets_player_collisions()

    def __check_enemy_bullets_player_collisions(self):
        global collisions01, collisions02
        if self.player.is_survival:
            collisions01 = pygame.sprite.spritecollide(
                self.player, self.enemy_bullets, True
            )
        if self.player02.is_survival:
            collisions02 = pygame.sprite.spritecollide(
                self.player02, self.enemy_bullets, True
            )
        if collisions01 and self.player.is_survival:
            self.player.player_life -= self.setting.enemy_bullet_damage
            # print("玩家扣除血量")
            if self.player.player_life <= 0:
                self.player.is_survival = False
                self.player.fire_identifier = False
                self.player.moving_down = False
                self.player.moving_up = False
                self.player.moving_left = False
                self.player.moving_right = False
        if collisions02 and self.player02.is_survival:
            self.player02.player_life -= self.setting.enemy_bullet_damage
            # print("玩家扣除血量")
            if self.player02.player_life <= 0:
                self.player02.is_survival = False
                self.player02.fire_identifier = False
                self.player02.moving_down = False
                self.player02.moving_up = False
                self.player02.moving_left = False
                self.player02.moving_right = False
        if not self.player.is_survival and not self.player02.is_survival:
            self.stats.game_active = "game_over"
            # print("GameOver")

    def __enemy_update(self):
        self.enemies.update()
        self.enemies.draw(self.screen)
        self.__check_enemy_player_collisions()

    def __check_enemy_player_collisions(self):
        global collisions01, collisions02
        if self.player.is_survival:
            collisions01 = pygame.sprite.spritecollide(
                self.player, self.enemies, True
            )
        if self.player02.is_survival:
            collisions02 = pygame.sprite.spritecollide(
                self.player02, self.enemies, True
            )
        if collisions01 and self.player.is_survival:
            self.player.player_life -= self.player.player_life
            # print("玩家扣除血量")
            if self.player.player_life <= 0:
                self.player.is_survival = False
                self.player.fire_identifier = False
                self.player.moving_down = False
                self.player.moving_up = False
                self.player.moving_left = False
                self.player.moving_right = False
        if collisions02 and self.player02.is_survival:
            self.player02.player_life -= self.player02.player_life
            # print("玩家扣除血量")
            if self.player02.player_life <= 0:
                self.player02.is_survival = False
                self.player02.fire_identifier = False
                self.player02.moving_down = False
                self.player02.moving_up = False
                self.player02.moving_left = False
                self.player02.moving_right = False

    def __player_update(self):
        if self.player.is_survival:
            self.player.update()
            self.player.blit_me()
        if self.player02.is_survival:
            self.player02.update()
            self.player02.blit_me()

    def __player_bullets_update(self):
        self.player_bullets.update()
        self.player_bullets.draw(self.screen)
        # 玩家子弹与敌方碰撞检测
        self.__check_player_bullets_enemies_collisions()

    def __check_player_bullets_enemies_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.player_bullets, self.enemies, True, False
        )
        if collisions:
            for enemies in collisions.values():
                for enemy in enemies:
                    if not enemy.is_boss:
                        enemy.enemy_life -= self.setting.player_bullet_damage
                        if enemy.enemy_life <= 0:
                            number = random.randint(1, 11)
                            if number == 1:
                                prop = Prop(self)
                                prop.x = enemy.rect.x
                                prop.y = enemy.rect.y
                                self.props.add(prop)
                                # print("创建了一个道具")
                            self.enemies.remove(enemy)

                            self.stats.score += enemy.enemy_score
                            # print("score:", self.stats.score)
                    # 如果敌人是boss并且boss是无敌状态, 则发出别的音效
                    elif enemy.is_boss and enemy.invincible_identifier:
                        # print("hit")
                        self.hit_invincible_boss_sound.play()
                    elif enemy.is_boss and not enemy.invincible_identifier:
                        enemy.enemy_life -= self.setting.player_bullet_damage
                        if enemy.enemy_life <= 0:
                            prop = Prop(self)
                            prop.x = enemy.rect.x
                            prop.y = enemy.rect.y
                            self.props.add(prop)
                            # print("创建了一个道具")
                            self.enemies.remove(enemy)

                            self.stats.score += enemy.enemy_score

                            # 判断敌方组里是否有boss组件, 若没有, 则设boss为非无敌状态
                            count = 0
                            for enemy in self.enemies:
                                if enemy.is_boss_component:
                                    count += 1
                            if count == 0:
                                for enemy in self.enemies:
                                    enemy.invincible_identifier = False
                            # print(count)

    def __screen_update(self):
        self.screen.fill((0, 0, 0))
        self.bg_image.update()

    def pause_game_screen_update(self):
        # self.screen.blit(self.ui_image.pause_menu_image, self.ui_image.pause_menu_image_rect)
        # self.screen.blit(self.ui_image.start_button.pause_start_button_image,
        #                  self.ui_image.start_button.pause_start_button_image_rect)
        # self.screen.blit(self.ui_image.home_button.pause_home_button_image,
        #                  self.ui_image.home_button.pause_home_button_image_rect)
        self.ui_image.update()

    def game_over_screen_update(self):
        # self.screen.fill(0)
        self.ui_image.update()

    def fire_bullet(self):
        # 获取当前游戏运行的时间
        now = pygame.time.get_ticks()
        # fire_cd越大, 子弹发射间隔越长
        if now - self.last_fire > self.fire_cd:
            self.last_fire = now
            new_player_bullet = PlayerBullet(self, self.player)
            self.player_bullets.add(new_player_bullet)
            # 播放音效
            self.fire_sound.play()

    def fire_bullet02(self):
        # 获取当前游戏运行的时间
        now = pygame.time.get_ticks()
        # fire_cd越大, 子弹发射间隔越长
        if now - self.last_fire02 > self.fire_cd:
            self.last_fire02 = now
            new_player_bullet = PlayerBullet(self, self.player02)
            self.player_bullets.add(new_player_bullet)
            # 播放音效
            self.fire_sound.play()

    def _create_enemy(self):
        global enemy
        now = pygame.time.get_ticks()
        if now - self.create_enemy_last_updated > self.create_enemy_cd:
            # print("已创建一个敌人")
            # 随机出现敌人的种类
            id = random.randint(1, 3)
            enemy = Enemy01(self)
            # 设置随机下一个敌人出现的时间
            self.create_enemy_cd = random.randint(0, 2000)
            self.create_enemy_last_updated = now
            if id == 1:
                enemy = Enemy01(self)
            if id == 2:
                enemy = Enemy02(self)
            self.enemies.add(enemy)

    def reset_game(self):
        self.stats.reset_stats()
        self.bg_image = Background(self)
        self.enemies.empty()
        self.enemy_bullets.empty()
        self.player_bullets.empty()
        self.props.empty()
        # 初始化玩家的位置
        self.player.reset_player()
        self.player02.reset_player()


if __name__ == '__main__':
    ai = ItTakesTwo()
    ai.run_game()
