from blessed import Terminal
import logging

logger = logging.getLogger('connect4')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('log/connect4.log'))

def print_welcome(t):
    print('')
    print(t.center(t.bold('Welcome to Connect 4. Press "q" or "Ctrl-c" to quit.')))
    print('')

class View:
    def __init__(self, term):
        self.term = term
        self.board_location = [0,3]
        self.message_location = [0,20]

    def render(self, game):
        with self.term.location(*self.board_location):
            # todo move to specific location
            print(self.term.yellow('''
.---.---.---.---.---.---.---.
|   |   |   |   |   |   |   |
.---.---.---.---.---.---.---.
|   |   |   |   |   |   |   |
.---.---.---.---.---.---.---.
|   |   |   |   |   |   |   |
.---.---.---.---.---.---.---.
|   |   |   |   |   |   |   |
.---.---.---.---.---.---.---.
|   |   |   |   |   |   |   |
.---.---.---.---.---.---.---.
|   |   |   |   |   |   |   |
.---.---.---.---.---.---.---.
            '''))

        # clear message line
        with self.term.location(*self.message_location):
            for i in range(0, self.term.width):
                print(' ', end='')

        with self.term.location(*self.message_location):
            print(game.message)

        for x, col in enumerate(game.board.board):
            for y, cell in enumerate(col):
                if cell == 0:
                    continue

                with self.term.location(*self.__location(x,y)):
                    if cell == 1:
                        print(self.term.red('Red'), end='')
                    else:
                        print(self.term.black_on_white('Blk'), end='')

    def __location(self, x, y):
        x = x * 4 + 1
        x = x + self.board_location[0]
        y = ((6 - y) * 2)
        y = y + self.board_location[1]

        return [x, y]

class Board:
    width = 7
    height = 6

    def __init__(self):
        # 2d array of 7 columns
        self.board = [[], [], [], [], [], [], []]
        self.message = ''

    # Returns boolean whether move was successful. Check message on False.
    def move(self, column_index, player):
        self.message = ''

        if column_index < 0 or column_index >= len(self.board):
            self.message = 'Invalid move. Column is unknown: {0}'.format(column_index)
            return False

        column = self.board[column_index]

        if len(column) < Board.height:
          column.append(player)
          winner = self.__check_win([column_index, len(column) - 1])
          if winner:
            self.message = 'Player {0} wins!'.format(winner)

          return True
        else:
          self.message = 'Invalid move. Column is full'
          return False

    def __check_win(self, last_move):
        logger.info("__check_win({0}, {1})".format(self.board, last_move))
        logger.info("width {0} height {1}".format(Board.width, Board.height))

        paths = []

        # rows
        if last_move[0] - 3 >= 0:
            paths.append(zip(range(last_move[0] - 3, last_move[0] + 1), [last_move[1]] * 4))
        if last_move[0] - 2 >= 0 and last_move[0] + 1 < Board.width:
            paths.append(zip(range(last_move[0] - 2, last_move[0] + 2), [last_move[1]] * 4))
        if last_move[0] - 1 >= 0 and last_move[0] + 2 < Board.width:
            paths.append(zip(range(last_move[0] - 1, last_move[0] + 3), [last_move[1]] * 4))
        if last_move[0] + 3 < Board.width:
            paths.append(zip(range(last_move[0], last_move[0] + 4), [last_move[1]] * 4))

        # cols
        if last_move[1] - 3 >= 0:
            paths.append(zip([last_move[0]] * 4, range(last_move[1] - 3, last_move[1] + 1)))
        if last_move[1] - 2 >= 0 and last_move[0] + 1 < Board.height:
            paths.append(zip([last_move[0]] * 4, range(last_move[1] - 2, last_move[1] + 2)))
        if last_move[1] - 1 >= 0 and last_move[0] + 2 < Board.height:
            paths.append(zip([last_move[0]] * 4, range(last_move[1] - 1, last_move[1] + 3)))
        if last_move[1] + 3 < Board.height:
            paths.append(zip([last_move[0]] * 4, range(last_move[0], last_move[0] + 4)))

        # top left to bottom right diags
        if last_move[0] - 3 >= 0 and last_move[1] - 3 >= 0:
            paths.append(zip(range(last_move[0] - 3, last_move[0] + 1), range(last_move[1] - 3, last_move[1] + 1)))
        if last_move[0] - 2 >= 0 and last_move[0] + 1 < Board.width and last_move[1] - 2 >= 0 and last_move[0] + 1 < Board.height:
            paths.append(zip(range(last_move[0] - 2, last_move[0] + 2), range(last_move[1] - 2, last_move[1] + 2)))
        if last_move[0] - 1 >= 0 and last_move[0] + 2 < Board.width and last_move[1] - 1 >= 0 and last_move[0] + 2 < Board.height:
            paths.append(zip(range(last_move[0] - 1, last_move[0] + 3), range(last_move[1] -1, last_move[1] + 3)))
        if last_move[0] + 3 < Board.width and last_move[1] + 3 < Board.height:
            paths.append(zip(range(last_move[0], last_move[0] + 4), range(last_move[1], last_move[1] + 4)))

        # top right to bottom left diags
        if last_move[0] + 3 < Board.width and last_move[1] - 3 >= 0:
            paths.append(zip(range(last_move[0] + 3, last_move[0] - 1, -1), range(last_move[1] - 3, last_move[1] + 1)))
        if last_move[0] - 1 >= 0 and last_move[0] + 2 < Board.width and last_move[1] - 2 >= 0 and last_move[0] + 1 < Board.height:
            paths.append(zip(range(last_move[0] + 2, last_move[0] - 2, -1), range(last_move[1] - 2, last_move[1] + 2)))
        if last_move[0] - 2 >= 0 and last_move[0] + 1 < Board.width and last_move[1] - 1 >= 0 and last_move[0] + 2 < Board.height:
            paths.append(zip(range(last_move[0] + 1, last_move[0] - 3, -1), range(last_move[1] -1, last_move[1] + 3)))
        if last_move[0] - 3 >= 0 and last_move[1] + 3 < Board.height:
            paths.append(zip(range(last_move[0], last_move[0] - 4, -1), range(last_move[1], last_move[1] + 4)))

        for path in paths:
            path = list(path)
            moves = list(map(self.__safely_index_board, path))

            if all(map(lambda x: x == 1, moves)):
                return 1
            elif all(map(lambda x: x == 2, moves)):
                return 2

    def __safely_index_board(self, pos):
        x = pos[0]
        y = pos[1]
        try:
            return self.board[x][y]
        except IndexError:
            return 0

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 1
        self.message = self.__default_message()

    def move(self, column_index):
        if self.board.move(column_index, self.current_player):

            # switch player
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1

            self.message = self.board.message or self.__default_message()

        else:
            self.message = self.board.message

    def __default_message(self):
        return 'It is players {0} move. Press 0-6 to choose a column'.format(self.current_player)

def main(term):
    game = Game()
    view = View(term)

    with term.cbreak():
        while True:
            view.render(game)

            key = term.inkey()
            if key == 'q':
                break

            try:
                column_index = int(key)

                if game.move(column_index):
                    pass

                else:
                    pass

            except ValueError:
                game.message = 'Invalid move. Column is unknown: {0}'.format(key)

term = Terminal()

with term.fullscreen():
    print_welcome(term)
    main(term)
