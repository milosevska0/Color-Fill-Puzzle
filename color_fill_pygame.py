import random
import pygame
import sys
import time
from pygame.locals import *

# Constants
FPS = 30
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
BOXSIZE = 80
GAPSIZE = 10
GRIDWIDTH = 5
GRIDHEIGHT = 5
MARGIN = 5
COLOR_BOX_SIZE = 40
COLOR_BOX_MARGIN = 15

# Colors
WHITE = (255, 255, 255)
RED = (255, 87, 34)
GREEN = (76, 175, 80)
BLUE = (33, 150, 243)
YELLOW = (255, 235, 59)
BLACK = (33, 33, 33)
BLUEISH = (46, 47, 92)
BURGUNDY = (140, 7, 20)

COLORS = [RED, GREEN, BLUE, YELLOW]
COLOR_NAMES = ['Red', 'Green', 'Blue', 'Yellow']
BGCOLOR = pygame.Color(255, 192, 203)

# PyGame Initialization
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Color Fill Puzzle")
font = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 32)

# Global variables
grid = [[None for _ in range(GRIDWIDTH)] for _ in range(GRIDHEIGHT)]
selected_color = None
best_score = 0
obstacle_positions = []  # the initial colors ("obstacles") placed in the game


def initialize_grid():
    global grid, obstacle_positions
    grid = [[None for _ in range(GRIDWIDTH)] for _ in range(GRIDHEIGHT)]
    obstacle_positions = []

    total_boxes = GRIDWIDTH * GRIDHEIGHT
    obstacles_to_place = total_boxes // 5

    placed_obstacles = 0

    while placed_obstacles < obstacles_to_place:
        row = random.randint(0, GRIDHEIGHT - 1)
        col = random.randint(0, GRIDWIDTH - 1)

        if grid[row][col] is None:
            available_colors = [color for color in COLORS if is_valid_color(row, col, color)]

            if available_colors:
                grid[row][col] = random.choice(available_colors)
                obstacle_positions.append((row, col))
                placed_obstacles += 1
    return grid


def draw_gradient_background():
    top_color = (210, 228, 252)
    bottom_color = (190, 158, 205)

    for i in range(WINDOWHEIGHT):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * (i / WINDOWHEIGHT))
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * (i / WINDOWHEIGHT))
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * (i / WINDOWHEIGHT))
        color = (r, g, b)
        pygame.draw.line(DISPLAYSURF, color, (0, i), (WINDOWWIDTH, i))


def draw_grid(mouse_x=None, mouse_y=None):
    total_grid_width = GRIDWIDTH * (BOXSIZE + MARGIN) + MARGIN
    total_grid_height = GRIDHEIGHT * (BOXSIZE + MARGIN) + MARGIN

    start_x = (WINDOWWIDTH - total_grid_width) // 2
    start_y = (WINDOWHEIGHT - total_grid_height) // 2 + 50

    for row in range(GRIDHEIGHT):
        for col in range(GRIDWIDTH):
            x = start_x + col * (BOXSIZE + MARGIN) + MARGIN
            y = start_y + row * (BOXSIZE + MARGIN) + MARGIN
            box_color = grid[row][col] if grid[row][col] else WHITE

            is_hovered = mouse_x is not None and x <= mouse_x <= x + BOXSIZE and y <= mouse_y <= y + BOXSIZE

            if box_color == WHITE:
                color_to_draw = (229, 232, 250) if is_hovered else box_color
            else:
                color_to_draw = lighten_color(box_color, 0.3) if is_hovered else box_color
            pygame.draw.rect(DISPLAYSURF, color_to_draw, (x, y, BOXSIZE, BOXSIZE), border_radius=4)


def lighten_color(color, factor):
    r, g, b = color
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return r, g, b


