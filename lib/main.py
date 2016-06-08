from blessed import Terminal

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
                if len(cell) != 3:
                    continue

                with self.term.location(*self.__location(x,y)):
                    if cell == 'Red':
                        print(self.term.red(cell), end='')
                    else:
                        print(self.term.black_on_white(cell), end='')

    def __location(self, x, y):
        x = x * 4 + 1
        x = x + self.board_location[0]
        y = ((6 - y) * 2)
        y = y + self.board_location[1]

        return [x, y]

class Board:
    def __init__(self):
        # array of 7 columns
        self.board = [[], [], [], [], [], [], []]
        self.message = ''

    # Returns boolean whether move was successful. Check message on False.
    def move(self, column_index, player):
        try:
            column = self.board[column_index]

            if len(column) < 6:
              column.append(player)
              return True
            else:
              self.message = 'Invalid move. Column is full'
              return False

        except IndexError:
            self.message = 'Invalid move. Column is unknown: {0}'.format(column_index)
            return False

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 'Red'
        self.message = self.__default_message()

    def move(self, column_index):
        if self.board.move(column_index, self.current_player):

            # switch player
            if self.current_player == 'Red':
                self.current_player = 'Blk'
            else:
                self.current_player = 'Red'

            self.message = self.__default_message()

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
