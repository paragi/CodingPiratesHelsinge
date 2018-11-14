# MIT License
# 
# Copyright (c) 2018 Peter Allin
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pygame


class Player:
    def __init__(self, rect, area):
        self.rect = rect
        self.speed_pixels_per_draw = 2
        self.area = area

    def move(self, player_input):
        if player_input.down and self.rect.bottom < self.area.bottom:
            self.rect.y = self.rect.y + self.speed_pixels_per_draw
        if player_input.up and self.rect.top > self.area.top:
            self.rect.y = self.rect.y - self.speed_pixels_per_draw
        if player_input.right and self.rect.right < self.area.right:
            self.rect.x = self.rect.x + self.speed_pixels_per_draw
        if player_input.left and self.rect.left > self.area.left:
            self.rect.x = self.rect.x - self.speed_pixels_per_draw


class PlayerShot:
    def __init__(self, rect):
        self.rect = rect
        self.speed_pixels_per_draw = 5

    def update(self):
        self.rect.x = self.rect.x + self.speed_pixels_per_draw


class PlayerInput:
    def __init__(self):
        self.stop = False
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.fire = False

    def update(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.stop = True

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    self.left = True
                if e.key == pygame.K_d:
                    self.right = True
                if e.key == pygame.K_s:
                    self.down = True
                if e.key == pygame.K_w:
                    self.up = True
                if e.key == pygame.K_RETURN:
                    self.fire = True

            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    self.left = False
                if e.key == pygame.K_d:
                    self.right = False
                if e.key == pygame.K_s:
                    self.down = False
                if e.key == pygame.K_w:
                    self.up = False
                if e.key == pygame.K_RETURN:
                    self.fire = False


class Graphics:
    def __init__(self):
        self.player = pygame.image.load("player.png").convert_alpha()
        self.player_shot = pygame.image.load("basic_shot.png").convert_alpha()


class GameState:
    def __init__(self, graphics, game_area):
        self.graphics = graphics
        self.game_area = game_area
        player_center = (game_area.width // 2, game_area.height // 2)
        player_rect = graphics.player.get_rect(center=player_center)
        self.player = Player(player_rect, game_area)
        self.player_shots = []
        self.has_shot = False

    def update(self, player_input):
        self.player.move(player_input)

        may_fire = not self.has_shot
        if player_input.fire and may_fire:
            shot_coord = self.player.rect.midright
            new_shot = PlayerShot(self.graphics.player_shot.get_rect(center=shot_coord))
            self.player_shots.append(new_shot)
            self.has_shot = True
        elif not player_input.fire:
            self.has_shot = False

        for shot in self.player_shots:
            shot.update()
        self.reap_outsiders(self.player_shots)

    def reap_outsiders(self, objects):
        for obj in list(objects):
            if not self.game_area.colliderect(obj.rect):
                objects.remove(obj)


def paint_screen(window, game_state, graphics):
    window.fill((0, 0, 0))
    window.blit(graphics.player, game_state.player.rect)
    for shot in game_state.player_shots:
        window.blit(graphics.player_shot, shot.rect)
    pygame.display.flip()


def main_loop():
    pygame.init()
    screen_width = 800
    screen_height = 600
    window = pygame.display.set_mode((screen_width, screen_height))

    graphics = Graphics()
    game_state = GameState(graphics, window.get_rect())
    player_input = PlayerInput()

    while not player_input.stop:
        pygame.time.delay(5)
        player_input.update()
        game_state.update(player_input)
        paint_screen(window, game_state, graphics)
    pygame.quit()


main_loop()