def handle_and_draw_color_selection(mouse_x=None, mouse_y=None, click=False):
    global selected_color

    text_instr = font_large.render("Click a color, then a box to fill it.", True, (46, 47, 92))
    text_instr_rect = text_instr.get_rect(center=(WINDOWWIDTH // 2, 20))
    DISPLAYSURF.blit(text_instr, text_instr_rect)

    total_color_box_width = len(COLORS) * (COLOR_BOX_SIZE + COLOR_BOX_MARGIN) - COLOR_BOX_MARGIN
    start_x = (WINDOWWIDTH - total_color_box_width) // 2

    for i, color in enumerate(COLORS):
        x = start_x + i * (COLOR_BOX_SIZE + COLOR_BOX_MARGIN)
        y = 40

        is_hovered = mouse_x is not None and x <= mouse_x <= x + COLOR_BOX_SIZE and y <= mouse_y <= y + COLOR_BOX_SIZE
        is_selected = (selected_color == color)

        draw_color = lighten_color(color, 0.2) if is_hovered else color

        if is_selected:
            pygame.draw.rect(DISPLAYSURF, (255, 255, 255), (x - 5, y - 5, COLOR_BOX_SIZE + 10, COLOR_BOX_SIZE + 10), border_radius=12, width=5)

        pygame.draw.rect(DISPLAYSURF, draw_color, (x, y, COLOR_BOX_SIZE, COLOR_BOX_SIZE), border_radius=10)

        name_text = font.render(COLOR_NAMES[i], True, BLACK)
        name_text_rect = name_text.get_rect(center=(x + COLOR_BOX_SIZE // 2, y + COLOR_BOX_SIZE + 20))
        DISPLAYSURF.blit(name_text, name_text_rect)

        if click and is_hovered:
            selected_color = color


def draw_timer_and_score(start_time):
    elapsed_time = int(time.time() - start_time)
    timer_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
    best_score_text = font.render(f"Best score: {best_score}", True, BLACK)

    timer_rect = timer_text.get_rect(topleft=(10, 10))
    DISPLAYSURF.blit(timer_text, timer_rect)

    best_score_rect = best_score_text.get_rect(topleft=(10, 40))
    DISPLAYSURF.blit(best_score_text, best_score_rect)

    return elapsed_time


def draw_restart_button():
    button_width = 100
    button_height = 40
    restart_button_rect = pygame.Rect(WINDOWWIDTH // 2 - button_width // 2, WINDOWHEIGHT // 2 + 80, button_width, button_height)
    pygame.draw.rect(DISPLAYSURF, BLUEISH, restart_button_rect, border_radius=12)

    restart_button_text = font_large.render("Restart", True, WHITE)
    text_rect = restart_button_text.get_rect(center=restart_button_rect.center)

    DISPLAYSURF.blit(restart_button_text, text_rect)

    return restart_button_rect


def show_restart_screen_with_score(message, current_score):
    global grid, best_score, selected_color

    selected_color = None
    message_text = font_large.render(message, True, BURGUNDY if message == "GAME OVER!" else GREEN)
    message_rect = message_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 20))

    score_text = font_large.render(f"Score: {current_score}", True, BLACK)
    score_rect = score_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 15))

    draw_gradient_background()
    DISPLAYSURF.blit(message_text, message_rect)
    DISPLAYSURF.blit(score_text, score_rect)

    if message == "PUZZLE SOLVED" and current_score > best_score:
        best_score = current_score

    restart_button_rect = draw_restart_button()

    pygame.display.update()
    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if restart_button_rect.collidepoint(mouse_x, mouse_y):
                    grid = initialize_grid()
                    waiting_for_click = False
                    return time.time()


def is_valid_color(row, col, color):

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]   # right, down, left, up
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < GRIDWIDTH and 0 <= c < GRIDHEIGHT and grid[r][c] == color:
            return False
    return True


def check_win():
    for row in range(GRIDHEIGHT):
        for col in range(GRIDWIDTH):
            if grid[row][col] is None:
                return False
    return True


def main():
    global grid, best_score, selected_color

    pygame.init()
    grid = initialize_grid()
    start_time = time.time()

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        draw_gradient_background()
        handle_and_draw_color_selection(mouse_x, mouse_y)
        draw_grid(mouse_x, mouse_y)
        elapsed_time = draw_timer_and_score(start_time)

        if check_win():
            current_score = max(1, 1000 - elapsed_time*25)
            start_time = show_restart_screen_with_score("PUZZLE SOLVED", current_score)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                handle_and_draw_color_selection(mouse_x, mouse_y, click=True)

                col = (mouse_x - (WINDOWWIDTH - (GRIDWIDTH * (BOXSIZE + MARGIN))) // 2) // (BOXSIZE + MARGIN)
                row = (mouse_y - ((WINDOWHEIGHT - (GRIDHEIGHT * (BOXSIZE + MARGIN))) // 2 + 50)) // (BOXSIZE + MARGIN)

                if 0 <= row < GRIDHEIGHT and 0 <= col < GRIDWIDTH:
                    if selected_color:
                        if (row, col) in obstacle_positions:
                            continue
                        elif is_valid_color(row, col, selected_color):
                            grid[row][col] = selected_color
                        else:
                            start_time = show_restart_screen_with_score("GAME OVER!", 0)

        pygame.display.update()


if __name__ == "__main__":
    main()
