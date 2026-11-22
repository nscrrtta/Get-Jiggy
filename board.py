from constants import BOARD_ROWS, BOARD_COLS, UNUSED, EMPTY, FILLED


Square = tuple[int, int]


class Board:

    def reset(self):
        self.board = [[EMPTY] * BOARD_COLS for _ in range(BOARD_ROWS)]

    def get(self, row: int, col: int) -> int:
        return self.board[row][col]

    def set(self, row: int, col: int, i: int):
        self.board[row][col] = i

    def cut_out_puzzle(self):
        """Filled squares become the empty puzzle. All other squares aren't used."""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.board[row][col] = EMPTY if self.board[row][col] == FILLED else UNUSED

    def num_filled(self) -> int:
        return sum(row.count(FILLED) for row in self.board)

    def full(self) -> bool:
        return all(EMPTY not in row for row in self.board)

    def out_of_bounds(self, row: int, col: int) -> bool:
        return row < 0 or row >= BOARD_ROWS or col < 0 or col >= BOARD_COLS

    def occupied(self, row: int, col: int) -> bool:
        return self.board[row][col] != EMPTY

    def invalid(self, row: int, col: int) -> bool:
        return self.out_of_bounds(row, col) or self.occupied(row, col)
