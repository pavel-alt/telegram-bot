from PIL import Image, ImageFont, ImageDraw
import os
import random
from io import BytesIO

PATH_TO_CORNER_ELEMENTS = "./images/corner_elements"
PATH_TO_BACKGROUNDS = "./images/backgrounds"
PATH_TO_FONTS = "./fonts"
PATH_TO_VIGNETTES = "./images/vignettes"


def get_valid_files(path: str, formats: list):
    list_images = os.listdir(path)
    valid_files = [file for file in list_images if file.split(".")[1] in formats]
    return valid_files


VALID_CORNER_PICTURES = get_valid_files(PATH_TO_CORNER_ELEMENTS, ["png"])
VALID_BACKGROUNDS = get_valid_files(PATH_TO_BACKGROUNDS, ["jpg", "jpeg"])
VALID_FONTS = get_valid_files(PATH_TO_FONTS, ["ttf", "otf"])
VALID_VIGNETTES = get_valid_files(PATH_TO_VIGNETTES, ["png"])


def get_elements_for_image() -> dict:
    return {"font": f"{PATH_TO_FONTS}/{random.sample(VALID_FONTS, k=1)[0]}",
            "corner_pictures": list(map(lambda x: f"{PATH_TO_CORNER_ELEMENTS}/{x}",
                                        random.sample(VALID_CORNER_PICTURES, k=4))),
            "background": f"{PATH_TO_BACKGROUNDS}/{random.sample(VALID_BACKGROUNDS, k=1)[0]}",
            "vignette": f"{PATH_TO_VIGNETTES}/{random.sample(VALID_VIGNETTES, k=1)[0]}"
            }


def draw_vignette(card_image, vignette_path):
    element_to_paste = Image.open(vignette_path).convert("RGBA")
    card_image.paste(element_to_paste, (100, 30), element_to_paste)
    return card_image


def paste_corner_elements(card_image, corner_elements):
    coordinates = {
        # координаты картинок сверху
        0: (20, 20),
        1: (430, 20),
        # координаты картинок снизу
        2: (20 , 280),
        3: (430, 280)
    }
    el_num = 0
    for element in corner_elements:
        element_to_paste = Image.open(element).convert("RGBA")
        card_image.paste(element_to_paste, coordinates[el_num], element_to_paste)
        el_num += 1
    return card_image


def draw_text_on_igage(card_image, congratulation_phrase, fontpath, color):
    font = ImageFont.truetype(font=fontpath, size=35)
    draw = ImageDraw.Draw(card_image)
    x, y = card_image.size
    w, h = draw.textsize(congratulation_phrase, font)
    draw.text(((x - w) / 2, (y - h) / 2), congratulation_phrase.upper(), font=font, fill=color, align="center")
    return card_image


def congratulation_func():
    output_content = BytesIO()
    output_content.name = "output_content.jpeg"
    picture_ingredients = get_elements_for_image()
    bg = Image.open(picture_ingredients["background"]).convert("RGBA")
    # тут хранятся пути
    corner_elements = picture_ingredients["corner_pictures"]
    vignette = picture_ingredients["vignette"]
    font = picture_ingredients["font"]
    card = Image.new(mode="RGB", size=bg.size)
    card.paste(bg, (0, 0, *bg.size), bg)

    card = draw_vignette(card, vignette)
    card = paste_corner_elements(card, corner_elements)
    card = draw_text_on_igage(card_image=card, congratulation_phrase="тестовое поздравление", fontpath=font, color="yellow")

    card.save(output_content, format='JPEG')
    output_content.seek(0)
    return output_content


congratulation_func()
