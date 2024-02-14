import pygame
import json

pygame.init()


with open("pokedex.json", "r") as file:
       pokemon_data = json.load(file)


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pokédex")


background = pygame.image.load("Imagepokemon/Pokedex.jpg")
background = pygame.transform.scale(background, (width, height))

#Couleurs
white = (255, 255, 255)


#Police
font = pygame.font.Font(None, 36)

def display_pokemon(pokemon_id):
    # Afficher les informations du Pokémon sur l'écran
        text = font.render(f"{pokemon_data[str(pokemon_id)]['name']} - {pokemon_data[str(pokemon_id)]['type']}", True)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.flip()

# Boucle principale
running = True
current_pokemon = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_pokemon += 1
                if current_pokemon > len(pokemon_data):
                    current_pokemon = 1
                display_pokemon(current_pokemon)
            elif event.key == pygame.K_LEFT:
                current_pokemon -= 1
                if current_pokemon < 1:
                    current_pokemon = len(pokemon_data)
                display_pokemon(current_pokemon)
    # Afficher le fond d'écran
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Quitter Pygame
pygame.quit()




