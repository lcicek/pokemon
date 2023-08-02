WINDOW_SPAWN = "5, 35"

UNIT_SIZE = 16
X = 17
Y = 13

X_HALF = X // 2
Y_HALF = Y // 2

CENTER_X_RATIO = X_HALF / X
CENTER_Y_RATIO = (Y_HALF - 1) / Y # due to player sprite being 16x32; ignore top half

DEFAULT_SCREEN_X = 0
DEFAULT_SCREEN_Y = 0

DEFAULT_SCALE = 2.5

VIEWPORT_WIDTH = X * UNIT_SIZE
VIEWPORT_HEIGHT = Y * UNIT_SIZE

DEFAULT_SCREEN_WIDTH = VIEWPORT_WIDTH * DEFAULT_SCALE
DEFAULT_SCREEN_HEIGHT = VIEWPORT_HEIGHT * DEFAULT_SCALE

### TIME ###
FPS = 25
TIME_PER_FRAME_MS = 1_000 // FPS # frame time in milliseconds

MOVE_DURATION = 300
TURN_DURATION = 100
NS_TO_MS_RATIO = 1_000_000 # e.g. 200_000_000 ns = 200 ms (= 0.2s)

### DIRECTION ###
LEFT = 'a'
RIGHT = 'd'
UP = 'w'
DOWN = 's'

### ACTION ###
STANDING = "standing"
WALKING = "walking"
SPRINTING = "sprinting"

### PLAYER SPRITES FOR ANIMATION ###
STANDING_FRONT = "sprites/player/standing-front.png"
STANDING_BACK = "sprites/player/standing-back.png"
STANDING_LEFT = "sprites/player/standing-left.png"
STANDING_RIGHT = "sprites/player/standing-right.png"

WALKING_FRONT = "sprites/player/walking-front.png"
WALKING_BACK = "sprites/player/walking-back.png"
WALKING_LEFT = "sprites/player/walking-left.png"
WALKING_RIGHT = "sprites/player/walking-right.png"

WALKING_FRONT_2 = "sprites/player/walking-front2.png"
WALKING_BACK_2 = "sprites/player/walking-back2.png"
WALKING_LEFT_2 = "sprites/player/walking-left2.png"
WALKING_RIGHT_2 = "sprites/player/walking-right2.png"

### LOCATION SPRITES ###
LOCATION_SPRITE = "tiles/map.png"