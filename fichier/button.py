class Button:
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        self.pos = pos
        self.text_input = text_input
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = self.text.get_rect(center=self.pos)


    def update(self, window):
        window.blit(self.text, self.rect)

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)



          