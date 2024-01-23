import json


class Pokedex:
    def __init__(self, save:str=None):
        if save is None:
            self.data = [None] * 24
            with open("pokedex.json", 'r', encoding='utf-8') as f:
                pokdata = json.load(f)
                for k in range(18, 24):
                    self.data[k] = pokdata[k]
            self.save_dex()
    
    def read_dex(self):
        return self.data
    
    def add_pokemon(self, id_pok: int):
        if isinstance(id_pok, int):
            with open('pokedex.json', "r", encoding='utf-8') as f:
                pokdata = json.load(f)
                self.data[id_pok] = pokdata[id_pok]
            self.save_dex()
    
    def save_dex(self):
        with open('pokemon.json', 'w') as f:
                json.dump(self.data, f, indent=2)


if __name__ == '__main__':
    dex = Pokedex()























