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
MAX_SCALE = 4

VIEWPORT_WIDTH = X * UNIT_SIZE
VIEWPORT_HEIGHT = Y * UNIT_SIZE

DEFAULT_SCREEN_WIDTH = VIEWPORT_WIDTH * DEFAULT_SCALE
DEFAULT_SCREEN_HEIGHT = VIEWPORT_HEIGHT * DEFAULT_SCALE

### TIME ###
FPS = 60
TIME_PER_FRAME_MS = 1_000 // FPS # frame time in milliseconds
FRAMES_PER_WALK = 15
FRAMES_PER_STANDING_TURN = 8
WALK_CYCLE_FRAMES = 4

### DIRECTION ###
LEFT = 'a'
RIGHT = 'd'
UP = 'w'
DOWN = 's'

### ACTION ###
STANDING = "standing"
WALKING = "walking"
SPRINTING = "sprinting"

### TILED ###
TILED_MAP_PATH = "tiles/maps/map_logic.tmx"

### LOCATION SPRITES ###
LOCATION_SPRITE = "tiles/render-images/map.png"
LOCATION_FOREGROUND = "tiles/render-images/map_foreground.png"

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