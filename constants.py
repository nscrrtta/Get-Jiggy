WINDOW_WIDTH = 950
WINDOW_HEIGHT = 800

BOARD_ROWS = 8
BOARD_COLS = 8

# Board squares are large, pieces waiting in the tray are small
SMALL_SQUARE_SIZE = 35
LARGE_SQUARE_SIZE = 45

# Distance from left edge of window to board
LEFT_EDGE = (WINDOW_WIDTH - BOARD_COLS * LARGE_SQUARE_SIZE) // 2

# Distance from top edge of window to board
TOP_EDGE = 30

# Pieces waiting to be placed sit in two rows below the board
TRAY_TOP = 420
TRAY_ROW_HEIGHT = 190
# Gap between pieces in the tray (in small squares)
TRAY_SPACING = 0.7

# Each puzzle uses NUM_PIECES pieces and fills at least MIN_SQUARES squares
NUM_PIECES = 12
MIN_SQUARES = 54

# Board square values
UNUSED = -1 # Not part of the puzzle
EMPTY  = 0
FILLED = 1

# Time to solve each puzzle (ms)
PUZZLE_MS = 60_000

# Timer turns red when this much time is left (ms)
WARNING_MS = 10_000

# Hints can't be used when less than this much time is left (ms)
HINT_CUTOFF_MS = 10_000

NUM_HINTS = 3

# Frames each piece is shown for during a hint
HINT_FRAMES = 30

# Where text is rendered
HINTS_TOPLEFT  = 45, 35
STREAK_TOPLEFT = 45, 85
TIMER_TOPRIGHT = WINDOW_WIDTH - 45, 35

FONT_SIZE = 40

FPS = 60

BG_COLOUR      = (50, 50, 50)
SQUARE_COLOUR  = (150, 150, 150) # Empty board square
TEXT_COLOUR    = (255, 255, 255)
WARNING_COLOUR = (255, 0, 0)     # Timer when time is almost up

# One colour per piece (needs at least NUM_PIECES)
COLOURS = [
    (240,150,230), # Magenta
    (185,130,220), # Purple
    (220,190,255), # Lavender

    (250,190,212), # Pink
    # (230,145,185), # Pink-Red
    (250,120,120), # Red
    # (200,100,100), # Dull Red

    # (255,215,180), # Apricot
    (255,150,100), # Orange
    (255,255,110), # Yellow

    # (200,255, 55), # Lime
    (105,185,135), # Green
    (175,255,200), # Mint
    # (140,220,205), # Dark mint

    ( 60,180,180), # Teal
    (120,255,255), # Cyan
    (176,208,250), # Blue
    # ( 86,118,160), # Dull Blue
]

LARGE_SHAPES = [
    # Square
    [[1,1,1],
     [1,1,1],
     [1,1,1]],

    # Line
    [[1,1,1,1,1]],

    # H
    [[1,0,1],
     [1,1,1],
     [1,0,1]],

    # J
    [[1,1,1],
     [0,1,0],
     [1,1,0]],

    # L
    [[1,0,0],
     [1,0,0],
     [1,1,1]],

    # O
    [[1,1,1],
     [1,0,1],
     [1,1,1]],

    # S
    [[0,1,1],
     [0,1,0],
     [1,1,0]],

    # T
    [[1,1,1],
     [0,1,0],
     [0,1,0]],

    # U
    [[1,0,1],
     [1,0,1],
     [1,1,1]],

    # W
    [[1,0,0],
     [1,1,0],
     [0,1,1]],

    # X
    [[1,0,1],
     [0,1,0],
     [1,0,1]],

    # Y
    [[1,0,1],
     [1,1,1],
     [0,1,0]],

    # /
    [[0,0,1],
     [0,1,0],
     [1,0,0]],

    # ?
    [[1,1,0],
     [0,1,1],
     [0,1,0]],

    # +
    [[0,1,0],
     [1,1,1],
     [0,1,0]]
]


SMALL_SHAPES = [
    # Squares
    [[1]],

    [[1,1],
     [1,1]],

    # Lines
    [[1,1]],

    [[1,1,1]],

    [[1,1,1,1]],

    # L1
    [[1,0],
     [1,1]],

    # L2
    [[1,0,0],
     [1,1,1]],

    # S
    [[1,1,0],
     [0,1,1]],

    # T
    [[1,1,1],
     [0,1,0]],

    # U
    [[1,0,1],
     [1,1,1]]
]
