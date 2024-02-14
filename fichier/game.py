import pygame
from pygame.locals import QUIT
import json
import requests
import io
from urllib.request import urlopen
from combat import *

pygame.init()

game_width = 900
game_height = 750
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption("Pokemon")

black = (0, 0, 0)
K = (129, 178, 154)

# Charger les données des Pokémon depuis le fichier pokemon.json
def load_pokemon_data():
    with open('pokemon.json', 'r') as file:
        pokemon_data = json.load(file)
    return pokemon_data['pokemon_list']

pokemon_list = load_pokemon_data()

# Liste des types de Pokémon
TYPES = [Type("Normal"), Type("Feu"), Type("Eau"), Type("Terre"), Type("Electric")]

# Classe pour représenter un Pokémon
class Pokemon(pygame.sprite.Sprite):
    def __init__(self, nom, points_de_vie, niveau, puissance_attaque, defense, types, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # Attributs du Pokémon
        self.nom = nom
        self.points_de_vie = points_de_vie
        self.puissance_attaque = puissance_attaque
        self.defense = defense
        self.type = [Type(type_name) for type_name in types]

        # Recherche du Pokémon dans la liste chargée depuis pokemon.json
        pokemon_info = next((p for p in pokemon_list if p['name'] == self.nom), None)
        if pokemon_info:
            self.image_url = pokemon_info['image_url']
        else:
            self.image_url = 'https://via.placeholder.com/150'  # URL de secours si le Pokémon n'est pas trouvé

        # Obtention de l'image du Pokémon
        image_stream = urlopen(self.image_url).read()
        image_file = io.BytesIO(image_stream)
        self.image = pygame.image.load(image_file).convert_alpha()

        # Autres attributs du Pokémon
        self.niveau = niveau
        self.x = x
        self.y = y
        self.num_potions = 3

        # Calcul des statistiques de santé basées sur le niveau du Pokémon
        self.current_hp = points_de_vie + self.niveau
        self.max_hp = points_de_vie + self.niveau

    # Méthode pour dessiner le sprite du Pokémon
    def draw(self, alpha=255):
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    # Méthode pour obtenir le rectangle englobant du sprite du Pokémon
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

# Fonction pour l'écran de sélection des Pokémon
def select_pokemon_screen():
    global pokemons
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
pokemon_positions = [
    (50, 50), (200, 50), (350, 50), (500, 50),
    (50, 250), (200, 250), (350, 250), (500, 250),
    (50, 450), (200, 450), (350, 450), (500, 450)
]

pokemons = []
for i, pokemon_info in enumerate(pokemon_list):
    x, y = pokemon_positions[i]
    pokemon = Pokemon(
        nom=pokemon_info['name'],
        points_de_vie=pokemon_info['hp'],
        niveau=30,  # Niveau par défaut
        puissance_attaque=pokemon_info['attack'],
        defense=pokemon_info['defense'],
        types=pokemon_info['types'],
        x=x,
        y=y
    )
    pokemons.append(pokemon)

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

if __name__ == "__main__":
    start_game()