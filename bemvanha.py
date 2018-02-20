import pygame
from gameover import *
pygame.init()


class Game:
    def __init__(self, window_width=640, window_height=480):
        global window, background, window_size
        self.window_size = window_width, window_height
        self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.background = pygame.image.load("bgroad.jpg")
        self.background = pygame.transform.scale(self.background, window_size)

        print("init Game")


class Player(pygame.sprite.Sprite):
    def __init__(self, filename=None):
        super(Player, self).__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.radius = self.image.get_width()/2

        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery

        print("init Player")

    def set_position(self, x, y):
        self.rect.x = x - self.origin_x
        self.rect.y = y - self.origin_y

    def update(self):
        if event is not None:
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                self.set_position(self.mouse_pos[0], self.mouse_pos[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_x=0, start_y=0, speed=5, filename=None):
        super(Enemy, self).__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.radius = self.image.get_width()/2

        self.pos_x = start_x
        self.pos_y = start_y

        self.x_speed = speed / 10
        self.y_speed = speed / 10

        print("init enemy")

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):

        self.pos_x += self.x_speed
        self.pos_y += self.y_speed
        self.set_position(self.pos_x, self.pos_y)

        if self.pos_x > window_size[0]-self.image.get_width():
            self.pos_x = window_size[0]-self.image.get_width()
            self.x_speed = -self.x_speed

        if self.pos_x < 0:
            self.pos_x = 0
            self.x_speed = -self.x_speed

        if self.pos_y > window_size[1]-self.image.get_height():
            self.pos_y = window_size[1]-self.image.get_height()
            self.y_speed = -self.y_speed

        if self.pos_y < 0:
            self.pos_y = 0
            self.y_speed = -self.y_speed


if __name__ == "__main__":
    game = Game()
    pygame.display.set_caption("Bemarifield 3.5")

    player = Player("bmwcurs.png")

    skoda = Enemy(100, 100, 10, "skoda.png")
    saab = Enemy(400, 100, 25, "saab.png")
    volkkari = Enemy(100, 200, 15, "volkkari.png")
    alfa = Enemy(100, 300, 20, "alfa.png")

    enemy_group = pygame.sprite.Group()
    enemy_group.add(skoda, saab, volkkari, alfa)

    player_group = pygame.sprite.Group()
    player_group.add(player)

    clock = pygame.time.Clock()
    fps = 120

    running = True

    while running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                Game(event.dict['w'], event.dict['h'])

        # Update functions

        player.update()
        skoda.update()
        saab.update()
        volkkari.update()
        alfa.update()

        # Logic Testing

        for hit in pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_circle):
            gameover(True, window_size[0], window_size[1])


        # Draw everything
        window.blit(background, (0, 0))
        enemy_group.draw(window)
        player_group.draw(window)

        # Delay Framerate

        clock.tick(fps)

        # Update the screen

        pygame.display.update()


    pygame.quit()
