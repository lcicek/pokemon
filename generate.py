from PIL import Image, ImageFont, ImageDraw
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dimensions', type=int, nargs=2)
parser.add_argument('name', type=str, nargs=1)
parser.add_argument('-cyan', action='store_true')

args = parser.parse_args()
width, height = args.dimensions
name = args.name[0]
cyan = args.cyan

BOTTOM_LEFT_CORNER_PATH = "sprites/displayBox/bottom-left-corner.png" if not cyan else "sprites/displayBox/bottom-left-corner-dialogue.png"
BOTTOM_EDGE_PATH = "sprites/displayBox/bottom-edge.png" if not cyan else "sprites/displayBox/bottom-edge-dialogue.png"
MIDDLE_PATH = "sprites/displayBox/middle.png"
FONT_PATH = "sprites/displayBox/bold_font.ttf"

unit_size = 8

w = width * unit_size
h = height * unit_size

bl_corner = Image.open(BOTTOM_LEFT_CORNER_PATH)
br_corner = bl_corner.rotate(90)
tr_corner = bl_corner.rotate(180)
tl_corner = bl_corner.rotate(270)

bottom_edge = Image.open(BOTTOM_EDGE_PATH)
right_edge = bottom_edge.rotate(90)
top_edge = bottom_edge.rotate(180)
left_edge = bottom_edge.rotate(270)

middle = Image.open(MIDDLE_PATH)

image = Image.new(mode="RGBA", size=(w, h))
font = ImageFont.truetype(font=FONT_PATH, size=8)
draw = ImageDraw.Draw(im=image)

for y in range(0, h, unit_size):
    for x in range(0, w, unit_size):
        if x == y and x == 0:
            curr = tl_corner
        elif x == w-unit_size and y == h-unit_size:
            curr = br_corner
        elif x == 0 and y == h-unit_size:
            curr = bl_corner
        elif x == w-unit_size and y == 0:
            curr = tr_corner
        elif x == 0:
            curr = left_edge
        elif y == 0:
            curr = top_edge
        elif x == w-unit_size:
            curr = right_edge
        elif y == h-unit_size:
            curr = bottom_edge
        else:
            curr = middle
        
        image.paste(curr, box=(x, y))

"""
texts = ["POKEMON", "BAG", "SAVE", "OPTIONS", "EXIT"]
i = 0
for y in range(2*unit_size, h-unit_size, unit_size*3):
    if i == len(texts):
        break

    draw.text(xy=(2*unit_size, y), text=texts[i], font=font, fill='#444444')
    i += 1
"""

image.save(f"sprites/displayBox/generated/{name}.png")