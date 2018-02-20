import gameover, menu, math, random, os
from colors import *

event = None


class Game:
    def __init__(self, width, height, filename="cruisin.jpg"):
        self.background = pygame.image.load(filename)
        self.window_size = width, height
        self.window = pygame.display.set_mode((width, height))
        self.background = pygame.transform.scale(self.background, (width, height))
        self.channel = pygame.mixer.Channel(1)
        self.score = 0

    def game_over(self):
        global time
        self.channel.play(fail_sound)

        for enemy in enemy_group:
            enemy.reset_pos()
            enemy.speed = [random.randint(20, 60) / 10, random.randint(20, 60) / 10]

        start_sound.stop()
        enemy_group.empty()
        gameover.Gameover(math.floor(self.score), game.window_size[0], game.window_size[1])
        time = -4
        self.score = 0

        checked_settings2 = game.check_settings()
        game.channel.set_volume(checked_settings2[1])

    def write(self, text, font_size, pos, color, dest, background=None, align='left', alpha=255):
        font = pygame.font.SysFont("Comic Sans MS", font_size)
        rendered_text = font.render(str(text), True, color, background)
        rendered_text.set_alpha(alpha)

        width = rendered_text.get_width()
        height = rendered_text.get_height()
        x, y = pos
        if align is 'left':
            dest.blit(rendered_text, [x, y])
        if align is 'right':
            dest.blit(rendered_text, [x - width, y])
        if align is 'center':
            dest.blit(rendered_text, [x - width / 2, y - height / 2])

    def update_settings(self, music, sound, name):
        fw = open("options.txt", "w")
        data = ["music_volume: " + str(music) + "\n",
                "sound_volume: " + str(sound) + "\n"
                "Name: " + str(name) + "\n"]
        fw.writelines(data)
        fw.close()

    def check_settings(self):
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
        pygame.mixer.music.set_volume(music)
        sound = int(settings[1][14])
        name = settings[2][6:-1]
        a = [music, sound, name]
        return a

    def update_score(self, player, score):
        fr = open("score.txt", "r")
        file = fr.readlines()
        name_list = eval(file[0])
        value_list = eval(file[1])
        iteration = 0
        for a in name_list:
            if iteration >= len(value_list):
                return
            if score > value_list[iteration]:
                value_list.insert(iteration, score)
                name_list.insert(iteration, player)
                del value_list[-1]
                del name_list[-1]

                fw = open("score.txt", "w")
                fw.writelines([str(name_list), "\n", str(value_list)])
                fw.close()
                fr.close()
                return
            else:
                iteration += 1

    def check_score(self):
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


class Player(pygame.sprite.Sprite):
    def __init__(self, filename=None):
        super(Player, self).__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.radius = self.image.get_width() / 2

        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery
        self.mouse_pos = pygame.mouse.get_pos()
        self.set_position(self.mouse_pos[0], self.mouse_pos[1])

    def set_position(self, x, y):
        self.rect.x = x - self.origin_x
        self.rect.y = y - self.origin_y

    def update(self):
        if event is not None:
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                self.set_position(self.mouse_pos[0], self.mouse_pos[1])

            if self.mouse_pos[0] > game.window_size[0] - self.radius:
                game.game_over()
            if self.mouse_pos[0] < self.radius:
                game.game_over()
            if self.mouse_pos[1] > game.window_size[1] - self.radius:
                game.game_over()
            if self.mouse_pos[1] < self.radius:
                game.game_over()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_x=0, start_y=0, speed=[], filename=None):
        super(Enemy, self).__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.radius = self.image.get_width() / 2

        self.pos = [start_x, start_y]
        self.speed = [speed[0], speed[1]]

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def reset_pos(self, x=0, y=0):
        self.pos[0] = x
        self.pos[1] = y
        self.set_position(self.pos[0], self.pos[1])

    def update(self):

        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.set_position(self.pos[0], self.pos[1])

        if self.pos[0] > game.window_size[0] - self.image.get_width():
            self.pos[0] = game.window_size[0] - self.image.get_width()
            self.speed[0] = -self.speed[0]

        if self.pos[0] < 0:
            self.pos[0] = 0
            self.speed[0] = -self.speed[0]

        if self.pos[1] > game.window_size[1] - self.image.get_height():
            self.pos[1] = game.window_size[1] - self.image.get_height()
            self.speed[1] = -self.speed[1]

        if self.pos[1] < 0:
            self.pos[1] = 0
            self.speed[1] = -self.speed[1]


if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()

    game = Game(640, 480)
    menu = menu.Menu()
    game.check_score()
    pygame.display.set_caption("Bemarifield 3.5")
    checked_settings = game.check_settings()
    game.channel.set_volume(checked_settings[1])
    player = Player("bmwcurs.png")

    skoda = Enemy(speed=[random.randint(20, 60) / 10, random.randint(20, 60) / 10], filename="skoda.png")
    saab = Enemy(speed=[random.randint(20, 60) / 10, random.randint(20, 60) / 10], filename="saab.png")
    volkkari = Enemy(speed=[random.randint(20, 60) / 10, random.randint(20, 60) / 10], filename="volkkari.png")
    alfa = Enemy(speed=[random.randint(20, 60) / 10, random.randint(20, 60) / 10], filename="alfa.png")

    enemy_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    clock = pygame.time.Clock()
    fps = 120
    time = -4
    game.score = 0
    running = True

    start_sound = pygame.mixer.Sound("beep.ogg")
    start_sound.set_volume(0.1)

    fail_sound = pygame.mixer.Sound("dong.ogg")
    fail_sound.set_volume(1)

    while running is True:
        if time == -4:
            game.channel.play(start_sound)

        time += 1 / fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update functions

        player.update()
        if time > -1:
            game.score = (time + 1) * 10
            enemy_group.add(skoda)
            skoda.update()
        if time > 2:
            enemy_group.add(saab)
            saab.update()
        if time > 5:
            enemy_group.add(volkkari)
            volkkari.update()
        if time > 8:
            enemy_group.add(alfa)
            alfa.update()

        # Logic Testing

        for collision in pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_circle):
            game.game_over()

        # Draw everything

        game.window.blit(game.background, [0, 0])
        enemy_group.draw(game.window)
        player_group.draw(game.window)

        if time < -4:
            game.write("3", 60, [320, 30], red, game.window, align='center')

        if -4 < time < -1.1:
            game.write(str(math.floor(-1 * time)), 60, [320, 30], black, game.window, align='center')

        if -1.1 < time < 0.3:
            game.write("GO!", 70, [320, 35], black, game.window, align='center')

        game.write(" Score: " + str(math.floor(game.score)) + "       ", 20, [530, 0], black, game.window, white)

        # Delay Framerate

        clock.tick(fps)

        # Update the screen

        pygame.display.update()

    pygame.quit()
