import pygame
import json

# Charge les données du Pokédex depuis le fichier JSON
def load_pokedex():
    with open('pokedex.json', 'r') as file:
        data = json.load(file)
    return data['pokemons']

# Affiche les informations du Pokédex à l'écran
def display_pokedex(pokemons):
    # Initialisation de Pygame
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pokédex')

    # Affichage des informations des Pokémon
    font = pygame.font.Font(None, 24)
    y_offset = 50
    for pokemon in pokemons:
        text = f"Nom: {pokemon['nom']} | Type: {', '.join(pokemon['type'])} | Défense: {pokemon['defense']} | Puissance d'attaque: {pokemon['puissance_attaque']} | Points de vie: {pokemon['points_de_vie']}"
        rendered_text = font.render(text, True, (255, 255, 255))
        screen.blit(rendered_text, (50, y_offset))
        y_offset += 30

    # Boucle principale du jeu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()

# Fonction principale du Pokédex
def pokedex_main():
    pokemons = load_pokedex()
    display_pokedex(pokemons)

# Code pour tester la fonctionnalité du Pokédex
if __name__ == "__main__":
    pokedex_main()


