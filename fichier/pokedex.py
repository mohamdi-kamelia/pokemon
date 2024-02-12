
"""import pygame
import json
import os
from pok import PokemonDataDownloader

class Pokedex:
    def __init__(self):
        pygame.init()

        self.downloader = PokemonDataDownloader()
        self.downloader.get_pokemon_data()

        self.pokedex_list = self.load_pokedex_data()
        self.selected_pokemon_index = 0
        self.selected_pokedex_info = None

        self.width, self.height = 900, 750
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pokédex")
        self.clock = pygame.time.Clock()
        self.white = (255, 255, 255)
        self.font = pygame.font.Font('photos/Pokemon Solid.ttf', 30)

    def load_pokedex_data(self):
        with open('pokedex.json', 'r') as file:
            pokedex_data = json.load(file)
        return pokedex_data['pokemons'] 

    def load_pokedex_images(self, pokedex_list):
        images = {}
        for pokedex_info in pokedex_list:
            image_path = pokedex_info['image_path']
            images[pokedex_info['nom']] = pygame.image.load(image_path) 
        return images
  

    def draw_pokemon_list(self):
        # Dessiner la liste des Pokémon
        pokemon_images = self.load_pokedex_images(self.pokedex_list)
        y = 50
        for i, pokemon_info in enumerate(self.pokedex_list):
            image = pokemon_images[pokemon_info['name']]
            self.screen.blit(image, (50, y))
            text = self.font.render(pokemon_info['name'].capitalize(), True, (0, 0, 0))
            text_y = y + image.get_height() / 2 - text.get_height() / 2
            self.screen.blit(text, (50 + image.get_width() + 10, text_y))
            y += image.get_height() + 10

    def draw_pokemon_info(self):
        # Dessiner les informations détaillées du Pokémon sélectionné
        if self.selected_pokedex_info:
            font = pygame.font.Font(None, 30)
            text_x = 400
            text_y = 400
            for key, value in self.selected_pokedex_info.items():
                text = font.render(f"{key.capitalize()}: {value}", True, pygame.Color('black'))
                self.screen.blit(text, (text_x, text_y))
                text_y += 30

    def display_pokedex(self):
        self.screen.fill(self.white)

        # Dessiner la liste des Pokémon
        self.draw_pokemon_list()

        # Dessiner les informations du Pokémon sélectionné
        self.draw_pokemon_info()

        pygame.display.flip()

    def handle_mouse_click(self, event):
        for i, pokemon in enumerate(self.downloader.pokemon_list):
            pokemon_area = pygame.Rect(50, 50 + 30 * i, 250, 25)
            if pokemon_area.collidepoint(event.pos):
                self.selected_pokemon_index = i
                break

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_click(event)

            self.display_pokedex()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    pokedex_app = Pokedex()
    pokedex_app.run()"""

"""
import pygame
import json
from combat import CombatGUI, Pokedex, get_random_rival

pokedex = Pokedex('pokedex.json')


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

def load_pokedex():
    pokedex = Pokedex('pokedex.json')
    return pokedex.get_pokemon_list()

def select_pokemon_screen(game, pokemons, K):
    selected_pokemon = None
    game_status = 'select_pokemon'
    # Boucle pour la sélection du Pokémon
    while game_status == 'select_pokemon':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si l'utilisateur clique sur le bouton de fermeture
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_cursor = pygame.mouse.get_pos()
                for pokemon in pokemons:
                    if pokemon['nom'] == 'Gengar':  # Utilisez le nom du Pokémon gagnant ici
                        print(f"Gagnant: {pokemon['nom']}")
                        print(f"Types: {', '.join(pokemon['types'])}")  # Utilisez la clé 'types' au lieu de 'type'
                        print(f"Points de vie: {pokemon['points_de_vie']}")
                        print(f"Attaque: {pokemon['puissance_attaque']}")  # Utilisez 'puissance_attaque' au lieu de 'attaque'
                        print(f"Défense: {pokemon['defense']}")
                        game_status = 'start_battle'

        game.fill(K)  # Remplit l'écran de jeu avec la couleur d'arrière-plan
        pygame.display.update()  # Met à jour l'affichage

    return selected_pokemon  # Retourne le Pokémon sélectionné


if __name__ == "__main__":
    main()"""

"""
import pypokedex
import PIL.Image, PIL.ImageTk
import tkinter as tk
import urllib3
from io import BytesIO

class Pokedex:
    def __init__(self, window):
        self.window = window
        self.window.geometry("900x700")
        self.window.title("Pokedex")
        self.window.config(padx=10, pady=10)

        self.title_label = tk.Label(self.window, text="Pokedex")
        self.title_label.config(font=("Arial", 32))
        self.title_label.pack(padx=10, pady=10)

        self.pokemon_image = tk.Label(self.window)
        self.pokemon_image.pack(padx=10, pady=10)

        self.pokemon_information = tk.Label(self.window)
        self.pokemon_information.config(font=("Arial", 20))
        self.pokemon_information.pack(padx=10, pady=10)

        self.pokemon_types = tk.Label(self.window)
        self.pokemon_types.config(font=("Arial", 20))
        self.pokemon_types.pack(padx=10, pady=10)

    def load_pokemon(self):
        pokemon_name = self.text_id_name.get(1.0, "end-1c")
        pokemon = pypokedex.get(name=pokemon_name)

        http = urllib3.PoolManager()
        response = http.request('GET', pokemon.sprites.front.get('default'))
        image = PIL.Image.open(BytesIO(response.data))

        img = PIL.ImageTk.PhotoImage(image)
        self.pokemon_image.config(image=img)
        self.pokemon_image.image = img

        self.pokemon_information.config(text=f"{pokemon.dex} - {pokemon.name}")
        self.pokemon_types.config(text=" - ".join([t for t in pokemon.types]).title())

if __name__ == "__main__":
    window = tk.Tk()
    pokedex = Pokedex(window)

    lebel_id_name = tk.Label(window, text="ID or Name")
    lebel_id_name.config(font=("Arial", 20))
    lebel_id_name.pack(padx=10, pady=10)

    pokedex.text_id_name = tk.Text(window, height=1)
    pokedex.text_id_name.config(font=("Arial", 20))
    pokedex.text_id_name.pack(padx=10, pady=10)

    btn_load = tk.Button(window, text="Load Pokemon", command=pokedex.load_pokemon)
    btn_load.config(font=("Arial", 20))
    btn_load.pack(padx=10, pady=10)

    window.mainloop()
    """


