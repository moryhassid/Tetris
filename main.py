import pygame
import random
import numpy as np
import time
from pygame import draw

# Colors:
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
PURPLE = (128, 0, 128)
BACKGROUND_COLOR = (255, 255, 255)

# Screen Size
WIDTH_SCREEN = 320
HEIGHT_SCREEN = 600
SQUARE_WIDTH = 20
SQUARE_HEIGHT = 20
NUMBER_OF_BRICKS_PER_ROW = WIDTH_SCREEN // SQUARE_WIDTH
VISIBLE_BRICK = 1
STEP_SIZE_TO_MOVE_PUZZLE_PIECE_ON_X_AXIS = SQUARE_WIDTH


class PuzzlePiece:
    def __init__(self):
        self.puzzles_types = [
            np.array([[1] * 4]),
            np.array([[0, 0, 0, 1], [1] * 4])
            # np.array([[1, 1, 1, 1], [1, 0, 0, 0]]),
            # np.array([[1, 1, 1, 1]]),
            # np.array([[1, 1], [1, 1]]),
            # np.array([[1, 1, 1], [0, 0, 1]]),
            # np.array([[1, 1]]),
            # np.array([[1, 1, 1], [0, 1, 0]]),
            # np.array([[1, 1, 0], [0, 1, 1]]),
            # np.array([[1, 0], [1, 1]])
        ]
        self.chosen_color = random.choice([BLUE, LIGHT_BLUE, GREEN, YELLOW, RED, ORANGE, PURPLE])
        self.start_pos_x = WIDTH_SCREEN // 2
        self.start_pos_y = 3 * SQUARE_HEIGHT
        NUM_TYPES_OF_PUZZLE_PIECES = len(self.puzzles_types)
        puzzle_number = random.randint(0, NUM_TYPES_OF_PUZZLE_PIECES - 1)
        self.puzzle_structure = self.puzzles_types[puzzle_number]

    def rotate_piece_of_puzzle(self):
        self.puzzle_structure = np.rot90(self.puzzle_structure)

    def show_piece_on_screen(self, given_screen):
        print("#" * 100)
        print(self.puzzle_structure)
        for row_idx, row in enumerate(self.puzzle_structure):
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
                    self.add_border_to_square(given_screen, pos_x, pos_y)

    @staticmethod
    def add_border_to_square(given_screen, pos_x, pos_y):
        for i in range(4):
            pygame.draw.rect(given_screen,
                             (0, 0, 0),
                             (pos_x, pos_y, SQUARE_WIDTH, SQUARE_HEIGHT),
                             1)

    def move_down_piece_of_puzzle(self):
        self.start_pos_y += SQUARE_HEIGHT

    def move_left_piece_of_puzzle(self):
        self.start_pos_x -= STEP_SIZE_TO_MOVE_PUZZLE_PIECE_ON_X_AXIS

    def move_right_piece_of_puzzle(self):
        self.start_pos_x += STEP_SIZE_TO_MOVE_PUZZLE_PIECE_ON_X_AXIS

    def has_reached_left_or_right_borders(self):
        right_part_of_the_puzzle_x_axis = self.start_pos_x + self.puzzle_structure.shape[1] * SQUARE_WIDTH
        left_part_of_the_puzzle_x_axis = self.start_pos_x

        if right_part_of_the_puzzle_x_axis >= WIDTH_SCREEN or left_part_of_the_puzzle_x_axis <= 0:
            return True

        return False

    @staticmethod
    def get_height_of_specific_column_in_puzzle(puzzle_piece, column_number):
        return len(np.where(puzzle_piece[:, column_number] > 0)[0])

    def has_reached_bottom_of_screen(self, collection, puzzle_number):
        lowest_part_of_the_puzzle_y_axis = self.start_pos_y + self.puzzle_structure.shape[0] * SQUARE_HEIGHT
        cell_number_start = self.start_pos_x // SQUARE_WIDTH
        cell_number_end = (self.start_pos_x + self.puzzle_structure.shape[1] * SQUARE_WIDTH) // SQUARE_WIDTH
        # number_of_cells_fits_on_screen_along_x_axis = WIDTH_SCREEN // SQUARE_WIDTH
        # print(f'puzzle number in x axis: {cell_number}/{number_of_cells_fits_on_screen_along_x_axis}')
        height_for_given_x = collection.heights_per_width_slices[cell_number_start]
        # print(f'{height_for_given_x=}')

        # if lowest_part_of_the_puzzle_y_axis == HEIGHT_SCREEN:
        #     print('debug')
        if lowest_part_of_the_puzzle_y_axis == height_for_given_x:
            for idx in range(cell_number_start, cell_number_end):
                # print(f'{collection.heights_per_width_slices=}')
                collection.heights_per_width_slices[idx] = \
                    height_for_given_x - SQUARE_HEIGHT * self.get_height_of_specific_column_in_puzzle(
                        puzzle_piece=self.puzzle_structure, column_number=idx - cell_number_start)
            return True, self.puzzle_structure, (cell_number_start, cell_number_end)

        return False, None, None

    # @staticmethod
    # def is_row_was_completed():
    #     return True
    #
    @staticmethod
    def update_heights_per_width_slices_after_row_completed(collection):
        for idx in range(len(collection.heights_per_width_slices)):
            collection.heights_per_width_slices[idx] -= SQUARE_HEIGHT

    def trim_puzzle(self):
        # puzzle1[:1, :]
        self.puzzle_structure = self.puzzle_structure[:1, :]

    def __str__(self):
        return f'{self.puzzle_structure=}\n{self.chosen_color=}\n{self.start_pos_x=}\n{self.start_pos_y=}\n'


