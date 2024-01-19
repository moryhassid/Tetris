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
WIDTH_SCREEN = 300
HEIGHT_SCREEN = 550
BACKGROUND_COLOR = (255, 255, 255)
NUM_TYPES_OF_PUZZLE_PIECES = 8
SQUARE_WIDTH = 20
SQUARE_HEIGHT = 20


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


def draw_piece_of_puzzle(piece_of_puzzle, given_screen):
    brick = pygame.Rect(WIDTH_SCREEN // 2,
                        HEIGHT_SCREEN // 2,
                        SQUARE_WIDTH,
                        SQUARE_HEIGHT)

    draw.rect(surface=given_screen,
              color=BLUE,
              rect=brick)


class Tetromino:
    def __init__(self, x, y, shape):
        colors = [BLUE, LIGHT_BLUE, GREEN, YELLOW, RED, ORANGE, PURPLE]
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(colors)
        self.rotation = 0


if __name__ == '__main__':
    print('Welcome!')
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    while True:
        screen.fill(BACKGROUND_COLOR)

        puzzle_piece = get_piece_of_puzzle()
        draw_piece_of_puzzle(piece_of_puzzle=puzzle_piece,
                             given_screen=screen)

        for event in pygame.event.get():
            # here we are checking if the user wants to exit the game
            if event.type == pygame.QUIT:
                print('Mory is closing the game')
                exit(0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            print('Right was pressed')
        elif keys[pygame.K_LEFT]:
            print('Left was pressed')
        elif keys[pygame.K_UP]:
            print('Up was pressed')
        elif keys[pygame.K_DOWN]:
            print('Down was pressed')
        elif keys[pygame.K_ESCAPE]:
            print('Mory is closing the game, he has pressed Escape button')
            exit(0)

        # Very important each frame we should use to  put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate independent physics.
        dt = clock.tick(20) / 1000

    pygame.quit()
