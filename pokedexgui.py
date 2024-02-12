import pygame
import json

pygame.init()





width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pokédex")


background = pygame.image.load("Imagepokemon/Pokedex.jpg")
background = pygame.transform.scale(background, (width, height))

#Couleurs
white = (255, 255, 255)


#Police
font = pygame.font.Font(None, 36)

def display_pokemon(pokemon_id):
    # Afficher les informations du Pokémon sur l'écran
        print(pokemon_data, "test")
        text = font.render(f"{pokemon_data[(pokemon_id)]['Nom']} - {pokemon_data[(pokemon_id)]['type']}", True)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        pygame.display.flip()
display_pokemon(1)




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

    



    def display_pokemon(pokemon_id):
            with open("pokedex.json", "r") as file:
                pokemon_data = json.load(file)

    # Afficher les informations du Pokémon sur l'écran
    text = font.render(f"{pokemon_data[(pokemon_id)]['Nom']} - {pokemon_data[(pokemon_id)]['type']}", True)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.flip()
display_pokemon(1)


if __name__ == '__main__':
    dex = Pokedex()
    dexc = Pokedex(save='pokedex.json')
    dex.add_pokemon(1)
    # Code pour utiliser la sauvegarde dex = Pokedex(save='pokemon.json')
    print(dex.read_dex())







# Boucle principale
running = True
current_pokemon = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_pokemon += 1
                if current_pokemon > len(pokemon_data):
                    current_pokemon = 1
                display_pokemon(current_pokemon)
            elif event.key == pygame.K_LEFT:
                current_pokemon -= 1
                if current_pokemon < 1:
                    current_pokemon = len(pokemon_data)
                display_pokemon(current_pokemon)
    # Afficher le fond d'écran
    screen.blit(background, (0, 0))
    pygame.display.flip()









#Quitter Pygame
pygame.quit()





