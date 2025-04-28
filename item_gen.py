import os
import random

from PIL import Image, ImageDraw, ImageFont

# Colors
text_colors = {
    "0": ["black", (0, 0, 0)], "1": ["dark blue", (0, 0, 170)], "2": ["dark green", (0, 170, 0)],
    "3": ["dark aqua", (0, 170, 170)], "4": ["dark red", (170, 0, 0)], "5": ["dark purple", (170, 0, 170)],
    "6": ["gold", (255, 170, 0)], "7": ["gray", (170, 170, 170)], "8": [
        "dark_gray", (85, 85, 85)], "9": ["blue", (85, 85, 255)], "a": ["green", (85, 255, 85)],
    "b": ["aqua", (85, 255, 255)], "c": ["red", (255, 85, 85)], "d": ["light purple", (255, 85, 255)],
    "e": ["yellow", (255, 255, 85)], "f": ["white", (255, 255, 255)]
}
shadow_colors = {
    "0": ["black", (0, 0, 0)], "1": ["dark blue", (0, 0, 42)], "2": ["dark green", (0, 42, 0)],
    "3": ["dark aqua", (0, 42, 42)], "4": ["dark red", (42, 0, 0)], "5": ["dark purple", (42, 0, 42)],
    "6": ["gold", (42, 42, 0)], "7": ["gray", (42, 42, 42)], "8": [
        "dark_gray", (21, 21, 21)], "9": ["blue", (21, 21, 63)], "a": ["green", (21, 63, 21)],
    "b": ["aqua", (21, 63, 63)], "c": ["red", (63, 21, 21)], "d": ["light purple", (63, 21, 63)],
    "e": ["yellow", (63, 63, 21)], "f": ["white", (63, 63, 63)]
}

# Fonts
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)


class Font:
    BOLD = ImageFont.truetype(dir_path + "/fonts/MinecraftBold.otf", 20)
    REGULAR = ImageFont.truetype(dir_path + "/fonts/MinecraftRegular.otf", 20)
    UNIFONT = ImageFont.truetype(dir_path + "/fonts/unifont.ttf", 16)


class CharacterTemplate:
    def __init__(self, character, color, shadow_color, bolded, italics, unicode, random, underline, strike):
        self.character = character
        self.color = color
        self.shadow_color = shadow_color
        self.bolded = bolded
        self.italics = italics
        self.unicode = unicode
        self.random = random
        self.original = character
        self.underline = underline
        self.strike = strike


def process_lines(lore_lines):
    processed_lines = []

    # Title and Lore have space in Between
    lore_lines.insert(1, [])

    for line in lore_lines:
        # Default Character Values
        code_character = False
        character_color = (255, 255, 255)
        character_shadow_color = (63, 63, 63)
        character_bold = False
        character_italic = False
        character_random = False
        character_underline = False
        character_strike = False

        current_line = []

        # Checks if line is blank
        if (line == []) or (line == ""):
            processed_lines.append([])
            continue

        for character in line:
            # Checks if the character is a special unicode character
            if ord(character) > 127 and not character == "§":
                unicode = True
            else:
                unicode = False
            # Check if character indicates a future code character
            if character == "&" or character == "§":
                code_character = True
            # Check if character is code character
            elif code_character is True:
                code_character = False
                # Check if Color Code Character
                if character.lower() in text_colors:
                    character_color = text_colors[character][1]
                    character_shadow_color = shadow_colors[character][1]
                # Check if Reset character
                elif character.lower() == "r":
                    character_color = (255, 255, 255)
                    character_shadow_color = (63, 63, 63)
                    character_italic = False
                    character_bold = False
                    character_random = False
                    character_strike = False
                    character_underline = False
                # Check if Bold Character
                elif character.lower() == "l":
                    character_bold = True
                # Check if Italic Charcter
                elif character.lower() == "o":
                    character_italic = True
                # Check if Random Character
                elif character.lower() == "k":
                    character_random = True
                # Check if Strike Character
                elif character.lower() == "m":
                    character_strike = True
                # Check if Underline Character
                elif character.lower() == "n":
                    character_underline = True
            else:
                image_character = CharacterTemplate(
                    character, character_color,
                    character_shadow_color, character_bold,
                    character_italic, unicode,
                    character_random, character_underline, character_strike
                )
                current_line.append(image_character)
        processed_lines.append(current_line)
    return processed_lines


