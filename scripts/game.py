import pygame as pyg
import sys, os
from scripts.levels import Levels
from scripts.levels import set_globals

pyg.init()


# print(resource_path("font.ttf"))
class Button:
    def __init__(self, surface, pos, size, font_size):
        self.surface = surface
        self.button_rect = pyg.Rect(0, 0, size[0], size[1])
        self.pos = pos
        self.button_rect.center = pos
        self.button_color = (99, 99, 102)
        self.text_color = (199, 199, 204)
        self.font = pyg.font.Font("assets/font.ttf", font_size)
        self.collision = False

    def collide(self, point):
        if self.button_rect.collidepoint(point):
            self.text_color = (48, 209, 88)
            self.collision = True
        else:
            self.collision = False

    def show(self, string):
        text = self.font.render(string, True, self.text_color)
        text_rect = text.get_rect()
        self.button_rect.center = self.pos
        text_rect.center = self.button_rect.centerx, self.button_rect.centery - 2
        pyg.draw.rect(self.surface, self.button_color, self.button_rect, border_radius=15)
        self.surface.blit(text, text_rect)


class Player:
    def __init__(self, x, y, width, height):
        self.rect = pyg.Rect(0, 0, width, height)
        self.rect.center = x, y
        self.direction = ""
        self.x_speed = 4
        self.y_speed = 5
        self.coll_top = self.coll_bottom = self.coll_right = self.coll_left = False
        self.collision_tolerance = 10
        self.paused = False

    def show(self, surf):
        pyg.draw.rect(surf, (10, 132, 255), self.rect)

    def change_dir(self, direction):
        if not self.paused:
            self.direction = direction

    def collision_check(self, rect):
        if self.rect.colliderect(rect):
            return True

    def collision_type(self, rect):
        if self.collision_check(rect):
            if abs(self.rect.top - rect.bottom) <= self.collision_tolerance:
                self.coll_top = True
                self.rect.top = rect.bottom
            else:
                self.coll_top = False
            if abs(self.rect.bottom - rect.top) <= self.collision_tolerance:
                self.coll_bottom = True
                self.rect.bottom = rect.top
            else:
                self.coll_bottom = False
            if abs(self.rect.right - rect.left) <= self.collision_tolerance:
                self.coll_right = True
                self.rect.right = rect.left
            else:
                self.coll_right = False
            if abs(self.rect.left - rect.right) <= self.collision_tolerance:
                self.coll_left = True
                self.rect.left = rect.right
            else:
                self.coll_left = False

    def move(self):
        if not self.paused:
            if self.direction == "DOWN":
                if not self.coll_bottom:
                    self.rect.y += self.y_speed
            elif self.direction == "UP":
                if not self.coll_top:
                    self.rect.y -= self.y_speed
            elif self.direction == "RIGHT":
                if not self.coll_right:
                    self.rect.x += self.x_speed
            elif self.direction == "LEFT":
                if not self.coll_left:
                    self.rect.x -= self.x_speed


font_56 = pyg.font.Font("assets/font.ttf", 56)
font_26 = pyg.font.Font("assets/font.ttf", 26)


def write_text(surface, string, pos, font, side, opt, string2=""):
    if opt == 0:
        text = font.render(string, True, (48, 209, 88))
        text_rect = text.get_rect()
        if side == "left":
            text_rect.bottomleft = pos
        elif side == "right":
            text_rect.bottomright = pos
        else:
            text_rect.midbottom = pos
        surface.blit(text, text_rect)
    elif opt == 1:
        text_1 = font_56.render(string, True, (48, 209, 88))
        text_2 = font_26.render(string2, True, (48, 209, 88))
        text1_rect = text_1.get_rect()
        text_2_rect = text_2.get_rect()
        text1_rect.bottomleft = pos
        text_2_rect.bottomleft = text1_rect.bottomleft[0] + 2, text1_rect.bottomleft[1] + 22
        surface.blit(text_1, text1_rect)
        surface.blit(text_2, text_2_rect)


# screen size
screenW, screenH = 1536, 864
center = screenW * 0.5, screenH * 0.5


