import random
import time

import pygame

# Define colors
BACKGROUND_COLOR = (18, 26, 37)
BLOCK_COLOR = (0, 204, 204)
TEXT_COLOR = (255, 255, 255)
SCORE_PANEL_COLOR = (26, 36, 51)
NEXT_BLOCK_PANEL_COLOR = (26, 36, 51)
BORDER_COLOR = (38, 52, 74)

# Define block shapes
S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..00.',
                     '.00..',
                     '.....'],
                    ['.....',
                     '..0..',
                     '..00.',
                     '...0.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.00..',
                     '..00.',
                     '.....'],
                    ['.....',
                     '..0..',
                     '.00..',
                     '.0...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..0..',
                     '..0..',
                     '..0..',
                     '..0..',
                     '.....'],
                    ['.....',
                     '0000.',
                     '.....',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.00..',
                     '.00..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.0...',
                     '.000.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..00.',
                     '..0..',
                     '..0..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.000.',
                     '...0.',
                     '.....'],
                    ['.....',
                     '..0..',
                     '..0..',
                     '.00..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...0.',
                     '.000.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..0..',
                     '..0..',
                     '..00.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.000.',
                     '.0...',
                     '.....'],
                    ['.....',
                     '.00..',
                     '..0..',
                     '..0..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..0..',
                     '.000.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..0..',
                     '..00.',
                     '..0..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.000.',
                     '..0..',
                     '.....'],
                    ['.....',
                     '..0..',
                     '.00..',
                     '..0..',
                     '.....']]

# Define block types
BLOCK_TYPES = {'S': S_SHAPE_TEMPLATE,
               'Z': Z_SHAPE_TEMPLATE,
               'I': I_SHAPE_TEMPLATE,
               'O': O_SHAPE_TEMPLATE,
               'J': J_SHAPE_TEMPLATE,
               'L': L_SHAPE_TEMPLATE,
               'T': T_SHAPE_TEMPLATE}

# Define block size
BLOCK_SIZE = 20

# Define board size
BOARD_WIDTH = 15
BOARD_HEIGHT = 35

# Define footer size
FOOTER_HEIGHT = 30

