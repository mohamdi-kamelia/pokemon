import pygame
import requests
import io
from urllib.request import urlopen
import json
import random
import time

black = (0, 0, 0)
white = (255, 255, 255)

base_url = 'https://pokeapi.co/api/v2'
pygame.mixer.init()
pygame.mixer.music.load('photos/PKMN_Surfing.mid')  
pygame.mixer.music.play(-1) 

class Type:
    def __init__(self, type_name):
        self.type_name = type_name

class CombatGUI:
    def __init__(self, player_pokemon, rival_pokemon):
        # Initialisation de l'interface graphique du combat
        self.player_pokemon = player_pokemon
        self.rival_pokemon = rival_pokemon
        self.width = 800
        self.height = 600
        self.game_display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pokemon Combat")
        self.background_image = pygame.image.load("photos/arriére plan battle.png") 
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

    # Méthode pour dessiner un Pokémon sur l'écran de combat
    def draw_pokemon(self, pokemon, x, y):
        pokemon.draw(self.game_display, x, y)
    
    # Méthode pour dessiner la barre de santé d'un Pokémon
    def draw_health_bar(self, pokemon, x, y):
        rect_width = int(pokemon.points_de_vie / pokemon.max_points_de_vie * 100)
        pygame.draw.rect(self.game_display, (0, 255, 0), [x, y, rect_width, 10])

    # Méthode pour afficher le texte de la santé d'un Pokémon
    def draw_health_text(self, pokemon, x, y):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(f"PV: {pokemon.points_de_vie}/{pokemon.max_points_de_vie}", True, white)
        self.game_display.blit(text_surface, (x, y))
    
    # Méthode pour dessiner l'écran de combat avec les Pokémon et leurs informations
    def draw_battle_screen(self):
        self.game_display.blit(self.background_image, (0, 0))  
        self.draw_pokemon(self.player_pokemon, 100, 400)   
        self.draw_health_bar(self.player_pokemon, 100, 380)  
        self.draw_health_text(self.player_pokemon, 100, 360)  # Affichage des PV du joueur
        self.draw_pokemon(self.rival_pokemon, 500, 200)  
        self.draw_health_bar(self.rival_pokemon, 500, 180)  
        self.draw_health_text(self.rival_pokemon, 500, 160)  # Affichage des PV du rival
        self.draw_buttons()  
        pygame.display.update()

    # Méthode pour dessiner du texte sur l'écran de combat
    def draw_text(self, text, x, y, color=(255, 255, 255)):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, color)
        self.game_display.blit(text_surface, (x, y))

    # Méthode pour afficher un message spécifique sur l'écran de combat
    def draw_message(self, message):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(message, True, white)
        self.game_display.blit(text_surface, (300, 300))


    def draw_buttons(self):
        # Dessine les boutons sur l'écran
        button_font = pygame.font.SysFont(None, 20)
        
        # Bouton d'attaque
        pygame.draw.rect(self.game_display,  (225, 225, 255), [50, 500, 100, 50])
        attack_text = button_font.render("Attaquer", True, black)
        self.game_display.blit(attack_text, (65, 515))
        
        # Bouton de potion
        pygame.draw.rect(self.game_display,  (225, 225, 255), [200, 500, 100, 50])
        potion_text = button_font.render("Potion", True, black)
        self.game_display.blit(potion_text, (225, 515))
        
        # Bouton de fuite
        pygame.draw.rect(self.game_display, (225, 225, 255), [350, 500, 100, 50])
        flee_text = button_font.render("Fuir", True, black)
        self.game_display.blit(flee_text, (380, 515))

    def handle_button_click(self, mouse_pos):
        # Gère les clics de souris sur les boutons
        x, y = mouse_pos

        # Vérifie si le clic de souris est sur un bouton
        if 50 <= x <= 150 and 500 <= y <= 550:  # Bouton Attaquer
            player_damage = self.calculate_damage(self.player_pokemon, self.rival_pokemon)
            self.apply_damage(self.rival_pokemon, player_damage)
            self.draw_text(f"{self.player_pokemon.nom} inflige {player_damage} dégâts à {self.rival_pokemon.nom}", 10, 10)
        elif 200 <= x <= 300 and 500 <= y <= 550:  # Bouton Potion
            if self.player_pokemon.num_potions > 0:
                # Augmente les points de vie du joueur et réduit le nombre de potions
                self.player_pokemon.points_de_vie += 20  # Par exemple, augmente de 20 points de vie
                self.player_pokemon.num_potions -= 1  # Réduit le nombre de potions
                self.draw_text("Vous avez utilisé une potion!", 10, 50)
            else:
                self.draw_text("Vous n'avez plus de potions!", 10, 50)
        elif 350 <= x <= 450 and 500 <= y <= 550:  # Bouton Fuir
            self.draw_text("Vous avez fui le combat!", 10, 50)
            pygame.quit()
            quit()


    def start_battle_gui(self):
        self.draw_message("Un combat commence!")  # Afficher le message de début de combat
        pygame.display.update()
        clock = pygame.time.Clock()
        player_turn = True  # Détermine si c'est le tour du joueur

        while True:
            self.handle_events()

            if player_turn:
                player_damage = self.calculate_damage(self.player_pokemon, self.rival_pokemon)
                self.apply_damage(self.rival_pokemon, player_damage)
                self.draw_text(f"{self.player_pokemon.nom} inflige {player_damage} dégâts à {self.rival_pokemon.nom}", 10, 10)
                time.sleep(2)  # Pause pour que le joueur puisse voir les dégâts infligés
            else:
                rival_damage = self.calculate_damage(self.rival_pokemon, self.player_pokemon)
                self.apply_damage(self.player_pokemon, rival_damage)
                self.draw_text(f"{self.rival_pokemon.nom} inflige {rival_damage} dégâts à {self.player_pokemon.nom}", 10, 30)
                time.sleep(2)  # Pause pour que le joueur puisse voir les dégâts infligés

            self.draw_battle_screen()
            self.draw_buttons()  # Dessiner les boutons

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_button_click(mouse_pos)

            if self.player_pokemon.points_de_vie <= 0 or self.rival_pokemon.points_de_vie <= 0:
                winner = self.determine_winner()
                self.draw_text(f"{winner} a gagné le combat!", 10, 50)
                self.record_in_pokedex()
                pygame.display.update()  # Met à jour l'affichage pour afficher le vainqueur
                time.sleep(2)  # Attend 2 secondes avant de fermer la fenêtre
                pygame.quit()  # Ferme la fenêtre de jeu
                quit()  # Quitte le programme

            player_turn = not player_turn  # Passage au tour suivant
            clock.tick(1)

    # Méthode pour gérer les événements (ex: fermeture de la fenêtre)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    # Méthode pour calculer les dégâts infligés par un Pokémon à un autre
    def calculate_damage(self, attacker, defender):
        type_multiplier = self.get_type_multiplier(attacker, defender)
        damage = int(attacker.puissance_attaque * type_multiplier) - defender.defense
        return max(damage, 0)

    # Méthode pour obtenir le multiplicateur de type entre deux Pokémon
    def get_type_multiplier(self, attacker, defender):
        # Dictionnaire contenant les multiplicateurs de type pour chaque combinaison de types
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
    # Méthode pour appliquer des dégâts à un Pokémon donné.
    def apply_damage(self, pokemon, damage):
        pokemon.points_de_vie -= damage
    # Méthode pour déterminer le vainqueur du combat.
    def determine_winner(self):
        if self.player_pokemon.points_de_vie <= 0:
            return self.rival_pokemon.nom
        elif self.rival_pokemon.points_de_vie <= 0:
            return self.player_pokemon.nom
        else:
            return "Aucun vainqueur"
    # Méthode pour enregistrer le Pokémon du joueur dans le Pokédex.
    def record_in_pokedex(self):
        if self.player_pokemon not in self.player_pokemon.pokedex:
            self.player_pokemon.pokedex.append(self.player_pokemon)
            print(f"{self.player_pokemon.nom} ajouté au Pokédex!")
