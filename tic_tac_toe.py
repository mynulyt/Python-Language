import pygame
import sys
import time

#Game settings
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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe Game")

clock = pygame.time.Clock()
font_big = pygame.font.SysFont("segoeui", 120, bold=True)
font_medium = pygame.font.SysFont("segoeui", 40, bold=True)
font_small = pygame.font.SysFont("segoeui", 24)

def create_empty_board():
    return [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

board = create_empty_board()
cell_appear_time = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = "X"
winner = None
win_cells = []
win_line_anim_start = None
game_over = False

def reset_game():
    global board, cell_appear_time, current_player, winner, win_cells, win_line_anim_start, game_over
    board = create_empty_board()
    cell_appear_time = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"
    winner = None
    win_cells = []
    win_line_anim_start = None
    game_over = False

def check_winner():
    global winner, win_cells, game_over, win_line_anim_start
    lines = []

    # Rows
    for r in range(GRID_SIZE):
        lines.append([(r, c) for c in range(GRID_SIZE)])
    # Cols
    for c in range(GRID_SIZE):
        lines.append([(r, c) for r in range(GRID_SIZE)])
    # Diagonals
    lines.append([(i, i) for i in range(GRID_SIZE)])
    lines.append([(i, GRID_SIZE - 1 - i) for i in range(GRID_SIZE)])

    for cells in lines:
        symbols = [board[r][c] for r, c in cells]
        if symbols[0] != "" and all(s == symbols[0] for s in symbols):
            winner = symbols[0]
            win_cells = cells
            game_over = True
            win_line_anim_start = time.time()
            return

    # Draw
    if all(board[r][c] != "" for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
        winner = "Draw"
        game_over = True

def get_cell_from_mouse(pos):
    x, y = pos
    if y < 100:  # top status bar area
        return None
    row = (y - 100) // CELL_SIZE
    col = x // CELL_SIZE
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        return row, col
    return None

def handle_click(pos):
    global current_player
    if game_over:
        return
    cell = get_cell_from_mouse(pos)
    if cell is None:
        return
    r, c = cell
    if board[r][c] == "":
        board[r][c] = current_player
        cell_appear_time[r][c] = time.time()
        check_winner()
        if not game_over:
            current_player = "O" if current_player == "X" else "X"

def draw_grid():
    # Background panel with rounded rect
    panel_rect = pygame.Rect(20, 110, WIDTH - 40, HEIGHT - 130)
    pygame.draw.rect(screen, (28, 28, 48), panel_rect, border_radius=20)

    for i in range(1, GRID_SIZE):
        # Vertical
        start_pos = (i * CELL_SIZE, 100)
        end_pos = (i * CELL_SIZE, HEIGHT)
        pygame.draw.line(screen, GRID_COLOR, start_pos, end_pos, LINE_WIDTH)
        # Horizontal
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

            # Render symbol surface
            surf = font_big.render(symbol, True, X_COLOR if symbol == "X" else O_COLOR)
            surf = surf.convert_alpha()
            surf.set_alpha(alpha)

            rect = surf.get_rect()
            center_x = c * CELL_SIZE + CELL_SIZE // 2
            center_y = 100 + r * CELL_SIZE + CELL_SIZE // 2
            rect.center = (center_x, center_y)

            # Slight scale animation
            scale_factor = 0.6 + 0.4 * t
            scaled_size = (int(rect.width * scale_factor), int(rect.height * scale_factor))
            scaled_surf = pygame.transform.smoothscale(surf, scaled_size)
            scaled_rect = scaled_surf.get_rect(center=(center_x, center_y))

            screen.blit(scaled_surf, scaled_rect)

def draw_status_bar():
    # Top bar
    top_rect = pygame.Rect(0, 0, WIDTH, 90)
    pygame.draw.rect(screen, (24, 24, 40), top_rect)
    pygame.draw.rect(screen, (60, 60, 100), top_rect, 1)

    title_surf = font_medium.render("Tic Tac Toe", True, TEXT_COLOR)
    title_rect = title_surf.get_rect(midleft=(30, 45))
    screen.blit(title_surf, title_rect)

    if not game_over:
        status_text = f"Turn: {current_player}"
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

    # Interpolate end point for animation
    x_end = x1 + (x2 - x1) * t
    y_end = y1 + (y2 - y1) * t

    pygame.draw.line(screen, WIN_LINE_COLOR, (x1, y1), (x_end, y_end), 10)

def main():
    global game_over
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

        screen.fill(BG_COLOR)
        draw_status_bar()
        draw_grid()
        draw_symbols()
        draw_win_line()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
