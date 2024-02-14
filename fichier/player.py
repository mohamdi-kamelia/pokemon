from typing import Any
import pygame

# Classe représentant le joueur contrôlé par l'utilisateur
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Chargement de la feuille de sprites du joueur
        self.sprite_sheet = pygame.image.load('Map/player.png')
        # Récupération de l'image du joueur
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])  # Pour enlever la couleur d'arrière-plan du joueur
        self.rect = self.image.get_rect()
        self.position = [x, y]
        # Paramètres pour différentes animations du joueur
        self.images = {
            'down': self.get_image(0, 0),
            'left': self.get_image(0, 32),
            'right': self.get_image(0, 64),
            'up': self.get_image(0, 96)
        }
        # Rectangle pour la détection des collisions au niveau des pieds du joueur
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()  # Ancienne position du joueur
        self.speed = 2  # Vitesse de déplacement du joueur

    # Méthode pour enregistrer la position actuelle du joueur
    def save_location(self):
        self.old_position = self.position.copy()

    # Méthode pour changer l'animation du joueur
    def change_animation(self, name):
        self.image = self.images[name]  # Copie de l'image correspondant à l'animation spécifiée
        self.image.set_colorkey((0, 0, 0))  # Suppression de la couleur d'arrière-plan

    # Méthodes pour les mouvements du joueur dans différentes directions
    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    # Méthode pour mettre à jour la position du joueur et son rectangle de collision
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    # Méthode pour revenir à la position précédente en cas de collision
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    # Méthode pour extraire une image de la feuille de sprites du joueur
    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
