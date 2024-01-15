import pygame
import sys
import zipfile
from pokemon import *
pygame.init()
class MenuPage:
    def __init__(self, width, height, background_image_path, font_path, pokemons):
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Menu Pokémon")
        self.clock = pygame.time.Clock()
        self.pokemons = pokemons
        self.selected_pokemon = None
        self.game_status = 'menu'
        # Charger l'arrière-plan
        self.background_image = pygame.image.load("fichier/" + background_image_path)
        self.background_rect = self.background_image.get_rect()

        # Redimensionner l'arrière-plan pour s'adapter à la fenêtre
        self.background_image = pygame.transform.scale(self.background_image, (width, height))
        self.background_rect = self.background_image.get_rect()

        # Charger la police
        with zipfile.ZipFile("fichier/" + font_path, 'r') as zip_ref:
            zip_ref.extractall()
        self.font = pygame.font.Font("fichier/Mecanix.ttf", 30)

        # Options du menu
        self.menu_options = [" Lancer une Partie", "Ajouter un Pokemon", "Acceder au Pokedex", "  Quitter"]
        self.button_rects = [
            pygame.Rect((self.width - 200) // 2, 100 + i * 70, 200, 50)
            for i in range(len(self.menu_options))
        ]

    def draw_menu(self):
        self.screen.blit(self.background_image, self.background_rect)

        for i, option in enumerate(self.menu_options):
            # Ajuster les coordonnées pour déplacer les phrases vers le bas et vers la gauche
            text = self.font.render(option, True, (225, 0, 0))
            text_rect = text.get_rect(center=(self.width // 2, 150 + i * 70))
            self.screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                for i, button_rect in enumerate(self.button_rects):
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        return i + 1
        return 0

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                option_selected = self.handle_event(event)
                if option_selected == 1:
                    print("Lancer une Partie")
                    # code pour lancer une nouvelle partie
                elif option_selected == 2:
                    print("Ajouter un Pokémon")
                    # Demander le nom du Pokémon à ajouter
                    nom_pokemon = input("Entrez le nom du Pokémon: ")

                    # Utiliser la méthode statique pour créer le Pokémon
                    new_pokemon = Pokemon.create_pokemon(nom_pokemon, 30, 0, 0)  # Remplacez les valeurs par défaut

                    # Ajouter le nouveau Pokémon à la liste des Pokémon existants
                    self.pokemons.append(new_pokemon)
                    print(f"{new_pokemon.nom} ajouté avec succès!")
                elif option_selected == 3:
                    print("Accéder au Pokédex")
                    print("Pokémons existants:")
                    for idx, pokemon in enumerate(self.pokemons, start=1):
                        print(f"{idx}. {pokemon.nom} (Niveau {pokemon.niveau})")

                    # Demander à l'utilisateur de choisir un Pokémon
                    choice = int(input("Entrez le numéro du Pokémon que vous voulez afficher (0 pour revenir): "))
                    if 0 < choice <= len(self.pokemons):
                        selected_pokemon = self.pokemons[choice - 1]
                        print(f"Affichage des détails de {selected_pokemon.nom}:")
                        print(f"Niveau: {selected_pokemon.niveau}")
                        print(f"Points de vie: {selected_pokemon.points_de_vie}")
                        print(f"Attaque: {selected_pokemon.puissance_attaque}")
                        print(f"Défense: {selected_pokemon.defense}")
                        print(f"Types: {', '.join(selected_pokemon.type)}")
                    elif choice == 0:
                        pass
                    else:
                        print("Choix invalide. Revenez au menu.")
                elif option_selected == 4:
                    pygame.quit()
                    sys.exit()

            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    # Initialisez les instances de la classe Pokemon avec les arguments nécessaires
    niveau = 30
    x_bulbasaur, y_bulbasaur = 50, 50
    x_charmander, y_charmander = 200, 50
    x_squirtle, y_squirtle = 350, 50
    x_pikachu, y_pikachu = 500, 50
    x_sandshrew, y_sandshrew = 50, 250
    x_eevee, y_eevee = 200, 250

    bulbasaur = Pokemon('Bulbasaur', 100, niveau, 25, 15, ['Type1', 'Type2'], x_bulbasaur, y_bulbasaur)
    charmander = Pokemon('Charmander', 90, niveau, 25, 18, ['Type1', 'Type2'], x_charmander, y_charmander)
    squirtle = Pokemon('Squirtle', 95, niveau, 23, 20, ['Type1', 'Type2'], x_squirtle, y_squirtle)
    pikachu = Pokemon('Pikachu', 85, niveau, 30, 15, ['Type1'], x_pikachu, y_pikachu)
    sandshrew = Pokemon('Sandshrew', 95, niveau, 20, 25, ['Type1'], x_sandshrew, y_sandshrew)
    eevee = Pokemon('Eevee', 80, niveau, 20, 20, ['Type1'], x_eevee, y_eevee)
    pokemons = [bulbasaur, charmander, squirtle, pikachu, sandshrew, eevee]

    menu = MenuPage(600, 650, "_caf418dd-8623-42c9-867c-ca4a5dc6d58a.jpg", "mecanix.zip", pokemons)
    menu.run_menu()


