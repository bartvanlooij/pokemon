from PIL import Image, ImageFilter, ImageOps
import pytesseract
import math
from print_pokemon_data import get_pokemon_data
import pandas as pd
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
im = Image.open("test_fotos/battle.png")

black_seen = False
for i in range(im.height):
    pixel_color = im.getpixel((0, i))
    if pixel_color == (0, 0, 0):
        black_seen = True
    if black_seen:
        if pixel_color != (0, 0, 0):
            top = i
            break

new_image = im.crop((0, top, im.width, im.height))
new_image.save("test_fotos/battle_format.png")

top_screen = im.crop((0, 0, im.width, top))

top_box_found = 0
for i in range(top_screen.height):

    if (top_screen.getpixel((0,i)) == (60,60,60) and top_box_found == 0):
        top_box_found += 1
    if (top_screen.getpixel((0,i)) != (60,60,60) and top_box_found == 1):
        top_box_found += 1
        top_box = i
    if (top_screen.getpixel((0, i)) == (60, 60, 60) and top_box_found == 2):
        bottom_box = i
        break
box_image = top_screen.crop((0,top_box, top_screen.width, bottom_box))
for i in range(0,box_image.width):
    if box_image.getpixel((i, 4)) == (60,60,60):
        box_right = i
        break

box_right = math.floor(box_right*0.61)
bottom_box = bottom_box - top_box
bottom_box = math.floor(bottom_box*0.6)
box_image = top_screen.crop((0,top_box, box_right, top_box + bottom_box))

box_image.save('test_fotos/pokemon_box.png')


get_pokemon_data(pytesseract.image_to_string(box_image), pd.read_csv("pokemon.csv", index_col=0), pd.read_csv("df_all_moves.csv", index_col=0))