def calculate_image_size(processed_lines):
    # Calculate Height and Width for Image
    width = 0
    height = 6*2 + 18 + (20 * (len(processed_lines) - 2))
    if len(processed_lines) > 2:
        height += 6
    x = 8
    for line in processed_lines:
        if not line == []:
            for character in line:
                if character.bolded is True:
                    fnt = Font.BOLD
                else:
                    fnt = Font.REGULAR
                if character.unicode:
                    fnt = Font.UNIFONT
                if character.character == " ":
                    size = 10
                    x += size
                else:
                    size = int(fnt.getlength(character.character))
                    x += size
            if x > width:
                width = x + 10
            x = 8
    return width, height


def draw_italics(char, x, y, width, height, background, fnt, color):
    """
    Draws charcters on new image,
    shift different parts of characters to italcize it,
    then take new image and imprint it on the old image
    """
    foreground = Image.new('RGBA', (width, height))
    foreground_draw = ImageDraw.Draw(foreground)

    size = int(fnt.getlength(char))
    foreground_draw.text((x, y), char, font=fnt, fill=color)

    # Pixel Number 1-2
    region = foreground.crop((x, y + 2, size + x, y + 4))
    foreground_draw.rectangle(
        (x, y + 2, size + x, y + 3),
        outline=(0, 0, 0), fill=(0, 0, 0)
    )
    foreground.paste(region, (x + 2, y + 2))

    # Pixel Number 3-4
    region = foreground.crop((x, y + 4, size + x, y + 6))
    foreground_draw.rectangle(
        (x, y + 4, size + x, y + 5),
        outline=(0, 0, 0), fill=(0, 0, 0)
    )
    foreground.paste(region, (x + 1, y + 4))

    # Pixel Number 5-6
    region = foreground.crop((x, y + 6, size + x, y + 8))
    foreground_draw.rectangle(
        (x, y + 6, size + x, y + 7),
        outline=(0, 0, 0), fill=(0, 0, 0)
    )
    foreground.paste(region, (x + 1, y + 6))

    # Pixel Number 7-10 - None

    # Pixel Number 11-14
    region = foreground.crop((x, y + 12, size + x, y + 16))
    foreground_draw.rectangle(
        (x, y + 12, size + x, y + 15),
        outline=(0, 0, 0), fill=(0, 0, 0)
    )
    foreground.paste(region, (x - 1, y + 12))

    # Pixel Number 15-16
    region = foreground.crop((x, y + 16, size + x, y + 19))
    foreground_draw.rectangle(
        (x, y + 16, size + x, y + 18),
        outline=(0, 0, 0), fill=(0, 0, 0)
    )
    foreground.paste(region, (x - 2, y + 16))

    # Combine 2 images together
    background.paste(foreground, (0, 0), foreground)
    return background