# Classe représentant un choix de Pokémon avec ses attributs.
# Inclut également des méthodes pour charger une image de sprite et la dessiner.
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
    # Méthode pour charger une image de sprite en fonction du côté donné (front_default dans ce cas).
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
    # Méthode pour dessiner le sprite du Pokémon à une position donnée.
    def draw(self, game, x, y, alpha=255):
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (x, y))
    # Méthode pour obtenir le rectangle englobant du sprite du Pokémon.
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
# Fonction pour choisir un Pokémon rival au hasard parmi les options disponibles.
def get_random_rival(pokemons, player_pokemon):
    rival_options = [p for p in pokemons if p != player_pokemon]
    return random.choice(rival_options)
# Fonction pour charger les données des Pokémon à partir d'un fichier JSON et les convertir en instances de la classe choix.
def load_pokedex():
    with open('pokedex.json', 'r') as file:
        data = json.load(file)

    return [choix(**entry) for entry in data['pokemons']]

def main():
    pygame.init()

    game_width = 700
    game_height = 700
    size = (game_width, game_height)
    game = pygame.display.set_mode(size)  # Initialise la fenêtre de jeu
    pygame.display.set_caption("Pokemon") # Définit le titre de la fenêtre

    K = (129, 178, 154)   # Couleur d'arrière-plan

    pokemons = load_pokedex() # Charge les Pokémon depuis le fichier pokedex.json
    player_pokemon = None
    # Boucle pour sélectionner un Pokémon tant qu'aucun n'est sélectionné
    while not player_pokemon:
        player_pokemon = select_pokemon_screen(game, pokemons, K)

    rival_pokemon = get_random_rival(pokemons, player_pokemon) # Sélectionne un Pokémon rival aléatoire

    combat = CombatGUI(player_pokemon, rival_pokemon) # Initialise l'interface de combat
    combat.start_battle_gui() # Lance le combat

    pygame.quit() # Quitte Pygame après la fin du jeu
# Fonction pour sélectionner un Pokémon à affronter
def select_pokemon_screen(game, pokemons, K):
    selected_pokemon = None
    game_status = 'select_pokemon'
    # Boucle pour la sélection du Pokémon
    while game_status == 'select_pokemon':
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_cursor = pygame.mouse.get_pos()
                for pokemon in pokemons:
                    if pokemon.get_rect().collidepoint(mouse_cursor):
                        selected_pokemon = pokemon
                        game_status = 'start_battle'

        game.fill(K)  # Remplit l'écran de jeu avec la couleur d'arrière-plan
        # Dessine les Pokémon disponibles à sélectionner
        for pokemon in pokemons:
            pokemon.draw(game, pokemon.x, pokemon.y)
            mouse_cursor = pygame.mouse.get_pos()
            if pokemon.get_rect().collidepoint(mouse_cursor):
                pygame.draw.rect(game, black, pokemon.get_rect(), 2) # Met en surbrillance le Pokémon survolé

        pygame.display.update()  # Met à jour l'affichage

    return selected_pokemon  # Retourne le Pokémon sélectionné

if __name__ == "__main__":
    main()

