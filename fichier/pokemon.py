import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN
import json
from pok import *

class PokemonApp:
    def __init__(self):
        pygame.init()
        self.downloader = PokemonDataDownloader()
        self.downloader.get_pokemon_data()

        self.pokemon_list = self.load_pokemon_data()
        self.selected_index = 0
        self.selected_pokemon_info = None

        self.screen = pygame.display.set_mode((800, 700))
        pygame.display.set_caption("Liste des Pokémon")
        self.clock = pygame.time.Clock()

        # Charger l'image d'arrière-plan
        self.background_image = pygame.image.load('photos/_5b7894b6-a498-45f7-9d9b-3a664b262059.jpg')
        self.font = pygame.font.Font('photos/Pokemon Solid.ttf', 30)


    def load_pokemon_data(self):
        with open('pokemon.json', 'r') as file:
            pokemon_data = json.load(file)
        return pokemon_data['pokemon_list']

    def load_pokemon_images(self, pokemon_list):
        images = {}
        for pokemon_info in pokemon_list:
            image_path = pokemon_info['image_path']
            images[pokemon_info['name']] = pygame.image.load(image_path)
        return images

    def draw_pokemon_list(self):
        # Dessiner l'arrière-plan
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

            # Dessiner les contours du rectangle autour des informations
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
                    if event.key == K_RETURN:
                        self.selected_pokemon_info = self.pokemon_list[self.selected_index]
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.pokemon_list)
                    elif event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.pokemon_list)

            self.draw_pokemon_list()
            self.draw_pokemon_info()

            pygame.display.flip()
            self.clock.tick(30)










