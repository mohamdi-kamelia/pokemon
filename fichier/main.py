import pygame
import sys
from combat import Combat

# Initialise Pygame
pygame.init()

# Définissez quelques couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Définissez la taille de la fenêtre
largeur, hauteur = 1000, 800
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Pokémon Combat")

# Définissez votre Pokémon
joueur_pokemon = {
    "nom": "Pikachu",
    "type": "Electrique",
    "attaque": 20,
    "defense": 10,
    "points_de_vie": 50
}

# Créez une instance de la classe Combat
combat = Combat(joueur_pokemon)

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Simuler un tour de combat à chaque clic de souris
            degats = combat.calculer_degats(combat.joueur_pokemon["type"], combat.joueur_pokemon["attaque"],
                                           combat.adversaire_pokemon["type"])
            combat.enlever_points_de_vie(degats)
            print(f"{combat.adversaire_pokemon['nom']} subit {degats} dégâts. Points de vie restants: {combat.adversaire_pokemon['points_de_vie']}")

            # Affichez le résultat du combat
            combat.afficher_resultat_combat()

            # Enregistrez le Pokémon dans le Pokédex
            combat.enregistrer_pokemon_dans_pokedex()

    # Affichez les détails du combat dans la fenêtre
    fenetre.fill(BLANC)
    font = pygame.font.Font(None, 36)
    joueur_texte = font.render(f"Joueur Pokémon: {combat.joueur_pokemon}", True, NOIR)
    adversaire_texte = font.render(f"Adversaire Pokémon: {combat.adversaire_pokemon}", True, NOIR)
    fenetre.blit(joueur_texte, (10, 10))
    fenetre.blit(adversaire_texte, (10, 50))

    # Rafraîchissez l'écran
    pygame.display.flip()

# Quittez Pygame
pygame.quit()
