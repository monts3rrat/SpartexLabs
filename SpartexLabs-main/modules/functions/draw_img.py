from PIL import Image, ImageFont, ImageDraw
import asyncio
from loguru import logger
import os


async def draw_profile(id_user, balance):
    try:
        current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
        path = f"{'/'.join(current_directory)[:-10]}/data/"

        id_user = str(id_user)
        balance = str(balance)

        input_image_path = f"{path}/photos/profile.png"
        output_image_path = f"{path}/photos/user_photos/profile_{id_user}.png"
        image = Image.open(input_image_path)
        draw = ImageDraw.Draw(image)
        font_path = f"{path}/fonts/Voltaire-Regular.ttf"
        font = ImageFont.truetype(font_path, size=126)
        print(balance)
        id_x = 51
        if len(id_user) == 9:
            id_x = 76
        elif len(id_user) == 8:
            id_x = 101
        elif len(id_user) < 8:
            id_x = 126

        balance_x = 275
        if len(balance) == 2:
            balance_x = 250
        elif len(balance) == 3:
            balance_x = 220
        elif len(balance) == 4:
            balance_x = 180
        elif len(balance) == 5:
            balance_x = 150
        elif len(balance) == 6:
            balance_x = 130
        elif len(balance) == 7:
            print("да")
            balance_x = 115

        draw.text((id_x, 453), id_user, font=font, fill=(255, 255, 255))
        draw.text((balance_x, 251), f"{balance}$", font=font, fill=(255, 255, 255))

        image.save(f"{output_image_path}")
        return output_image_path

    except Exception as e:
        logger.error(f"Error {e}")


async def draw_ref(id_user, ref):
    try:
        current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
        path = f"{'/'.join(current_directory)[:-10]}/data/"

        id_user = str(id_user)
        ref = str(ref)

        input_image_path = f"{path}/photos/ref.png"
        output_image_path = f"{path}/photos/user_photos/ref_{id_user}.png"
        image = Image.open(input_image_path)
        draw = ImageDraw.Draw(image)
        font_path = f"{path}/fonts/Voltaire-Regular.ttf"
        font = ImageFont.truetype(font_path, size=126)

        ref_x = 320
        if len(ref) == 2:
            ref_x = 280
        elif len(ref) == 3:
            ref_x = 250
        elif len(ref) == 4:
            ref_x = 215

        draw.text((ref_x, 251), ref, font=font, fill=(255, 255, 255))

        image.save(f"{output_image_path}")
        return output_image_path

    except Exception as e:
        logger.error(f"Error {e}")


async def draw_sessions(id_user, sessions):
    try:
        current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
        path = f"{'/'.join(current_directory)[:-10]}/data/"

        id_user = str(id_user)
        sessions = str(sessions)

        input_image_path = f"{path}/photos/sessions.png"
        output_image_path = f"{path}/photos/user_photos/sessions_{id_user}.png"
        image = Image.open(input_image_path)
        draw = ImageDraw.Draw(image)
        font_path = f"{path}/fonts/Voltaire-Regular.ttf"
        font = ImageFont.truetype(font_path, size=126)

        sessions_x = 320
        if len(sessions) == 2:
            sessions_x = 280
        elif len(sessions) == 3:
            sessions_x = 250
        elif len(sessions) == 4:
            sessions_x = 215

        draw.text((sessions_x, 251), sessions, font=font, fill=(255, 255, 255))

        image.save(f"{output_image_path}")
        return output_image_path

    except Exception as e:
        logger.error(f"Error {e}")


async def delete_photo(path_img):
    current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
    path = f"{'/'.join(current_directory)}/modules/data/photos/user_photos"

    os.remove(f"{path_img}")
