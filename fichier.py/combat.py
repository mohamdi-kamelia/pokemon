import pygame
from pygame.locals import QUIT
from pygame import MOUSEBUTTONDOWN, Rect
import requests 
import io 
from urllib.request import urlopen
import random 
import time
import math
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

class Move():
    def __init__(self, url):
        
        # call the moves API endpoint
        req = requests.get(url)
        self.json = req.json()

        self.name = self.json['name']
        self.power = self.json['power']
        self.type = self.json['type']['name']

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
        #for i in range(len(self.json['types'])):
        for pokemon_type in self.json['types']:
            type_name = pokemon_type['type']['name']
            self.type.append(type_name)

        # définir la largeur du sprite
        self.size = 150

        #définir le sprite comme le sprite orienté vers l'avant
        self.set_sprite('front_default') 
    def perform_attack(self , other , move):
        display_message(f'{self.nom}used {move.nom}')
        time.sleep(2)

        damage = (2 * self.level + 10)/ 250 * self.attack /other.defense * move.power

        if move.type in self.types :
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

    def set_moves(self):
        self.moves = []

        # go through all moves from the api
        for move_info in self.json['moves']:
            # get the move from different game versions 
            versions = move_info['version_group_details']    
            for version in versions:

                # only get moves from red-blue version 
                if version['version_group']['name'] != 'red_blue':
                    continue

                # only get moves that can be learned from leveling up (i.e., exclude TM moves)
                learn_method = version['move_learn_method']['name']
                if learn_method != 'level_up':
                    continue

                # add move if pokemon level is high enough 
                level_learned = version['level_learned_at']
                if self.niveau >= level_learned:
                    move = Move(move_info['move']['url'])

                    # only include attack moves 
                    if move.power is not None:
                        self.moves.append(move)

        # select up to 4 random moves 
        if len(self.moves) > 4:
            self.moves = random.sample(self.moves, 4)
        



    def draw(self, alpha=255):
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    def draw_hp(self):
        bar_scale = 200 // self.max_hp
        for i in range(self.max_hp):
            bar = (self.hp_x + bar_scale * i ,self.hp_y , bar_scale , 20)
            pygame.draw.rect(game , red , bar)

        for i in range(self.current_hp):
            bar = (self.hp_x + bar_scale * i , self.hp_y , bar_scale , 20)
            pygame.draw.rect(game , green ,bar )

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.current_hp} / {self.max_hp}' , True , black)
        text_rect = text.get_rect()
        text_rect.x = self.hp_x
        text_rect.y =self.hp_y + 30
        game.blit(text , text_rect)


    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
def display_message(message):
    pygame.draw.rect(game , white ,(10 , 350 , 480 , 140))
    pygame.draw.rect(game, black, (10 , 350 , 480, 140),3)

    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = font.render(message , True , black)
    text_rect = text.get_rect()
    text_rect.x = 30
    text_rect.y = 410
    game.blit(text , text_rect)

    pygame.display.update()

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

        # detect mouse click
        if event.type == MOUSEBUTTONDOWN :
            # coordinates of the mouse click
            mouse_click = event.pos

            # for selection a pokemon
            if game_status == 'select pokemon':

                #check which pokemon was clicked on 
                for current_pokemon in pokemons:
                    if current_pokemon.get_rect().collidepoint(mouse_click):
                        # assign the player's and rival's pokemon 
                        player_pokemon = current_pokemon
                        rival_pokemon = pokemons[(pokemons.index(current_pokemon) + 1) % len(pokemons)]

                        # lower the rival pokemon's level to make the battle easier
                        rival_pokemon.niveau = int(rival_pokemon.niveau * .75)

                        # set the coordinates of the hp bars 
                        player_pokemon.hp_x = 275
                        player_pokemon.hp_y = 250
                        rival_pokemon.hp_x = 50
                        rival_pokemon.hp_y = 50

                        game_status = 'prebattle'
            elif game_status == 'player turn':
                if fight_button.rect.collidepoint(mouse_click):
                    game_status = 'player move'
                if position_button.rect.collidepoint(mouse_click):
                    if player_pokemon.num_potions == 0:
                        display_message('No more potions left')
                        time.sleep(2)
                        game_status ='rival turn'
                    else:
                        player_pokemon.use_potion()
                        display_message(f'{player_pokemon.nom}used potion')
                        time.sleep(2)
                        game_status = 'rival turn'
                    
            elif game_status == 'player move':
                for i in range(len(move_buttons)):
                    button = move_buttons[i]
                    if button.rect.collidepoint(mouse_click):###############
                        move = player_pokemon.moves[i]
                        player_pokemon.perform_attack(rival_pokemon , move)

                        if rival_pokemon.current_hp == 0:
                            game_status = 'fainted'
                        else:
                            game_status = 'rival turn'
                        


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

    # get moves from the API reposition the pokemons 
    if game_status == 'prebattle':

        # draw the selected pokemon 
        game.fill(white)
        player_pokemon.draw()
        pygame.display.update()


        player_pokemon.set_moves()
        rival_pokemon.set_moves()

        #reposition the pokemon
        player_pokemon.x = -50
        player_pokemon.y = 100
        rival_pokemon.x = 250
        rival_pokemon.y = -50

        # resize the sprites 
        player_pokemon.size = 300
        rival_pokemon.size = 300
        player_pokemon.set_sprite('back_default')
        rival_pokemon.set_sprite('front_default')

        game_status = 'start battle'  

    if game_status ==  'start battle':
        alpha = 0
        while alpha < 255:
            game.fill(white)
            rival_pokemon.draw(alpha)
            display_message(f'Rival sent out {rival_pokemon.nom}!')

            alpha += .4

            pygame.display.update()
        time.sleep(1)  

        alpha = 0 
        while alpha < 225:
            game.fill(white)
            rival_pokemon.draw()
            player_pokemon.draw(alpha)
            display_message(f'Go {player_pokemon.nom}')  
            alpha += .4

            pygame.display.update()

        player_pokemon.draw_hp()
        rival_pokemon.draw_hp()

        if rival_pokemon.speed > player_pokemon.speed:
            game_status = 'rival turn'
        else:
            game_status = 'player turn'

        pygame.display.update()

        time.sleep(1)
    
    if game_status == 'player turn':
        game.fill(white)
        player_pokemon.draw()
        rival_pokemon.draw()
        player_pokemon.draw_hp()
        rival_pokemon.draw_hp()

        fight_button = create_button(240 , 140 , 10 , 350 , 130 , 412 , 'Fight')
        position_button = create_button(240 , 140 , 250 , 350 , 370 , 412 , f'USE Potion ({player_pokemon.num_potions})')
        pygame.draw.rect(game , black , (10 , 350 , 480 , 140), 3)

        pygame.display.update()

    if game_status == 'player move':
        game.fill(white)
        player_pokemon.draw()
        rival_pokemon.draw()
        player_pokemon.draw_hp()
        rival_pokemon.draw_hp()

        move_buttons = []
        for i in range(len(player_pokemon.moves)):
            move = player_pokemon.moves[i]
            button_width = 240
            button_height = 70
            left = 10 + i % 2 * button_width
            top = 350 + i // 2 * button_height
            text_center_x = left + 120
            text_center_y = top + 35
            button = create_button(button_width, button_height, left, top, text_center_x, text_center_y, move.nom.capitalize())
            move_buttons.append(button)

        pygame.draw.rect(game, black, (10, 350, 480, 140), 3)
        pygame.display.update()

pygame.quit()



        
