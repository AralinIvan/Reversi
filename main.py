import pygame
import sys
import board1
import board
import random
import pygame.sprite
import particle

size = WIDTH, HEIGHT = 800, 800
tile_size = 100
offset_size = 10
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


class Eng(object):
    def __init__(self):
        super(Eng, self).__init__()
        pygame.init()
        self.q = 0
        self.font = pygame.font.SysFont('arial', 48)
        self.textures = {}
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size)
        self.screen2 = pygame.Surface(size)
        pygame.display.set_caption('Реверси')
        self.textures['board'] = pygame.image.load('data/board.png')
        self.textures['black'] = pygame.image.load('data/black.png')
        self.textures['white'] = pygame.image.load('data/white.png')
        self.game = board1.Board()
        self.draw_board()

    def drawtext(self, text, surface, x, y):
        text_object = self.font.render(text, True, (0, 0, 0))
        text_rect = text_object.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_object, text_rect)

    def draw_board(self):
        the_board = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.screen.blit(self.textures['board'], the_board)
        for i in range(0, 8):
            for j in range(0, 8):
                player = self.game.board[i][j]
                counter = pygame.Rect(i * tile_size + offset_size, j * tile_size + offset_size,
                                      tile_size - offset_size * 2, tile_size - offset_size * 2)
                if player == 1:
                    self.screen.blit(self.textures['white'], counter)
                elif player == 2:
                    self.screen.blit(self.textures['black'], counter)

                if self.game.victory == 0:
                    if self.game.a != '':
                        self.drawtext(self.game.a, self.screen, 38, 10)
                    else:
                        if self.game.player == 2:
                            self.drawtext('ход чёрных', self.screen, 39, 40)
                        else:
                            self.drawtext('ход белых', self.screen, 39, 40)
                    all_tiles = [item for sublist in self.game.board for item in sublist]
                    white_tiles = sum(1 for tile in all_tiles if tile == 1)
                    black_tiles = sum(1 for tile in all_tiles if tile == 2)
                    self.drawtext('белые/черные', self.screen, 520, 20)
                    self.drawtext(str(white_tiles) + '/' + str(black_tiles), self.screen, 609, 60)
                if self.game.victory == 1:

                    self.drawtext('Победа белых', self.screen, 38, 10)
                    if self.q == 63:
                        self.create_particles()
                    self.q += 1
                elif self.game.victory == 2:
                    self.drawtext('Победа чёрных', self.screen, 39, 10)
                    if self.q == 63:
                        self.create_particles()
                    self.q += 1
                pygame.display.flip()

    def create_particles(self):
        self.clock.tick(50)
        self.screen2 = self.screen.copy()
        particle_count = 300
        numbers = range(-5, 6)
        for i in range(particle_count):
            particle.Particle((random.randint(0, 800), random.randint(0, 200)), random.choice(numbers),
                              random.choice(numbers))
        for i in range(100):
            particle.all_sprites.update()
            self.screen.blit(self.screen2, (0, 0))
            particle.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(50)

    def mouse_click(self, event):
        x, y = event.pos
        tile_x = int(x // tile_size)
        tile_y = int(y // tile_size)
        try:
            self.game.player_move(tile_x, tile_y)
        except board1.IllegalMove as e:
            print("Невозможный ход", e)
        except board.IllegalMove as e:
            print("Невозможный ход", e)
        except Exception as e:
            print(e)
            raise

    def start(self):
        self.game.__init__()
        self.s = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        self.game.__init__()
                        return self.start()
                    elif event.key == pygame.K_2:
                        self.game = board.Board()
                        self.game.__init__()
                        return self.start()
                    elif event.key == pygame.K_1:
                        self.game = board1.Board()
                        self.game.__init__()
                        return self.start()
                    elif event.key == pygame.K_RIGHT:
                        self.s += 1
                        if self.s == 5:
                            self.s = 0
                        if self.s == 0:
                            self.textures['board'] = pygame.image.load('data/board.png')
                            self.draw_board()
                        elif self.s == 1:
                            self.textures['board'] = pygame.image.load('data/board1.png')
                            self.draw_board()
                        elif self.s == 2:
                            self.textures['board'] = pygame.image.load('data/board2.png')
                            self.draw_board()
                        elif self.s == 3:
                            self.textures['board'] = pygame.image.load('data/board3.png')
                            self.draw_board()
                        elif self.s == 4:
                            self.textures['board'] = pygame.image.load('data/board4.png')
                            self.draw_board()

            if self.game.has_changed:
                self.draw_board()
                self.game.has_changed = False
                self.game.a = ''
            self.clock.tick()


if __name__ == '__main__':
    eng = Eng()
    eng.start()
