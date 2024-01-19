# jeu.py
import random
import requests
from pokemon import Pokemon
from combat import Combat
from pokedex import Pokedex

class Jeu:
    def __init__(self):
        self.pokedex = Pokedex()
        self.combat = Combat()
        self.current_pokemon = None  
        self.opponent_pokemon = None

    def start_game(self):
        print("Bienvenue dans le jeu Pokémon!")

        player_pokemon = self.choose_pokemon()
        opponent_pokemon = self.create_random_pokemon_from_api()

        self.combat.battle(player_pokemon, opponent_pokemon)

        self.pokedex.add_pokemon(player_pokemon)
        self.pokedex.add_pokemon(opponent_pokemon)

        self.pokedex.display_pokemon()

    def choose_pokemon(self):
        print("\nChoisissez votre Pokémon:")
        pokemon_data = self.get_random_pokemon_data_from_api()
        return Pokemon(**pokemon_data)

    def create_random_pokemon_from_api(self):
        pokemon_data = self.get_random_pokemon_data_from_api()
        return Pokemon(**pokemon_data)

    def get_random_pokemon_data_from_api(self):
        response = requests.get("https://tyradex.vercel.app/api/v1/pokemon")

        if response.status_code == 200:
            pokemon_data_list = response.json()
            
            if pokemon_data_list:
                pokemon_data = random.choice(pokemon_data_list)
                print(pokemon_data)
                if all(key in pokemon_data for key in ('name', 'stats', 'types')):
                    return {
                        'name': pokemon_data['name'],
                        'hp': pokemon_data['stats']['hp'],  # Ajustement ici
                        'attack_power': pokemon_data['stats']['atk'],  # Ajustement ici
                        'defense': pokemon_data['stats']['def'],  # Ajustement ici
                        'types': [type_data['type']['name'] for type_data in pokemon_data['types']]
                    }
                else:
                    print("Données Pokémon manquantes dans la réponse de l'API.")
            else:
                print("La réponse de l'API ne contient pas de données de Pokémon.")
        else:
            print("Erreur lors de la récupération des données depuis l'API.")

# Exemple d'utilisation
if __name__ == "__main__":
    jeu = Jeu()
    jeu.start_game()
