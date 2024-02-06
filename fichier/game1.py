import pygame
import sys
import pytmx
import pyscroll
from player import Player
from combat import CombatGUI, get_random_rival, load_pokedex, select_pokemon_screen
from pokemon import PokemonApp
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
import requests
import io
from urllib.request import urlopen
import json
import random

black = (0, 0, 0)
white = (255, 255, 255)

base_url = 'https://pokeapi.co/api/v2'

class Type:
    def __init__(self, type_name):
        self.type_name = type_name

class CombatGUI:
    def __init__(self, player_pokemon, rival_pokemon):
        self.player_pokemon = player_pokemon
        self.rival_pokemon = rival_pokemon
        self.width = 800
        self.height = 600
        self.game_display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pokemon Combat")
        self.background_image = pygame.image.load("photos/arriére plan battle.png") 
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

    def draw_pokemon(self, pokemon, x, y):
        pokemon.draw(self.game_display, x, y)

    def draw_health_bar(self, pokemon, x, y):
        rect_width = int(pokemon.points_de_vie / pokemon.max_points_de_vie * 100)
        pygame.draw.rect(self.game_display, (0, 255, 0), [x, y, rect_width, 10])

    def draw_battle_screen(self):
        self.game_display.blit(self.background_image, (0, 0))  
        self.draw_pokemon(self.player_pokemon, 100, 400)   
        self.draw_health_bar(self.player_pokemon, 100, 380)  
        self.draw_pokemon(self.rival_pokemon, 500, 200)  
        self.draw_health_bar(self.rival_pokemon, 500, 180)  
        pygame.display.update()

    def start_battle_gui(self):
        print("Un combat commence!")
        clock = pygame.time.Clock()

        while True:
            self.handle_events()
            player_damage = self.calculate_damage(self.player_pokemon, self.rival_pokemon)
            rival_damage = self.calculate_damage(self.rival_pokemon, self.player_pokemon)

            self.apply_damage(self.rival_pokemon, player_damage)
            self.apply_damage(self.player_pokemon, rival_damage)

            self.draw_battle_screen()

            print(f"{self.player_pokemon.nom} inflige {player_damage} dégâts à {self.rival_pokemon.nom}")
            print(f"{self.rival_pokemon.nom} inflige {rival_damage} dégâts à {self.player_pokemon.nom}")

            if self.player_pokemon.points_de_vie <= 0 or self.rival_pokemon.points_de_vie <= 0:
                winner = self.determine_winner()
                print(f"{winner} a gagné le combat!")
                self.record_in_pokedex()
                pygame.quit()
                quit()

            clock.tick(1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player_attack()

    def player_attack(self):
        print(f"{self.player_pokemon.nom} utilise une attaque spéciale!")
        special_damage = self.calculate_special_damage(self.player_pokemon, self.rival_pokemon)
        self.apply_damage(self.rival_pokemon, special_damage)

    def calculate_damage(self, attacker, defender):
        type_multiplier = self.get_type_multiplier(attacker, defender)
        damage = int(attacker.puissance_attaque * type_multiplier) - defender.defense
        return max(damage, 0)

    def calculate_special_damage(self, attacker, defender):
        type_multiplier = self.get_type_multiplier(attacker, defender)
        special_damage = int(attacker.puissance_attaque * type_multiplier * 1.5) - defender.defense
        return max(special_damage, 0)

    def get_type_multiplier(self, attacker, defender):
        type_multiplier_table = {
            "Feu": {"Eau": 0.5, "Terre": 2.0, "Feu": 1.0, "Normal": 1},
            "Eau": {"Eau": 1.0, "Terre": 0.5, "Feu": 2.0, "Normal": 1},
            "Terre": {"Eau": 2.0, "Terre": 1.0, "Feu": 1.0, "Normal": 1},
            "Normal": {"Eau": 0.75, "Terre": 0.75, "Feu": 0.75, "Normal": 1}
        }

        attacker_types = attacker.type
        defender_types = defender.type

        type_multiplier = 1.0  # Valeur par défaut

        for attacker_type in attacker_types:
            for defender_type in defender_types:
                if attacker_type in type_multiplier_table and defender_type in type_multiplier_table[attacker_type]:
                    type_multiplier *= type_multiplier_table[attacker_type][defender_type]

        return type_multiplier

    def apply_damage(self, pokemon, damage):
        pokemon.points_de_vie -= damage

    def determine_winner(self):
        if self.player_pokemon.points_de_vie <= 0:
            return self.rival_pokemon.nom
        elif self.rival_pokemon.points_de_vie <= 0:
            return self.player_pokemon.nom
        else:
            return "Aucun vainqueur"

    def record_in_pokedex(self):
        if self.player_pokemon not in self.player_pokemon.pokedex:
            self.player_pokemon.pokedex.append(self.player_pokemon)
            print(f"{self.player_pokemon.nom} ajouté au Pokédex!")

class Pokemon(pygame.sprite.Sprite):
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

def get_random_rival(pokemons, player_pokemon):
    rival_options = [p for p in pokemons if p != player_pokemon]
    return random.choice(rival_options)

def load_pokedex():
    with open('pokedex.json', 'r') as file:
        data = json.load(file)

    return [Pokemon(**entry) for entry in data['pokemons']]

def main():
    pygame.init()

    game_width = 700
    game_height = 700
    size = (game_width, game_height)
    game = pygame.display.set_mode(size)
    pygame.display.set_caption("Pokemon")

    K = (129, 178, 154)

    pokemons = load_pokedex()
    player_pokemon = None

    while not player_pokemon:
        player_pokemon = select_pokemon_screen(game, pokemons, K)

    rival_pokemon = get_random_rival(pokemons, player_pokemon)

    combat = CombatGUI(player_pokemon, rival_pokemon)
    combat.start_battle_gui()

    pygame.quit()

def select_pokemon_screen(game, pokemons, K):
    selected_pokemon = None
    game_status = 'select_pokemon'

    while game_status == 'select_pokemon':
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_cursor = pygame.mouse.get_pos()
                for pokemon in pokemons:
                    if pokemon.get_rect().collidepoint(mouse_cursor):
                        selected_pokemon = pokemon
                        game_status = 'start_battle'

        game.fill(K)

        for pokemon in pokemons:
            pokemon.draw(game, pokemon.x, pokemon.y)
            mouse_cursor = pygame.mouse.get_pos()
            if pokemon.get_rect().collidepoint(mouse_cursor):
                pygame.draw.rect(game, black, pokemon.get_rect(), 2)

        pygame.display.update()

    return selected_pokemon

class Game:
    def __init__(self):
        # Créer la fenêtre du jeu 
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Pokemon')

        self.map = 'world'
        # Charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('Map/carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # Générer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # Définir une liste qui va stocker les rectangles
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # Définir le rect de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    # Toutes les méthodes pour le joueur 
    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')    

    def switch_house(self):

        # Charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("Map/house.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # Définir une liste qui va stocker les rectangles
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # Définir le rect de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # Récupérer le point de spawn dans la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 30

    def switch_world(self):
        # Charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("Map/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # Définir une liste qui va stocker les rectangles
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # Définir le rect de collision pour entrer devant la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # Récupérer le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 30

        # Afficher un bouton pour démarrer le combat
        button_font = pygame.font.Font("photos/Pokemon Solid.ttf", 45)
        button_text = button_font.render("Start Combat", True, (255, 215, 0))
        button_rect = button_text.get_rect(center=(400, 300))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        self.start_combat() 

            self.screen.fill((129, 178, 154))
            self.screen.blit(button_text, button_rect)
            pygame.display.flip()
        
    def start_combat(self):

        pokemons = load_pokedex()
        pokemon_joueur = select_pokemon_screen(self.screen, pokemons, (255, 255, 255))
        pokemon_rival = get_random_rival(pokemons, pokemon_joueur)

        combat = CombatGUI(pokemon_joueur, pokemon_rival)
        combat.start_battle_gui()

    def update(self):
        self.group.update()

        # Vérifier l'entrée dans la maison
        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()


        # Vérifier l'entrée dans la maison
        if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'       

        # Vérifier l'entrée dans la maison
        if self.map == 'house' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = 'world'


        # Vérification collision 
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back() # Revenir à position avant le déplacement


    def run(self):
        clock = pygame.time.Clock()


        # Boucle du jeu 
        running = True

        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)        
        pygame.quit()

if __name__ == "__main__":
    main()
