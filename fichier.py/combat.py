# combat.py
import random
import json

class Combat:
    def __init__(self, player_pokemon, opponent_pokemon):
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon

    def get_type_multiplier(self, attacker, defender):
        return 1.0  # Simplification, vous pouvez ajouter votre logique ici

    def calculate_damage(self, attacker, defender):
        base_damage = random.randint(10, 20)  # À ajuster
        type_multiplier = self.get_type_multiplier(attacker, defender)
        damage = (attacker.get_attack() / defender.get_defense()) * base_damage * type_multiplier
        return int(damage)

    def apply_damage(self, damage, target):
        target.receive_damage(damage)

    def determine_winner(self):
        if self.player_pokemon.get_hp() > 0 and self.opponent_pokemon.get_hp() <= 0:
            return 'player'
        elif self.opponent_pokemon.get_hp() > 0 and self.player_pokemon.get_hp() <= 0:
            return 'opponent'
        else:
            return 'none'

    def get_winner_name(self):
        winner = self.determine_winner()
        if winner == 'player':
            return self.player_pokemon.get_name()
        elif winner == 'opponent':
            return self.opponent_pokemon.get_name()
        else:
            return 'none'

    def save_to_pokedex(self, pokedex):
        if self.determine_winner() == 'player':
            pokedex.add_pokemon(self.player_pokemon)
        elif self.determine_winner() == 'opponent':
            pokedex.add_pokemon(self.opponent_pokemon)

    def start_combat(self):
        damage_to_opponent = self.calculate_damage(self.player_pokemon, self.opponent_pokemon)
        self.apply_damage(damage_to_opponent, self.opponent_pokemon)

        damage_to_player = self.calculate_damage(self.opponent_pokemon, self.player_pokemon)
        self.apply_damage(damage_to_player, self.player_pokemon)

        return {
            'winner': self.determine_winner(),
            'winner_name': self.get_winner_name(),
            'damage_to_opponent': damage_to_opponent,
            'damage_to_player': damage_to_player
        }
