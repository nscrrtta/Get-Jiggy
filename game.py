from constants import *
from piece import Piece
from board import Board
from hint import Hint
import pygame
import random


class Game:

    def __init__(self):
        self.board = Board()
        self.hint = Hint()

        self.large_pieces = [Piece(shape) for shape in LARGE_SHAPES]
        self.small_pieces = [Piece(shape) for shape in SMALL_SHAPES]

        # Pieces used in the current puzzle
        self.pieces: list[Piece] = []

        self.solved = False
        self.streak = 0

        self._new_puzzle()

    def _new_puzzle(self):
        self.streak = self.streak + 1 if self.solved else 0
        self.solved = False

        # Time left (ms)
        self.timer = PUZZLE_MS

        self.held_piece: Piece | None = None
        self.hint.reset()

        self._create_puzzle()

    @property
    def puzzle_over(self) -> bool:
        return self.solved or self.timer == 0

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self._key_down(event.key)
        elif self.held_piece is None:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT \
            and not self.puzzle_over:
                self._pick_up_piece(*event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            self._drop_held_piece(*event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.held_piece.follow_mouse(*event.pos)

    def update(self, elapsed: int):
        """Advance the hint by one frame and the timer by elapsed ms."""
        self.hint.update()

        if self.puzzle_over:
            return

        self.timer = max(self.timer - elapsed, 0)

        # When time runs out, reveal the solution
        if self.timer == 0:
            self.held_piece = None
            for piece in self.pieces:
                piece.reveal()

    def _key_down(self, key: int):
        # New puzzle
        if key == pygame.K_SPACE and self.puzzle_over:
            self._new_puzzle()

        elif self.puzzle_over:
            return

        # Remove all pieces from board
        elif key == pygame.K_BACKSPACE:
            for piece in self.pieces:
                if piece.on_board:
                    self._remove_from_board(piece)
                    piece.return_home()

        # Give hint (not in the last few seconds)
        elif key == pygame.K_h and self.timer >= HINT_CUTOFF_MS:
                self.hint.give_hint(self.pieces)

    def _pick_up_piece(self, x: int, y: int):
        for piece in self.pieces:
            if piece.contains_point(x, y):
                if piece.on_board:
                    self._remove_from_board(piece)
                piece.pick_up(x, y)
                self.held_piece = piece
                return

    def _drop_held_piece(self, x: int, y: int):
        piece = self.held_piece
        self.held_piece = None

        piece.follow_mouse(x, y)
        row, col = piece.nearest_square()

        # Can't place pieces on the board while giving a hint
        if self.hint.giving_hint or not piece.fits_here(row, col, self.board):
            piece.return_home()
            return

        for r, c in piece.squares:
            self.board.set(row + r, col + c, FILLED)
        piece.place(row, col)

        self.solved = self.board.full()

    def _remove_from_board(self, piece: Piece):
        for row, col in piece.squares:
            self.board.set(piece.row + row, piece.col + col, EMPTY)

    ### Creating a puzzle ###

    def _create_puzzle(self):
        """
        Create a random puzzle that uses NUM_PIECES pieces
        and fills at least MIN_SQUARES squares on the board.
        """
        random.shuffle(self.large_pieces)
        random.shuffle(self.small_pieces)

        while True:
            self.pieces.clear()
            self.board.reset()

            # Use large pieces first, then small pieces
            for piece in self.large_pieces + self.small_pieces:
                self._rotate_flip(piece)
                piece.set_squares()

                # If it can't fit anywhere, move onto next piece
                options = self._where_piece_fits(piece)
                if not options:
                    continue

                # Randomly place piece on board
                row, col = random.choice(options)
                for r, c in piece.squares:
                    self.board.set(row + r, col + c, FILLED)
                piece.solution_row, piece.solution_col = row, col
                self.pieces.append(piece)

                if len(self.pieces) == NUM_PIECES:
                    break
            # Not enough pieces -> keep trying
            else:
                continue

            # Enough pieces, but is the board full enough?
            if self.board.num_filled() >= MIN_SQUARES:
                break

        self.board.cut_out_puzzle()
        self._organize_pieces()
        self._assign_colours()

    def _rotate_flip(self, piece: Piece):
        """Randomly rotate and flip a piece."""
        piece.rotate(random.randint(0, 3))
        if random.choice([True, False]): piece.flip_x_axis()
        if random.choice([True, False]): piece.flip_y_axis()

    def _where_piece_fits(self, piece: Piece) -> list[tuple[int, int]]:
        return [(row, col)
            for row in range(BOARD_ROWS - piece.height + 1)
            for col in range(BOARD_COLS - piece.width + 1)
            if piece.fits_here(row, col, self.board)
        ]

    def _organize_pieces(self):
        """Organize pieces into two rows below the board, centered in the window."""
        n = NUM_PIECES // 2

        for row in range(2):
            pieces = self.pieces[n * row : n * (row + 1)]
            total_width = sum(piece.width + TRAY_SPACING for piece in pieces)

            x = (WINDOW_WIDTH - SMALL_SQUARE_SIZE * total_width) / 2
            y = TRAY_TOP + TRAY_ROW_HEIGHT * row

            for piece in pieces:
                piece.set_home(int(x), y)
                x += (piece.width + TRAY_SPACING) * SMALL_SQUARE_SIZE

    def _assign_colours(self):
        """Give each piece a different random colour."""
        colours = COLOURS[:]
        random.shuffle(colours)
        for piece, colour in zip(self.pieces, colours):
            piece.colour = colour
