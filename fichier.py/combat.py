# combat.py
import pygame
from pygame.locals import *
from pygame import MOUSEBUTTONDOWN, Rect
import random
import time
from pokemon import  *

pygame.init()

game_width = 700
game_height = 700
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption("Pokemon")

black = (0, 0, 0)
gold = (218, 165, 32)
grey = (200, 200, 200)
green = (0, 200, 0)
red = (200, 0, 0)
white = (255, 255, 255)
K = (129, 178, 154)

niveau = 30

x_bulbasaur, y_bulbasaur = 50, 50
x_charmander, y_charmander = 200, 50
x_squirtle, y_squirtle = 350, 50
x_pikachu, y_pikachu = 500, 50
x_sandshrew, y_sandshrew = 50, 250
x_eevee, y_eevee = 200, 250

bulbasaur = Pokemon('Bulbasaur', 100, niveau, 25, 15, ['Type1', 'Type2'], x_bulbasaur, y_bulbasaur , game)
charmander = Pokemon('Charmander', 90, niveau, 25, 18, ['Type1', 'Type2'], x_charmander, y_charmander , game)
squirtle = Pokemon('Squirtle', 95, niveau, 23, 20, ['Type1', 'Type2'], x_squirtle, y_squirtle , game)
pikachu = Pokemon('Pikachu', 85, niveau, 30, 15, ['Type1'], x_pikachu, y_pikachu, game)
sandshrew = Pokemon('Sandshrew', 95, niveau, 20, 25, ['Type1'], x_sandshrew, y_sandshrew , game)
eevee = Pokemon('Eevee', 80, niveau, 20, 20, ['Type1'], x_eevee, y_eevee , game)
pokemons = [bulbasaur, charmander, squirtle, pikachu, sandshrew, eevee, game]

player_pokemon = None
rival_pokemon = None
def display_message(game, message):
    font = pygame.font.Font(pygame.font.get_default_font(), 32)
    text = font.render(message, True, (255, 255, 255))
    game.blit(text, (200, 300))
    pygame.display.flip()
    pygame.time.delay(2000)

game_status = 'select pokemon'
while game_status != 'quit':

    for event in pygame.event.get():
        if event.type == QUIT:
            game_status = 'quit'
        if event.type == KEYDOWN:
            if event.key == K_y:
                bulbasaur = Pokemon('Bulbasaur', niveau, 25, 150)
                charmander = Pokemon('Charmander', niveau, 25, 18)
                squirtle = Pokemon('Squirtle', niveau, 23, 20)
                pikachu = Pokemon('Pikachu', niveau, 30, 15)
                sandshrew = Pokemon('Sandshrew', niveau, 20, 25)
                eevee = Pokemon('Eevee', niveau, 20, 20)
                game_status = 'select pokemon'
            elif event.key == K_n:
                game_status = 'quit'

        if event.type == MOUSEBUTTONDOWN:
            mouse_click = event.pos

            if game_status == 'select pokemon':
                for current_pokemon in pokemons:
                    if current_pokemon.get_rect().collidepoint(mouse_click):
                        player_pokemon = current_pokemon
                        rival_pokemon = pokemons[(pokemons.index(current_pokemon) + 1) % len(pokemons)]
                        rival_pokemon.niveau = int(rival_pokemon.niveau * .75)
                        player_pokemon.hp_x = 275
                        player_pokemon.hp_y = 250
                        rival_pokemon.hp_x = 50
                        rival_pokemon.hp_y = 50
                        game_status = 'prebattle'
            elif game_status == 'player turn':
                # Gestion du clic de la souris pendant le combat
                pass

    if game_status == 'select pokemon':
        game.fill(K)
        for pokemon in pokemons:
            game.blit(pokemon.image, (pokemon.x, pokemon.y))  # Utilisez blit pour dessiner l'image du Pokémon
        mouse_cursor = pygame.mouse.get_pos()
        for pokemon in pokemons:
            if pokemon.get_rect().collidepoint(mouse_cursor):
                pygame.draw.rect(game, black, pokemon.get_rect(), 2)
        pygame.display.update()


    if game_status == 'prebattle':
        game.fill(white)
        player_pokemon.draw()
        pygame.display.update()
        player_pokemon.set_moves()
        rival_pokemon.set_moves()
        player_pokemon.x = -50
        player_pokemon.y = 100
        rival_pokemon.x = 250
        rival_pokemon.y = -50
        player_pokemon.size = 300
        rival_pokemon.size = 300
        player_pokemon.set_sprite('back_default')
        rival_pokemon.set_sprite('front_default')
        game_status = 'start battle'

    if game_status == 'start battle':
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

        pygame.draw.rect(game, black, (10, 350, 480, 140), 3)
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

    if game_status == 'rival turn':
        game.fill(white)
        player_pokemon.draw()
        rival_pokemon.draw()
        player_pokemon.draw_hp()
        rival_pokemon.draw_hp()
        display_message('')
        time.sleep(2)

        move = random.choice(rival_pokemon.moves)
        rival_pokemon.perform_attack(player_pokemon, move)

        if player_pokemon.current_hp == 0:
            game_status = 'fainted'
        else:
            game_status = 'player turn'
        pygame.display.update()

    if game_status == 'fainted':
        alpha = 255
        while alpha > 0:
            game.fill(white)
            player_pokemon.draw_hp()
            rival_pokemon.draw_hp()

            if rival_pokemon.current_hp == 0:
                player_pokemon.draw()
                rival_pokemon.draw(alpha)
                display_message(f'{rival_pokemon.nom} fainted')
            else:
                player_pokemon.draw(alpha)
                rival_pokemon.draw()
                display_message(f'{player_pokemon.nom} fainted')
            alpha -= .4
            pygame.display.update()
        game_status = 'gameover'

    if game_status == 'gameover':
        display_message('Try again!(Y/N)')

pygame.quit()



        
