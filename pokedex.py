import json


class Pokedex:
    def __init__(self, save:str=None):
        self.data = [None] * 24
        if save is None:
            with open("pokedex.json", 'r', encoding='utf-8') as f:
                pokdata = json.load(f)
                for k in range(18, 24):
                    self.data[k] = pokdata[k]
            self.save_dex()
        else:
            with open(save, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
    
    def read_dex(self):
        data = []
        for k in range(len(self.data)):
            if self.data[k] is not None:
                data.append(self.data[k])
        return data
    
    def add_pokemon(self, id_pok: int):
        if isinstance(id_pok, int):
            with open('pokedex.json', 'r', encoding='utf-8') as f:
                pokdata = json.load(f)
                self.data[id_pok] = pokdata[id_pok]
            self.save_dex()
    
    def save_dex(self):
        with open('pokemon.json', 'w') as f:
                json.dump(self.data, f, indent=2)


if __name__ == '__main__':
    dex = Pokedex()
    dexc = Pokedex(save='pokedex.json')
    dex.add_pokemon(1)
    # Code pour utiliser la sauvegarde dex = Pokedex(save='pokemon.json')
    print(dex.read_dex())



