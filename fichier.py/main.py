import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN
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

    def display_menu(self):
        self.screen.fill((255, 255, 255))

        menu_text = [
            "1. Lancer une partie",
            "2. Accéder au Pokédex",
            "3. Quitter"
        ]

        y = 50
        for line in menu_text:
            text = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(text, (50, y))
            y += 40

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

    def display_pokedex(self):
        self.pokedex.display_pokemon()

    def run(self):
        running = True
        while running:
            self.display_menu()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    choice = input("Votre choix (1-3): ")
                    if choice == "1":
                        self.start_game()
                    elif choice == "2":
                        self.display_pokedex()
                    elif choice == "3":
                        print("Au revoir !")
                        running = False
                    else:
                        print("Choix invalide. Veuillez entrer un nombre entre 1 et 3.")

            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    game = PokemonGame()
    game.run()
