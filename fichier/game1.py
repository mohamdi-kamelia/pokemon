import pygame
import sys
import pytmx
import pyscroll
from pokemon import PokemonApp
from player import Player # Importation de la classe Player depuis le module player.py
from combat import CombatGUI, get_random_rival, load_pokedex, select_pokemon_screen # Importation de fonctions pour le combat depuis le module combat.py
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT  # Importation des touches directionnelles
# Classe principale représentant le jeu Pokémon
class Game:
    def __init__(self):
        # creer la fenetre du jeu 
        self.screen = pygame.display.set_mode((900, 750))
        pygame.display.set_caption('Pokemon')
        # Attribut pour suivre la carte actuelle ('world' ou 'house')
        self.map = 'world'
        # Chargement de la carte TMX
        tmx_data = pytmx.util_pygame.load_pygame('Map/carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # generer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)
        # Initialisation de la liste des rectangles de collision
        # definir une liste qui va stocker les rectangle
        self.walls = []
        # Recherche des objets de collision dans la carte TMX
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        # dessiner le groupe de calques avec le joueur
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # definir le rect de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)


    # tout le clay pour le joueur 
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
               
    # Méthode pour changer de carte vers l'intérieur de la maison
    def switch_house(self):

        # charger la carte (tmx) de la maison
        tmx_data = pytmx.util_pygame.load_pygame("Map/house.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1


        # Réinitialisation de la liste des rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques avec le joueur dans la maison
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # definir le rect de collision pour sortir deans la maison
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # recuperer du joueur dans la mison
        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 30

    def switch_world(self):
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("Map/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1


        # definir une liste qui va stocker les rectangle
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques avec le joueur dans le monde
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)


        # definir le rect de collision pour entrer devant la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # recuperer 
        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 30

        
        # Afficher un bouton pour démarrer le combat
        button_font = pygame.font.Font("photos/Pokemon Solid.ttf", 45)
        button_text = button_font.render("Start Combat", True, (255, 215, 0))
        button_rect = button_text.get_rect(center=(450, 375))
        button_font = pygame.font.Font("photos/Pokemon Solid.ttf", 45)
        return_button_text = button_font.render("Return to Map", True, (255, 215, 0))
        return_button_rect = return_button_text.get_rect(center=(450, 475))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        self.start_combat() 
                    elif return_button_rect.collidepoint(mouse_pos):
                        return  # Retour à la carte
    

            self.screen.fill((129, 178, 154))
            self.screen.blit(button_text, button_rect)
            self.screen.blit(return_button_text, return_button_rect)
            pygame.display.flip()
        
    def start_combat(self):

        pokemons = load_pokedex()
        pokemon_joueur = select_pokemon_screen(self.screen, pokemons, (129, 178, 154))
        pokemon_rival = get_random_rival(pokemons, pokemon_joueur)

        combat = CombatGUI(pokemon_joueur, pokemon_rival)
        combat.start_battle_gui()


    def update(self):
        self.group.update()

        # verifier l'entrer dans la maison
        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()


        # verifier l'entrer dans la maison
        if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'       

        # verifier l'entrer dans la maison
        if self.map == 'house' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = 'world'


        # verification collision 
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back() # revenir a position avent le déplassemant

    def run(self):
        clock = pygame.time.Clock()


        # boucle du jeu 
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:    
                    #if event.key == pygame.K_ESCAPE:
                        return     
            clock.tick(60)        
        pygame.quit()