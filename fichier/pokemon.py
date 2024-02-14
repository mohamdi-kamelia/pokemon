import pygame
from pygame.locals import QUIT, KEYDOWN
import json
import requests
from pok import PokemonDataDownloader

class PokemonApp:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.downloader = PokemonDataDownloader()
        self.downloader.get_pokemon_data()

        self.pokemon_list = self.load_pokemon_data()
        self.selected_index = 0
        self.selected_pokemon_info = None

        self.screen = pygame.display.set_mode((900, 750))
        pygame.display.set_caption("Liste des Pokémon")
        self.clock = pygame.time.Clock()

        self.background_image = pygame.image.load('photos/_5b7894b6-a498-45f7-9d9b-3a664b262059.jpg')
        self.font = pygame.font.Font('photos/Pokemon Solid.ttf', 30)

        # Initialisation de la zone de texte et du bouton de recherche
        self.input_text = ''
        self.active = False
        self.text_input_rect = pygame.Rect(550, 50, 200, 50)
        self.search_button_rect = pygame.Rect(760, 50, 100, 50)
        self.search_button_color = (0, 0, 255)

    def load_pokemon_data(self):
        with open('pokemon.json', 'r') as file:
            pokemon_data = json.load(file)
        return pokemon_data['pokemon_list']

    def save_pokemon_data(self):
        pokemon_data = {"pokemon_list": self.pokemon_list}
        with open('pokemon.json', 'w') as file:
            json.dump(pokemon_data, file)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.text_input_rect.collidepoint(event.pos):
                self.active = True
            elif self.search_button_rect.collidepoint(event.pos):
                self.search_pokemon()
                self.active = False
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.search_pokemon()
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                self.selected_pokemon_info = None
                return

    def draw_text_input(self):
        pygame.draw.rect(self.screen, (0, 0, 255), self.text_input_rect, 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.input_text, True, (255, 255, 255))
        self.screen.blit(text, (self.text_input_rect.x + 5, self.text_input_rect.y + 5))

    def draw_search_button(self):
        pygame.draw.rect(self.screen, self.search_button_color, self.search_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Ajouter", True, (0, 0, 0))
        self.screen.blit(text, (self.search_button_rect.x + 10, self.search_button_rect.y + 10))

    def search_pokemon(self):
        pokemon_id = self.input_text.strip()

        if not 1 <= int(pokemon_id) <= 898:
            print("ID de Pokémon invalide. Veuillez entrer un ID entre 1 et 898.")
            return

        full_url = f"{self.downloader.base_url}{pokemon_id}"
        response = requests.get(full_url)

        if response.status_code != 200:
            print(f"Impossible de trouver le Pokémon avec l'ID {pokemon_id}. Veuillez réessayer.")
            return

        data = response.json()

        pokemon_info = {
            'name': data['name'],
            'types': [type_data['type']['name'] for type_data in data['types']],
            'hp': data['stats'][0]['base_stat'],
            'attack': data['stats'][1]['base_stat'],
            'defense': data['stats'][2]['base_stat'],
            'speed': data['stats'][5]['base_stat'],
            'image_url': data['sprites']['front_default'],
        }

        image_save_path = f"images/{pokemon_info['name']}.png"
        self.downloader.download_image(pokemon_info['image_url'], image_save_path)
        pokemon_info['image_path'] = image_save_path

        self.pokemon_list.append(pokemon_info)
        self.save_pokemon_data()  # Enregistrer les données dans le fichier pokemon.json

        print(f"Le Pokémon {pokemon_info['name']} a été ajouté avec succès !")

    def load_pokemon_images(self, pokemon_list):
        images = {}
        for pokemon_info in pokemon_list:
            image_path = pokemon_info['image_path']
            images[pokemon_info['name']] = pygame.image.load(image_path).convert_alpha()
        return images

    def draw_pokemon_list(self):
        self.screen.blit(self.background_image, (0, 0))

        pokemon_images = self.load_pokemon_images(self.pokemon_list)

        for i, pokemon_info in enumerate(self.pokemon_list):
            color = (0, 0, 255) if i == self.selected_index else (0, 0, 0)

            image = pokemon_images[pokemon_info['name']]
            self.screen.blit(image, (50, 50 + i * 50))

            text = self.font.render(pokemon_info['name'].capitalize(), True, color)
            text_y = 50 + i * 50 + image.get_height() / 2 - text.get_height() / 2 + 5
            self.screen.blit(text, (50 + image.get_width() + 10, text_y))

    def draw_pokemon_info(self):
        if self.selected_pokemon_info:
            font = pygame.font.Font(None, 30)
            text_x = 450
            text_y = 170

            keys_to_display = ['name', 'types', 'hp', 'attack', 'defense', 'speed']

            info_rect = pygame.Rect(400, 150, 350, 200)
            pygame.draw.rect(self.screen, (0, 0, 255), info_rect, 3) 

            for key, value in self.selected_pokemon_info.items():
                if key in keys_to_display:
                    text = font.render(f"{key.capitalize()}: {value}", True, pygame.Color('black'))
                    self.screen.blit(text, (text_x, text_y))
                    text_y += 30

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.selected_pokemon_info = self.pokemon_list[self.selected_index]
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.pokemon_list)
                    elif event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.pokemon_list)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:    
                        #if event.key == pygame.K_ESCAPE:
                            return    

                self.handle_events(event)        

            self.draw_pokemon_list()
            self.draw_pokemon_info()
            self.draw_text_input()
            self.draw_search_button()

            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    app = PokemonApp()
    app.run()












