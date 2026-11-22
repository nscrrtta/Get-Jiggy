from constants import NUM_HINTS, HINT_FRAMES
from piece import Piece
import random


class Hint:
    """Shows where each piece belongs, one at a time."""

    def reset(self):
        self.num_hints = NUM_HINTS
        # Pieces still to be shown, in order
        self.pieces: list[Piece] = []

    @property
    def giving_hint(self) -> bool:
        return len(self.pieces) > 0

    @property
    def piece(self) -> Piece:
        """The piece being shown."""
        return self.pieces[0]

    def give_hint(self, pieces: list[Piece]):
        if self.giving_hint or self.num_hints == 0:
            return

        self.num_hints -= 1
        self.frames_left = HINT_FRAMES

        # Reveal pieces in a different order each time
        self.pieces = random.sample(pieces, len(pieces))

    def update(self):
        if not self.giving_hint:
            return

        self.frames_left -= 1
        if self.frames_left == 0:
            self.pieces.pop(0)
            self.frames_left = HINT_FRAMES
