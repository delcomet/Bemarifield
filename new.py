from colors import *
from pygame.locals import *
import button, os, math


class Game:
    def __init__(self, width, height, filename="cruisin.jpg"):
        self.background = pygame.image.load(filename)
        self.window_size = width, height
        self.window = pygame.display.set_mode((width, height))
        self.background = pygame.transform.scale(self.background, (width, height))
        self.score = 0

        self.button_group = pygame.sprite.Group()
        self.static_button_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()

        self.settings = check_settings()
        self.score_board = check_score()
        self.name = self.settings[2]
        if len(self.name) == 0:
            self.name = "default"

    def game(self):
        pass

    def gameover(self):
        pass

    def menu(self):
        newgame = button.Button(black, 170, 40, 10, 150, "NEW GAME", 20)
        options_button = button.Button(black, 170, 40, 10, 200, "OPTIONS", 20)
        score_button = button.Button(black, 170, 40, 10, 250, "SCOREBOARD", 20)
        quitbutton = button.Button(black, 170, 40, 10, 360, "QUIT", 20)
        options_ok = button.Button(black, 170, 40, 370, 400, "OK", 20, 255, True)
        music_button = button.Button(black, 170, 40, 370, 200, "Music", 20, 255, True)
        sound_button = button.Button(black, 170, 40, 370, 300, "Sounds", 20, 255, True)
        name_button = button.Button(black, 150, 40, 470, 0, str(self.name), 20, 150)
        options_box = button.Button(white, 300, 400, 320 + 50, 240, "", 20, 150, True)
        score_box = button.Button(white, 300, 400, 320 + 50, 240, "", 20, 150, True)
        self.button_group.add(newgame, options_button, quitbutton, score_button, name_button)

        music_button.active(self.settings[0])
        sound_button.active(self.settings[1])

        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONUP:
                    for pressed_button in self.button_group:
                        pressed_button.active(0)
                    if quitbutton.rect.collidepoint(mouse):
                        return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for pressed_button in self.button_group:
                        if pressed_button.rect.collidepoint(pygame.mouse.get_pos()):
                            pressed_button.active()

            self.window.blit(self.background, (0, 0))
            self.button_group.draw(self.window)
            pygame.display.update()



class Player:
    def __init__(self):
        pass


class Enemy:
    def __init__(self):
        pass


def check_score():
    if os.path.isfile("score.txt"):
        if os.stat("score.txt").st_size == 0:
            fw = open("score.txt", "w")
            name_list = ["default", "default", "default", "default", "default"]
            value_list = [0, 0, 0, 0, 0]
            fw.writelines([str(name_list), "\n", str(value_list)])
            fw.close()
    else:
        fw = open("score.txt", "w")
        name_list = ["default", "default", "default", "default", "default"]
        value_list = [0, 0, 0, 0, 0]
        fw.writelines([str(name_list), "\n", str(value_list)])
        fw.close()

    fr = open("score.txt", "r")
    score_board = fr.readlines()
    name_list = eval(score_board[0])
    value_list = eval(score_board[1])

    return name_list, value_list


def update_score():
    pass


def check_settings():
    if os.path.isfile("options.txt"):
        if os.stat("options.txt").st_size == 0:
            fw = open("options.txt", "w")
            fw.writelines(["music_volume: 1\n", "sound_volume: 1\n", "Name: default\n"])
            fw.close()
    else:
        fw = open("options.txt", "w")
        fw.writelines(["music_volume: 1\n", "sound_volume: 1\n", "Name: default\n"])
        fw.close()

    fr = open("options.txt", "r")
    settings = fr.readlines()
    music = int(settings[0][14])
    #pygame.mixer.music.set_volume(music)
    sound = int(settings[1][14])
    name = settings[2][6:-1]
    a = [music, sound, name]
    return a


def update_check_settings():
    pass


def write():
    pass


def player_input():
    pass

if __name__ == "__main__":
    pygame.init()
    game = Game(640, 480)
    game.menu()
