import pygame
from pygame.locals import QUIT
from pygame import Rect
import requests 
import io 
from urllib.request import urlopen 

pygame.init()

# créer la fenêtre
game_width = 700
game_height = 700
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption("Pokemon")

# définir les couleurs
black = (0, 0, 0)
gold = (218, 165, 32)
grey = (200, 200, 200)
green = (0, 200, 0)
red = (200, 0, 0)
white = (255, 255, 255)
K = (129, 178, 154)

base_url = 'https://pokeapi.co/api/v2'


class Type:
    def __init__(self, type_name):
        self.type_name = type_name

TYPES = [Type("Normal"), Type("Feu"), Type("Eau"), Type("Terre"), Type("Electric")]        

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, nom, points_de_vie, niveau, puissance_attaque, defense, types, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.nom = nom
        self.points_de_vie = points_de_vie
        self.puissance_attaque = puissance_attaque
        self.defense = defense
        self.type = [Type(type_name) for type_name in types]

        #Appeler l'API Pokemon
        req = requests.get(f"{base_url}/pokemon/{self.nom.lower()}")
        self.json = req.json()

       
        self.niveau = niveau

        # position fenêtre
        self.x = x
        self.y = y

        # nombre de potions restantes
        self.num_potions = 3

        # obtenir les statistiques du Pokémon depuis l'API
        stats = self.json ['stats']
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

            # définir la largeur du sprite
            self.size = 150

            #définir le sprite comme le sprite orienté vers l'avant
            self.set_sprite('front_default') 

    def set_sprite(self, side):

        # définir le sprite du Pokémon
        image = self.json['sprites'][side]
        image_stream = urlopen(image).read()
        image_file = io.BytesIO(image_stream)
        self.image = pygame.image.load(image_file).convert_alpha()

        #mettre à l'échelle l'image

        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height =self.image.get_height() * scale
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def draw(self, alpha=255):
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())




niveau = 30
# Définir les positions x et y pour l'affichage des Pokémon
x_bulbasaur, y_bulbasaur = 50, 50
x_charmander, y_charmander = 200, 50
x_squirtle, y_squirtle = 350, 50
x_pikachu, y_pikachu = 500, 50
x_sandshrew, y_sandshrew = 50, 250
x_eevee, y_eevee = 200, 250

# Créez les instances de la classe Pokemon avec les arguments nécessaires
bulbasaur = Pokemon('Bulbasaur', 100, niveau, 25, 15, ['Type1', 'Type2'], x_bulbasaur, y_bulbasaur)
charmander = Pokemon('Charmander', 90, niveau, 25, 18, ['Type1', 'Type2'], x_charmander, y_charmander)
squirtle = Pokemon('Squirtle', 95, niveau, 23, 20, ['Type1', 'Type2'], x_squirtle, y_squirtle)
pikachu = Pokemon('Pikachu', 85, niveau, 30, 15, ['Type1'], x_pikachu, y_pikachu)
sandshrew = Pokemon('Sandshrew', 95, niveau, 20, 25, ['Type1'], x_sandshrew, y_sandshrew)
eevee = Pokemon('Eevee', 80, niveau, 20, 20, ['Type1'], x_eevee, y_eevee)
pokemons = [bulbasaur, charmander, squirtle, pikachu, sandshrew, eevee]

#Les Pokémon sélectionnés par les joueurs et les rivaux 

player_pokemon = None
rival_pokemon = None 

# game loop 
game_status = 'select pokemon'
while game_status != 'quit':

    for event in pygame.event.get():
        if event.type == QUIT:
            game_status = 'quit'

    # Écran de sélection des Pokémon
    if game_status == 'select pokemon':
        game.fill(K)

        # Dessinez les Pokémon de départ
        bulbasaur.draw()
        charmander.draw()
        squirtle.draw()
        pikachu.draw()
        eevee.draw()
        sandshrew.draw()

        #Dessiner une boîte autour du Pokémon pointé par la souris
        mouse_cursor = pygame.mouse.get_pos()
        for pokemon in pokemons:
            if pokemon.get_rect().collidepoint(mouse_cursor):
                pygame.draw.rect(game, black, pokemon.get_rect(), 2)

        pygame.display.update()
            
pygame.quit()


