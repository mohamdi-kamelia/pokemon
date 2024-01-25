import pygame
from pygame.locals import QUIT
import requests
import io
from urllib.request import urlopen
from combat import *

pygame.init()

game_width = 700
game_height = 700
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption("Pokemon")

black = (0, 0, 0)
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

        self.type = []
        for pokemon_type in self.json['types']:
            type_name = pokemon_type['type']['name']
            self.type.append(type_name)

        self.size = 150
        self.set_sprite('front_default') 

    def set_sprite(self, side):
        image = self.json['sprites'][side]
        image_stream = urlopen(image).read()
        image_file = io.BytesIO(image_stream)
        self.image = pygame.image.load(image_file).convert_alpha()

        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height = self.image.get_height() * scale
        self.image = pygame.transform.scale(self.image, (int(new_width), int(new_height)))

    def draw(self, alpha=255):
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

def select_pokemon_screen():
    global player_pokemon, rival_pokemon

    selected_pokemon = None
    game_status = 'select_pokemon'

    while game_status == 'select_pokemon':
        for event in pygame.event.get():
            if event.type == QUIT:
                game_status = 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_cursor = pygame.mouse.get_pos()
                for pokemon in pokemons:
                    if pokemon.get_rect().collidepoint(mouse_cursor):
                        selected_pokemon = pokemon
                        game_status = 'select_pokemon'

        game.fill(K)

        for pokemon in pokemons:
            pokemon.draw()
            mouse_cursor = pygame.mouse.get_pos()
            if pokemon.get_rect().collidepoint(mouse_cursor):
                pygame.draw.rect(game, black, pokemon.get_rect(), 2)

        pygame.display.update()

    return selected_pokemon

# Positions x et y pour l'affichage des Pokémon
x_bulbasaur, y_bulbasaur = 50, 50
x_charmander, y_charmander = 200, 50
x_squirtle, y_squirtle = 350, 50
x_pikachu, y_pikachu = 500, 50
x_sandshrew, y_sandshrew = 50, 250
x_eevee, y_eevee = 200, 250
x_gengar, y_gengar = 350, 250
x_ivysaur, y_ivysaur = 500, 250
x_onix, y_onix = 50, 450
x_staryu, y_staryu = 200, 450
x_voltorb, y_voltorb = 350, 450
x_wartortle, y_wartortle = 500, 450

bulbasaur = Pokemon('Bulbasaur', 100, 30, 25, 15, ['Type1', 'Type2'], x_bulbasaur, y_bulbasaur)
charmander = Pokemon('Charmander', 90, 30, 25, 18, ['Type1', 'Type2'], x_charmander, y_charmander)
squirtle = Pokemon('Squirtle', 95, 30, 23, 20, ['Type1', 'Type2'], x_squirtle, y_squirtle)
pikachu = Pokemon('Pikachu', 85, 30, 30, 15, ['Type1'], x_pikachu, y_pikachu)
sandshrew = Pokemon('Sandshrew', 95, 30, 20, 25, ['Type1'], x_sandshrew, y_sandshrew)
eevee = Pokemon('Eevee', 80, 30, 20, 20, ['Type1'], x_eevee, y_eevee)
gengar = Pokemon('Gengar', 110, 35, 28, 22, ['Type1', 'Type2'], x_gengar, y_gengar)
ivysaur = Pokemon('Ivysaur', 105, 32, 26, 17, ['Type1', 'Type2'], x_ivysaur, y_ivysaur)
onix = Pokemon('Onix', 120, 40, 20, 30, ['Type1', 'Type2'], x_onix, y_onix)
staryu = Pokemon('Staryu', 90, 28, 35, 15, ['Type1'], x_staryu, y_staryu)
voltorb = Pokemon('Voltorb', 88, 30, 25, 28, ['Type1'], x_voltorb, y_voltorb)
wartortle = Pokemon('Wartortle', 98, 35, 30, 22, ['Type1'], x_wartortle, y_wartortle)
pokemons = [bulbasaur, charmander, squirtle, pikachu, sandshrew, eevee, gengar, ivysaur, onix, staryu, voltorb, wartortle]

def start_game():
    global player_pokemon, rival_pokemon , game_status
    game_status = 'select_pokemon'
    player_pokemon = select_pokemon_screen()
    rival_pokemon = get_random_rival(pokemons, player_pokemon)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_status = 'quit'

        if game_status == 'select_pokemon':
            player_pokemon = select_pokemon_screen()
            rival_pokemon = get_random_rival(pokemons, player_pokemon)
            game_status = 'select_pokemon'

        pygame.display.flip()

    pygame.quit()
