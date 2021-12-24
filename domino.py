import collections
import random

print("""
Ваши костяшки это йор писес
ходить просто ввести номер костяшки
правила как в настоящем домино
если вводить число без - (минуса) то пробуете добавить справа
с минусом слева
брать костяшку 0

""")
def start():
    domino = []
    for a in range(6, -1, -1):
        for b in range(a, -1, -1):
            domino.append([a, b])
    snake = None
    status = None
    queue = None
    random.shuffle(domino)  # tosuem kolodu
    computer_hand = domino[:7]
    player_hand = domino[7:14]
    stock = domino[14:]  # raspredelyaem

    player_double = [a for a in player_hand if len(set(a)) == 1]
    computer_double = [a for a in computer_hand if len(set(a)) == 1]
    if player_double and computer_double:
        if max(player_double[:]) > max(computer_double[:]):
            snake = max(player_double[:])
            player_hand.remove(snake)
            queue = 0
            status = 'Computer is about to make a move. Press Enter to continue...'
        else:
            snake = max(computer_double[:])
            computer_hand.remove(snake)
            status = "It's your turn to make a move. Enter your command."
            queue = 1
    elif player_double:
        snake = max(player_double[:])
        player_hand.remove(snake)
        status = 'Computer is about to make a move. Press Enter to continue...'
        queue = 0
    elif computer_double:
        snake = max(computer_double[:])
        computer_hand.remove(snake)
        status = "It's your turn to make a move. Enter your command."
        queue = 1  # proveryaem kto perviy

    player = []
    for number, num in enumerate(map(str, player_hand), 1):
        player.append(str(number) + ':' + num)

    print('''
======================================================================
Stock size: {stock}
Computer pieces: {computer}

{snake}

Your pieces:
{player}

Status: {status}
'''.format(stock=len(stock), player='\n'.join(player), computer=len(computer_hand),
           snake=snake, status=status))

    return stock, computer_hand, [snake], player_hand, queue, status


def turn(q, stock, c_h, snake, p_h, status):
    if q == 1:
        status, snake, p_h, stock = m_p(stock, p_h, snake)
        end = field(stock, c_h, snake, p_h, status)
        return 0, end
    elif q == 0:
        status, snake, c_h, stock = m_c(stock, c_h, snake)
        end = field(stock, c_h, snake, p_h, status)
        return 1, end


def c_num(snake, c_h):
    d = {}
    xs = [b for a in c_h for b in a] + [b for a in snake for b in a]
    for x in range(0, 7):
        d[x] = xs.count(x)
    sx = []
    for i in range(0, len(c_h)):
        x = [d.get(c_h[i][0]), d.get(c_h[i][1])]
        x = sum(x)
        sx.append(x)
    k = {}
    for x in range(1, len(sx) + 1):
        k[x] = sx[x - 1]
    f = collections.Counter(k).most_common()
    return f


def m_c(stock, c_h, snake):
    while True:
        try:
            m = input()
            if m != '':
                raise ValueError
            f = c_num(snake, c_h)
            i = 0
            status = None
            for x in range(0, len(f)):
                i += 1
                n = f[x][0]
                if i == len(f):
                    n = 0
                status, snake, c_h, stock = snake_check_perform_c(snake,-n, c_h, stock)
                if status == 0:
                    pass
                else:
                    return status, snake, c_h, stock
                status, snake, c_h, stock = snake_check_perform_c(snake, n, c_h, stock)
                if status == 0:
                    continue
                return status, snake, c_h, stock
            return status, snake, c_h, stock
        except ValueError:
            print("Invalid input. Please try again.")


def m_p(stock, p_h, snake):  # move player
    while True:
        try:
            m = int(input())  # m = move
            if abs(m) > (len(p_h)):
                raise ValueError
            status, snake, p_h, stock = snake_check_perform_p(snake, m, p_h, stock)
            if status == 0:
                continue
            return status, snake, p_h, stock
        except ValueError:
            print("Invalid input. Please try again.")


def check_snake(snake):
    if len(snake) > 6:
        snake_f = snake[:3] + ['...'] + snake[len(snake) - 3:]
        return snake_f
    else:
        return snake


