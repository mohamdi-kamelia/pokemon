class Button:
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        # Initialisation de la classe Button
        self.pos = pos  # Position du bouton
        self.text_input = text_input  # Texte affiché sur le bouton
        self.font = font  # Police d'écriture utilisée pour le texte
        self.base_color = base_color  # Couleur de base du bouton
        self.hovering_color = hovering_color  # Couleur lorsque la souris survole le bouton
        self.text = self.font.render(self.text_input, True, self.base_color)  # Surface contenant le texte rendu avec la couleur de base
        self.rect = self.text.get_rect(center=self.pos)  # Rectangle englobant le texte pour la détection des collisions

    def update(self, window):
        # Met à jour l'affichage du bouton sur la fenêtre donnée
        window.blit(self.text, self.rect)

    def checkForInput(self, position):
        # Vérifie si la position donnée est à l'intérieur du rectangle du bouton
        if self.rect.collidepoint(position):
            return True  # La position est à l'intérieur du bouton
        return False  # La position n'est pas à l'intérieur du bouton

    def changeColor(self, position):
        # Change la couleur du texte du bouton si la position donnée est à l'intérieur du rectangle du bouton
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)  # Change la couleur du texte à la couleur de survol
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)  # Reviens à la couleur de base du texte




          