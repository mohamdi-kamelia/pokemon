# pokedex.py
class Pokedex:
    def __init__(self):
        self.pokemon_list = []

    def add_pokemon(self, pokemon):
        if pokemon not in self.pokemon_list:
            self.pokemon_list.append(pokemon)
            print(f"{pokemon.name} added to the Pokedex.")

    def display_pokemon(self):
        print("\n--- Pokedex ---")
        for pokemon in self.pokemon_list:
            pokemon.display_info()