class CollectionOfPuzzles:
    def __init__(self):
        self.all_pieces_of_puzzles_so_far = []
        # For following the perimeter of the bricks that are on the screen,
        # I'm using a list of heights per each slice of width SQUARE_WIDTH.
        self.heights_per_width_slices = [HEIGHT_SCREEN] * (WIDTH_SCREEN // SQUARE_WIDTH)
        self.grid = []

    def add_piece_of_puzzle_to_collection(self, puzzle_piece):
        self.all_pieces_of_puzzles_so_far.append(puzzle_piece)

    def update_all_pieces_of_puzzle_for_trimming(self, row_number_to_remove):
        for puzzle in range(104545):
            puzzle.trim_puzzle()

        # TODO: Write the logic to iterate over all pieces of puzzles and
        # modify the puzzle_shape and start_pos_y
        pass

    #     for row_idx, row in enumerate(puzzle_piece.puzzle_shape):
    #         for col_idx, cell in enumerate(row):
    #             if cell == VISIBLE_BRICK:
    #                 grid_row = (puzzle_piece.start_pos_y // SQUARE_HEIGHT) + row_idx
    #                 grid_col = (puzzle_piece.start_pos_x // SQUARE_WIDTH) + col_idx
    #                 self.grid[grid_row, grid_col] = 1
    #
    # def clear_full_rows(self):
    #     full_rows = []
    #     for row_idx in range(len(self.grid)):
    #         if np.all(self.grid[row_idx]):
    #             full_rows.append(row_idx)
    #
    #     # Clear full rows and shift down
    #     for row_idx in full_rows:
    #         self.grid[1:row_idx + 1] = self.grid[:row_idx]
    #         self.grid[0] = 0  # Clear the top row
    #
    #     # Adjust heights based on cleared rows
    #     for col_idx in range(len(self.heights_per_width_slices)):
    #         # Reduce heights for each column based on the number of cleared rows
    #         for cleared_row in full_rows:
    #             # Only reduce height if the cleared row was below this column
    #             if self.heights_per_width_slices[col_idx] >= cleared_row * SQUARE_HEIGHT:
    #                 self.heights_per_width_slices[col_idx] -= SQUARE_HEIGHT
    #
    #     return len(full_rows)

    def show_all_pieces_on_screen(self, given_screen):
        # print("*" * 100)
        for piece in self.all_pieces_of_puzzles_so_far:
            # print(piece.puzzle_shape)
            piece.show_piece_on_screen(given_screen)
        # print("*" * 100)

    def print_all_pieces(self):
        # print("*" * 100)
        for idx, piece in enumerate(self.all_pieces_of_puzzles_so_far):
            print(f'{idx}) {piece}')
        # print("*" * 100)


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

    counter_puzzle_pieces = 1
    score = 0
    while True:
        screen.fill(BACKGROUND_COLOR)

        if has_reached_floor:
            counter_puzzle_pieces += 1
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
            # print('Right was pressed')
            if not has_reached_left_right_borders:
                current_puzzle_piece.move_right_piece_of_puzzle()
        elif keys[pygame.K_LEFT]:
            # print('Left was pressed')
            if not has_reached_left_right_borders:
                current_puzzle_piece.move_left_piece_of_puzzle()
        elif keys[pygame.K_UP]:
            current_puzzle_piece.rotate_piece_of_puzzle()
            # print('Up was pressed')
        elif keys[pygame.K_DOWN]:
            # print('Down was pressed')
            if not has_reached_floor:
                current_puzzle_piece.move_down_piece_of_puzzle()
        elif keys[pygame.K_ESCAPE]:
            print('Mory is closing the game, he has pressed Escape button')
            exit(0)

        has_reached_floor, puzzle_shape_reached, range_puzzle_on_x = current_puzzle_piece.has_reached_bottom_of_screen(
            collection_of_puzzle_pieces,
            counter_puzzle_pieces)

        if has_reached_floor:
            collection_of_puzzle_pieces.print_all_pieces()
            # time.sleep(3)  # TODO: remove
            if counter_puzzle_pieces == 1:
                collection_of_puzzle_pieces.grid = np.zeros((puzzle_shape_reached.shape[0], NUMBER_OF_BRICKS_PER_ROW),
                                                            dtype=int)
            start_col, end_col = range_puzzle_on_x
            piece_puzzle_height = puzzle_shape_reached.shape[0]
            piece_puzzle_width = puzzle_shape_reached.shape[1]
            collection_of_puzzle_pieces.grid[0:0 + piece_puzzle_height,
            start_col:start_col + piece_puzzle_width] += current_puzzle_piece.puzzle_structure
            # collection_of_puzzle_pieces.update_all_pieces_of_puzzle_for_trimming(row_number_to_remove=121212)
            rows_status = np.all(collection_of_puzzle_pieces.grid == 1, axis=1)
            number_of_completed_rows = np.sum(rows_status)
            if number_of_completed_rows > 0:
                completed_rows_index = np.where(rows_status)
                print("Rows index which were filled completely: ", completed_rows_index)
                print("Debug")
            score += number_of_completed_rows

            # print("#" * 30 + "Grid" + "#" * 30)
            # print(collection_of_puzzle_pieces.grid)
            # print("#" * 30)
            print(f"We should remove {number_of_completed_rows} rows!!!")
            print("Updating grid")
            # collection_of_puzzle_pieces.add_piece_of_puzzle_to_collection()
            collection_of_puzzle_pieces.grid = collection_of_puzzle_pieces.grid[~rows_status]
            print("#" * 30 + "Grid" + "#" * 30)
            print(collection_of_puzzle_pieces.grid)
            print("#" * 30)

        has_reached_left_right_borders = current_puzzle_piece.has_reached_left_or_right_borders()

        # The piece puzzle is moving constantly down towards the ground.
        # until it meets another brick or the ground
        # print(f'heights_per_width_slices = {collection_of_puzzle_pieces.heights_per_width_slices}')
        if not has_reached_floor:
            current_puzzle_piece.move_down_piece_of_puzzle()

        # Very important each frame we should use to  put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate independent physics.
        dt = clock.tick(10) / 1  # 1000

    pygame.quit()