# Set the window size
WINDOW_SIZE = (BOARD_WIDTH * BLOCK_SIZE + 200, BOARD_HEIGHT * BLOCK_SIZE + FOOTER_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Initialize Pygame
pygame.init()

# Set the window title
pygame.display.set_caption("Tetris")

# Define the font
font = pygame.font.SysFont("Century Gothic", 20)

# Define the game variables
board = [['.' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
current_block = None
next_block = None
score = 0
game_over = False
paused = False


# Define the function to create a new block
def create_block():
    block_shape = random.choice(list(BLOCK_TYPES.keys()))
    block_color = BLOCK_COLOR
    block = {'shape': block_shape, 'rotation': 0, 'x': BOARD_WIDTH // 2 - 2, 'y': -2, 'color': block_color}
    return block


# Define the function to draw the board
def draw_board():
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x] != '.':
                pygame.draw.rect(screen, board[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(screen, BORDER_COLOR, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    # Add a border around the board for better visualization
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, BOARD_WIDTH * BLOCK_SIZE, BOARD_HEIGHT * BLOCK_SIZE), 2)


# Define the function to add the block to the board
def add_to_board(block):
    shape = BLOCK_TYPES[block['shape']][block['rotation']]
    for y in range(5):
        for x in range(5):
            if shape[y][x] == '0':
                board[block['y'] + y][block['x'] + x] = block['color']


# Define the function to draw the score
def draw_score():
    score_panel_width = 180
    score_panel_height = 60  # Increase height to accommodate the score text and value
    score_panel_x = BOARD_WIDTH * BLOCK_SIZE + 10
    score_panel_y = 20

    # Draw score panel background
    pygame.draw.rect(screen, SCORE_PANEL_COLOR, (score_panel_x, score_panel_y, score_panel_width, score_panel_height))
    pygame.draw.rect(screen, BORDER_COLOR, (score_panel_x, score_panel_y, score_panel_width, score_panel_height), 2)

    # Define font for the score text
    score_font = pygame.font.SysFont("Century Gothic", 20)

    # Render the score text
    score_text = score_font.render("Score", True, TEXT_COLOR)
    score_text_width = score_text.get_width()
    score_text_height = score_text.get_height()
    score_text_x = score_panel_x + (score_panel_width - score_text_width) // 2
    score_text_y = score_panel_y + (
            score_panel_height - score_text_height) // 2 - score_text_height // 2  # Adjust the offset
    screen.blit(score_text, (score_text_x, score_text_y))

    # Render the actual score value
    score_value_text = score_font.render(str(score), True, TEXT_COLOR)
    score_value_text_width = score_value_text.get_width()
    score_value_text_height = score_value_text.get_height()
    score_value_text_x = score_panel_x + (score_panel_width - score_value_text_width) // 2
    score_value_text_y = score_panel_y + (
            score_panel_height - score_value_text_height) // 2 + score_text_height // 2  # Adjust the offset
    screen.blit(score_value_text, (score_value_text_x, score_value_text_y))


# Define the function to draw a block
def draw_block(block, offset_x=0, offset_y=0):
    shape = BLOCK_TYPES[block['shape']][block['rotation']]
    for y in range(5):
        for x in range(5):
            if shape[y][x] == '0':
                pygame.draw.rect(screen, block['color'], (
                    (block['x'] + x + offset_x) * BLOCK_SIZE, (block['y'] + y + offset_y) * BLOCK_SIZE, BLOCK_SIZE,
                    BLOCK_SIZE), 0)
                pygame.draw.rect(screen, BORDER_COLOR, (
                    (block['x'] + x + offset_x) * BLOCK_SIZE, (block['y'] + y + offset_y) * BLOCK_SIZE, BLOCK_SIZE,
                    BLOCK_SIZE), 1)


# Define the function to draw the next block
def draw_next_block():
    next_block_text = font.render("Next Block", True, TEXT_COLOR)
    screen.blit(next_block_text, (BOARD_WIDTH * BLOCK_SIZE + 5, 150))
    draw_block(next_block, offset_x=BOARD_WIDTH + 5 // BLOCK_SIZE, offset_y=10)
    # Draw a border around the next block area
    pygame.draw.rect(screen, BORDER_COLOR, (BOARD_WIDTH * BLOCK_SIZE, 150, 180, 180), 2)


# Define the function to draw the game over message
def draw_game_over():
    game_over_text = font.render("Game Over!", True, TEXT_COLOR)
    text_width = game_over_text.get_width()
    text_height = game_over_text.get_height()
    draw_footer()
    screen.blit(game_over_text,
                ((BOARD_WIDTH * BLOCK_SIZE - text_width) // 2, (BOARD_HEIGHT * BLOCK_SIZE - text_height) // 2))


# Define the function to check if a block's position is valid
def is_valid_position(block, adjX=0, adjY=0):
    shape = BLOCK_TYPES[block['shape']][block['rotation']]
    for y in range(5):
        for x in range(5):
            if shape[y][x] == '0':
                newX, newY = block['x'] + x + adjX, block['y'] + y + adjY
                if not (0 <= newX < BOARD_WIDTH and newY < BOARD_HEIGHT):
                    return False
                elif newY >= 0 and board[newY][newX] != '.':
                    return False
    return True


# Define the function to draw the paused message
def draw_paused():
    paused_text = font.render("Paused", True, TEXT_COLOR)
    text_width = paused_text.get_width()
    text_height = paused_text.get_height()
    screen.blit(paused_text,
                ((BOARD_WIDTH * BLOCK_SIZE - text_width) // 2, (BOARD_HEIGHT * BLOCK_SIZE - text_height) // 2))


# Define the function to remove complete lines
def remove_complete_lines():
    num_lines_removed = 0
    for y in range(BOARD_HEIGHT - 1, -1, -1):  # Iterate from the bottom up
        if all(board[y][x] != '.' for x in range(BOARD_WIDTH)):  # Check for '.' not BLOCK_COLOR
            # This row is complete, so remove it and move everything above it down
            for pull_down_Y in range(y, 0, -1):
                for x in range(BOARD_WIDTH):
                    board[pull_down_Y][x] = board[pull_down_Y - 1][x]
            # Set the top row to '.' not BLOCK_COLOR
            for x in range(BOARD_WIDTH):
                board[0][x] = '.'
            num_lines_removed += 1
    return num_lines_removed


# Create the current block if it doesn't exist
def update_game():
    global current_block
    global next_block
    global score
    global game_over

    if current_block is None:
        current_block = create_block()
        if next_block is None:
            next_block = create_block()
        else:
            current_block, next_block = next_block, create_block()
        if not is_valid_position(current_block):
            game_over = True

    # Move the current block down
    if not is_valid_position(current_block, adjY=1):
        # The block has landed
        add_to_board(current_block)
        score += remove_complete_lines()
        current_block = None
        # Check if game over
        if any(board[0][x] != '.' for x in range(BOARD_WIDTH)):  # Game over when the top row has any blocks
            game_over = True
    else:
        # The block is still falling
        current_block['y'] += 1


"""def show_start_screen():
    screen.fill(BACKGROUND_COLOR)
    start_screen_text = font.render("Welcome to TETRIS", True, TEXT_COLOR)
    text_width = start_screen_text.get_width()
    text_height = start_screen_text.get_height()
    screen.blit(start_screen_text, ((WINDOW_SIZE[0] - text_width) // 2, (WINDOW_SIZE[1] - text_height) // 2))
    draw_footer()
    pygame.display.flip()"""


def show_start_screen():
    screen.fill(BACKGROUND_COLOR)
    start_screen_text = "TETRIS"
    x = (WINDOW_SIZE[0] - font.size(start_screen_text)[0]) // 2
    y = (WINDOW_SIZE[1] - font.size(start_screen_text)[1]) // 2
    for i in range(len(start_screen_text)):
        screen.blit(font.render(start_screen_text[:i + 1], True, TEXT_COLOR), (x, y))
        pygame.display.flip()
        time.sleep(0.1)  # Adjust the sleep duration to control the speed of animation
    draw_footer()
    pygame.display.flip()


"""def show_start_screen():
    screen.fill(BACKGROUND_COLOR)
    start_screen_text = "TETRIS"
    font_size = 60

    x = (WINDOW_SIZE[0] - font.size(start_screen_text)[0]) // 2
    y = (WINDOW_SIZE[1] - font.size(start_screen_text)[1]) // 2

    for i in range(len(start_screen_text)):
        screen.blit(font.render(start_screen_text[:i + 1], True, TEXT_COLOR), (x, y))
        pygame.display.flip()
        time.sleep(0.1)  # Adjust the sleep duration to control the speed of animation

    # Calculate the number of rows and columns to evenly distribute blocks
    block_size = 20
    num_blocks = 30  # Adjust the number of blocks as desired
    rows = int(WINDOW_SIZE[1] / block_size)
    cols = int(WINDOW_SIZE[0] / block_size)
    total_blocks = rows * cols

    if num_blocks > total_blocks:
        num_blocks = total_blocks

    # Randomly select block types for each block
    block_types = random.choices(list(BLOCK_TYPES.keys()), k=num_blocks)

    # Calculate the spacing between blocks
    row_spacing = int(WINDOW_SIZE[1] / rows)
    col_spacing = int(WINDOW_SIZE[0] / cols)

    # Randomly assign positions for blocks
    positions = random.sample(range(total_blocks), num_blocks)

    # Draw the Tetris blocks at random positions
    for pos in positions:
        row = pos // cols
        col = pos % cols

        block_type = block_types.pop()
        block_shape = random.choice(BLOCK_TYPES[block_type])
        block_color = BLOCK_COLOR
        block_x = col * col_spacing + (col_spacing - len(block_shape[0]) * block_size) // 2
        block_y = row * row_spacing + (row_spacing - len(block_shape) * block_size) // 2

        for shape_row in range(len(block_shape)):
            for shape_col in range(len(block_shape[shape_row])):
                if block_shape[shape_row][shape_col] == '0':
                    pygame.draw.rect(
                        screen,
                        block_color,
                        (block_x + shape_col * block_size, block_y + shape_row * block_size, block_size, block_size),
                    )

    draw_footer()
    pygame.display.flip()"""


def show_game_over_screen():
    screen.fill(BACKGROUND_COLOR)
    game_over_text = font.render("Game Over", True, TEXT_COLOR)
    text_width = game_over_text.get_width()
    text_height = game_over_text.get_height()
    screen.blit(game_over_text, ((WINDOW_SIZE[0] - text_width) // 2, (WINDOW_SIZE[1] - text_height) // 2))
    pygame.display.flip()


def wait_for_key_press():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  # Exit the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # K_RETURN is the "enter" key
                    waiting = False


def reset_game():
    global board
    global current_block
    global next_block
    global score
    global game_over
    global paused

    # Reset game variables
    board = [['.' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    current_block = None
    next_block = None
    score = 0
    game_over = False
    paused = False


# Define the function to draw the developer details
def draw_footer():
    # Define footer area
    global FOOTER_HEIGHT
    footer_width = WINDOW_SIZE[0]  # Use the width of the window as the width of the footer area
    footer_x = 0  # Align the footer to the left side of the window
    footer_y = WINDOW_SIZE[1] - FOOTER_HEIGHT  # Position the footer at the bottom of the window

    pygame.draw.rect(screen, SCORE_PANEL_COLOR, (footer_x, footer_y, footer_width, FOOTER_HEIGHT))  # Footer background
    pygame.draw.rect(screen, BORDER_COLOR, (footer_x, footer_y, footer_width, FOOTER_HEIGHT), 1)  # Footer border

    # Define the font for the footer, smaller than the main font
    footer_font = pygame.font.SysFont("Century Gothic", 15)

    # Render the footer text
    footer_text = footer_font.render("Developed by: Abhishek Shah | Developed Year: 2020", True, TEXT_COLOR)
    text_width = footer_text.get_width()
    text_height = footer_text.get_height()
    text_x = (footer_width - text_width) // 2  # Calculate the x-coordinate to center the text
    text_y = footer_y + (FOOTER_HEIGHT - text_height) // 2  # Calculate the y-coordinate to center the text
    screen.blit(footer_text, (text_x, text_y))


# Define the function to run the game
def run_game():
    global paused
    global game_over

    clock = pygame.time.Clock()
    start_screen = True
    while True:  # Outer loop that restarts the game if necessary
        if start_screen:
            show_start_screen()
            wait_for_key_press()
            game_over = False

            reset_game()

        while not game_over:  # Game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    elif current_block is not None:  # Ensure current_block is not None before using it
                        if event.key == pygame.K_UP:
                            current_block['rotation'] = (current_block['rotation'] + 1) % len(
                                BLOCK_TYPES[current_block['shape']])
                            if not is_valid_position(current_block):
                                current_block['rotation'] = (current_block['rotation'] - 1) % len(
                                    BLOCK_TYPES[current_block['shape']])
                        elif event.key == pygame.K_DOWN:
                            update_game()

            if not paused:
                keys = pygame.key.get_pressed()  # Get the state of all keys
                if keys[pygame.K_LEFT] and current_block is not None and is_valid_position(current_block, adjX=-1):
                    current_block['x'] -= 1
                if keys[pygame.K_RIGHT] and current_block is not None and is_valid_position(current_block, adjX=1):
                    current_block['x'] += 1
                update_game()

            # Draw everything
            screen.fill(BACKGROUND_COLOR)
            pygame.draw.rect(screen, SCORE_PANEL_COLOR,
                             (BOARD_WIDTH * BLOCK_SIZE, 0, 200, BOARD_HEIGHT * BLOCK_SIZE + FOOTER_HEIGHT))
            pygame.draw.rect(screen, NEXT_BLOCK_PANEL_COLOR,
                             (BOARD_WIDTH * BLOCK_SIZE + 15, 20, 170, 100))  # Draw score panel
            pygame.draw.rect(screen, NEXT_BLOCK_PANEL_COLOR,
                             (BOARD_WIDTH * BLOCK_SIZE + 15, 140, 170, 170))  # Draw next block panel
            draw_board()
            draw_score()
            draw_next_block()
            draw_footer()
            if paused:
                draw_paused()
            if current_block is not None:  # Ensure current_block is not None before drawing it
                draw_block(current_block)
            pygame.display.update()

            clock.tick(10)

        # When the game is over show the game over screen
        show_game_over_screen()
        wait_for_key_press()
        start_screen = True  # Reset to the start screen for the next game


run_game()
