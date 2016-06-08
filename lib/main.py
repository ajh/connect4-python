from blessed import Terminal

def print_welcome(t):
    print('')
    print(t.center(t.bold('Welcome to Connect 4. Press "q" or "Ctrl-c" to quit.')))
    print('')

def render(t):
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

def main(t):
    with t.cbreak():
        while True:
            render(t)
            key = t.inkey()
            if key == 'q':
              break

            print(key)

term = Terminal()
with term.fullscreen():
    print_welcome(term)
    main(term)

