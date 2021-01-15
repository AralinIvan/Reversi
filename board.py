class IllegalMove(Exception):
    pass


class Board(object):
    def __init__(self):
        super(Board, self).__init__()
        self.turn = 1
        self.a = ''
        self.player = 2
        self.victory = 0
        self.board = [[0 for x in range(8)] for x in range(8)]
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        self.has_changed = True

    def player_move(self, x, y):
        if self.victory != 0:
            return
        self.perform_move(x, y)

    def perform_move(self, x, y):
        if self.board[x][y] != 0:
            return IllegalMove()
        self.place_piece(x, y)
        all_tiles = [item for sublist in self.board for item in sublist]
        empty_tiles = sum(1 for tile in all_tiles if tile == 0)
        white_tiles = sum(1 for tile in all_tiles if tile == 1)
        black_tiles = sum(1 for tile in all_tiles if tile == 2)
        if white_tiles < 1 or black_tiles < 1 or empty_tiles < 1:
            self.end_game()
            return
        self.player = 3 - self.player
        move_found = self.move_can_be_made()
        if not move_found:
            self.a = 'игрок ' + str(self.player) + ' не имеет возможных ходов ход переходит игроку ' + str(
                3 - self.player)
            self.player = 3 - self.player
        self.has_changed = True

    def move_can_be_made(self):
        move_found = False

        for x in range(0, 8):
            for y in range(0, 8):
                if move_found:
                    continue
                if self.board[x][y] == 0:
                    c = self.place_piece(x, y, live_mode=False)
                    if c > 0:
                        move_found = True

        return move_found

    def place_piece(self, x, y, live_mode=True):
        if live_mode:
            self.board[x][y] = self.player
        change_count = 0
        column = self.board[x]
        row = [self.board[i][y] for i in range(0, 8)]
        if self.player in column[:y]:
            changes = []
            search_complete = False
            for i in range(y - 1, -1, -1):
                if search_complete:
                    continue
                counter = column[i]
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[x][i] = self.player

        if self.player in column[y:]:
            changes = []
            search_complete = False
            for i in range(y + 1, 8, 1):
                if search_complete:
                    continue
                counter = column[i]
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[x][i] = self.player

        if self.player in row[:x]:
            changes = []
            search_complete = False
            for i in range(x - 1, -1, -1):
                if search_complete:
                    continue
                counter = row[i]
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[i][y] = self.player

        if self.player in row[x:]:
            changes = []
            search_complete = False
            for i in range(x + 1, 8, 1):
                if search_complete:
                    continue
                counter = row[i]
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[i][y] = self.player

        i, j = x - 7, y + 7
        bl_tr_diagonal = []
        for q in range(0, 16):
            if 0 <= i < 8 and 0 <= j < 8:
                bl_tr_diagonal.append(self.board[i][j])

            i += 1
            j -= 1
        i, j = x - 7, y - 7
        br_tl_diagonal = []
        for q in range(0, 16):
            if 0 <= i < 8 and 0 <= j < 8:
                br_tl_diagonal.append(self.board[i][j])
            i += 1
            j += 1
        if self.player in bl_tr_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx += 1
                ly -= 1
                if lx > 7 or ly < 0:
                    break
                if search_complete:
                    continue
                counter = self.board[lx][ly]
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append((lx, ly))
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player
        if self.player in bl_tr_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx -= 1
                ly += 1
                if lx < 0 or ly > 7:
                    break
                if search_complete:
                    continue
                counter = self.board[lx][ly]
                if counter == 0:
                    changes = []
                    search_complete = True
                    break
                elif counter == self.player:
                    search_complete = True
                    break
                else:
                    changes.append((lx, ly))
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player
        if self.player in br_tl_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx -= 1
                ly -= 1
                if lx < 0 or ly < 0:
                    break
                if search_complete:
                    continue
                counter = self.board[lx][ly]
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append((lx, ly))
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player

        if self.player in br_tl_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx += 1
                ly += 1
                if lx > 7 or ly > 7:
                    break
                if search_complete:
                    continue
                counter = self.board[lx][ly]
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append((lx, ly))
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player
        if change_count == 0 and live_mode:
            self.board[x][y] = 0
            raise IllegalMove()
        return change_count

    def end_game(self):
        all_tiles = [item for sublist in self.board for item in sublist]

        white_tiles = sum(1 for tile in all_tiles if tile == 1)
        black_tiles = sum(1 for tile in all_tiles if tile == 2)

        if white_tiles > black_tiles:
            self.victory = 1
        elif white_tiles < black_tiles:
            self.victory = 2
        else:
            self.victory = -1

        self.has_changed = True
