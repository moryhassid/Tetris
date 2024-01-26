import pygame
import random
import numpy as np
import time
from pygame import draw

BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
PURPLE = (128, 0, 128)
WIDTH_SCREEN = 320
HEIGHT_SCREEN = 550
BACKGROUND_COLOR = (255, 255, 255)
NUM_TYPES_OF_PUZZLE_PIECES = 8
SQUARE_WIDTH = 20
SQUARE_HEIGHT = 20
VISIBLE_BRICK = 1
STEP_SIZE_TO_MOVE_PUZZLE_PIECE_ON_X_AXIS = 10


def get_piece_of_puzzle():
    collection_of_puzzles = [np.array([[1, 1, 1, 1], [1, 0, 0, 0]]),
                             np.array([[1, 1, 1, 1]]),
                             np.array([[1, 1], [1, 1]]),
                             np.array([[1, 1, 1], [0, 0, 1]]),
                             np.array([[1, 1]]),
                             np.array([[1, 1, 1], [0, 1, 0]]),
                             np.array([[1, 1, 0], [0, 1, 1]]),
                             np.array([[1, 0], [1, 1]])]
    angles = [0, 90, 180, 270]
    # for piece_of_puzzle in collection_of_puzzles:
    #     print(piece_of_puzzle)
    #     print('#' * 50)
    puzzle_number = random.randint(0, NUM_TYPES_OF_PUZZLE_PIECES - 1)
    chosen_puzzle = collection_of_puzzles[puzzle_number]
    chosen_angle = random.choice(angles)
    num_rotations = chosen_angle // 90
    # print(f'To get to {chosen_angle}, we need to rotate {num_rotations} times')
    # print('Original chosen puzzle:')
    # print(chosen_puzzle)
    # print('-' * 50)
    for idx in range(num_rotations):
        chosen_puzzle = np.rot90(chosen_puzzle)
        # print(chosen_puzzle)
        # print('#' * 50)

    return chosen_puzzle


def draw_piece_of_puzzle(piece_of_puzzle, given_screen, color_chosen, start_x_pos, start_y_pos):
    for row_idx, row in enumerate(piece_of_puzzle):
        for col_idx, cell in enumerate(row):
            # print(f'cell[{row_idx},{col_idx}] = {cell}')

            if cell == VISIBLE_BRICK:
                pos_x = start_x_pos + col_idx * SQUARE_WIDTH
                pos_y = start_y_pos + row_idx * SQUARE_HEIGHT
                brick = pygame.Rect(pos_x,
                                    pos_y,
                                    SQUARE_WIDTH,
                                    SQUARE_HEIGHT)

                draw.rect(surface=given_screen,
                          color=color_chosen,
                          rect=brick)

                # Perimeter for the puzzle piece
                for i in range(4):
                    pygame.draw.rect(given_screen,
                                     (0, 0, 0),
                                     (pos_x, pos_y, SQUARE_WIDTH, SQUARE_HEIGHT),
                                     1)


class PuzzlePiece:
    def __init__(self):
        self.collection_of_puzzles = [np.array([[1, 1, 1, 1], [1, 0, 0, 0]]),
                                      np.array([[1, 1, 1, 1]]),
                                      np.array([[1, 1], [1, 1]]),
                                      np.array([[1, 1, 1], [0, 0, 1]]),
                                      np.array([[1, 1]]),
                                      np.array([[1, 1, 1], [0, 1, 0]]),
                                      np.array([[1, 1, 0], [0, 1, 1]]),
                                      np.array([[1, 0], [1, 1]])]

        self.puzzle = []

    def init_new_piece(self):
        puzzle_number = random.randint(0, NUM_TYPES_OF_PUZZLE_PIECES - 1)
        chosen_puzzle = self.collection_of_puzzles[puzzle_number]
        self.puzzle = chosen_puzzle

    def rotate_piece_of_puzzle(self):
        self.puzzle = np.rot90(self.puzzle)

    def bring_down(self):
        pass


def have_reached_bottom_of_screen(puzzle, pos_y):
    lowest_part_of_the_puzzle_y_axis = pos_y + puzzle.shape[0] * SQUARE_HEIGHT

    if lowest_part_of_the_puzzle_y_axis >= HEIGHT_SCREEN:
        return True

    return False


def have_reached_left_or_right_borders(puzzle, pos_x):
    right_part_of_the_puzzle_x_axis = pos_x + puzzle.shape[1] * SQUARE_WIDTH
    left_part_of_the_puzzle_x_axis = pos_x

    if right_part_of_the_puzzle_x_axis >= WIDTH_SCREEN or left_part_of_the_puzzle_x_axis <= 0:
        return True

    return False


class Tetromino:
    def __init__(self, x, y, shape):
        colors = [BLUE, LIGHT_BLUE, GREEN, YELLOW, RED, ORANGE, PURPLE]
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(colors)
        self.rotation = 0


if __name__ == '__main__':

    puzzle = PuzzlePiece()
    puzzle.init_new_piece()
    puzzle.rotate_piece_of_puzzle()

    # exit()
    print('Welcome!')
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    puzzle_piece = get_piece_of_puzzle()
    color_of_piece = random.choice([BLUE, LIGHT_BLUE, GREEN, YELLOW, RED, ORANGE, PURPLE])
    counter_key_pressed = 0
    counter_to_move_down_puzzle_piece = 0
    puzzle_piece_x = WIDTH_SCREEN // 2
    puzzle_piece_y = HEIGHT_SCREEN // 10
    has_reached_floor = False
    has_reached_left_right_borders = False
    while True:
        screen.fill(BACKGROUND_COLOR)
        counter_to_move_down_puzzle_piece += 1
        draw_piece_of_puzzle(piece_of_puzzle=puzzle_piece,
                             given_screen=screen,
                             color_chosen=color_of_piece, start_x_pos=puzzle_piece_x, start_y_pos=puzzle_piece_y)

        for event in pygame.event.get():
            # here we are checking if the user wants to exit the game
            if event.type == pygame.QUIT:
                print('Mory is closing the game')
                exit(0)

        if counter_to_move_down_puzzle_piece > 10 and not has_reached_floor:
            puzzle_piece_y += 20
            counter_to_move_down_puzzle_piece = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            print('Right was pressed')
            if not has_reached_left_right_borders:
                puzzle_piece_x += STEP_SIZE_TO_MOVE_PUZZLE_PIECE_ON_X_AXIS
        elif keys[pygame.K_LEFT]:
            print('Left was pressed')
            if not has_reached_left_right_borders:
                puzzle_piece_x -= STEP_SIZE_TO_MOVE_PUZZLE_PIECE_ON_X_AXIS
        elif keys[pygame.K_UP]:
            counter_key_pressed += 1
            if counter_key_pressed == 2:
                puzzle_piece = np.rot90(puzzle_piece)
                counter_key_pressed = 0
            print('Up was pressed')
        elif keys[pygame.K_DOWN]:
            print('Down was pressed')
            if not has_reached_floor:
                puzzle_piece_y += 5
        elif keys[pygame.K_ESCAPE]:
            print('Mory is closing the game, he has pressed Escape button')
            exit(0)

        has_reached_floor = have_reached_bottom_of_screen(puzzle=puzzle_piece,
                                                          pos_y=puzzle_piece_y)

        has_reached_left_right_borders = have_reached_left_or_right_borders(puzzle=puzzle_piece,
                                                                            pos_x=puzzle_piece_x)

        # Very important each frame we should use to  put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate independent physics.
        dt = clock.tick(20) / 1000

    pygame.quit()
