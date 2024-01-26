import requests
import json
import os

class PokemonDataDownloader:
    def __init__(self):
        self.base_url = 'https://pokeapi.co/api/v2/pokemon/'
        self.pokemon_numbers = [ 100, 1, 4, 7, 27, 25, 133 , 8 , 120 , 2 , 94]
        self.pokemon_list = []

        # Créez un dossier pour stocker les images localement
        if not os.path.exists('images'):
            os.makedirs('images')

    def download_image(self, url, save_path):
        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)

    def get_pokemon_data(self):
        for i in self.pokemon_numbers:
            full_url = f"{self.base_url}{i}"
            response = requests.get(full_url)
            data = response.json()

            pokemon_info = {
                'name': data['name'],
                'types': [type_data['type']['name'] for type_data in data['types']],
                'hp': data['stats'][0]['base_stat'],
                'attack': data['stats'][1]['base_stat'],
                'defense': data['stats'][2]['base_stat'],
                'speed': data['stats'][5]['base_stat'],
                'image_url': data['sprites']['front_default'],
            }

            # Téléchargez l'image et sauvegardez-la localement
            image_save_path = f"images/{pokemon_info['name']}.png"
            self.download_image(pokemon_info['image_url'], image_save_path)

            # Ajoutez le chemin local de l'image à la structure des données
            pokemon_info['image_path'] = image_save_path

            self.pokemon_list.append(pokemon_info)

        with open('pokemon.json', 'w') as file:
            json.dump({'pokemon_list': self.pokemon_list}, file)
    
# Exemple d'utilisation de la classe
if __name__ == "__main__":
    downloader = PokemonDataDownloader()
    downloader.get_pokemon_data()


