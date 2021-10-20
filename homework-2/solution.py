"""
Tic-Tac-Toe game.
"""
import numpy as np
import pygame
import random
import sys
import time


def choose_first():
    """Random selection of player mark"""
    return PLAYERS_MARKS if random.choice((0, 1)) else PLAYERS_MARKS[::-1]


def display_board(board):
    """display the game board."""
    for row in range(SIZE_BOARD):
        for col in range(SIZE_BOARD):
            if board[row][col] == PLAYERS_MARKS[0]:
                color = 'red'
            elif board[row][col] == PLAYERS_MARKS[1]:
                color = 'blue'
            else:
                color = 'white'
            x = col * SIZE_BLOCK + (col + 1) * MARGIN
            y = row * SIZE_BLOCK + (row + 1) * MARGIN
            drawing_cell(x, y, color)


def drawing_cell(x, y, color):
    pygame.draw.rect(screen, COLOR_DICT[color], (x, y, SIZE_BLOCK, SIZE_BLOCK))
    if color == 'red':
        pygame.draw.line(screen, COLOR_DICT['white'], (x, y), (x + SIZE_BLOCK, y + SIZE_BLOCK), 3)
        pygame.draw.line(screen, COLOR_DICT['white'], (x + SIZE_BLOCK, y), (x, y + SIZE_BLOCK), 3)
    elif color == 'blue':
        half_size = SIZE_BLOCK // 2
        pygame.draw.circle(screen, COLOR_DICT['white'], (x + half_size, y + half_size), half_size, 3)


def player_choice():
    """Gets player's next position coord"""
    x_mouse, y_mouse = pygame.mouse.get_pos()
    col = x_mouse // (SIZE_BLOCK + MARGIN)
    row = y_mouse // (SIZE_BLOCK + MARGIN)
    return row, col


def cell_full(board, x, y):
    """Сhecks the emptiness of the cell"""
    return board[x][y] not in PLAYERS_MARKS


def place_marker(board, marker, x, y):
    """Puts a player mark to appropriate position."""
    board[x][y] = marker


def lose_check(board, x, y, mark):
    """Returns boolean value whether the player loses the game."""
    win_comb = [mark] * 5
    #left, right, bot, top, main diag, other diag
    win_slice = [board[x, y:y + 5], board[x, y - 4:y + 1], board[x - 4:x + 1, y], board[x:x + 5, y]]
    main_diag = np.diag(play_board[:, ::-1], k=SIZE_BOARD - x - y - 1)
    [win_slice.append(main_diag[i: i + 5]) for i in range(len(main_diag))]
    other_diag = np.diag(play_board, k=y - x)
    [win_slice.append(other_diag[i: i + 5]) for i in range(len(other_diag))]
    for s in win_slice:
        if len(s) == 5 and all(s == win_comb):
            return True
    return False


def full_board_check(board):
    return EMPTY_CHAR not in board


def check_game_finish(board, x, y, mark):
    """Return boolean value is the game finished or not."""
    if lose_check(board, x, y, mark):
        return f'Проиграли "{mark}". Нажмите пробел для продолжения'

    if full_board_check(board):
        return 'Доска заполнена. Нажмите пробел для продолжения'
    return False


def game_over_screen(game_over_text):
    screen.fill(COLOR_DICT['black'])
    font = pygame.font.SysFont('kacstbook', 40)
    text = font.render(game_over_text, True, COLOR_DICT['white'])
    text_rect = text.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = screen.get_height() / 2 - text_rect.height / 2
    screen.blit(text, [text_x, text_y])


def minimax(board, x, y, depth, is_ai_turn):
    if lose_check(board, x, y, bot_mark):
        return scores[bot_mark]
    if lose_check(board, x, y, player_mark):
        return scores[player_mark]
    if full_board_check(board):
        return scores['draw']
    if is_ai_turn:
        best_score = -sys.maxsize
        for y in range(SIZE_BOARD):
            for x in range(SIZE_BOARD):
                if board[y][x] == EMPTY_CHAR:
                    board[y][x] = bot_mark
                    if depth > 10:
                        return best_score
                    score = minimax(board, x, y, depth + 1, False)
                    board[y][x] = EMPTY_CHAR
                    best_score = min(best_score, score)
    else:
        best_score = sys.maxsize
        for y in range(SIZE_BOARD):
            for x in range(SIZE_BOARD):
                if board[y][x] == EMPTY_CHAR:
                    board[y][x] = player_mark
                    score = minimax(board, x, y, depth + 1, True)
                    board[y][x] = EMPTY_CHAR
                    best_score = max(best_score, score)
    return best_score


def bot_choice(field):
    move = None
    best_score = -sys.maxsize
    board = np.array([field[y].copy() for y in range(SIZE_BOARD)])
    for y in range(SIZE_BOARD):
        for x in range(SIZE_BOARD):
            if cell_full(board, x, y):
                place_marker(board, bot_mark, x, y)
                board[y][x] = bot_mark
                score = minimax(board, x, y, 0, False)
                board[y][x] = EMPTY_CHAR
                if random.choice((0, 1)):
                    move = (random.randint(0, SIZE_BOARD-1), random.randint(0, SIZE_BOARD-1))
                if score > best_score:
                    best_score = score
                    move = (x, y)
    time.sleep(1)
    return move


def step(board, mark, move):
    """common features for humans and bot"""
    row, col = player_choice() if mark == player_mark else bot_choice(board)
    if cell_full(board, row, col):
        place_marker(board, mark, row, col)
        game_over = check_game_finish(play_board, row, col, current_mark)
        move += 1
        return move, game_over
    return move, False


pygame.init()
SIZE_BOARD = 10
EMPTY_CHAR = '0'
SIZE_BLOCK, MARGIN = 70, 10
width = height = SIZE_BLOCK * SIZE_BOARD + MARGIN * SIZE_BOARD + 1

size_window = (width, height)
screen = pygame.display.set_mode(size_window)
pygame.display.set_caption("Обратные крестики-нолики")

COLOR_DICT = {'black': (0, 0, 0),
               'red': (255, 0, 0),
               'white': (255, 255, 255),
               'blue': (0, 191, 255)}
play_board = np.array([[EMPTY_CHAR] * SIZE_BOARD for i in range(SIZE_BOARD)])
PLAYERS_MARKS = ['X', 'O']
player_mark, bot_mark = PLAYERS_MARKS[0], PLAYERS_MARKS[1]
scores = {
    player_mark: 100,
    bot_mark: -100,
    'draw': 50
}

move_number = 0
game_over = False

while True:
    current_mark = PLAYERS_MARKS[move_number % 2]
    if not game_over:
        display_board(play_board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and (not game_over) and current_mark == player_mark:
            move_number, game_over = step(play_board, current_mark, move_number)
        elif current_mark == bot_mark and (not game_over):
            move_number, game_over = step(play_board, current_mark, move_number)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # restart game
            game_over = False
            play_board = np.array([[EMPTY_CHAR] * SIZE_BOARD for i in range(SIZE_BOARD)])
            move_number = 0
            screen.fill(COLOR_DICT['black'])
            #player_mark, bot_mark = choose_first()
    if game_over:
        game_over_screen(game_over)
    pygame.display.update()

