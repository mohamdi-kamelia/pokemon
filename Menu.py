import pygame 
import sys

class Menu :
    def __init__(self , width , height , arriére_plan):
        self.width = width
        self.height = height
        self.menu = ["Lancer une partie " , "Ajouter un Pokémon" , "Accéder au pokédex" , "Quitter le jeu "]
        self.arriére_plan = arriére_plan
        self.arriére_plan = pygame.image.load("pokemon-go-suivi-exploration-tutoriel.jpg")
    def afficher_menu(self , fenetre):
        fenetre.blit(self.arriére_plan , (0 ,0))
        

