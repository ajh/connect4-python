from blessed import Terminal

def print_welcome(t):
    print('')
    print(t.center(t.bold('Welcome to Connect 4. Press "q" or "Ctrl-c" to quit.')))
    print('')

class View:
    def __init__(self, term):
        self.term = term

    def render(self, game):
        with self.term.location(0, 3):
            # todo move to specific location
            print('''
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
            ''')


        # clear message line
        with self.term.location(0, 20):
            for i in range(0, self.term.width):
                print(' ', end='')

        with self.term.location(0, 20):
            print(game.message)

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