def draw_characters(img, draw, lines, width, height, shadow=False):
    # Draw Actual Characters
    # K Random Code Character in Image
    random_detected = False
    x = 8
    line_number = 0
    for line in lines:
        line_number += 1
        if not line == []:
            # Draw each character
            for character in line:
                # Setting Font for the Character
                if character.bolded is True:
                    fnt = Font.BOLD
                else:
                    fnt = Font.REGULAR

                # Set Color
                color = character.color
                shadow_color = character.shadow_color

                # Check if Random
                if character.random is True:
                    if not character.character == " ":
                        # character.character = chr(random.randint(33, 127))
                        magic = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{" \
                                "|}~⌂ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜø£Ø×ƒáíóúñÑªº¿®¬½¼¡«»"
                        character.character = random.choice(magic)
                        random_detected = True

                # Draw Shadow Strike
                if character.strike is True:
                    if line_number == 1:
                        y_line = 16
                        draw.line(
                            (x + 2, y_line, x + 2 + int(fnt.getlength(character.original)), y_line),
                            fill=shadow_color, width=2
                        )

                    else:
                        y_line = 23 + ((line_number - 2) * 7 + (13 * (line_number - 3))) + 10
                        draw.line(
                            (x + 2, y_line, x + 2 + (fnt.getlength(character.original)), y_line),
                            fill=shadow_color, width=2
                        )

                # Draw Shadow Underline
                if character.underline is True:
                    if line_number == 1:
                        y_line = 28
                        draw.line(
                            (x + 2, y_line, x + 2 + int(fnt.getlength(character.original)), y_line),
                            fill=shadow_color, width=2
                        )

                    else:
                        y_line = 23 + ((line_number - 2) * 7 + (13 * (line_number - 3))) + 20
                        draw.line(
                            (x + 2, y_line, x + 2 + int(fnt.getlength(character.original)), y_line),
                            fill=shadow_color, width=2
                        )

                # Set fonts if Unicode
                if character.unicode is True:
                    fnt = Font.UNIFONT

                    # Special Drawing for Unifont Characters
                    if line_number == 1:
                        draw.text((x, 8), character.character, font=fnt, fill=shadow_color)
                        draw.text((x, 8), character.character, font=fnt, fill=color)
                    else:
                        draw.text(
                            (x, 25 + ((line_number - 2) * 7 + (13 * (line_number - 3)))), character.character, font=fnt,
                            fill=shadow_color
                        )
                        draw.text(
                            (x, 25 + ((line_number - 2) * 7 + (13 * (line_number - 3)))), character.character, font=fnt,
                            fill=color
                        )
                else:
                    if character.italics is True:
                        # Drawing Italics
                        if line_number == 1:
                            img = draw_italics(
                                character.character, x + 2, 8, width, height, img, fnt, shadow_color
                            )
                            img = draw_italics(
                                character.character, x, 6, width, height, img, fnt, color
                            )
                        else:
                            img = draw_italics(
                                character.character, x + 2, 25 + ((line_number - 2) * 7 + (13 * (line_number - 3))),
                                width, height, img, fnt, shadow_color
                            )
                            img = draw_italics(
                                character.character, x, 23 + ((line_number - 2) * 7 + (13 * (line_number - 3))), width,
                                height, img, fnt, color
                            )

                    else:
                        # Drawing Normal Characters
                        if line_number == 1:
                            draw.text((x + 2, 8), character.character, font=fnt, fill=shadow_color)
                            draw.text((x, 6), character.character, font=fnt, fill=color)
                        else:
                            draw.text(
                                (x + 2, 25 + ((line_number - 2) * 7 + (13 * (line_number - 3)))), character.character,
                                font=fnt, fill=shadow_color
                            )
                            draw.text(
                                (x, 23 + ((line_number - 2) * 7 + (13 * (line_number - 3)))), character.character,
                                font=fnt, fill=color
                            )

                # Draw Strike
                if character.strike is True:
                    if line_number == 1:
                        y_line = 14
                        draw.line(
                            (x, y_line, x + int(fnt.getlength(character.original)), y_line),
                            fill=color, width=2
                        )
                    else:

                        y_line = 23 + ((line_number - 2) * 7 + (13 * (line_number - 3))) + 8
                        draw.line(
                            (x, y_line, x + int(fnt.getlength(character.original)), y_line),
                            fill=color, width=2
                        )

                # Draw Underline
                if character.underline is True:
                    if line_number == 1:
                        y_line = 24
                        draw.line(
                            (x, y_line, x + int(fnt.getlength(character.original)), y_line),
                            fill=color, width=2
                        )
                    else:
                        y_line = 23 + ((line_number - 2) * 7 + (13 * (line_number - 3))) + 18
                        draw.line(
                            (x, y_line, x + int(fnt.getlength(character.original)), y_line),
                            fill=color, width=2
                        )

                # Increment x value to tell where to draw next character
                if character.original == " ":
                    if character.bolded is True:
                        size = 10
                    else:
                        size = 8
                    x += size
                else:
                    size = int(fnt.getlength(character.original))
                    x += size
            x = 8
    return img, random_detected


def render(lines, *, background: bool = True):
    # Process lines
    lines = process_lines(lines)

    # Get Width and Height
    width, height = calculate_image_size(lines)
    # Intialize Image
    if background:
        img = Image.new('RGB', (width, height), color=(0, 0, 0))
    else:
        img = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Image Border
    if background:
        draw.line((2, 2, 2, height - 3), fill=(44, 8, 99), width=2)
        draw.line((2, 2, width - 4, 2), fill=(44, 8, 99), width=2)
        draw.line((width - 4, 2, width - 4, height - 4), fill=(44, 8, 99), width=2)
        draw.line((2, height - 4, width - 3, height - 4), fill=(44, 8, 99), width=2)

    # Draw Characters
    # Copy Image for GIF
    original_image = img.copy()
    img = img.copy()
    draw = ImageDraw.Draw(img)

    img, random_detected = draw_characters(img, draw, lines, width, height)
    images = []
    if random_detected is True:
        for i in range(0, 20):
            # Copy Image for GIF
            img = original_image.copy()
            draw = ImageDraw.Draw(img)
            # Generate GIF
            img, random_detected = draw_characters(
                img, draw, lines, width, height
            )
            images.append(img)

    return img, images