# noinspection PyGlobalUndefined
def game(zen_mode):
    clock = pyg.time.Clock()  # FPS
    screen = pyg.Surface((screenW, screenH))
    window = pyg.display.set_mode((pyg.display.Info().current_w, pyg.display.Info().current_h), pyg.FULLSCREEN)

    # game surface
    surface = pyg.Surface(screen.get_size())
    surface = surface.convert()

    # header
    header = pyg.Surface((screenW, 100))
    header_shadow = header.copy()
    header_shadow.convert()
    header.convert()

    # pause menu surface
    pause_menu = pyg.Surface((screenW, screenH), pyg.SRCALPHA)
    pause_menu_background_rect = pyg.Rect(0, 0, 300, 500)
    pause_menu_background_rect.center = center[0], center[1],
    paused = False

    # lost menu
    lost = False

    # mouse show/hide
    pyg.mouse.set_visible(False)
    start_pos = pyg.mouse.get_pos()
    start_time = pyg.time.get_ticks()

    current_lvl = 1
    advance_level = True
    coins = 0
    lives = 3
    level = Levels(surface, coins, lives, paused=False, zen_mode=zen_mode)

    player = Player(140, center[1], 40, 40)

    # main loop
    running = True
    while running:
        clock.tick(120)
        surface.fill((175, 82, 222))
        header.fill((72, 72, 74))
        header_shadow.fill((44, 44, 46))

        # mouse show/hide
        end_pos = pyg.mouse.get_pos()
        if end_pos != start_pos:
            start_pos = end_pos
            pyg.mouse.set_visible(True)
            start_time = pyg.time.get_ticks()
        else:
            end_time = pyg.time.get_ticks()
            dt = end_time * 0.001 - start_time * 0.001
            if dt >= 1:
                start_time = end_time
                pyg.mouse.set_visible(False)

        # paused buttons
        pyg.draw.rect(pause_menu, (44, 44, 46), pause_menu_background_rect, border_radius=30)
        if lost:
            menu_text = "LOST"
        else:
            menu_text = "PAUSED"
        write_text(pause_menu, menu_text, (center[0], center[1] - 120), font_56, "", 0)
        button_return = Button(pause_menu, (center[0], center[1] + 20), (240, 60), 40)  # button return
        button_return.collide(pyg.mouse.get_pos())
        if not lost:
            button_return.show("Return")
        button_retry = Button(pause_menu, (center[0], center[1] + 100), (240, 60), 40)  # button main menu
        button_retry.collide(pyg.mouse.get_pos())
        button_retry.show("Retry")
        button_exit = Button(pause_menu, (center[0], center[1] + 180), (240, 60), 40)  # button quit
        button_exit.collide(pyg.mouse.get_pos())
        button_exit.show("Exit")

        # event management
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    set_globals()
                    current_lvl = 0
                    running = False
                elif event.key == pyg.K_DOWN:
                    player.change_dir("DOWN")
                    player.coll_top = False
                elif event.key == pyg.K_UP:
                    player.change_dir("UP")
                    player.coll_bottom = False
                elif event.key == pyg.K_RIGHT:
                    player.change_dir("RIGHT")
                    player.coll_left = False
                elif event.key == pyg.K_LEFT:
                    player.change_dir("LEFT")
                    player.coll_right = False
                elif event.key == pyg.K_n:
                    current_lvl += 1
                elif event.key == pyg.K_e:
                    paused = not paused
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if paused or lost:  # Button Press
                        if button_return.collision:
                            paused = False
                        if button_retry.collision:
                            current_lvl = 0
                            set_globals()
                            running = False
                            game(zen_mode)
                        if button_exit.collision:
                            current_lvl = 0
                            set_globals()
                            running = False

            elif event.type == pyg.KEYUP:
                if event.key == pyg.K_DOWN or event.key == pyg.K_UP or event.key == pyg.K_RIGHT or event.key == pyg.K_LEFT:
                    player.change_dir(" ")
                    player.coll_top = player.coll_bottom = player.coll_right = player.coll_left = False

        # paused
        if paused or lost:
            player.paused = True
            if not lost:
                level.paused = True
            pyg.mouse.set_visible(True)
        else:
            player.paused = False
            level.paused = False

        # Header and text
        write_text(header, "Level: " + str(current_lvl), (60, 70), font_56, "left", 0)
        string1 = "Coins: " + str(level.level_coin) + "/" + str(level.level_coins)
        string2 = "or: " + str(level.return_coins()) + "/" + str(level.return_coins_total())
        write_text(header, string1, (center[0] - 114, 64), font_56, "", 1, string2)
        if level.zen_mode:
            lives_txt = "zen"
        else:
            lives_txt = str(level.return_lives())
        write_text(header, "Lives: " + lives_txt, (screenW - 206, 70), font_56, "left", 0)

        level.background()
        level.level_chooser(surface, player.rect, current_lvl)

        for border in level.border_lines:
            player.collision_type(border)
        for border in level.level_borders:
            player.collision_type(border)

        player.move()
        player.show(surface)

        if level.return_lives() == 0:
            lost = True
            paused = True

        level.borders()

        if level.level_type != "bonus":
            enough_coins = level.level_coin >= 30 / 100 * level.level_coins
        else:
            enough_coins = True
        if enough_coins:
            if player.rect.centerx >= screenW - 222:
                if advance_level:
                    current_lvl += 1
                    player.rect.center = 140, center[1]
                    player.direction = ""
                    advance_level = False
                else:
                    advance_level = True
            else:
                pass
        else:
            if player.rect.right >= screenW - 251:
                player.rect.right = screenW - 251
            level.show_lock()

        screen.blit(surface, (0, 50))
        screen.blit(header_shadow, (0, 6))
        screen.blit(header, (0, 0))
        if paused:
            screen.blit(pause_menu, (0, 0))

        screen = pyg.transform.scale(screen, (pyg.display.Info().current_w, pyg.display.Info().current_h))
        window.blit(screen, (0,0))
        pyg.display.update()
