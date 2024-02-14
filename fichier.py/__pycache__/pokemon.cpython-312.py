�
    �\�eU  �            
       �T  � d dl Z d dlmZ d dl mZ d dlZd dlZd dlmZ  e j                  �        dZ	dZ
e	e
fZe j                  j                  e�      Ze j                  j                  d�       dZdZd	Zd
ZdZdZdZdZ G d� d�      Z ed�       ed�       ed�       ed�       ed�      gZ G d� de j4                  j6                  �      ZdZd\  ZZd\  Z Z!d\  Z"Z#d\  Z$Z%d\  Z&Z'd\  Z(Z) edded d!d"d#gee�      Z* ed$d%ed d&d"d#ge e!�      Z+ ed'd(ed)d*d"d#ge"e#�      Z, ed+d,edd!d"ge$e%�      Z- ed-d(ed*d d"ge&e'�      Z. ed.d/ed*d*d"ge(e)�      Z/e*e+e,e-e.e/gZ0dZ1dZ2d0Z3e3d1k7  �r5e jh                  jk                  �       D ]  Z4e4jl                  ek(  s�d1Z3� e3d0k(  r�ejo                  e�       e*jq                  �        e+jq                  �        e,jq                  �        e-jq                  �        e/jq                  �        e.jq                  �        e jr                  ju                  �       Z;e0D ]N  Z<e<j{                  �       j}                  e;�      s�#e jp                  j                  eee<j{                  �       d2�       �P e j                  j�                  �        e3d1k7  r��5 e j�                  �        y)3�    N)�QUIT)�Rect)�urlopeni�  �Pokemon)r   r   r   )��   �   �    )��   r
   r
   )r   r
   r   )r
   r   r   )��   r   r   )�   �   �   zhttps://pokeapi.co/api/v2c                   �   � e Zd Zd� Zy)�Typec                 �   � || _         y �N)�	type_name)�selfr   s     �:c:\Users\utilisateur\Desktop\pokemon\fichier.py\pokemon.py�__init__zType.__init__   s	   � �"���    N)�__name__�
__module__�__qualname__r   � r   r   r   r      s   � �#r   r   �Normal�Feu�Eau�Terre�Electricc                   �&   � e Zd Zd� Zd� Zdd�Zd� Zy)r   c	                 �r  � t         j                  j                  j                  | �       || _        || _        || _        || _        |D �	cg c]  }	t        |	�      �� c}	| _	        t        j                  t        � d| j                  j                  �       � ��      }
|
j                  �       | _        || _        || _        || _        d| _        | j                  d   }|D ]~  }|d   d   dk(  r/|d   | j                  z   | _        |d   | j                  z   | _        �=|d   d   dk(  r|d   | _        �S|d   d   d	k(  r|d   | _        �i|d   d   d
k(  s�u|d   | _        �� g | _	        | j                  d   D ]=  }|d   d   }	| j                  j/                  |	�       d| _        | j3                  d�       �? y c c}	w )Nz	/pokemon/�   �stats�stat�name�hp�	base_stat�attack�defense�speed�types�type�   �front_default)�pygame�sprite�Spriter   �nom�points_de_vie�puissance_attaquer*   r   r-   �requests�get�base_url�lower�json�niveau�x�y�num_potions�
current_hp�max_hpr)   r+   �append�size�
set_sprite)r   r3   r4   r;   r5   r*   r,   r<   r=   r   �reqr$   r%   �pokemon_types                 r   r   zPokemon.__init__$   s�  � ������%�%�d�+����*���!2������6;�<��T�)�_�<��	� �l�l�h�Z�y������1A�0B�C�D���H�H�J��	� ��� ������ ��� �	�	�7�#��� 		/�D��F�|�F�#�t�+�"&�{�"3�d�k�k�"A���"�;�/�$�+�+�=����f��f�%�(�2�"�;�/����f��f�%��2�#�K�0����f��f�%��0�!�+�.��
�		/� ��	� �I�I�g�.� 	-�L�$�V�,�V�4�I��I�I���Y�'� �D�I� �O�O�O�,�	-��? =s   �
F4c                 �  � | j                   d   |   }t        |�      j                  �       }t        j                  |�      }t
        j                  j                  |�      j                  �       | _        | j                  | j                  j                  �       z  }| j                  j                  �       |z  }| j                  j                  �       |z  }t
        j                  j                  | j                  ||f�      | _        y )N�sprites)r:   r   �read�io�BytesIOr0   �image�load�convert_alpharB   �	get_width�
