# pokemon.py
import requests
import random

class Pokemon:
    def __init__(self, pokemon_name, hp=None, attack_power=None, defense=None, types=None):
        self.name = pokemon_name
        self.base_url = 'https://pokeapi.co/api/v2/pokemon/'
        self.url = f'{self.base_url}{self.name.lower()}/'

        if hp is None or attack_power is None or defense is None or types is None:
            self.data = self.get_pokemon_data()
        else:
            self.data = {
                'name': pokemon_name,
                'stats': {
                    'hp': hp,
                    'attack': attack_power,
                    'defense': defense
                },
                'types': types
            }

    def get_pokemon_data(self):
        response = requests.get(self.url)
        return response.json()

    def get_name(self):
        return self.data['name']

    def get_stats(self):
        stats = self.data['stats']
        return {stat['stat']['name']: stat['base_stat'] for stat in stats}

    def get_attack(self):
        return self.get_stats()['attack']

    def get_defense(self):
        return self.get_stats()['defense']

    def get_hp(self):
        return self.get_stats()['hp']

    def receive_damage(self, damage):
        # Réduit les points de vie du Pokémon en fonction des dégâts reçus
        current_hp = self.get_hp()
        new_hp = max(0, current_hp - damage)
        self.data['stats']['hp'] = new_hp

    def display_info(self):
        print(f"Name: {self.get_name()}")
        print(f"HP: {self.get_hp()}")
        print(f"Attack: {self.get_attack()}")
        print(f"Defense: {self.get_defense()}")
        print(f"Types: {', '.join(self.data['types'])}")









