import time
from battle_detection import *
from calibration import calibration, find_name_box
import pygetwindow as gw
from PIL import Image, ImageFilter, ImageOps
from compare_images import *
from print_pokemon_data import get_pokemon_data
import pytesseract
import math
from print_pokemon_data import get_pokemon_data
import pandas as pd

def main():
    print_order = ["Name", "Type 1", "Type 2", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Total"]
    df_pokemon = pd.read_csv("pokemon.csv", index_col=0)
    df_all_moves = pd.read_csv("df_all_moves.csv", index_col=0)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    all_windows = gw.getAllTitles()
    name_desmume = [x for x in all_windows if "DeSmuME" in x][0]
    calibration_image = screenshot(name_desmume)
    top_coords, bot_coords = calibration(calibration_image)
    top_screen = calibration_image.crop(top_coords)
    bot_screen = calibration_image.crop(bot_coords)
    battle_format = Image.open("test_fotos/battle_format.png")
    bot_now, test_screen = make_images_same_size(battle_format, bot_screen)
    bot_now = ImageOps.grayscale(bot_now)
    test_screen = ImageOps.grayscale(test_screen)
    similairity = similarity(bot_now,test_screen)
    if similairity > 0.85:
        currently_in_battle = True
    if currently_in_battle:
        box_coords = find_name_box(top_screen)
        box_image = top_screen.crop(box_coords)
        # box_image = Image.open("test_fotos/pokemon_box.png")
        box_image = ImageOps.grayscale(box_image)
        pokemon_name = pytesseract.image_to_string(box_image)
        df_current_pokemon = get_pokemon_data(pokemon_name, df_pokemon, df_all_moves)
        for element in print_order:
            print(f"{element}: {df_current_pokemon.loc[element]}")
    while True:
        break



if __name__ == "__main__":
    main()
