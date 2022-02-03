import random


def menu():
    while True:
        input_c = input().split(' ')
        if input_c[0] == 'exit':
            exit()
        else:
            try:
                assert input_c[0] == 'start'
                assert input_c[1] in {'user', 'easy', 'medium', 'hard'}
                assert input_c[2] in {'user', 'easy', 'medium', 'hard'}
                return [input_c[1], input_c[2]]
            except (AssertionError, ValueError, IndexError):
                print("Bad parameters!")


def print_board():
    print('---------')
    print(f'| {table[0][0]} {table[0][1]} {table[0][2]} |')
    print(f'| {table[1][0]} {table[1][1]} {table[1][2]} |')
    print(f'| {table[2][0]} {table[2][1]} {table[2][2]} |')
    print('---------')


def is_end():

    diagonal_1 = [table[0][0], table[1][1], table[2][2]]
    diagonal_2 = [table[0][2], table[1][1], table[2][0]]

    if diagonal_1.count('X') == 3 or diagonal_2.count('X') == 3:
        return 'X wins'
    elif diagonal_1.count('O') == 3 or diagonal_2.count('O') == 3:
        return 'O wins'

    for x in range(3):
        column = [table[0][x], table[1][x], table[2][x]]
        if table[x].count('X') == 3 or column.count('X') == 3:
            return 'X wins'
        elif table[x].count('O') == 3 or column.count('O') == 3:
            return 'O wins'

    number_of_none = table[0].count(' ') + table[1].count(' ') + table[2].count(' ')
    if number_of_none == 0:
        return 'Draw'
    else:
        return 'not end'


def move(symbol):
    cell = input("Enter the coordinates: ").split()
    try:
        x = int(cell[0])
        y = int(cell[1])
        if x not in [1, 2, 3] or y not in [1, 2, 3]:
            print("Coordinates should be from 1 to 3!")
            move(symbol)
        elif table[x - 1][y - 1] != " ":
            print("This cell is occupied! Choose another one!")
            move(symbol)
        else:
            table[x - 1][y - 1] = symbol
            print_board()
    except ValueError:
        print("You should enter numbers!")
        move(symbol)


def move_easy(symbol):
    while True:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if table[x][y] == ' ':
            table[x][y] = symbol
            print_board()
            break


def move_medium(symbol, vs):
    diagonal_1 = [table[0][0], table[1][1], table[2][2]]
    diagonal_2 = [table[0][2], table[1][1], table[2][0]]

    if diagonal_1.count(symbol) == 2 or diagonal_1.count(vs) == 2:
        for num in range(3):
            if table[num][num] == ' ':
                table[num][num] = symbol
                return print_board()
    elif diagonal_2.count(symbol) == 2 or diagonal_2.count(vs) == 2:
        for num in range(3):
            if table[num][len(diagonal_2)-num-1] == ' ':
                table[num][len(diagonal_2)-num-1] = symbol
                return print_board()

    for x in range(3):
        for y in range(3):
            if table[x][y] == ' ':
                column = [table[0][y], table[1][y], table[2][y]]
                if table[x].count(symbol) == 2 or column.count(symbol) == 2 or table[x].count(vs) == 2 or \
                        column.count(vs) == 2:
                    table[x][y] = symbol
                    return print_board()
    return move_easy(symbol)


def maxi(symbol, vs, alpha, beta):
    value = -2
    x = None
    y = None

    result = is_end()
    if result == f'{symbol} wins':
        return 1, 0, 0
    elif result == f'{vs} wins':
        return -1, 0, 0
    elif result == 'Draw':
        return 0, 0, 0

    for mx in range(3):
        for my in range(3):
            if table[mx][my] == ' ':
                table[mx][my] = symbol
                m, min_x, min_y = mini(symbol, vs, alpha, beta)
                if m > value:
                    value = m
                    x = mx
                    y = my
                table[mx][my] = ' '
                if value >= beta:
                    return value, x, y
                if value > alpha:
                    alpha = value

    return value, x, y


def mini(symbol, vs, alpha, beta):
    value = 2
    x = None
    y = None

    result = is_end()
    if result == f'{symbol} wins':
        return 1, 0, 0
    elif result == f'{vs} wins':
        return -1, 0, 0
    elif result == 'Draw':
        return 0, 0, 0

    for mx in range(3):
        for my in range(3):
            if table[mx][my] == ' ':
                table[mx][my] = vs
                m, max_x, max_y = maxi(symbol, vs, alpha, beta)
                if m < value:
                    value = m
                    x = mx
                    y = my
                table[mx][my] = ' '
                if value <= alpha:
                    return value, x, y
                if value < beta:
                    beta = value

    return value, x, y


def move_hard(symbol, vs):
    value, x, y = maxi(symbol, vs, -2, 2)
    table[x][y] = symbol
    return print_board()


def game(type_g):
    for turn in range(9):
        result = is_end()
        if result == 'not end':
            if turn % 2 == 0:
                symbol = 'X'
                vs = 'O'
            else:
                symbol = 'O'
                vs = 'X'

            if type_g[turn % 2] == 'user':
                move(symbol)
            elif type_g[turn % 2] == 'easy':
                print('Making move level "easy"')
                move_easy(symbol)
            elif type_g[turn % 2] == 'medium':
                print('Making move level "medium"')
                move_medium(symbol, vs)
            elif type_g[turn % 2] == 'hard':
                print('Making move level "hard"')
                move_hard(symbol, vs)
        else:
            return print(result)

    print('Draw')


while True:
    type_game = menu()
    table = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    print_board()
    game(type_game)
