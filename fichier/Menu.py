import pygame
import sys
from button import Button
from pokedex import Pokedex
from game1 import Game
from pokemon import PokemonApp
from combat import load_pokedex



pygame.init()
SCREEN = pygame.display.set_mode((900, 750))
pygame.display.set_caption("Menu")

BG = pygame.image.load("photos/_005551e8-0912-4606-bc6e-c497483f9886.jpg")

pokemons = load_pokedex()

def get_font(size): 
    return pygame.font.Font("photos/Pokemon Solid.ttf", size)

def Lancer_une_partie():
    game = Game()
    game.run()
  

def Pokemon():
    pokemon_app = PokemonApp()
    pokemon_app.run()


def Pokédex():
    
    pokedex = Pokedex()  # Créer une instance de la classe Pokedex
    pokedex.run()



def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        resized_bg = pygame.transform.scale(BG, (900, 750))

        SCREEN.fill((0, 0, 0))  # Efface l'écran
        resized_bg = pygame.transform.scale(BG.convert_alpha(), (SCREEN.get_width(), SCREEN.get_height()))
        SCREEN.blit(resized_bg, (0, 0))

 
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(80).render("  POKEMON  ", True, "#FFD700")
        MENU_RECT = MENU_TEXT.get_rect(center=(450, 60))

        PLAY_BUTTON = Button(pos=(450, 500), text_input="Lancer une partie", font=get_font(45), base_color="#000000", hovering_color="White")
        POKEMON_BUTTON = Button(pos=(450, 550), text_input="Voir les  Pokémons ", font=get_font(45), base_color="#000000", hovering_color="White")
        POKEDEX_BUTTON = Button(pos=(460, 610), text_input="Accéder au Pokédex ", font=get_font(45), base_color="#000000", hovering_color="White")
        QUIT_BUTTON = Button(pos=(450, 690), text_input="QUIT", font=get_font(60), base_color="#000000", hovering_color="White")


        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, POKEMON_BUTTON, QUIT_BUTTON, POKEDEX_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Lancer_une_partie()
                if POKEMON_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Pokemon()
                if POKEDEX_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Pokédex()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()  
