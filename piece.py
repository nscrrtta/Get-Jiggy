from constants import SMALL_SQUARE_SIZE, LARGE_SQUARE_SIZE, LEFT_EDGE, TOP_EDGE
from board import Board, Square


class Piece:

    def __init__(self, shape: list[list[int]]):
        self.shape = shape
        self.colour = None

        self.held = self.on_board = False

        # Top-left pixel position of this piece's spot in the tray
        self.home_x = self.home_y = 0
        # Current top-left pixel position (follows the mouse while held)
        self.x = self.y = 0
        # Offset from the mouse to the top-left of the piece while held
        self.grab_dx = self.grab_dy = 0

        # Board square of the top-left of the piece while on the board
        self.row = self.col = 0
        # Board square of the top-left of the piece in the solution
        self.solution_row = self.solution_col = 0

    @property
    def size(self) -> int:
        """Pixel size of this piece's squares."""
        if self.on_board or self.held:
            return LARGE_SQUARE_SIZE
        return SMALL_SQUARE_SIZE

    def set_squares(self):
        self.height = len(self.shape)
        self.width = len(self.shape[0])

        self.squares = [(row, col)
            for row in range(self.height)
            for col in range(self.width)
            if self.shape[row][col]
        ]

    def rotate(self, n: int):
        """Rotate clockwise n times."""
        for _ in range(n):
            self.shape = list(zip(*self.shape[::-1]))

    def flip_x_axis(self):
        self.shape = self.shape[::-1]

    def flip_y_axis(self):
        self.shape = [row[::-1] for row in self.shape]

    def set_home(self, x: int, y: int):
        self.home_x, self.home_y = x, y
        self.return_home()

    def return_home(self):
        self.x, self.y = self.home_x, self.home_y
        self.on_board = False
        self.held = False

    def contains_point(self, x: int, y: int) -> bool:
        return self._square_at(x, y) is not None

    def pick_up(self, x: int, y: int):
        # Small pieces grow to full size around the square under the mouse
        row, col = self._square_at(x, y)
        size_diff = LARGE_SQUARE_SIZE - self.size
        self.grab_dx = self.x - col * size_diff - x
        self.grab_dy = self.y - row * size_diff - y

        self.on_board = False
        self.held = True
        self.follow_mouse(x, y)

    def follow_mouse(self, x: int, y: int):
        self.x = x + self.grab_dx
        self.y = y + self.grab_dy

    def nearest_square(self) -> Square:
        """Return the board square nearest the top-left of this piece."""
        x = self.x + LARGE_SQUARE_SIZE // 2 - LEFT_EDGE
        y = self.y + LARGE_SQUARE_SIZE // 2 - TOP_EDGE
        return y // LARGE_SQUARE_SIZE, x // LARGE_SQUARE_SIZE

    def fits_here(self, r: int, c: int, board: Board) -> bool:
        for row, col in self.squares:
            if board.invalid(row + r, col + c):
                return False
        return True

    def place(self, row: int, col: int):
        self.row, self.col = row, col
        self.x = LARGE_SQUARE_SIZE * col + LEFT_EDGE
        self.y = LARGE_SQUARE_SIZE * row + TOP_EDGE
        self.on_board = True
        self.held = False

    def reveal(self):
        self.place(self.solution_row, self.solution_col)

    def _square_at(self, x: int, y: int) -> Square | None:
        """Return the (row, col) of this piece's square at pixel (x, y), if any."""
        size = self.size
        for row, col in self.squares:
            left = self.x + col * size
            top  = self.y + row * size

            if left < x < left + size and top < y < top + size:
                return row, col
        return None
