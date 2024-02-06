import pygame
import sys
from button import Button
from game import *
from game1 import Game
from pokemon import PokemonApp


pygame.init()
SCREEN = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Menu")

BG = pygame.image.load("photos/_005551e8-0912-4606-bc6e-c497483f9886.jpg")

pokemons = load_pokedex()

def get_font(size): 
    return pygame.font.Font("photos/Pokemon Solid.ttf", size)
def Lancer_une_partie():
    global player_pokemon, rival_pokemon

   
    start_game()

    # Réinitialiser les variables globales après le jeu
    player_pokemon = None
    rival_pokemon = None


    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render(" ", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def Lancer_une_partie():
    game = Game()
    game.run()
  

def Pokemon():
    pokemon_app = PokemonApp()
    pokemon_app.run()


def Pokédex():
    while True:
        POKEDEX_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        POKEDEX_TEXT = get_font(45).render(" ", True, "Black")
        POKEDEX_RECT = POKEDEX_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(POKEDEX_TEXT, POKEDEX_RECT)

        POKEDEX_BACK = Button(pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        POKEDEX_BACK.changeColor(POKEDEX_MOUSE_POS)
        POKEDEX_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if POKEDEX_BACK.checkForInput(POKEDEX_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        resized_bg = pygame.transform.scale(BG, (1000, 700))

        # Centrer l'image redimensionnée
        bg_rect = resized_bg.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
        SCREEN.blit(resized_bg, bg_rect)

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(80).render("  POKEMON  ", True, "#FFD700")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 60))

        PLAY_BUTTON = Button(pos=(480, 440), text_input="Lancer une partie", font=get_font(45), base_color="#000000", hovering_color="White")
        POKEMON_BUTTON = Button(pos=(480, 510), text_input="Voir les  Pokémons ", font=get_font(45), base_color="#000000", hovering_color="White")
        POKEDEX_BUTTON = Button(pos=(490, 600), text_input="Accéder au Pokédex ", font=get_font(45), base_color="#000000", hovering_color="White")
        QUIT_BUTTON = Button(pos=(480, 680), text_input="QUIT", font=get_font(60), base_color="#000000", hovering_color="White")


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
