import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Menu")


BG = pygame.image.load("photos/_6326d2ef-150c-49d9-9f30-88edb17c7953.jpg")


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("photos/font.ttf", size)
    

def Lancer_une_partie():
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
    
def Pokemon():
    while True:
        POKEMON_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        POKEMON_TEXT = get_font(45).render(" ", True, "Black")
        POKEMON_RECT = POKEMON_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(POKEMON_TEXT, POKEMON_RECT)

        POKEMON_BACK = Button(pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        POKEMON_BACK.changeColor(POKEMON_MOUSE_POS)
        POKEMON_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if POKEMON_BACK.checkForInput(POKEMON_MOUSE_POS):
                    main_menu()

        pygame.display.update()
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

        # Calculate the position to center the image
        bg_rect = resized_bg.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
        SCREEN.blit(resized_bg, bg_rect)

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("  POKEMON  ", True, "#FFD700")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 60))

        # Ajustez les coordonnées x pour déplacer les boutons vers la gauche
        PLAY_BUTTON = Button(pos=(480, 440), text_input="Lancer une partie", font=get_font(35), base_color="#000000", hovering_color="White")
        POKEMON_BUTTON = Button(pos=(480, 510), text_input="Accéder au Pokédex ", font=get_font(35), base_color="#000000", hovering_color="White")
        POKEDEX_BUTTON = Button(pos=(490, 600), text_input="Ajouter un Pokémon ", font=get_font(35), base_color="#000000", hovering_color="White")
        QUIT_BUTTON = Button(pos=(480, 680), text_input="QUIT", font=get_font(40), base_color="#000000", hovering_color="White")


        #MENU_TEXT = get_font(100).render("  POKEMON  ", True, "#FFD700")
        #MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        #PLAY_BUTTON = Button(pos=(640, 410), text_input="Lancer une partie", font=get_font(35), base_color="#000000", hovering_color="White")
        #POKEMON_BUTTON = Button(pos=(640, 510), text_input="Accéder au Pokédex ", font=get_font(35), base_color="#000000", hovering_color="White")
        #POKEDEX_BUTTON = Button(pos=(650, 600), text_input="Ajouter un Pokémon ", font=get_font(35), base_color="#000000", hovering_color="White")
        #QUIT_BUTTON = Button(pos=(640, 680), text_input="QUIT", font=get_font(40), base_color="#000000", hovering_color="White") 


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

main_menu()

