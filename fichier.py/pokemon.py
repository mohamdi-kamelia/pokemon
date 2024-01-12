import pygame
import requests
import io
from urllib.request import urlopen

pygame.init()

class Type:
    def __init__(self, type_name):
        self.type_name = type_name

TYPES = [Type("Normal"), Type("Feu"), Type("Eau"), Type("Terre"), Type("Electric")]

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, nom, points_de_vie, niveau, puissance_attaque, defense, types, x, y, json_data=None):
        pygame.sprite.Sprite.__init__(self)

        self.nom = nom
        self.points_de_vie = points_de_vie
        self.puissance_attaque = puissance_attaque
        self.defense = defense
        self.type = [Type(type_name) for type_name in types]

        if json_data:
            self.json = json_data
        else:
            # Appeler l'API Pokemon
            req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.nom.lower()}")
            self.json = req.json()

        self.niveau = niveau

        # position fenêtre
        self.x = x
        self.y = y

        # nombre de potions restantes
        self.num_potions = 3

        # obtenir les statistiques du Pokémon depuis l'API
        stats = self.json['stats']
        for stat in stats:
            if stat['stat']['name'] == 'hp':
                self.current_hp = stat['base_stat'] + self.niveau
                self.max_hp = stat['base_stat'] + self.niveau
            elif stat['stat']['name'] == 'attack':
                self.attack = stat['base_stat']
            elif stat['stat']['name'] == 'defense':
                self.defense = stat['base_stat']
            elif stat['stat']['name'] == 'speed':
                self.speed = stat['base_stat']

        self.type = []
        for pokemon_type in self.json['types']:
            type_name = pokemon_type['type']['name']
            self.type.append(type_name)

        # définir la largeur du sprite
        self.size = 150

        # définir le sprite comme le sprite orienté vers l'avant
        self.set_sprite('front_default')

    def set_sprite(self, side):
        # définir le sprite du Pokémon
        image = self.json['sprites'][side]
        image_stream = urlopen(image).read()
        image_file = io.BytesIO(image_stream)
        self.image = pygame.image.load(image_file).convert_alpha()

        # mettre à l'échelle l'image
        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height = self.image.get_height() * scale
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def draw(self, alpha=255):
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        pygame.display.get_surface().blit(sprite, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    # Ajouter une méthode statique pour créer un Pokémon à partir d'un nom
    @staticmethod
    def create_pokemon(nom, niveau, x, y):
        # Appeler l'API Pokemon
        req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nom.lower()}")
        json_data = req.json()

        # Récupérer les statistiques du Pokémon depuis l'API
        stats = json_data['stats']
        for stat in stats:
            if stat['stat']['name'] == 'hp':
                current_hp = stat['base_stat'] + niveau
                max_hp = stat['base_stat'] + niveau
            elif stat['stat']['name'] == 'attack':
                attack = stat['base_stat']
            elif stat['stat']['name'] == 'defense':
                defense = stat['base_stat']
            elif stat['stat']['name'] == 'speed':
                speed = stat['base_stat']

        types = [pokemon_type['type']['name'] for pokemon_type in json_data['types']]

        # Créer et retourner un objet Pokemon
        return Pokemon(nom, max_hp, niveau, attack, defense, types, x, y, json_data)


