### INPUT KEYS ###
LEFT = 'a'
RIGHT = 'd'
UP = 'w'
DOWN = 's'

A = 'o'
B = 'k'

START = 'i'

### DIALOGUE ###
CHARACTERS_PER_LINE = 43
FONT_COLOR = (50, 50, 50)

### GAME STATES ###
OUTSIDE = 0
GAME_MENU = 1
DIALOGUE = 2

### ACTION ###
STANDING = "standing"
WALKING = "walking"
SPRINTING = "sprinting"
JUMPING = "jumping"

### WINDOW ###
WINDOW_SPAWN = "5, 35"
WINDOW_CAPTION = "Pokemon"

UNIT_SIZE = 16
X = 17
Y = 13

X_HALF = X // 2
Y_HALF = Y // 2

CENTER_X_RATIO = X_HALF / X
CENTER_Y_RATIO = (Y_HALF - 1) / Y # due to player sprite being 16x32; ignore top half

DEFAULT_SCREEN_X = 0
DEFAULT_SCREEN_Y = 0

DEFAULT_SCALE = 3
MIN_SCALE = 2
MAX_SCALE = 4

VIEWPORT_WIDTH = X * UNIT_SIZE
VIEWPORT_HEIGHT = Y * UNIT_SIZE

DEFAULT_SCREEN_WIDTH = VIEWPORT_WIDTH * DEFAULT_SCALE
DEFAULT_SCREEN_HEIGHT = VIEWPORT_HEIGHT * DEFAULT_SCALE

### TIME ###
FPS = 60
TIME_PER_FRAME_MS = 1_000 // FPS # frame time in milliseconds

### TIME: SELECT ###
FRAMES_PER_SELECT = 10
CHARACTERS_PER_FRAME = 5 # For dialogue animation

### TIME: ANIMATIONS ###
FRAMES_PER_GRASS_ANIMATION = 60

### TIME: MOVEMENT ###
FRAMES_PER_TURN = 8
FRAMES_PER_SPRINT = 8
FRAMES_PER_WALK = 16
FRAMES_PER_JUMP = 30

WALK_CYCLE_LENGTH = 4
JUMP_CYCLE_LENGTH = 3
SPRINT_CYCLE_LENGTH = 4

assert FRAMES_PER_SPRINT % SPRINT_CYCLE_LENGTH == 0
assert FRAMES_PER_WALK % WALK_CYCLE_LENGTH == 0
assert FRAMES_PER_JUMP % JUMP_CYCLE_LENGTH == 0