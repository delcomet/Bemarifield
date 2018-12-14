import button, bem
from colors import *
from helpers import static_path

class Menu:
    def __init__(self, width=640, height=480):
        self.game = bem.Game(width, height, static_path("bggirl2.jpg"))
        pygame.mixer.music.load(static_path("sail.ogg"))
        pygame.mixer.music.play()
        
        self.clock = pygame.time.Clock()
        self.fps = 120

        self.settings = self.game.check_settings()
        self.score_board = self.game.check_score()
        self.name = self.settings['name']
        if len(self.name) == 0:
            self.name = "default"

        # Buttons
        self.newgame = button.Button(black, 170, 40, 10, 150, "NEW GAME", 20)
        self.options_button = button.Button(black, 170, 40, 10, 200, "OPTIONS", 20)
        self.score_button = button.Button(black, 170, 40, 10, 250, "SCOREBOARD", 20)
        self.quitbutton = button.Button(black, 170, 40, 10, 360, "QUIT", 20)
        self.options_ok = button.Button(black, 170, 40, 370, 400, "OK", 20, 255, True)
        self.music_button = button.Button(black, 170, 40, 370, 200, "Music", 20, 255, True)
        self.sound_button = button.Button(black, 170, 40, 370, 300, "Sounds", 20, 255, True)
        self.name_button = button.Button(black, 150, 40, 470, 0, str(self.name), 20, 150)
        self.options_box = button.Button(white, 300, 400, 320 + 50, 240, "", 20, 150, True)
        self.score_box = button.Button(white, 300, 400, 320 + 50, 240, "", 20, 150, True)

        pygame.mixer.music.set_volume(self.settings['music'])
        self.music_button.active(self.settings['music'])
        self.sound_button.active(self.settings['sound'])

        self.button_group = pygame.sprite.Group()
        self.static_button_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.button_group.add(self.newgame, self.options_button, self.quitbutton, self.score_button, self.name_button)
        self.gameloop()

    def input(self):
        self.name = ""
        pygame.key.set_repeat(500, 100)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if self.name_button.width > self.name_button.text.get_rect().width+20:
                        if event.unicode.isalpha() or event.unicode.isalnum():
                            self.name += event.unicode
                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    if event.key == pygame.K_RETURN:
                        if len(self.name) == 0:
                            self.name = "default"
                        self.name_button.inputtedtext = str(self.name)
                        self.name_button.active()
                        self.game.update_settings(name=self.name)

                        return
                elif event.type == pygame.QUIT:
                    quit()
            self.name_button.inputtedtext = str(self.name)
            self.name_button.active()
            self.draw_everything()

            self.clock.tick(self.fps)
            pygame.display.update()

    def apply_settings(self):
        pygame.mixer.music.set_volume(self.settings['music'])
        self.music_button.active(self.settings['music'])
        self.sound_button.active(self.settings['sound'])

        self.game.update_settings(
            music=self.settings['music'], 
            sound=self.settings['sound'], 
            name=self.settings['name']
        )

    def draw_everything(self):
        self.game.window.blit(self.game.background, (0, 0))
        self.box_group.draw(self.game.window)
        self.button_group.draw(self.game.window)
        self.static_button_group.draw(self.game.window)
        self.game.write("Name:", 25, [390, 0], white, self.game.window)
        if self.box_group.has(self.options_box):
            self.game.write("Options", 40, [320 + 50, 90], black, self.game.window, align='center')
        if self.box_group.has(self.score_box):
            self.game.write("Scoreboard", 40, [320 + 50, 90], black, self.game.window, align='center')
            y_pos = 140
            for name in self.score_board[0]:
                self.game.write(str(name) + ":", 20, [370, y_pos], black, self.game.window, align='right')
                y_pos += 30
            y_pos = 140
            for value in self.score_board[1]:
                self.game.write(str(value), 20, [380, y_pos], black, self.game.window)
                y_pos += 30

    def gameloop(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.MOUSEBUTTONUP:
                    for pressed_button in self.button_group:
                        pressed_button.active(0)

                    if self.quitbutton.rect.collidepoint(pygame.mouse.get_pos()):
                        quit()

                    if self.newgame.rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.mixer.music.load(static_path("king_kunta.ogg"))
                        pygame.mixer.music.play()
                        return 

                    if self.name_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.name_button.inputtedtext = ""
                        self.name_button.active()
                        self.input()
                        self.name_button.inputtedtext = str(self.name)
                        self.name_button.active(0)

                    if self.static_button_group.has(self.music_button):
                        if self.music_button.rect.collidepoint(pygame.mouse.get_pos()):
                            self.settings['music'] = int(not self.settings['music'])
                            self.apply_settings()

                    if self.static_button_group.has(self.sound_button):
                        if self.sound_button.rect.collidepoint(pygame.mouse.get_pos()):
                            self.settings['sound'] = int(not self.settings['sound'])
                            self.apply_settings()

                    if self.options_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.box_group.remove(self.score_box)
                        self.box_group.add(self.options_box)
                        self.static_button_group.add(self.options_ok, self.music_button, self.sound_button)

                    if self.score_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.box_group.remove(self.options_box)
                        self.static_button_group.remove(self.music_button, self.sound_button)
                        self.box_group.add(self.score_box)
                        self.static_button_group.add(self.options_ok)

                    if self.static_button_group.has(self.options_ok):
                        if self.options_ok.rect.collidepoint(pygame.mouse.get_pos()):
                            self.box_group.remove(self.options_box, self.score_box)
                            self.static_button_group.remove(self.options_ok, self.music_button, self.sound_button)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for pressed_button in self.button_group:
                        if pressed_button.rect.collidepoint(pygame.mouse.get_pos()):
                            pressed_button.active()

            self.draw_everything()

            self.clock.tick(self.fps)
            pygame.display.update()
