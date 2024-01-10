import pygame
import sys
import zipfile

class MenuPage:
    def __init__(self, width, height, background_image_path, font_path):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Menu Pokémon")
        self.clock = pygame.time.Clock()

        # Charger l'arrière-plan
        self.background_image = pygame.image.load(background_image_path)
        self.background_rect = self.background_image.get_rect()

        # Redimensionner l'arrière-plan pour s'adapter à la fenêtre tout en conservant le ratio d'aspect
        aspect_ratio = self.background_rect.width / self.background_rect.height
        new_width = self.width
        new_height = int(new_width / aspect_ratio)
        self.background_image = pygame.transform.scale(self.background_image, (new_width, new_height))
        self.background_rect = self.background_image.get_rect()

        # Charger la police
        with zipfile.ZipFile("mecanix.zip", 'r') as zip_ref:
            zip_ref.extractall()
        self.font = pygame.font.Font("Mecanix.ttf", 30)

        # Options du menu
        self.menu_options = [" Lancer une Partie", "Ajouter un Pokemon", "Acceder au Pokedex", "            Quitter"]
        self.button_rects = [
            pygame.Rect((self.width - 200) // 2, 100 + i * 70, 200, 50)
            for i in range(len(self.menu_options))
        ]

    def draw_menu(self):
        self.screen.blit(self.background_image, self.background_rect)

        for i, option in enumerate(self.menu_options):
            # Ajuster les coordonnées pour déplacer les phrases vers le bas et vers la gauche
            text = self.font.render(option, True, (225, 0, 0))
            text_rect = text.get_rect(left=(self.width // 7), top=(self.height // 2) + i * 90)
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
                    # code pour ajouter un Pokémon
                elif option_selected == 3:
                    print("Accéder au Pokédex")
                    # code pour accéder au Pokédex
                elif option_selected == 4:
                    pygame.quit()
                    sys.exit()

            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    menu = MenuPage(600, 650, "_caf418dd-8623-42c9-867c-ca4a5dc6d58a.jpg", "mecanix.zip")
    menu.run_menu()

