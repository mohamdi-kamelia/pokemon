import json
import random
import requests

class Combat:
    def __init__(self, joueur_pokemon):
        self.joueur_pokemon = joueur_pokemon
        self.adversaire_pokemon = self.choisir_adversaire()

    
    def choisir_adversaire():
    # Fonction pour choisir un adversaire depuis l'API
        api_url = "https://pokeapi.co/api/v2/pokemon/"
        pokemon_id = random.randint(1, 100)  # Choisissez un Pokémon au hasard
        url = f"{api_url}{pokemon_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur lors de la requête à l'API: {response.status_code}")
            return None

    def get_type_multiplier(self, attaquant_type, defenseur_type):
        type_multipliers = {
            "eau": {"eau": 1, "feu": 2, "terre": 0.5, "normal": 1},
            "feu": {"eau": 0.5, "feu": 1, "terre": 2, "normal": 1},
            "terre": {"eau": 2, "feu": 0.5, "terre": 1, "normal": 1},
            "normal": {"eau": 0.75, "feu": 0.75, "terre": 0.75, "normal": 1}
        }

        try:
            type_multiplier = type_multipliers[attaquant_type][defenseur_type]
        except KeyError:
            # Gérer le cas où le type n'est pas défini, par exemple en renvoyant un multiplicateur neutre
            type_multiplier = 1

        return type_multiplier

    def calculer_degats(self, attaquant_type, attaquant_attaque, defenseur_type):
        type_multiplier = self.get_type_multiplier(attaquant_type, defenseur_type)
        degats = int(attaquant_attaque * type_multiplier)
        return degats

    def enlever_points_de_vie(self, degats):
        self.adversaire_pokemon["points_de_vie"] -= degats

    def est_vivant(self):
        return self.adversaire_pokemon["points_de_vie"] > 0

    def obtenir_vainqueur(self):
        if self.est_vivant():
            return None
        else:
            return self.joueur_pokemon["nom"]

    def enregistrer_pokemon_dans_pokedex(self):
        try:
            with open("pokedex.json", "r") as file:
                pokedex = json.load(file)
        except FileNotFoundError:
            # Si le fichier n'existe pas, créez-le avec un dictionnaire vide
            pokedex = {}

        if self.adversaire_pokemon["nom"] not in pokedex:
            pokedex[self.adversaire_pokemon["nom"]] = {
                "type": self.adversaire_pokemon["type"],
                "defense": self.adversaire_pokemon["defense"],
                "attaque": self.adversaire_pokemon["attaque"],
                "points_de_vie": self.adversaire_pokemon["points_de_vie"]
            }

            with open("pokedex.json", "w") as file:
                json.dump(pokedex, file, indent=2)

    def afficher_resultat_combat(self):
        vainqueur = self.obtenir_vainqueur()
        if vainqueur:
            print(f"Le Pokémon {vainqueur} remporte le combat!")
        else:
            print("Le combat se termine par un match nul.")