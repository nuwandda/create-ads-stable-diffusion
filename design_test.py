from utils import overlay_images, add_text, add_button, add_semi_rounded_rectangle, hex_to_rgb, find_best_font_size
from PIL import Image

# Example usage
overlay_image_path = "sample_images/logo.png"  # Image with a transparent background
output_image_path = "output_image.png"
target_image_size = (768, 768)
target_resize_width_logo = 150
target_resize_width_product = 400

overlay_logo = Image.open(overlay_image_path).convert("RGBA")

result = overlay_images(overlay_logo, (round(target_image_size[0] / 2) - round(target_resize_width_logo / 2), 0),
                        target_image_size, target_resize_width_logo, True)

empty_button_size = (round(target_image_size[0] / 4 * 3), 20)
result = add_semi_rounded_rectangle(result, button_size=empty_button_size, button_position=(target_image_size[0] / 8, -5), button_color=hex_to_rgb('#065535'))
result = add_semi_rounded_rectangle(result, button_size=empty_button_size, button_position=(target_image_size[0] / 8, target_image_size[1] - 5), button_color=hex_to_rgb('#065535'))

overlay = Image.open('sample.jpg')
result = overlay_images(overlay, (round(target_image_size[0] / 2) - round(target_resize_width_product / 2), round(target_image_size[1] / 2) - round(target_resize_width_product / 2)),
                            (result.width, result.height), target_resize_width_product, False, result)

aspect_ratio = overlay.width / overlay.height
target_resize_height_product = round(target_resize_width_product / aspect_ratio)

text_to_add = "AI add banners lead to higher conversions ratesxxxx"
text_position = (round(target_image_size[0] / 8), 
                 round(target_image_size[1] / 2) + round(target_resize_height_product / 2))  # (x, y) position of the top-left corner of the text
text_color = hex_to_rgb('#065535')  # RGB color of the text
font_path = "Trajan-Regular.ttf"  # Replace with the path to your TrueType font file if using a custom font
max_width = round(target_image_size[0] * 6 / 8)
max_height = 300
best_font_size, _, _ = find_best_font_size(text_to_add, max_width, max_height, font_path)

result_with_text = add_text(result, text_to_add, text_position, best_font_size, text_color, font_path)

button_position = (round(target_image_size[0] / 2) - round(target_resize_width_product / 4), 
                   round(target_image_size[1] / 2) + round(target_resize_height_product / 2) + best_font_size * 4)

text = "Call to action text here!"
max_width = 200
max_height = 50

best_font_size, _, _ = find_best_font_size(text, max_width, max_height, font_path)
result = add_button(result_with_text, font_path=font_path, button_position=button_position, 
                    text='Call to action text here!', button_color=hex_to_rgb('#065535'), font_size=best_font_size)

result.save(output_image_path)