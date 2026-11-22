from constants import *
from piece import Piece
from game import Game
import pygame
import math


Colour = tuple[int, int, int]


class GameRenderer:

    def __init__(self, window: pygame.Surface, game: Game):
        self.window = window
        self.game = game

        # Dynamic
        self.hints_text  = Text('', topleft=HINTS_TOPLEFT)
        self.streak_text = Text('', topleft=STREAK_TOPLEFT)
        self.timer_text  = Text('', topright=TIMER_TOPRIGHT)

    def draw(self):
        self.window.fill(BG_COLOUR)
        self._draw_board()
        self._draw_hint()
        self._draw_pieces()
        self._draw_text()

    def _draw_board(self):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.game.board.get(row, col) == UNUSED:
                    continue
                left = LARGE_SQUARE_SIZE * col + LEFT_EDGE
                top  = LARGE_SQUARE_SIZE * row + TOP_EDGE
                self._draw_square(left, top, LARGE_SQUARE_SIZE, SQUARE_COLOUR)

    def _draw_hint(self):
        hint = self.game.hint
        if not hint.giving_hint:
            return

        piece = hint.piece
        for row, col in piece.squares:
            left = LARGE_SQUARE_SIZE * (col + piece.solution_col) + LEFT_EDGE
            top  = LARGE_SQUARE_SIZE * (row + piece.solution_row) + TOP_EDGE
            self._draw_square(left, top, LARGE_SQUARE_SIZE, piece.colour)

    def _draw_pieces(self):
        # Pieces on the board are hidden while giving a hint
        giving_hint = self.game.hint.giving_hint

        # Draw the held piece last, so it's on top
        held_piece = self.game.held_piece
        for piece in self.game.pieces:
            if piece is held_piece or (piece.on_board and giving_hint):
                continue
            self._draw_piece(piece)
        if held_piece:
            self._draw_piece(held_piece)

    def _draw_piece(self, piece: Piece):
        size = piece.size
        for row, col in piece.squares:
            left = piece.x + col * size
            top  = piece.y + row * size
            self._draw_square(left, top, size, piece.colour)

    def _draw_square(self, left: int, top: int, size: int, colour: Colour):
        rect = pygame.Rect(left + 1, top + 1, size - 2, size - 2)
        pygame.draw.rect(self.window, colour, rect, border_radius=6)

    def _draw_text(self):
        game = self.game

        self.hints_text.set(f'Hints: {game.hint.num_hints}')
        self.hints_text.draw(self.window)

        self.streak_text.set(f'Streak: {game.streak}')
        self.streak_text.draw(self.window)

        colour = WARNING_COLOUR if game.timer <= WARNING_MS else TEXT_COLOUR
        self.timer_text.set(f'{math.ceil(game.timer / 1000)}', colour)
        self.timer_text.draw(self.window)


class Text:

    def __init__(self, text: str, **rect_kwargs):
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.rect_kwargs = rect_kwargs
        self.text = self.colour = None
        self.set(text)

    def set(self, text: str, colour: Colour = TEXT_COLOUR):
        if text == self.text and colour == self.colour:
            return
        self.text, self.colour = text, colour
        self.surface = self.font.render(text, True, colour)
        self.rect = self.surface.get_rect(**self.rect_kwargs)

    def draw(self, window: pygame.Surface):
        window.blit(self.surface, self.rect)
