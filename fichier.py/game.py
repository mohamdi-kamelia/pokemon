import pygame
from pygame.locals import QUIT
from pygame import Rect
import requests 
import io 
from urllib.request import urlopen 
import random

pygame.init()

game_width = 700
game_height = 700
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption("Pokemon")

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
                        rival_pokemon = get_random_rival(pokemons, selected_pokemon)
                        game_status = 'battle'

        game.fill(K)

        bulbasaur.draw()
        charmander.draw()
        squirtle.draw()
        pikachu.draw()
        eevee.draw()
        sandshrew.draw()

        mouse_cursor = pygame.mouse.get_pos()
        for pokemon in pokemons:
            if pokemon.get_rect().collidepoint(mouse_cursor):
                pygame.draw.rect(game, black, pokemon.get_rect(), 2)

        pygame.display.update()

    return selected_pokemon
def get_random_rival(pokemons, player_pokemon):
    # Choisir un Pokémon aléatoire qui n'est pas le Pokémon du joueur
    rival_options = [p for p in pokemons if p != player_pokemon]
    return random.choice(rival_options)

def battle_screen(player_pokemon, rival_pokemon):
    game_status = 'battle'
    player_turn = True  # Indique si c'est le tour du joueur

    while game_status == 'battle':
        for event in pygame.event.get():
            if event.type == QUIT:
                game_status = 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player_turn:
                    # Logique des actions du joueur
                    mouse_x, mouse_y = event.pos

                    # Supposez que vous ayez des boutons pour différentes attaques
                    attack_button_rect = pygame.Rect(50, 500, 150, 50)
                    if attack_button_rect.collidepoint(mouse_x, mouse_y):
                        # Exécutez l'attaque du joueur
                        damage = calculate_damage(player_pokemon, rival_pokemon)
                        apply_damage(rival_pokemon, damage)

                        # Vérifiez s'il y a un vainqueur
                        winner = determine_winner(player_pokemon, rival_pokemon)
                        if winner:
                            print(f"{winner} a gagné le combat!")
                            record_in_pokedex(player_pokemon, rival_pokemon)
                            game_status = 'select_pokemon'  # Retour à l'écran de sélection après le combat

                        player_turn = False  # Passer au tour du rival

        # Dessinez l'écran de combat ici
        draw_battle_screen(player_pokemon, rival_pokemon, player_turn)
        pygame.display.flip()
    pygame.quit()

def calculate_damage(attacker, defender):
    # Logique pour calculer les dégâts en fonction des attributs des Pokémon
    damage = attacker.puissance_attaque - defender.defense
    return max(damage, 0)  # Les dégâts ne peuvent pas être négatifs

def apply_damage(pokemon, damage):
    # Logique pour appliquer les dégâts au Pokémon
    pokemon.points_de_vie -= damage

def determine_winner(player_pokemon, rival_pokemon):
    # Logique pour déterminer le vainqueur du combat
    if player_pokemon.points_de_vie <= 0:
        return "Le Pokémon rival"
    elif rival_pokemon.points_de_vie <= 0:
        return "Le Pokémon joueur"
    return None  # Le combat continue

def record_in_pokedex(player_pokemon, rival_pokemon):
    # Logique pour enregistrer le Pokémon rencontré dans le Pokédex du joueur
    if player_pokemon not in player_pokemon.pokedex:
        player_pokemon.pokedex.append(player_pokemon)
        print(f"{player_pokemon.nom} ajouté au Pokédex!")

def draw_battle_screen(player_pokemon, rival_pokemon, player_turn):
    # Effacer l'écran
    game.fill(white)

    # Dessiner les images des Pokémon
    player_pokemon.draw()
    rival_pokemon.draw()

    # Dessiner les barres de vie
    draw_health_bar(player_pokemon, (50, 550))
    draw_health_bar(rival_pokemon, (400, 50))

    # Afficher le texte du tour
    font = pygame.font.Font(None, 36)
    if player_turn:
        text = font.render("C'est votre tour!", True, black)
    else:
        text = font.render("Tour du Pokémon rival", True, black)

    game.blit(text, (50, 500))

    # Mettre à jour l'affichage
    pygame.display.update()

def draw_health_bar(pokemon, position):
    # Dessiner une barre de vie en fonction des points de vie du Pokémon
    bar_width = 200
    bar_height = 20
    health_ratio = pokemon.points_de_vie / pokemon.max_hp
    health_bar_width = int(bar_width * health_ratio)

    pygame.draw.rect(game, green, (*position, bar_width, bar_height))
    pygame.draw.rect(game, red, (*position, bar_width - health_bar_width, bar_height))


# Positions x et y pour l'affichage des Pokémon
x_bulbasaur, y_bulbasaur = 50, 50
x_charmander, y_charmander = 200, 50
x_squirtle, y_squirtle = 350, 50
x_pikachu, y_pikachu = 500, 50
x_sandshrew, y_sandshrew = 50, 250
x_eevee, y_eevee = 200, 250

bulbasaur = Pokemon('Bulbasaur', 100, 30, 25, 15, ['Type1', 'Type2'], x_bulbasaur, y_bulbasaur)
charmander = Pokemon('Charmander', 90, 30, 25, 18, ['Type1', 'Type2'], x_charmander, y_charmander)
squirtle = Pokemon('Squirtle', 95, 30, 23, 20, ['Type1', 'Type2'], x_squirtle, y_squirtle)
pikachu = Pokemon('Pikachu', 85, 30, 30, 15, ['Type1'], x_pikachu, y_pikachu)
sandshrew = Pokemon('Sandshrew', 95, 30, 20, 25, ['Type1'], x_sandshrew, y_sandshrew)
eevee = Pokemon('Eevee', 80, 30, 20, 20, ['Type1'], x_eevee, y_eevee)
pokemons = [bulbasaur, charmander, squirtle, pikachu, sandshrew, eevee]
def start_game():
    global player_pokemon, rival_pokemon
    player_pokemon = select_pokemon_screen()
    rival_pokemon = get_random_rival(pokemons, player_pokemon)
    battle_screen(player_pokemon, rival_pokemon)

    while game_status != 'quit':
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_status = 'quit'

            if game_status == 'select_pokemon':
                player_pokemon = select_pokemon_screen()
                rival_pokemon = get_random_rival(pokemons, player_pokemon)
                game_status = 'battle'
            elif game_status == 'battle':
                battle_screen(player_pokemon, rival_pokemon)
                game_status = 'select_pokemon'
    pygame.quit()

