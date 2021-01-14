import pygame
import sys
import board1

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
        self.font = pygame.font.SysFont('arial', 48)
        self.textures = {}
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Реверси')
        self.textures['board'] = pygame.image.load('data/board.png')
        self.textures['black'] = pygame.image.load('data/black.png')
        self.textures['white'] = pygame.image.load('data/white.png')
        self.game = board1.Board()
        self.draw_board()

    def drawtext(self, text, surface, x, y):
        textobject = self.font.render(text, 1, (0, 0, 0))
        textrect = textobject.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobject, textrect)

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
                    self.drawtext(str(white_tiles)+'/'+str(black_tiles), self.screen, 609, 60)
                if self.game.victory == 1:
                    self.drawtext('Победа белых', self.screen, 38, 10)
                elif self.game.victory == 2:
                    self.drawtext('Победа чёрных', self.screen, 39, 10)
                pygame.display.update()

    def mouse_click(self, event):
        x, y = event.pos
        tile_x = int(x // tile_size)
        tile_y = int(y // tile_size)
        try:
            self.game.player_move(tile_x, tile_y)
        except board1.Illegal_move as e:
            print("Невозможный ход")
        except Exception as e:
            raise

    def start(self):
        self.__init__()
        self.game.__init__()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click(event)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        return self.start()

            if self.game.has_changed:
                self.draw_board()
                self.game.has_changed = False
                self.game.a = ''
            self.clock.tick()


if __name__ == '__main__':
    eng = Eng()
    eng.start()




