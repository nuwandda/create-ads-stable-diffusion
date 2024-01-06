import random
from PIL import Image, ImageDraw, ImageFont
import webcolors


def set_seed():
    seed = random.randint(42, 4294967295)
    return seed


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
        
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        
    return closest_name


def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')  # Remove '#' if present
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


def find_best_font_size(text, max_width, max_height, font_path=None, min_font_size=1, max_font_size=100):
    best_font_size = min_font_size
    best_text_width, best_text_height = 0, 0

    for font_size in range(min_font_size, max_font_size + 1):
        font = ImageFont.load_default() if font_path is None else ImageFont.truetype(font_path, font_size)
        text_width, text_height = ImageDraw.Draw(Image.new("RGB", (1, 1))).textsize(text, font)

        if text_width <= max_width and text_height <= max_height:
            best_font_size = font_size
            best_text_width, best_text_height = text_width, text_height
        else:
            break

    return best_font_size, best_text_width, best_text_height


def resize_image_with_ratio(input_image, target_width):
    # Calculate the new height to maintain the aspect ratio
    aspect_ratio = input_image.width / input_image.height
    target_height = round(target_width / aspect_ratio)

    # Resize the image
    resized_image = input_image.resize((target_width, target_height), Image.ANTIALIAS)

    return resized_image


def add_text(input_image, text, position=(10, 10), font_size=20, text_color=(255, 255, 255), font_path=None):  
    # Create a drawing object
    draw = ImageDraw.Draw(input_image)

    # Load a font (if font_path is provided) or use a default font
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # Add text to the image
    draw.text(position, text, font=font, fill=text_color, align="center")

    return input_image


def add_button(input_image, button_size=(200, 50), text="Click Me", text_color=(255, 255, 255), button_color=(0, 128, 255), font_size=20, font_path=None, button_position=(10, 10)):
    # Create a drawing object
    draw = ImageDraw.Draw(input_image)

    # Draw a filled rectangle to simulate the button
    draw.rounded_rectangle([button_position[0], button_position[1], button_position[0] + button_size[0], button_position[1] + button_size[1]], 20, fill=button_color)

    # Load a font (if font_path is provided) or use a default font
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # Calculate the position to center the text on the button
    text_width, text_height = draw.textsize(text, font)
    text_position = ((button_size[0] - text_width) // 2 + button_position[0], (button_size[1] - text_height) // 2 + button_position[1])

    # Add text to the button
    draw.text(text_position, text, font=font, fill=text_color, align="center")

    return input_image


def add_semi_rounded_rectangle(input_image, button_size=(200, 50), button_color=(0, 128, 255), button_position=(10, 10), corner_radius=10):
    # Create a drawing object
    draw = ImageDraw.Draw(input_image)

    # Create semi-rounded rectangles for the top and bottom
    top_rect = [button_position[0], button_position[1], button_position[0] + button_size[0], button_position[1] + button_size[1] // 2]

    draw.rounded_rectangle(top_rect, corner_radius, fill=button_color)

    return input_image


def overlay_images(overlay_image, coordinates, background_size, target_resize_width, logo, background_image=None):
    # Open the background image
    background = None
    if background_image is None:
        background = Image.new("RGB", (background_size[0], background_size[1]), "white")
    else:
        background = background_image

    # Resize overlay image to fit on the background
    overlay = resize_image_with_ratio(overlay_image, target_resize_width)
    
    rounded_image = None
    if not logo:
        # Create a mask with rounded corners
        mask = Image.new("L", overlay.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), overlay.size], 20, fill=255)

        # Apply the mask to the image
        rounded_image = Image.new("RGBA", overlay.size, (255, 255, 255, 0))
        rounded_image.paste(overlay, mask=mask)

    # Paste the overlay on top of the background
    if logo:
        background.paste(overlay, coordinates, overlay)
    else:
        background.paste(rounded_image, coordinates)
    
    # Save the result
    return background
