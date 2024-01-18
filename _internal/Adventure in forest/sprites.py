import pygame
from config import *
import math
import random


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(black)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "P"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(9, 4, 15, 27)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += player_speed
            self.x_change -= player_speed
            self.facing = "left"
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= player_speed
            self.x_change += player_speed
            self.facing = "right"
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += player_speed
            self.y_change -= player_speed
            self.facing = "up"
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= player_speed
            self.y_change += player_speed
            self.facing = "down"

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.play = False

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += player_speed
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= player_speed
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += player_speed
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= player_speed

    def animate(self):

        down_animations = [self.game.character_spritesheet.get_sprite(9, 4, 15, 27),
                           self.game.character_spritesheet.get_sprite(41, 4, 15, 28),
                           self.game.character_spritesheet.get_sprite(73, 5, 15, 27),
                           self.game.character_spritesheet.get_sprite(105, 4, 15, 28)]

        up_animations = [self.game.character_spritesheet.get_sprite(9, 37, 15, 28),
                         self.game.character_spritesheet.get_sprite(41, 36, 15, 27),
                         self.game.character_spritesheet.get_sprite(73, 37, 15, 28),
                         self.game.character_spritesheet.get_sprite(105, 36, 15, 27)]

        right_animations = [self.game.character_spritesheet.get_sprite(9, 68, 14, 28),
                            self.game.character_spritesheet.get_sprite(41, 68, 14, 28),
                            self.game.character_spritesheet.get_sprite(73, 68, 14, 28),
                            self.game.character_spritesheet.get_sprite(105, 68, 14, 28)]

        left_animations = [self.game.character_spritesheet.get_sprite(10, 101, 14, 28),
                           self.game.character_spritesheet.get_sprite(42, 100, 14, 28),
                           self.game.character_spritesheet.get_sprite(74, 101, 14, 28),
                           self.game.character_spritesheet.get_sprite(106, 100, 14, 28)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(9, 4, 15, 27)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(9, 37, 15, 28)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(10, 101, 14, 28)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(9, 68, 14, 28)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y,):

        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = tilesize
        self.height = tilesize

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, *args, **kwargs):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)  # "#"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(160, 416, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)  # "W"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "."

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Desks(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = desks_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "D"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.interrain_spritesheet.get_sprite(0, 192, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Tree(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)  # "@"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(192, 416, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Flower(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "F"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(64, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Trope(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = trope_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "O"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(288, 65, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class TropeA(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = trope_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "A"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(193, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class TropeB(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = trope_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "B"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(222, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class TropeC(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = trope_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "C"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(161, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class TropeUP(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = trope_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "U"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(256, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class TropeDW(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = trope_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "T"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(256, 64, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Trope1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = trope_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)  # "0"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(288, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = enemy_layer
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)  # "E"

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(10, 50)

        self.image = self.game.enemy_spritesheet.get_sprite(9, 68, 14, 28)
        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= enemy_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += enemy_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):

        right_animations = [self.game.enemy_spritesheet.get_sprite(9, 68, 14, 28),
                            self.game.enemy_spritesheet.get_sprite(41, 68, 14, 28),
                            self.game.enemy_spritesheet.get_sprite(73, 68, 14, 28),
                            self.game.enemy_spritesheet.get_sprite(105, 68, 14, 28)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(10, 101, 14, 28),
                           self.game.enemy_spritesheet.get_sprite(42, 100, 14, 28),
                           self.game.enemy_spritesheet.get_sprite(74, 101, 14, 28),
                           self.game.enemy_spritesheet.get_sprite(106, 100, 14, 28)]

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(10, 101, 14, 28)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(9, 68, 14, 28)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("fonts/pixel-anchor-jack_0.ttf", fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