"""
import pygame
import pypokedex
import urllib3
from io import BytesIO

pygame.init()

game_width = 700
game_height = 700
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption("Pokedex")
clock = pygame.time.Clock()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Fonctions d'affichage
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_button(surface, color, x, y, width, height, text, text_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, GRAY, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(surface, color, (x, y, width, height))

    small_text = pygame.font.Font("freesansbold.ttf", 20)
    draw_text(text, small_text, text_color, surface, x + width / 2 - 50, y + height / 2 - 10)

# Fonction de chargement du Pokémon
def load_pokemon(text_id_name):
    pokemon_name = text_id_name.get(1.0, "end-1c").strip()
    if pokemon_name:
        try:
            pokemon = pypokedex.get(name=pokemon_name)
            http = urllib3.PoolManager()
            response = http.request('GET', pokemon.sprites.front.get('default'))
            image = pygame.image.load(BytesIO(response.data))
            game.blit(image, (50, 50))

            font = pygame.font.Font(None, 30)
            draw_text(f"{pokemon.dex} - {pokemon.name}", font, WHITE, game, 50, 300)
            draw_text(" - ".join([t for t in pokemon.types]).title(), font, WHITE, game, 50, 350)
        except pypokedex.exceptions.PyPokedexHTTPError:
            draw_text("Pokemon not found", font, WHITE, game, 50, 50)

# Boucle principale
def main():
    input_box = pygame.Rect(50, 500, 200, 32)
    color_inactive = WHITE
    color_active = GRAY
    color = color_inactive
    active = False
    text = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        load_pokemon()
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        game.fill(BLACK)
        pygame.draw.rect(game, color, input_box, 2)
        font = pygame.font.Font(None, 32)
        draw_text(text, font, color_inactive, game, input_box.x + 5, input_box.y + 5)

        # Bouton "Load Pokemon"
        draw_button(game, WHITE, 300, 500, 150, 50, "Load Pokemon", BLACK, load_pokemon)

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
    """
"""
import pypokedex
import PIL.Image, PIL.ImageTk
import tkinter as tk
import urllib3
from io import BytesIO

class Pokedex:
    def __init__(self, window):
        self.window = window
        self.window.geometry("900x750")
        self.window.title("Pokedex")
        self.window.config(padx=10, pady=10)

        self.title_label = tk.Label(self.window, text="Pokedex")
        self.title_label.config(font=("Arial", 32))
        self.title_label.pack(padx=10, pady=10)

        self.pokemon_image = tk.Label(self.window)
        self.pokemon_image.pack(padx=10, pady=10)

        self.pokemon_information = tk.Label(self.window)
        self.pokemon_information.config(font=("Arial", 20))
        self.pokemon_information.pack(padx=10, pady=10)

        self.pokemon_types = tk.Label(self.window)
        self.pokemon_types.config(font=("Arial", 20))
        self.pokemon_types.pack(padx=10, pady=10)

    def load_pokemon(self):
        pokemon_name = self.text_id_name.get(1.0, "end-1c").strip()  # Supprimez les espaces blancs autour du nom
        try:
            pokemon = pypokedex.get(name=pokemon_name)

            http = urllib3.PoolManager()
            response = http.request('GET', pokemon.sprites.front.get('default'))
            image = PIL.Image.open(BytesIO(response.data))

            img = PIL.ImageTk.PhotoImage(image)
            self.pokemon_image.config(image=img)
            self.pokemon_image.image = img

            self.pokemon_information.config(text=f"ID: {pokemon.dex} - Name: {pokemon.name}")
            self.pokemon_types.config(text=" - ".join([t for t in pokemon.types]).title())
        except pypokedex.exceptions.PyPokedexHTTPError:
            # Gestion d'erreur pour le cas où le Pokémon n'est pas trouvé
            self.pokemon_information.config(text="Pokemon not found")
            self.pokemon_types.config(text="")
        except Exception as e:
            # Gestion d'erreur générique pour d'autres exceptions possibles
            print(f"Error: {e}")
            self.pokemon_information.config(text="Error loading Pokemon")
            self.pokemon_types.config(text="")

if __name__ == "__main__":
    window = tk.Tk()
    pokedex = Pokedex(window)

    lebel_id_name = tk.Label(window, text="ID or Name")
    lebel_id_name.config(font=("Arial", 20))
    lebel_id_name.pack(padx=10, pady=10)

    pokedex.text_id_name = tk.Text(window, height=1)
    pokedex.text_id_name.config(font=("Arial", 20))
    pokedex.text_id_name.pack(padx=10, pady=10)

    btn_load = tk.Button(window, text="Load Pokemon", command=pokedex.load_pokemon)
    btn_load.config(font=("Arial", 20))
    btn_load.pack(padx=10, pady=10)

    window.mainloop()
    """
























