import pygame
import sys
import time
import math

# Game settings
WIDTH, HEIGHT = 500, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 6
BG_COLOR = (18, 18, 32)
GRID_COLOR = (80, 80, 120)
X_COLOR = (255, 90, 90)
O_COLOR = (90, 200, 255)
WIN_LINE_COLOR = (255, 215, 0)
TEXT_COLOR = (230, 230, 240)

ANIMATION_DURATION = 0.25  # seconds
WINLINE_DURATION = 0.5
BOT_THINK_DELAY = 0.20     # bot চিন্তা করার মতো একটু delay

HUMAN = "X"
BOT = "O"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe Game")

clock = pygame.time.Clock()
font_big = pygame.font.SysFont("segoeui", 90, bold=True)
font_medium = pygame.font.SysFont("segoeui", 35, bold=True)
font_small = pygame.font.SysFont("segoeui", 20)

def create_empty_board():
    return [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

board = create_empty_board()
cell_appear_time = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = HUMAN
winner = None
win_cells = []
win_line_anim_start = None
game_over = False

# Bot control
bot_pending = False
bot_move_time = None

def reset_game():
    global board, cell_appear_time, current_player, winner, win_cells, win_line_anim_start, game_over
    global bot_pending, bot_move_time
    board = create_empty_board()
    cell_appear_time = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = HUMAN
    winner = None
    win_cells = []
    win_line_anim_start = None
    game_over = False
    bot_pending = False
    bot_move_time = None

def get_lines():
    lines = []
    for r in range(GRID_SIZE):
        lines.append([(r, c) for c in range(GRID_SIZE)])
    for c in range(GRID_SIZE):
        lines.append([(r, c) for r in range(GRID_SIZE)])
    lines.append([(i, i) for i in range(GRID_SIZE)])
    lines.append([(i, GRID_SIZE - 1 - i) for i in range(GRID_SIZE)])
    return lines

def evaluate_state(b):
    """Return winner symbol or None, and draw flag."""
    for cells in get_lines():
        symbols = [b[r][c] for r, c in cells]
        if symbols[0] != "" and all(s == symbols[0] for s in symbols):
            return symbols[0]
    if all(b[r][c] != "" for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
        return "Draw"
    return None

def check_winner():
    global winner, win_cells, game_over, win_line_anim_start
    for cells in get_lines():
        symbols = [board[r][c] for r, c in cells]
        if symbols[0] != "" and all(s == symbols[0] for s in symbols):
            winner = symbols[0]
            win_cells = cells
            game_over = True
            win_line_anim_start = time.time()
            return

    if all(board[r][c] != "" for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
        winner = "Draw"
        game_over = True

def get_cell_from_mouse(pos):
    x, y = pos
    if y < 100:
        return None
    row = (y - 100) // CELL_SIZE
    col = x // CELL_SIZE
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        return row, col
    return None

def handle_click(pos):
    global current_player, bot_pending, bot_move_time
    if game_over or current_player != HUMAN:
        return

    cell = get_cell_from_mouse(pos)
    if cell is None:
        return
    r, c = cell

    if board[r][c] == "":
        board[r][c] = HUMAN
        cell_appear_time[r][c] = time.time()
        check_winner()

        if not game_over:
            current_player = BOT
            bot_pending = True
            bot_move_time = time.time() + BOT_THINK_DELAY

# ---------------- BOT AI (minimax) ----------------
def available_moves(b):
    return [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if b[r][c] == ""]

def minimax(b, is_maximizing):
    result = evaluate_state(b)
    if result == BOT:
        return 1
    if result == HUMAN:
        return -1
    if result == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for (r, c) in available_moves(b):
            b[r][c] = BOT
            score = minimax(b, False)
            b[r][c] = ""
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for (r, c) in available_moves(b):
            b[r][c] = HUMAN
            score = minimax(b, True)
            b[r][c] = ""
            best_score = min(best_score, score)
        return best_score

def bot_best_move():
    best_score = -math.inf
    move = None
    for (r, c) in available_moves(board):
        board[r][c] = BOT
        score = minimax(board, False)
        board[r][c] = ""
        if score > best_score:
            best_score = score
            move = (r, c)
    return move

def bot_play_if_needed():
    global current_player, bot_pending
    if game_over or current_player != BOT or not bot_pending:
        return
    if time.time() < bot_move_time:
        return

    move = bot_best_move()
    if move:
        r, c = move
        board[r][c] = BOT
        cell_appear_time[r][c] = time.time()
        check_winner()

    bot_pending = False
    if not game_over:
        current_player = HUMAN

# ---------------- Drawing ----------------
def draw_grid():
    panel_rect = pygame.Rect(20, 110, WIDTH - 40, HEIGHT - 130)
    pygame.draw.rect(screen, (28, 28, 48), panel_rect, border_radius=20)

    for i in range(1, GRID_SIZE):
        start_pos = (i * CELL_SIZE, 100)
        end_pos = (i * CELL_SIZE, HEIGHT)
        pygame.draw.line(screen, GRID_COLOR, start_pos, end_pos, LINE_WIDTH)

        start_pos = (0, 100 + i * CELL_SIZE)
        end_pos = (WIDTH, 100 + i * CELL_SIZE)
        pygame.draw.line(screen, GRID_COLOR, start_pos, end_pos, LINE_WIDTH)

def draw_symbols():
    now = time.time()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            symbol = board[r][c]
            if symbol == "":
                continue
            appear_time = cell_appear_time[r][c] or now
            t = min(1.0, (now - appear_time) / ANIMATION_DURATION)
            alpha = int(255 * t)

            surf = font_big.render(symbol, True, X_COLOR if symbol == "X" else O_COLOR)
            surf = surf.convert_alpha()
            surf.set_alpha(alpha)

            rect = surf.get_rect()
            center_x = c * CELL_SIZE + CELL_SIZE // 2
            center_y = 100 + r * CELL_SIZE + CELL_SIZE // 2
            rect.center = (center_x, center_y)

            scale_factor = 0.6 + 0.4 * t
            scaled_size = (int(rect.width * scale_factor), int(rect.height * scale_factor))
            scaled_surf = pygame.transform.smoothscale(surf, scaled_size)
            scaled_rect = scaled_surf.get_rect(center=(center_x, center_y))

            screen.blit(scaled_surf, scaled_rect)

def draw_status_bar():
    top_rect = pygame.Rect(0, 0, WIDTH, 90)
    pygame.draw.rect(screen, (24, 24, 40), top_rect)
    pygame.draw.rect(screen, (60, 60, 100), top_rect, 1)

    title_surf = font_medium.render("Tic Tac Toe", True, TEXT_COLOR)
    title_rect = title_surf.get_rect(midleft=(30, 45))
    screen.blit(title_surf, title_rect)

    if not game_over:
        if current_player == HUMAN:
            status_text = "Your Turn (X)"
        else:
            status_text = "Bot Thinking (O)..."
    else:
        if winner == "Draw":
            status_text = "It's a Draw! Press R to Restart."
        else:
            status_text = f"{winner} Wins! Press R to Restart."

    status_surf = font_small.render(status_text, True, TEXT_COLOR)
    status_rect = status_surf.get_rect(midright=(WIDTH - 20, 35))
    screen.blit(status_surf, status_rect)

def draw_win_line():
    if not game_over or winner == "Draw" or not win_cells or win_line_anim_start is None:
        return
    now = time.time()
    t = min(1.0, (now - win_line_anim_start) / WINLINE_DURATION)

    (r1, c1) = win_cells[0]
    (r2, c2) = win_cells[-1]

    x1 = c1 * CELL_SIZE + CELL_SIZE // 2
    y1 = 100 + r1 * CELL_SIZE + CELL_SIZE // 2
    x2 = c2 * CELL_SIZE + CELL_SIZE // 2
    y2 = 100 + r2 * CELL_SIZE + CELL_SIZE // 2

    x_end = x1 + (x2 - x1) * t
    y_end = y1 + (y2 - y1) * t

    pygame.draw.line(screen, WIN_LINE_COLOR, (x1, y1), (x_end, y_end), 10)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_click(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

        bot_play_if_needed()

        screen.fill(BG_COLOR)
        draw_status_bar()
        draw_grid()
        draw_symbols()
        draw_win_line()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
