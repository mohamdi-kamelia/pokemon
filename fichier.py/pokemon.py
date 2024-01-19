# main_gui.py
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, K_RETURN
from pokemon import Pokemon
from combat import Combat
from pokedex import Pokedex

class PokemonGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Pokemon Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.pokedex = Pokedex()

        # Définir les boutons
        self.buttons = [
            {"text": "Lancer une partie", "action": self.start_game, "rect": pygame.Rect(50, 50, 300, 30)},
            {"text": "Choisir un Pokémon", "action": self.choose_pokemon, "rect": pygame.Rect(50, 100, 300, 30)},
            {"text": "Accéder au Pokédex", "action": self.display_pokedex, "rect": pygame.Rect(50, 150, 300, 30)},
            {"text": "Quitter", "action": self.quit_game, "rect": pygame.Rect(50, 200, 300, 30)}
        ]

    def display_menu(self):
        self.screen.fill((255, 255, 255))

        for button in self.buttons:
            pygame.draw.rect(self.screen, (200, 200, 200), button["rect"])
            text = self.font.render(button["text"], True, (0, 0, 0))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def start_game(self):
        player_pokemon_name = input("Choisissez un Pokémon pour commencer: ")
        if not player_pokemon_name:
            return

        player_pokemon = Pokemon(player_pokemon_name)
        opponent_pokemon_name = "bulbasaur"  # Choisissez un Pokémon arbitraire ici
        opponent_pokemon = Pokemon(opponent_pokemon_name)

        combat = Combat(player_pokemon, opponent_pokemon)
        combat_result = combat.start_combat()

        print(f"Le gagnant est : {combat_result['winner_name']}")
        print(f"Dommages infligés à l'adversaire : {combat_result['damage_to_opponent']}")
        print(f"Dommages subis par le joueur : {combat_result['damage_to_player']}")

        combat.save_to_pokedex(self.pokedex)

    def choose_pokemon(self):
        # Implémentez la logique pour afficher la page Pokémon ici
        # Vous pouvez utiliser une nouvelle classe ou une fonction dédiée pour cela
        print("Page Pokémon : Choisissez votre Pokémon")

    def display_pokedex(self):
        self.pokedex.display_pokemon()

    def quit_game(self):
        print("Au revoir !")
        pygame.quit()

    def run(self):
        running = True
        while running:
            self.display_menu()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # Vérifier si un bouton a été cliqué
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            button["action"]()

            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    game = PokemonGame()
    game.run()










