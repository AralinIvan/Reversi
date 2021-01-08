import pygame, sys


size = WIDTH, HEIGHT = 800, 800
tile_size = 100
offset_size = 5

def terminate(self):
    pygame.quit()
    sys.exit()


class Eng(object):
    def __init__(self):
        super(Eng, self).__init__()
        pygame.init()
        self.textures = {}
        self.clock = pygame.time.clock
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Реверси')
        self.textures['board'] = pygame.image.load('data/board.png')
        self.textures['black'] = pygame.image.load('data/black.png')
        self.textures['white'] = pygame.image.load('data/white.png')
        self.game = reversi.Reversi()
        self.draw_board()

    def draw_board(self):
        the_board = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.screen.blit(self.textures['board'], the_board)
        for i in range(0, 8):
            for j on range(0, 8):
                player = self.game.board[i][j]
                counter = pygame.Rect(i * tile_size + offset_size, j * tile_size + offset_size,
                                      tile_size - offset_size * 2, tile_size - offset_size * 2)
                if player == 1:
                    self.screen.blit(self.textures['white'], counter)
                elif player == 2:
                    self.screen.blit(self.textures['black'], counter)

                if self.game.victory == 1:
                    self.drawText('Победа белых', self.screen, 38, 10)
                elif self.game.victory == 2:
                    self.drawText('Победа чёрных', self.screen, 39, 10)
                else:
                    self.drawText('Ничья', self.screen, 38, 10)
                pygame.display.update()

    def mouse_click(self, event):
        x,y = event.pos
        tile_x = int(x // tile_size)
        tile_y = int(y // tile_size)
        try:
            self.game.player_move(tx, ty)
        except reversi.Illegal_move as e:
            print("Illegal move")
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