def runout(stock, c_h, p_h, snake, end, status):
    if len(stock) == 0:
        left = snake[0]
        right = snake[len(snake) - 1]
        if right[1] not in c_h and left[0] not in c_h:
            if right[1] not in p_h and left[0] not in p_h:
                status = "The game is over. It's a draw!"
                return status, True
    return status, end


def draw(snake, status, end):
    arr_s = snake
    for i in range(0, 7, +1):
        xs = [x for x in arr_s if i in x]
        if len(xs) == 7:
            if snake[0][0] == snake[len(snake) - 1][1]:
                status = "The game is over. It's a draw!"
                return status, True
        if i == 6:
            return status, end


def c_w(c_h, status, end):  # computer won
    if len(c_h) == 0:
        status = 'The game is over. The computer won!'
        return status, True
    return status, end


def p_w(p_h, status, end):
    if len(p_h) == 0:
        status = 'The game is over. You won!'
        return status, True
    return status, end


def field(stock, c_h, snake, p_h, status):
    end = False
    snake_field = check_snake(snake)
    status, end = draw(snake, status, end)
    status, end = c_w(c_h, status, end)
    status, end = p_w(p_h, status, end)
    status, end = runout(stock, c_h, p_h, snake, end, status)
    player = []
    for number, num in enumerate(map(str, p_h), 1):
        player.append(str(number) + ':' + num)

    print('''
======================================================================
Stock size: {stock}
Computer pieces: {computer}

{snake}

Your pieces:
{player}

Status: {status}
'''.format(stock=len(stock), player='\n'.join(player), computer=len(c_h),
           snake="".join(map(str, snake_field)), status=status))
    return end


def turn_check(hand, snake, m):
    if m == 0:
        return False, hand
    elif m > 0:
        right = snake[len(snake) - 1]
        f = hand[m - 1]
        if right[1] in f:
            if right[1] == f[0]:
                return False, hand
            else:
                f[0], f[1] = f[1], f[0]
                hand[m - 1] = f
                return False, hand
    elif m < 0:
        m = abs(m)
        f = hand[m - 1]
        left = snake[0]
        if left[0] in f:
            if left[0] == f[1]:
                return False, hand
            else:
                f[0], f[1] = f[1], f[0]
                hand[m - 1] = f
                return False, hand
    return True, hand


def status_change(status):
    if status == 0:
        status = 'Computer is about to make a move. Press Enter to continue...'
        return status
    elif status == 1:
        status = "It's your turn to make a move. Enter your command."
        return status


def snake_check_perform_p(snake, m, h, stock):
    ok, h = turn_check(h, snake, m)
    if ok:
        print('Illegal move. Please try again.')
        return 0, snake, h, stock
    status = status_change(0)

    if m > 0:
        snake.append(h[m - 1])
        h.remove(h[m - 1])
    elif m < 0:
        m = abs(m)
        snake.insert(0, h[m - 1])
        h.remove(h[m - 1])
    elif m == 0:
        if len(stock) == 0:
            return status, snake, h, stock
        pie = stock[random.randint(0, len(stock) - 1)]  # kusok stocka
        h.append(pie)
        stock.remove(pie)
    status = status_change(0)
    return status, snake, h, stock


def snake_check_perform_c(snake, m, h, stock):
    ok, h = turn_check(h, snake, m)
    if ok:
        return 0, snake, h, stock
    status = status_change(1)

    if m > 0:
        snake.append(h[m - 1])
        h.remove(h[m - 1])
    elif m < 0:
        m = abs(m)
        snake.insert(0, h[m - 1])
        h.remove(h[m - 1])
    elif m == 0:
        if len(stock) == 0:
            return status, snake, h, stock
        pie = stock[random.randint(0, len(stock) - 1)]  # kusok stocka
        h.append(pie)
        stock.remove(pie)
    return status, snake, h, stock


def main():
    stock, c_h, snake, p_h, q, status = start()
    while True:
        q, end = turn(q, stock, c_h, snake, p_h, status)
        if end:
            break


main()
