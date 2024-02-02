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


class PuzzlePiece:
    def __init__(self):
        self.puzzles_types = [np.array([[1, 1, 1, 1], [1, 0, 0, 0]]),
                              np.array([[1, 1, 1, 1]]),
                              np.array([[1, 1], [1, 1]]),
                              np.array([[1, 1, 1], [0, 0, 1]]),
                              np.array([[1, 1]]),
                              np.array([[1, 1, 1], [0, 1, 0]]),
                              np.array([[1, 1, 0], [0, 1, 1]]),
                              np.array([[1, 0], [1, 1]])]
        self.chosen_color = random.choice([BLUE, LIGHT_BLUE, GREEN, YELLOW, RED, ORANGE, PURPLE])
        self.start_pos_x = WIDTH_SCREEN // 2
        self.start_pos_y = HEIGHT_SCREEN // 10
        puzzle_number = random.randint(0, NUM_TYPES_OF_PUZZLE_PIECES - 1)
        self.puzzle_shape = self.puzzles_types[puzzle_number]

    def rotate_piece_of_puzzle(self):
        self.puzzle_shape = np.rot90(self.puzzle_shape)

    def show_piece_on_screen(self, given_screen):
        for row_idx, row in enumerate(self.puzzle_shape):
            for col_idx, cell in enumerate(row):
                # print(f'cell[{row_idx},{col_idx}] = {cell}')

                if cell == VISIBLE_BRICK:
                    #     puzzle_piece_x = WIDTH_SCREEN // 2
                    #     puzzle_piece_y = HEIGHT_SCREEN // 10
                    pos_x = self.start_pos_x + col_idx * SQUARE_WIDTH
                    pos_y = self.start_pos_y + row_idx * SQUARE_HEIGHT
                    brick = pygame.Rect(pos_x,
                                        pos_y,
                                        SQUARE_WIDTH,
                                        SQUARE_HEIGHT)

                    draw.rect(surface=given_screen,
                              color=self.chosen_color,
                              rect=brick)

                    # Perimeter for the puzzle piece
                    for i in range(4):
                        pygame.draw.rect(given_screen,
                                         (0, 0, 0),
                                         (pos_x, pos_y, SQUARE_WIDTH, SQUARE_HEIGHT),
                                         1)

    def move_down_piece_of_puzzle(self):
        self.start_pos_y += 5

    def move_left_piece_of_puzzle(self):
        self.start_pos_x -= STEP_SIZE_TO_MOVE_PUZZLE_PIECE_ON_X_AXIS

    def move_right_piece_of_puzzle(self):
        self.start_pos_x += STEP_SIZE_TO_MOVE_PUZZLE_PIECE_ON_X_AXIS

    def has_reached_left_or_right_borders(self):
        right_part_of_the_puzzle_x_axis = self.start_pos_x + self.puzzle_shape.shape[1] * SQUARE_WIDTH
        left_part_of_the_puzzle_x_axis = self.start_pos_x

        if right_part_of_the_puzzle_x_axis >= WIDTH_SCREEN or left_part_of_the_puzzle_x_axis <= 0:
            return True

        return False

    def has_reached_bottom_of_screen(self):
        lowest_part_of_the_puzzle_y_axis = self.start_pos_y + self.puzzle_shape.shape[0] * SQUARE_HEIGHT

        if lowest_part_of_the_puzzle_y_axis >= HEIGHT_SCREEN:
            return True

        return False


class CollectionOfPuzzles:
    def __init__(self):
        self.all_pieces_of_puzzles_so_far = []

    def add_piece_of_puzzle_to_collection(self, puzzle_piece):
        self.all_pieces_of_puzzles_so_far.append(puzzle_piece)

    def show_all_pieces_on_screen(self, given_screen):
        for piece in self.all_pieces_of_puzzles_so_far:
            piece.show_piece_on_screen(given_screen)


if __name__ == '__main__':

    print('Welcome!')
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    color_of_piece = random.choice([BLUE, LIGHT_BLUE, GREEN, YELLOW, RED, ORANGE, PURPLE])
    counter_key_pressed = 0
    counter_to_move_down_puzzle_piece = 0
    puzzle_piece_x = WIDTH_SCREEN // 2
    puzzle_piece_y = HEIGHT_SCREEN // 10
    has_reached_floor = False
    has_reached_left_right_borders = False
    puzzle_counter_appears_on_screen = 0

    current_puzzle_piece = PuzzlePiece()
    collection_of_puzzle_pieces = CollectionOfPuzzles()
    collection_of_puzzle_pieces.add_piece_of_puzzle_to_collection(current_puzzle_piece)

    while True:
        screen.fill(BACKGROUND_COLOR)

        if has_reached_floor:
            current_puzzle_piece = PuzzlePiece()
            collection_of_puzzle_pieces.add_piece_of_puzzle_to_collection(current_puzzle_piece)

        collection_of_puzzle_pieces.show_all_pieces_on_screen(screen)
        counter_to_move_down_puzzle_piece += 1

        for event in pygame.event.get():
            # here we are checking if the user wants to exit the game
            if event.type == pygame.QUIT:
                print('Mory is closing the game')
                exit(0)

        # if counter_to_move_down_puzzle_piece > 10 and not has_reached_floor:
        #     puzzle_piece_y += 20
        #     counter_to_move_down_puzzle_piece = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            print('Right was pressed')
            if not has_reached_left_right_borders:
                current_puzzle_piece.move_right_piece_of_puzzle()
        elif keys[pygame.K_LEFT]:
            print('Left was pressed')
            if not has_reached_left_right_borders:
                current_puzzle_piece.move_left_piece_of_puzzle()
        elif keys[pygame.K_UP]:
            current_puzzle_piece.rotate_piece_of_puzzle()
            # counter_key_pressed += 1
            # if counter_key_pressed == 2:
            #     collection_of_pieces_of_puzzle_on_screen[puzzle_counter_appears_on_screen] = np.rot90(
            #         collection_of_pieces_of_puzzle_on_screen[puzzle_counter_appears_on_screen])
            #     counter_key_pressed = 0
            print('Up was pressed')
        elif keys[pygame.K_DOWN]:
            print('Down was pressed')
            if not has_reached_floor:
                current_puzzle_piece.move_down_piece_of_puzzle()
        elif keys[pygame.K_ESCAPE]:
            print('Mory is closing the game, he has pressed Escape button')
            exit(0)

        has_reached_floor = current_puzzle_piece.has_reached_bottom_of_screen()
        has_reached_left_right_borders = current_puzzle_piece.has_reached_left_or_right_borders()

        # The piece puzzle is moving constantly down towards the ground.
        # until it meets another brick or the ground
        if not has_reached_floor:
            current_puzzle_piece.move_down_piece_of_puzzle()

        # Very important each frame we should use to  put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate independent physics.
        dt = clock.tick(20) / 1000

    pygame.quit()
