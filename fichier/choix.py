import pygame
import requests  # Ajout de l'import pour requests
import io
from urllib.request import urlopen

base_url = 'https://pokeapi.co/api/v2'  # Définition de base_url

class Type:
    def __init__(self, type_name):
        self.type_name = type_name

class choix(pygame.sprite.Sprite):
    def __init__(self, nom, points_de_vie, niveau, puissance_attaque, defense, types, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.nom = nom
        self.points_de_vie = points_de_vie
        self.max_points_de_vie = points_de_vie
        self.puissance_attaque = puissance_attaque
        self.defense = defense
        self.type = [Type(type_name) for type_name in types]
        self.niveau = niveau
        self.x = x
        self.y = y
        self.num_potions = 3
        self.size = 150
        self.set_sprite('front_default')
        self.pokedex = []

    def set_sprite(self, side):
        req = requests.get(f"{base_url}/pokemon/{self.nom.lower()}")
        self.json = req.json()

        image = self.json['sprites'][side]
        image_stream = urlopen(image).read()
        image_file = io.BytesIO(image_stream)
        self.image = pygame.image.load(image_file).convert_alpha()

        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height = self.image.get_height() * scale
        self.image = pygame.transform.scale(self.image, (int(new_width), int(new_height)))

    def draw(self, game, x, y, alpha=255):
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (x, y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

