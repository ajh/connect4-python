from blessed import Terminal

def print_welcome(t):
    print('')
    print(t.center(t.bold('Welcome to Connect 4. Press "q" or "Ctrl-c" to quit.')))
    print('')

def render(t, game):
    with t.location(0, 3):
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


    with t.location(0, 20):
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
              self.message = 'Column is full'
              return False

        except IndexError:
            self.message = 'Column is unknown: {0}'.format(column_index)
            return False

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 'Red'
        self.message = self.__default_message()

    def move(self, column_index):
        if self.board.move(column_index, self.current_player):
            if self.current_player == 'Red':
                self.current_player == 'Blk'
            else:
                self.current_player == 'Red'

            self.message = self.__default_message()

        else:
            self.message = self.board.message

    def __default_message(self):
        return 'It is players {0} move. Press 0-6 to choose a column'.format(self.current_player)

def main(t):
    game = Game()

    with t.cbreak():
        while True:
            render(t, game)
            key = t.inkey()
            if key == 'q':
                break

            try:
                column_index = int(key)

                if game.move(column_index):
                    pass

                else:
                    pass

            except ValueError:
                pass

term = Terminal()

with term.fullscreen():
    print_welcome(term)
    main(term)
