import pygame as pyg

pyg.init()
screenW, screenH = 1536, 864
center = screenW * 0.5, screenH * 0.5
screen = pyg.display.set_mode((screenW, screenH))

save_border_rect = True
save_level_border = True
coin_creation = False
enemy_creation = False
st_time = pyg.time.get_ticks()
t = 0
tt = 0


def set_globals():
    global t, tt
    t = 0
    tt = 0


class Levels:
    def __init__(self, surface, coins, lives, paused=False, zen_mode=False):
        self.border_lines = []
        self.level_borders = []
        self.surface = surface
        self.coins_list = []
        self.coins = coins
        self.enemies = []
        self.lives = lives
        self.coins_total = 0
        self.level_coins = 0
        self.level_coin = self.coins
        self.zen_mode = zen_mode
        self.paused = paused
        self.level_type = ""

    def borders(self):
        global save_border_rect, tt
        width = 3
        line_color = (28, 28, 30)

        # left borders
        l_edge = pyg.draw.line(self.surface, line_color, (100, center[1] + 110), (100, center[1] - 110), width)  # edge
        l_top = pyg.draw.line(self.surface, line_color, (100, center[1] - 110), (222, center[1] - 110), width)  # top
        l_bottom = pyg.draw.line(self.surface, line_color, (100, center[1] + 110), (222, center[1] + 110), width)  # bottom
        l_inner_top = pyg.draw.line(self.surface, line_color, (222, center[1] - 110), (222, center[1] - 52), width)  # inner top
        l_inner_bottom = pyg.draw.line(self.surface, line_color, (222, center[1] + 110), (222, center[1] + 52), width)  # inner bottom
        l_tunnel_top = pyg.draw.line(self.surface, line_color, (222, center[1] - 52), (290, center[1] - 52), width)  # tunnel top
        l_tunnel_bottom = pyg.draw.line(self.surface, line_color, (222, center[1] + 52), (290, center[1] + 52), width)  # tunnel bottom

        # right borders
        r_edge = pyg.draw.line(self.surface, line_color, (screenW - 100, center[1] + 110), (screenW - 100, center[1] - 110), width)  # edge
        r_top = pyg.draw.line(self.surface, line_color, (screenW - 100, center[1] - 110), (screenW - 220, center[1] - 110), width)  # top
        r_bottom = pyg.draw.line(self.surface, line_color, (screenW - 100, center[1] + 110), (screenW - 220, center[1] + 110), width)  # bottom
        r_inner_top = pyg.draw.line(self.surface, line_color, (screenW - 220, center[1] - 110), (screenW - 220, center[1] - 52), width)  # inner top
        r_inner_bottom = pyg.draw.line(self.surface, line_color, (screenW - 220, center[1] + 110), (screenW - 220, center[1] + 52), width)  # inner bottom
        r_tunnel_top = pyg.draw.line(self.surface, line_color, (screenW - 220, center[1] - 52), (screenW - 290, center[1] - 52), width)  # tunnel top
        r_tunnel_bottom = pyg.draw.line(self.surface, line_color, (screenW - 220, center[1] + 52), (screenW - 290, center[1] + 52), width)  # tunnel bottom

        # center borders
        top = pyg.draw.line(self.surface, line_color, (290, center[1] - 230), (screenW - 290, center[1] - 230), width)  # top
        bottom = pyg.draw.line(self.surface, line_color, (290, center[1] + 230), (screenW - 290, center[1] + 230), width)  # bottom
        left_top = pyg.draw.line(self.surface, line_color, (290, center[1] - 230), (290, center[1] - 52), width)  # left side top
        left_bottom = pyg.draw.line(self.surface, line_color, (290, center[1] + 230), (290, center[1] + 52), width)  # left side bottom
        right_top = pyg.draw.line(self.surface, line_color, (screenW - 290, center[1] - 230), (screenW - 290, center[1] - 52), width)  # right side top
        right_bottom = pyg.draw.line(self.surface, line_color, (screenW - 290, center[1] + 230), (screenW - 290, center[1] + 52), width)  # right side bottom

        # append all borders to a list for collision checks
        if not save_border_rect:
            if tt == 0:
                save_border_rect = True
                tt = 1
        else:

            l_lines = [l_edge, l_top, l_bottom, l_inner_top, l_inner_bottom, l_tunnel_top, l_tunnel_bottom]
            r_lines = [r_edge, r_top, r_bottom, r_inner_top, r_inner_bottom, r_tunnel_top, r_tunnel_bottom]
            self.border_lines.extend(l_lines)
            self.border_lines.extend(r_lines)
            self.level_borders = [top, bottom, left_top, left_bottom, right_top, right_bottom]
            save_border_rect = False

    def background(self):
        rect_color = (255, 159, 10)
        # left background
        pyg.draw.rect(self.surface, rect_color, pyg.Rect(100, center[1] - 110, 121, 220))
        # right background
        pyg.draw.rect(self.surface, rect_color, pyg.Rect(screenW - 221, center[1] - 110, 122, 220), )

        # center background
        rect_color = (209, 209, 214)
        pyg.draw.rect(self.surface, rect_color, pyg.Rect(290, center[1] - 230, screenW - 580, 460))
        pyg.draw.rect(self.surface, rect_color, pyg.Rect(221, center[1] - 52, 69, 104))
        pyg.draw.rect(self.surface, rect_color, pyg.Rect(screenW - 290, center[1] - 52, 69, 104))

    def show_lock(self):
        locked_line = pyg.draw.line(self.surface, (99, 99, 102), (screenW - 250, center[1] - 52), (screenW - 250, center[1] + 52), 4)
        return locked_line

    def return_coins(self):
        return self.coins

    def return_lives(self):
        return self.lives

    def return_coin_list(self):
        return self.coins_list

    def return_coins_total(self):
        return self.coins_total

    # ** Coins ** #
    class Coins:
        def __init__(self, surface, x, y, width, height):
            self.surface = surface
            self.rect = pyg.Rect(x, y, width, height)
            self.shadow = self.rect.copy().inflate(4, 4)
            self.color = 255, 204, 0

        def show(self):
            pyg.draw.rect(self.surface, (99, 99, 102), self.shadow, border_radius=30)
            pyg.draw.rect(self.surface, self.color, self.rect, border_radius=30)

        def collide(self, rect):
            if self.rect.colliderect(rect):
                return True

    def coin_handling(self, rect):
        for con in self.coins_list:
            con.show()
            if con.collide(rect):
                self.coins_list.remove(con)
                self.coins += 1
                self.level_coin += 1

    def create_coins(self, surface, x_vars, y_vars):
        global coin_creation
        yn, yp, r1 = y_vars
        xn, xp, r2 = x_vars
        if coin_creation:
            y = yn
            for i in range(r1):
                x = xn
                for ii in range(r2):
                    coin = Levels(surface, 0, 0).Coins(surface, x, y - 13, 26, 26)
                    self.coins_list.append(coin)
                    x += xp
                y += yp
            self.coins_total += len(self.coins_list)
            self.level_coins = len(self.coins_list)
            coin_creation = False

    # ** Enemies ** #

    class Enemies:
        def __init__(self, surface, x, y, width, height, speed=4.0):
            self.surface = surface
            self.rect = pyg.Rect(x, y, width, height)
            self.shadow = self.rect.copy().inflate(4, 4)
            self.color = 255, 59, 48
            self.speed = speed
            self.en_start = pyg.time.get_ticks()

        def show(self):
            pyg.draw.rect(self.surface, (99, 99, 102), self.shadow, border_radius=30)
            pyg.draw.rect(self.surface, self.color, self.rect, border_radius=30)

        def collide(self, rect):
            if self.rect.colliderect(rect):
                return True

        def move(self):
            self.rect.y += self.speed
            self.shadow.y += self.speed
            if self.rect.bottom >= center[1] + 228 or self.rect.top <= center[1] - 228:
                en_end = pyg.time.get_ticks()
                dt = en_end * 0.001 - self.en_start * 0.001
                if dt >= 0.1:
                    self.en_start = en_end
                    self.speed *= -1

    def enemy_handling(self, rect):
        global st_time
        for enemy in self.enemies:
            enemy.show()
            if not self.paused:
                enemy.move()
            if enemy.collide(rect):
                end_time = pyg.time.get_ticks()
                dt = end_time * 0.001 - st_time * 0.001
                if dt >= 0.2:
                    st_time = end_time
                    if not self.zen_mode:
                        if self.lives > 0:
                            self.lives -= 1

    """################################################################"""
    """################################################################"""
    """ ----------------------------------------------------- LEVELS START ----------------------------------------------------- """

    # LEVEL 1
    def level_1(self, surface, rect):
        global coin_creation, enemy_creation, st_time
        # Coins
        self.create_coins(surface, x_vars=(center[0] - 364, 64, 12), y_vars=(center[1] - 60, 120, 2))
        self.coin_handling(rect)

        # Enemies
        if enemy_creation:
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] - 110, center[1], 34, 34, 3))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] + 110, center[1], 34, 34, -3))
            enemy_creation = False

        self.enemy_handling(rect)

    # LEVEL 2
    def level_2(self, surface, rect):
        global coin_creation, enemy_creation, st_time
        # Coins
        # (center[0] - 324, 54, 12), (center[1] - 140, 91, 4)
        self.create_coins(surface, x_vars=(center[0] - 378, 68, 12), y_vars=(center[1] - 106, 106, 3))
        self.coin_handling(rect)

        # Enemies
        if enemy_creation:
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] - 180, center[1], 34, 34, 3.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0], center[1], 34, 34, -3.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] + 180, center[1], 34, 34, 3.5))
            enemy_creation = False

        self.enemy_handling(rect)

    # LEVEL 3
    def level_3(self, surface, rect):
        global coin_creation, enemy_creation, st_time
        # Coins
        self.create_coins(surface, (center[0] - 378, 58, 14), (center[1] - 140, 91, 4))
        self.coin_handling(rect)

        # Enemies
        if enemy_creation:
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] - 260, center[1], 34, 34, 3.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] - 160, center[1], 34, 34, -3.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] + 160, center[1], 34, 34, 3.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] + 260, center[1], 34, 34, -3.5))
            enemy_creation = False

        self.enemy_handling(rect)

    # LEVEL 4
    def level_4(self, surface, rect):
        global coin_creation, enemy_creation, st_time
        # Coins
        self.create_coins(surface, x_vars=(center[0] - 358, 78, 10), y_vars=(center[1] - 130, 130, 3))
        self.coin_handling(rect)

        # Enemies
        if enemy_creation:
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] - 210, center[1], 34, 34, 4.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0], center[1], 34, 34, -5.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] + 210, center[1], 34, 34, 4.5))
            enemy_creation = False

        self.enemy_handling(rect)

    # LEVEL 5
    def level_5(self, surface, rect):
        global coin_creation, enemy_creation, st_time
        # Coins
        self.create_coins(surface, x_vars=(center[0] - 418, 68, 13), y_vars=(center[1] - 140, 91, 4))
        self.coin_handling(rect)

        # Enemies
        if enemy_creation:
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] - 280, center[1], 34, 34, -4.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] - 180, center[1], 34, 34, 4.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0], center[1], 34, 34, -5.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] + 180, center[1], 34, 34, 4.5))
            self.enemies.append(Levels(surface, 0, 0).Enemies(surface, center[0] + 280, center[1], 34, 34, -4.5))
            enemy_creation = False

        self.enemy_handling(rect)

    # LEVEL BONUS
    def level_bonus(self, surface, rect):
        global coin_creation, enemy_creation, st_time
        # Coins
        self.create_coins(surface, x_vars=(center[0] - 324, 94, 8), y_vars=(center[1] - 60, 120, 2))
        self.coin_handling(rect)

    """ ------------------------------------------------------- LEVELS END ------------------------------------------------------- """
    """################################################################"""
    """################################################################"""

    def new_level(self, lvl):
        global coin_creation, enemy_creation, st_time, t
        if t == lvl - 1:
            coin_creation = True
            enemy_creation = True
            st_time = pyg.time.get_ticks()
            self.enemies.clear()
            self.coins_list.clear()
            self.level_coins = 0
            self.level_coin = 0
            t = lvl

    def level_chooser(self, surface, rect, lvl):
        global t
        if lvl == 1:
            self.new_level(lvl)
            self.level_1(surface, rect)
            self.level_type = "level"
        elif lvl == 2:
            self.new_level(lvl)
            self.level_2(surface, rect)
            self.level_type = "level"
        elif lvl == 3:
            self.new_level(lvl)
            self.level_3(surface, rect)
            self.level_type = "level"
        if not self.zen_mode:
            if lvl == 4:
                self.new_level(lvl)
                self.level_4(surface, rect)
                self.level_type = "level"
            elif lvl == 5:
                self.new_level(lvl)
                self.level_5(surface, rect)
                self.level_type = "level"
            elif lvl == 6:
                self.new_level(lvl)
                self.level_bonus(surface, rect)
                self.level_type = "bonus"
