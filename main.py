import time
from battle_detection import *
from calibration import calibration, find_name_box
import pygetwindow as gw
from PIL import Image, ImageFilter, ImageOps
from compare_images import *
import pytesseract
from print_pokemon_data import get_pokemon_data
import pandas as pd
import numpy as np
def check_for_battle(bot : PIL.Image.Image, test_screen : PIL.Image.Image):
    bot, test_screen = make_images_same_size(test_screen, bot)
    bot = ImageOps.grayscale(bot)
    test_screen = ImageOps.grayscale(test_screen)
    similairity = similarity(bot, test_screen)
    return similairity


# def print_evolution_order(df_current_pokemon):
#     return_string = ""
#     for count in range(8):
#         if type(df_current_pokemon.loc[f"{count}"]) != np.float64:
#             print(type(df_current_pokemon.loc[f"{count}"]))
#             return_string = return_string + df_current_pokemon.loc[f"{count}"]
#         if type(df_current_pokemon.loc[f"{count+1}_{count+2}"]) != np.float64:
#             evolution_req = df_current_pokemon.loc[f'{count + 1}_{count + 2}']
#             return_string = return_string +  f"---{evolution_req}-->"
#
#     return return_string
def main():
    calibrated = False
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
    box_coords = find_name_box(top_screen)
    calibrated = True
    pokemon_name = "pickacu"
    while calibrated:
        time.sleep(2)
        screen = screenshot(name_desmume)
        bot_screen = screen.crop(bot_coords)
        if (check_for_battle(bot_screen, test_screen) > 0.85):
            currently_in_battle = True
        else:
            currently_in_battle = False


        if currently_in_battle:

            top_screen = screen.crop(top_coords)
            box_image = top_screen.crop(box_coords)
            box_image = ImageOps.grayscale(box_image)
            if pytesseract.image_to_string(box_image) != pokemon_name:
                pokemon_name = pytesseract.image_to_string(box_image)
                df_current_pokemon = get_pokemon_data(pokemon_name, df_pokemon)
                print("\n---------------------------------------------\n")
                for element in print_order:
                    print(f"{element}: {df_current_pokemon.loc[element]}")

                # print(print_evolution_order(df_current_pokemon))





if __name__ == "__main__":
    main()