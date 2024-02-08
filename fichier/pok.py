import requests
import json
import os

# Classe pour télécharger les données des Pokémon et leurs images
class PokemonDataDownloader:
    def __init__(self):
        # URL de base de l'API Pokémon
        self.base_url = 'https://pokeapi.co/api/v2/pokemon/'
        # Liste des numéros de Pokémon à télécharger
        self.pokemon_numbers = [100, 1, 4, 7, 27, 25, 133, 8, 120, 2, 94]
        # Liste pour stocker les informations des Pokémon téléchargés
        self.pokemon_list = []

        # Créez un dossier pour stocker les images localement s'il n'existe pas déjà
        if not os.path.exists('images'):
            os.makedirs('images')

    # Méthode pour télécharger une image à partir d'une URL et la sauvegarder localement
    def download_image(self, url, save_path):
        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)

    # Méthode pour récupérer les données des Pokémon
    def get_pokemon_data(self):
        for i in self.pokemon_numbers:
            full_url = f"{self.base_url}{i}"
            response = requests.get(full_url)
            data = response.json()

            # Extraire les informations pertinentes du Pokémon
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

            # Ajoutez les informations du Pokémon à la liste
            self.pokemon_list.append(pokemon_info)

        # Écrivez les données des Pokémon dans un fichier JSON
        with open('pokemon.json', 'w') as file:
            json.dump({'pokemon_list': self.pokemon_list}, file)
    
# Exemple d'utilisation de la classe
if __name__ == "__main__":
    # Création d'une instance de PokemonDataDownloader
    downloader = PokemonDataDownloader()
    # Téléchargement des données des Pokémon
    downloader.get_pokemon_data()



