import json
from combat import choix

class Pokedex:
    @staticmethod
    def load_pokedex():
        with open('pokedex.json', 'r') as file:
            data = json.load(file)
        return [choix(**entry) for entry in data['pokemons']]


