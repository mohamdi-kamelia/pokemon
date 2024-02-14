import pygame
import json

class Pokedex:
    def __init__(self):
        pygame.init()

        with open("pokedex.json", "r") as file:
            self.pokemon_data = json.load(file)

        self.width, self.height = 900, 750
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pokédex")

        self.background_buffer = pygame.Surface(self.screen.get_size())
        self.background_buffer = self.background_buffer.convert()

        self.background = pygame.image.load("photos/_1a67a30d-c6c7-4d2e-968b-ff5b3f533b80.jpg")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # Couleurs
        self.K = (255, 215, 0)

        # Police
        self.font = pygame.font.Font("photos/Pokemon Solid.ttf", 26)

        self.current_pokemon = 0

    def display_pokemon(self, pokemon_id, screen):
        screen.blit(self.background, (0, 0))  # Efface l'écran avant d'afficher les informations
        if pokemon_id >= 0 and pokemon_id < len(self.pokemon_data["pokemons"]):
            pokemon = self.pokemon_data["pokemons"][pokemon_id]
            y_offset = 50
            text_x_position = 25  # Position horizontale des textes à droite
            for key, value in pokemon.items():
                text = self.font.render(f"{key.capitalize()}: {value}", True, self.K)
                screen.blit(text, (text_x_position, y_offset))
                y_offset += 50  # Augmente le décalage en y pour éviter que les textes ne se superposent
            pygame.display.flip()

    def add_pokemon(self, id_pok: int):
        if isinstance(id_pok, int):
            new_pokemon = self.pokemon_data["pokemons"][id_pok]  # Obtenir les données du nouveau Pokémon
            self.data.append(new_pokemon)
            self.save_dex()

    def save_dex(self):
        with open('pokemon.json', 'w') as f:
            json.dump(self.data, f, indent=2)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.current_pokemon += 1
                        if self.current_pokemon > len(self.pokemon_data["pokemons"]):
                            self.current_pokemon = 0
                    elif event.key == pygame.K_LEFT:
                        self.current_pokemon -= 1
                        if self.current_pokemon < 0:
                            self.current_pokemon = len(self.pokemon_data["pokemons"]) - 1
                    elif event.key == pygame.K_BACKSPACE:  # Touche "M" pour retourner au menu
                        return     
                            

            # Effacement de l'écran avec le tampon arrière
            self.background_buffer.fill((0, 0, 0))

            # Affichage du Pokémon courant sur le tampon arrière
            self.display_pokemon(self.current_pokemon, self.background_buffer)

            # Affichage du tampon arrière sur la surface d'affichage principale
            self.screen.blit(self.background_buffer, (0, 0))

            # Mise à jour de l'affichage
            pygame.display.flip()

            # Limite le taux de rafraîchissement à 30 FPS
            clock.tick(30)

        # Quitter Pygame
        pygame.quit()

if __name__ == '__main__':
    dex = Pokedex()
    dex.run()




























