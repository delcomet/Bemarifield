import button, bem, menu
from colors import *


class Gameover:
    def __init__(self, score, width=640, height=480):
        self.game = bem.Game(width, height, "burn1.jpg")
        # 20pixels from the edge (640,480)
        self.newgame = button.Button(black, 230, 70, 20, 390, "NEW GAME")
        self.menubutton = button.Button(black, 130, 70, 300, 390, "MENU")
        self.quitbutton = button.Button(black, 130, 70, 490, 390, "QUIT")
        self.button_group = pygame.sprite.Group()
        self.button_group.add(self.quitbutton, self.newgame, self.menubutton)

        self.checked_score_values = self.game.check_score()[1]
        self.checked_settings = self.game.check_settings()
        self.game.update_score(self.checked_settings['name'], score)

        clock = pygame.time.Clock()
        fps = 120

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.MOUSEBUTTONUP:
                    self.quitbutton.active(0)
                    self.newgame.active(0)
                    self.menubutton.active(0)

                    if self.quitbutton.rect.collidepoint(pygame.mouse.get_pos()):
                        quit()
                    if self.newgame.rect.collidepoint(pygame.mouse.get_pos()):
                        return
                    if self.menubutton.rect.collidepoint(pygame.mouse.get_pos()):
                        menu.Menu()
                        return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.quitbutton.rect.collidepoint(pygame.mouse.get_pos()):
                        self.quitbutton.active()
                    if self.newgame.rect.collidepoint(pygame.mouse.get_pos()):
                        self.newgame.active()
                    if self.menubutton.rect.collidepoint(pygame.mouse.get_pos()):
                        self.menubutton.active()

            self.game.window.blit(self.game.background, (0, 0))
            self.button_group.draw(self.game.window)

            if score > self.checked_score_values[0]:
                self.game.write("  NEW HIGH SCORE!  ", 50, [640/2, 480/2-100], red, self.game.window, white, 'center', 200)

            self.game.write("  Score: " + str(score)+"  ", 40, [320, 20], black, self.game.window, white, 'center')

            clock.tick(fps)
            pygame.display.update()
