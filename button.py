from colors import *


class Button(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, text, font=35, alpha=255, center=False):
        super(Button, self).__init__()

        self.image = pygame.Surface((width, height))
        self.color = color
        self.inputtedtext = text
        self.image.fill(color)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        if center is False:
            self.rect.x = x
            self.rect.y = y
        if center is True:
            self.rect.x = x - width/2
            self.rect.y = y - height/2
        self.font = pygame.font.SysFont("Comic Sans MS", font)
        self.text = self.font.render(text, True, white, )
        self.width = width
        self.height = height
        self.originx = width / 2 - self.text.get_rect().width / 2
        self.originy = height / 2 - self.text.get_rect().height / 2
        self.image.blit(self.text, (self.originx, self.originy))

    def active(self, value=1):
        if value is 1:
            self.image.fill(blue)
            self.text = self.font.render(self.inputtedtext, True, white, )
            self.originx = self.width / 2 - self.text.get_rect().width / 2
            self.originy = self.height / 2 - self.text.get_rect().height / 2
            self.image.blit(self.text, (self.originx, self.originy))
            return value

        if value is 0:

            self.image.fill(self.color)
            self.text = self.font.render(self.inputtedtext, True, white, )
            self.image.blit(self.text, (self.originx, self.originy))
            return value