get_height�	transform�scale)r   �siderK   �image_stream�
image_filerQ   �	new_width�
new_heights           r   rC   zPokemon.set_spriteT   s�   � � �	�	�)�$�T�*���u�~�*�*�,���Z�Z��-�
��\�\�&�&�z�2�@�@�B��
� �	�	�D�J�J�0�0�2�2���J�J�(�(�*�U�2�	��J�J�)�)�+�e�3�
��%�%�+�+�D�J�J��J�8O�P��
r   c                 ��   � | j                   j                  �       }ddd|f}|j                  |d t        j                  �       t
        j                  || j                  | j                  f�       y )Nr   )	rK   �copy�fillr0   �BLEND_RGBA_MULT�game�blitr<   r=   )r   �alphar1   �transparencys       r   �drawzPokemon.drawc   sQ   � ������"���S�#�u�-�����L�$��(>�(>�?��	�	�&�4�6�6�4�6�6�*�+r   c                 �   � t        j                  | j                  | j                  | j                  j                  �       | j                  j                  �       �      S r   )r0   r   r<   r=   rK   rN   rO   )r   s    r   �get_rectzPokemon.get_recti   s9   � ��{�{�4�6�6�4�6�6�4�:�:�+?�+?�+A�4�:�:�CX�CX�CZ�[�[r   N)r   )r   r   r   r   rC   r_   ra   r   r   r   r   r   #   s   � �.-�`Q�,�\r   �   )�2   rc   )r
   rc   )i^  rc   )i�  rc   )rc   ��   )r
   rd   �	Bulbasaur�d   �   �   �Type1�Type2�
Charmander�Z   �   �Squirtle�_   �   �   �Pikachu�U   �	Sandshrew�Eevee�P   zselect pokemon�quit�   )Br0   �pygame.localsr   r   r6   rI   �urllib.requestr   �init�
game_width�game_heightrB   �display�set_moder[   �set_caption�black�gold�grey�green�red�white�Kr8   r   �TYPESr1   r2   r   r;   �x_bulbasaur�y_bulbasaur�x_charmander�y_charmander�
x_squirtle�
y_squirtle�	x_pikachu�	y_pikachu�x_sandshrew�y_sandshrew�x_eevee�y_eevee�	bulbasaur�
charmander�squirtle�pikachu�	sandshrew�eevee�pokemons�player_pokemon�rival_pokemon�game_status�eventr7   r-   rY   r_   �mouse�get_pos�mouse_cursor�pokemonra   �collidepoint�rect�updaterw   r   r   r   �<module>r�      s�  �� � � � � 	� "� ����� �
����K� ���~�~���t�$�� ��� � �9� %� 	��������������&��#� #� 
�h���e��d�5�k�4��=�$�z�BR�S��G\�f�m�m�"�"� G\�X 
��!� ��[�$� ��l� � �
�J�� �	�9�"� ��[�� ��� �K��f�b�"�w��6H�+�Wb�c�	��\�2�v�r�2���7I�<�Ye�f�
��:�r�6�2�r�G�W�3E�z�S]�^��
�)�R���R�'��I�y�
Q���K��V�R��g�Y��[�Y�	����V�R��g�Y���I���z�8�W�i��G�� ���� ���V�����!�!�#� !���:�:��� �K�!�
 �&�&��	�	�!�� 	�����������������
�
������ �|�|�+�+�-��� 	E�G����!�.�.�|�<���� � ��u�g�.>�.>�.@�!�D�	E� 	������1 �V��4 �����r   