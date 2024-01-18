# pokemon.py
import pygame
from pygame.locals import *
import requests 
import io 
from urllib.request import urlopen
import random 
import time
import math


pygame.init()

base_url = 'https://pokeapi.co/api/v2'

class Type:
    def __init__(self, type_name):
        self.type_name = type_name

TYPES = [Type("Normal"), Type("Feu"), Type("Eau"), Type("Terre"), Type("Electric")]

class Move:
    def __init__(self, url):
        req = requests.get(url)
        self.json = req.json()
        self.name = self.json['name']
        self.power = self.json['power']
        self.type = self.json['type']['name']
     

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, nom, points_de_vie, niveau, puissance_attaque, defense, types, x, y , game):
        pygame.sprite.Sprite.__init__(self)
        self.nom = nom
        self.points_de_vie = points_de_vie
        self.puissance_attaque = puissance_attaque
        self.defense = defense
        self.type = [Type(type_name) for type_name in types]
        self.game = game 

        req = requests.get(f"{base_url}/pokemon/{self.nom.lower()}")
        self.json = req.json()

        self.niveau = niveau
        self.x = x
        self.y = y
        self.num_potions = 3

        stats = self.json['stats']
        for stat in stats:
            if stat['stat']['name'] == 'hp':
                self.current_hp = stat['base_stat'] + self.niveau
                self.max_hp = stat['base_stat'] + self.niveau
            elif stat['stat']['name']  == 'attack':
                self.attack = stat['base_stat']
            elif stat['stat']['name'] == 'defense':
                self.defense = stat['base_stat']
            elif stat['stat']['name'] == 'speed':
                self.speed = stat['base_stat']

        self.type = []
        for pokemon_type in self.json['types']:
            type_name = pokemon_type['type']['name']
            self.type.append(type_name)

        self.size = 150
        self.set_sprite('front_default')

    def perform_attack(self , other , move):
        display_message(f'{self.nom} used {move.name}')
        time.sleep(2)

        damage = (2 * self.niveau + 10)/ 250 * self.attack /other.defense * move.power

        if move.type in self.type:
            damage *= 1,5

        random_num = random.randint(1 , 10000)
        if random_num <= 625:
            damage *= 1.5

        damage = math.floor(damage)
        other.take_damage(damage)

    def take_damage(self , damage):
        self.current_hp -= damage

        if self.current_hp < 0:
            self.current_hp = 0

    def use_potion(self):
        if self.num_potions > 0:
            self.current_hp +=30
            if self.current_hp >self.max_hp:
                self.current_hp = self.max_hp
            self.num_potions -= 1

    def set_sprite(self, side):
        image = self.json['sprites'][side]
        image_stream = urlopen(image).read()
        image_file = io.BytesIO(image_stream)
        self.image = pygame.image.load(image_file).convert_alpha()

        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height =self.image.get_height() * scale
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def set_moves(self):
        self.moves = []

        for move_info in self.json['moves']:
            versions = move_info['version_group_details']    
            for version in versions:
                if version['version_group']['name'] != 'red_blue':
                    continue

                learn_method = version['move_learn_method']['name']
                if learn_method != 'level_up':
                    continue

                level_learned = version['level_learned_at']
                if self.niveau >= level_learned:
                    move = Move(move_info['move']['url'])
                    if move.power is not None:
                        self.moves.append(move)

        if len(self.moves) > 4:
            self.moves = random.sample(self.moves, 4)

    def draw(self, alpha=255):
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        self.game.blit(sprite, (self.x, self.y))

    def draw_hp(self):
        bar_scale = 200 // self.max_hp
        for i in range(self.max_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(game, red, bar)

        for i in range(self.current_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(game, green, bar)

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.current_hp} / {self.max_hp}', True, black)
        text_rect = text.get_rect()
        text_rect.x = self.hp_x
        text_rect.y = self.hp_y + 30
        self.game.blit(text, text_rect)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

class Button:
    def __init__(self, rect, label):
        self.rect = rect
        self.label = label

def create_button(width, height, left, top, text_cx, text_cy, label):
    mouse_cursor = pygame.mouse.get_pos()
    button_rect = Rect(left, top, width, height)
    if button_rect.collidepoint(mouse_cursor):
        pygame.draw.rect(game, gold, button_rect)
    else:
        pygame.draw.rect(game, white, button_rect)
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f'{label}', True, black)
    text_rect = text.get_rect(center=(text_cx, text_cy))
    game.blit(text, text_rect)
    return Button(button_rect, label)



