import pygame  # Importation de la bibliothèque Pygame pour créer l'interface graphique
from urllib.request import urlopen  # Importation de la fonction urlopen pour effectuer des requêtes HTTP
import json  # Importation du module json pour travailler avec des données JSON
import random  # Importation du module random pour générer des nombres aléatoires
import time  # Importation du module time pour gérer le temps dans le jeu
from choix import *  # Importation de la classe 'choix', mais elle n'est pas utilisée dans ce code

# Définition des constantes de couleur pour une utilisation ultérieure dans le code
black = (0, 0, 0)
white = (255, 255, 255)

# URL de base pour l'API des Pokémon, mais non utilisée dans ce code
base_url = 'https://pokeapi.co/api/v2'

# Initialisation de Pygame et chargement de la musique de fond
pygame.mixer.init()
pygame.mixer.music.load('photos/PkmRB-Enc2.mid')
pygame.mixer.music.play(-1)

# Définition de la classe Type (représentant les types de Pokémon)
class Type:
    def __init__(self, type_name):  # Initialisation de la classe avec le nom du type de Pokémon
        self.type_name = type_name  # Assignation du nom du type

# Définition de la classe CombatGUI pour gérer l'interface du combat Pokémon
class CombatGUI:
    def __init__(self, player_pokemon, rival_pokemon):  # Initialisation de la classe avec les Pokémon du joueur et du rival
        self.player_pokemon = player_pokemon  # Assignation du Pokémon du joueur
        self.rival_pokemon = rival_pokemon  # Assignation du Pokémon rival
        self.width = 800  # Largeur de la fenêtre de jeu
        self.height = 600  # Hauteur de la fenêtre de jeu
        # Initialisation de la fenêtre de jeu avec la largeur et la hauteur spécifiées
        self.game_display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pokemon Combat")  # Définition du titre de la fenêtre
        # Chargement de l'image d'arrière-plan et redimensionnement pour correspondre à la taille de la fenêtre
        self.background_image = pygame.image.load("photos/arriére plan battle.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

    # Méthode pour dessiner un Pokémon à une position spécifique sur l'écran
    def draw_pokemon(self, pokemon, x, y):
        pokemon.draw(self.game_display, x, y)
    
    # Méthode pour dessiner la barre de santé d'un Pokémon à une position spécifique sur l'écran
    def draw_health_bar(self, pokemon, x, y):
        rect_width = int(pokemon.points_de_vie / pokemon.max_points_de_vie * 100)
        pygame.draw.rect(self.game_display, (0, 255, 0), [x, y, rect_width, 10])

    # Méthode pour afficher le texte de santé d'un Pokémon à une position spécifique sur l'écran
    def draw_health_text(self, pokemon, x, y):
        font = pygame.font.SysFont("photos/Pokemon Solid.ttf", 24)
        text_surface = font.render(f"PV: {pokemon.points_de_vie}/{pokemon.max_points_de_vie}", True, white)
        self.game_display.blit(text_surface, (x, y))
    
    # Méthode pour dessiner l'écran de combat avec les Pokémon, les barres de santé et les boutons
    def draw_battle_screen(self):
        self.game_display.blit(self.background_image, (0, 0))  # Dessin de l'arrière-plan
        self.draw_pokemon(self.player_pokemon, 100, 400)  # Dessin du Pokémon du joueur
        self.draw_health_bar(self.player_pokemon, 100, 380)  # Dessin de la barre de santé du Pokémon du joueur
        self.draw_health_text(self.player_pokemon, 100, 360)  # Affichage du texte de santé du Pokémon du joueur
        self.draw_pokemon(self.rival_pokemon, 500, 200)  # Dessin du Pokémon rival
        self.draw_health_bar(self.rival_pokemon, 500, 180)  # Dessin de la barre de santé du Pokémon rival
        self.draw_health_text(self.rival_pokemon, 500, 160)  # Affichage du texte de santé du Pokémon rival
        self.draw_buttons()  # Dessin des boutons d'action
        pygame.display.update()  # Mise à jour de l'affichage de la fenêtre de jeu

    # Méthode pour dessiner du texte à une position spécifique sur l'écran
    def draw_text(self, text, x, y, color=(255, 255, 255)):
        font = pygame.font.SysFont(None, 24)  # Définition de la police de caractères
        text_surface = font.render(text, True, color)  # Création d'une surface de texte avec la police spécifiée
        self.game_display.blit(text_surface, (x, y))  # Affichage du texte sur l'écran

    # Méthode pour afficher un message au centre de l'écran
    def draw_message(self, message):
        font = pygame.font.SysFont(None, 24)  # Définition de la police de caractères
        text_surface = font.render(message, True, white)  # Création d'une surface de texte avec le message spécifié
        self.game_display.blit(text_surface, (300, 300))  # Affichage du message au centre de l'écran

    # Méthode pour dessiner les boutons d'action (Attaquer, Potion, Fuir)
    def draw_buttons(self):
        button_font = pygame.font.SysFont("Arial", 20)  # Définition de la police de caractères pour les boutons
        
        # Dessin du bouton "Attaquer"
        pygame.draw.rect(self.game_display,  (129, 178, 154), [75, 525, 100, 50])
        attack_text = button_font.render("Attaquer", True, black)
        self.game_display.blit(attack_text, (90, 540))
        
        # Dessin du bouton "Potion"
        pygame.draw.rect(self.game_display,  (129, 178, 154), [225, 525, 100, 50])
        potion_text = button_font.render("Potion", True, black)
        self.game_display.blit(potion_text, (250, 540))
        
        # Dessin du bouton "Fuir"
        pygame.draw.rect(self.game_display, (129, 178, 154), [375, 525, 100, 50])
        flee_text = button_font.render("Fuir", True, black)
        self.game_display.blit(flee_text, (405, 540))

    # Méthode pour gérer les clics de souris sur les boutons d'action
    def handle_button_click(self, mouse_pos):
        x, y = mouse_pos  # Récupération de la position du clic de souris

        # Vérification du clic sur le bouton "Attaquer"
        if 50 <= x <= 150 and 500 <= y <= 550:  
            player_damage = self.calculate_damage(self.player_pokemon, self.rival_pokemon)  # Calcul des dégâts infligés par le joueur
            self.apply_damage(self.rival_pokemon, player_damage)  # Application des dégâts au Pokémon rival
            self.draw_text(f"{self.player_pokemon.nom} inflige {player_damage} dégâts à {self.rival_pokemon.nom}", 10, 10)  # Affichage du message de dégâts
        # Vérification du clic sur le bouton "Potion"
        elif 200 <= x <= 300 and 500 <= y <= 550:  
            if self.player_pokemon.num_potions > 0:  # Vérification si le joueur a des potions disponibles
                self.player_pokemon.points_de_vie += 20  # Ajout de points de vie au Pokémon du joueur
                self.player_pokemon.num_potions -= 1  # Réduction du nombre de potions du joueur
                self.draw_text("Vous avez utilisé une potion!", 10, 50)  # Affichage du message d'utilisation de la potion
            else:
                self.draw_text("Vous n'avez plus de potions!", 10, 50)  # Affichage du message si le joueur n'a plus de potions
        # Vérification du clic sur le bouton "Fuir"
        elif 350 <= x <= 450 and 500 <= y <= 550:  
            self.draw_text("Vous avez fui le combat!", 10, 50)  # Affichage du message de fuite du combat
            pygame.quit()  # Fermeture de Pygame
            quit()  # Fermeture du programme

    # Méthode pour démarrer l'interface graphique du combat
    def start_battle_gui(self):
        self.draw_message("Un combat commence!")  # Affichage du message de début de combat
        pygame.display.update()  # Mise à jour de l'affichage de la fenêtre de jeu
        clock = pygame.time.Clock()  # Initialisation de l'horloge pour contrôler la vitesse du jeu
        player_turn = True  # Initialisation du tour du joueur à True

        while True:  # Boucle principale du jeu
            self.handle_events()  # Gestion des événements Pygame

            if player_turn:  # Si c'est le tour du joueur
                player_damage = self.calculate_damage(self.player_pokemon, self.rival_pokemon)  # Calcul des dégâts du joueur
                self.apply_damage(self.rival_pokemon, player_damage)  # Application des dégâts au Pokémon rival
                self.draw_text(f"{self.player_pokemon.nom} inflige {player_damage} dégâts à {self.rival_pokemon.nom}", 10, 10)  # Affichage des dégâts infligés par le joueur
                time.sleep(2)  # Pause de 2 secondes pour laisser le temps au joueur de voir les actions effectuées
            else:  # Si c'est le tour du rival
                rival_damage = self.calculate_damage(self.rival_pokemon, self.player_pokemon)  # Calcul des dégâts du rival
                self.apply_damage(self.player_pokemon, rival_damage)  # Application des dégâts au Pokémon du joueur
                self.draw_text(f"{self.rival_pokemon.nom} inflige {rival_damage} dégâts à {self.player_pokemon.nom}", 10, 30)  # Affichage des dégâts infligés par le rival
                time.sleep(2)  # Pause de 2 secondes pour laisser le temps au joueur de voir les actions effectuées

            self.draw_battle_screen()  # Dessin de l'écran de combat
            self.draw_buttons()  # Dessin des boutons d'action

            for event in pygame.event.get():  # Parcours des événements Pygame
                if event.type == pygame.MOUSEBUTTONDOWN:  # Si un clic de souris est détecté
                    mouse_pos = pygame.mouse.get_pos()  # Récupération de la position du clic
                    self.handle_button_click(mouse_pos)  # Gestion du clic sur les boutons d'action

            if self.player_pokemon.points_de_vie <= 0 or self.rival_pokemon.points_de_vie <= 0:  # Si le Pokémon du joueur ou du rival n'a plus de points de vie
                winner = self.determine_winner()  # Détermination du vainqueur du combat
                self.draw_text(f"{winner} a gagné le combat!", 10, 50)  # Affichage du message de victoire du vainqueur
                self.record_in_pokedex()  # Enregistrement du Pokémon vainqueur dans le Pokédex
                pygame.display.update()  # Mise à jour de l'affichage de la fenêtre de jeu
                time.sleep(2)  # Pause de 2 secondes pour laisser le temps au joueur de voir le résultat du combat
                pygame.quit()  # Fermeture de Pygame
                quit()  # Fermeture du programme

            player_turn = not player_turn  # Changement de tour (du joueur au rival ou vice versa)
            clock.tick(1)  # Limitation de la vitesse du jeu à 1 image par seconde

    # Méthode pour gérer les événements Pygame (comme fermer la fenêtre)
    def handle_events(self):
        for event in pygame.event.get():  # Parcours des événements Pygame
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                pygame.quit()  # Fermeture de Pygame
                quit()  # Fermeture du programme

    # Méthode pour calculer les dégâts infligés par un Pokémon à un autre
    def calculate_damage(self, attacker, defender):
        type_multiplier = self.get_type_multiplier(attacker, defender)  # Calcul du multiplicateur de type entre l'attaquant et le défenseur
        damage = int(attacker.puissance_attaque * type_multiplier) - defender.defense  # Calcul des dégâts (puissance d'attaque * multiplicateur de type - défense)
        return max(damage, 0)  # Les dégâts ne peuvent pas être négatifs, donc on retourne la valeur maximale entre les dégâts calculés et 0

    # Méthode pour obtenir le multiplicateur de type entre un attaquant et un défenseur
    def get_type_multiplier(self, attacker, defender):
        # Tableau des multiplicateurs de type pour chaque combinaison d'attaquant et de défenseur
        type_multiplier_table = {
            "Feu": {"Eau": 0.5, "Terre": 2.0, "Feu": 1.0, "Normal": 1},
            "Eau": {"Eau": 1.0, "Terre": 0.5, "Feu": 2.0, "Normal": 1},
            "Terre": {"Eau": 2.0, "Terre": 1.0, "Feu": 1.0, "Normal": 1},
            "Normal": {"Eau": 0.75, "Terre": 0.75, "Feu": 0.75, "Normal": 1}
        }

        attacker_types = attacker.type  # Types de l'attaquant
        defender_types = defender.type  # Types du défenseur

        type_multiplier = 1.0  # Initialisation du multiplicateur de type à 1.0

        # Parcours des types de l'attaquant et du défenseur pour trouver le multiplicateur de type approprié
        for attacker_type in attacker_types:
            for defender_type in defender_types:
                if attacker_type in type_multiplier_table and defender_type in type_multiplier_table[attacker_type]:
                    type_multiplier *= type_multiplier_table[attacker_type][defender_type]  # Multiplication du multiplicateur de type

        return type_multiplier  # Retour du multiplicateur de type calculé

    # Méthode pour appliquer des dégâts à un Pokémon
    def apply_damage(self, pokemon, damage):
        pokemon.points_de_vie -= damage  # Réduction des points de vie du Pokémon par le montant des dégâts

    # Méthode pour déterminer le vainqueur du combat
    def determine_winner(self):
        if self.player_pokemon.points_de_vie <= 0:  # Si le Pokémon du joueur n'a plus de points de vie
            return self.rival_pokemon.nom  # Le vainqueur est le Pokémon rival
        elif self.rival_pokemon.points_de_vie <= 0:  # Si le Pokémon rival n'a plus de points de vie
            return self.player_pokemon.nom  # Le vainqueur est le Pokémon du joueur
        else:
            return "Aucun vainqueur"  # Aucun vainqueur si les deux Pokémon ont encore des points de vie

    # Méthode pour enregistrer le Pokémon vainqueur dans le Pokédex
    def record_in_pokedex(self):
        if self.player_pokemon not in self.player_pokemon.pokedex:  # Si le Pokémon du joueur n'est pas déjà enregistré dans le Pokédex
            self.player_pokemon.pokedex.append(self.player_pokemon)  # Ajout du Pokémon du joueur au Pokédex
            print(f"{self.player_pokemon.nom} ajouté au Pokédex!")  # Affichage d'un message indiquant l'ajout du Pokémon au Pokédex

# Fonction pour charger les données des Pokémon à partir d'un fichier JSON
def load_pokedex():
    with open('pokedex.json', 'r') as file:  # Ouverture du fichier JSON en lecture
        data = json.load(file)  # Chargement des données JSON
    return [choix(**entry) for entry in data['pokemons']]  # Création d'une liste de Pokémon à partir des données chargées

# Fonction pour obtenir un Pokémon rival aléatoire parmi une liste de Pokémon
def get_random_rival(pokemons, player_pokemon):
    rival_pokemon = random.choice(pokemons)  # Sélection aléatoire d'un Pokémon rival
    while rival_pokemon == player_pokemon:  # Si le Pokémon rival est le même que le Pokémon du joueur
        rival_pokemon = random.choice(pokemons)  # On sélectionne un autre Pokémon rival aléatoirement
    return rival_pokemon  # Retour du Pokémon rival sélectionné

# Fonction pour afficher l'écran de sélection du Pokémon du joueur
def select_pokemon_screen(game, pokemons, K):
    selected_pokemon = None  # Initialisation du Pokémon sélectionné à None
    game_status = 'select_pokemon'  # Définition du statut du jeu à 'select_pokemon'

    while game_status == 'select_pokemon':  # Boucle pour l'écran de sélection du Pokémon du joueur
        for event in pygame.event.get():  # Parcours des événements Pygame
            if event.type == pygame.MOUSEBUTTONDOWN:  # Si un clic de souris est détecté
                mouse_cursor = pygame.mouse.get_pos()  # Récupération de la position du curseur de souris
                for pokemon in pokemons:  # Parcours des Pokémon disponibles
                    if pokemon.get_rect().collidepoint(mouse_cursor):  # Si le curseur de souris est sur le Pokémon
                        selected_pokemon = pokemon  # Le Pokémon est sélectionné
                        game_status = 'start_battle'  # Changement du statut du jeu à 'start_battle'

        game.fill(K)  # Remplissage de l'écran avec une couleur spécifiée
        for pokemon in pokemons:  # Parcours des Pokémon disponibles
            pokemon.draw(game, pokemon.x, pokemon.y)  # Affichage des Pokémon sur l'écran
            mouse_cursor = pygame.mouse.get_pos()  # Récupération de la position du curseur de souris
            if pokemon.get_rect().collidepoint(mouse_cursor):  # Si le curseur de souris est sur le Pokémon
                pygame.draw.rect(game, black, pokemon.get_rect(), 2)  # Affichage d'un contour noir autour du Pokémon sélectionné

        pygame.display.update()  # Mise à jour de l'affichage de la fenêtre de jeu

    return selected_pokemon  # Retour du Pokémon sélectionné

