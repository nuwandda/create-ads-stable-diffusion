import torch 
from diffusers import StableDiffusionImg2ImgPipeline
import os
from dotenv import load_dotenv
from PIL import Image
import utils

load_dotenv()
MODEL_PATH = os.getenv('MODEL_PATH')
SEED = -1
NUM_INFERENCE_STEPS = 50
GUIDANCE_SCALE = 15
STRENGTH = 0.6
NEGATIVE_PROMPT = 'noisy, blurry, amateurish, sloppy, unattractive'


def create_pipeline(model_path):
    # Create the pipe 
    pipe = None
    if torch.cuda.is_available():
        # Create the pipe 
        pipe = StableDiffusionImg2ImgPipeline.from_single_file(
            model_path, 
            revision="fp16", 
            torch_dtype=torch.float16
        )
    else:
        pipe = StableDiffusionImg2ImgPipeline.from_single_file(model_path)
    
    # pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")

    if torch.backends.mps.is_available():
        device = "mps"
    else: 
        device = "cuda" if torch.cuda.is_available() else "cpu"

    pipe.to(device)
    
    return pipe


pipe = create_pipeline('weights/realisticVisionV60B1_v20Novae.safetensors')


def create_ad(init_image, logo_image, hex_color, prompt, punchline_text, punchline_color, button_text, button_color,) -> Image:
    generator = torch.Generator().manual_seed(utils.set_seed()) if float(SEED) == -1 else torch.Generator().manual_seed(int(SEED))
    init_image = init_image.resize((512, 512))
    requested_color = utils.hex_to_rgb(hex_color)
    closest_color_name = utils.get_colour_name(requested_color)
    
    final_prompt = 'Retail packaging style {} {}. Vibrant, enticing, commercial, product-focused, eye-catching, professional, highly detailed'.format(closest_color_name, prompt)

    base_image: Image = pipe(final_prompt,
                        image=init_image,
                       strength=STRENGTH,
                        negative_prompt=NEGATIVE_PROMPT,
                        guidance_scale=GUIDANCE_SCALE, 
                        num_inference_steps=NUM_INFERENCE_STEPS, 
                        generator = generator, 
                    ).images[0]
    
    target_image_size = (768, 768)
    target_resize_width_logo = 150
    target_resize_width_product = 400
    
    result = utils.overlay_images(logo_image, (round(target_image_size[0] / 2) - round(target_resize_width_logo / 2), 0),
                            target_image_size, target_resize_width_logo, True)
    empty_button_size = (round(target_image_size[0] / 4 * 3), 20)
    result = utils.add_semi_rounded_rectangle(result, button_size=empty_button_size, 
                                              button_position=(target_image_size[0] / 8, -5), 
                                              button_color=utils.hex_to_rgb(button_color))
    result = utils.add_semi_rounded_rectangle(result, button_size=empty_button_size, 
                                              button_position=(target_image_size[0] / 8, target_image_size[1] - 5), 
                                              button_color=utils.hex_to_rgb(button_color))
    
    result = utils.overlay_images(base_image, (round(target_image_size[0] / 2) - round(target_resize_width_product / 2), 
                                             round(target_image_size[1] / 2) - round(target_resize_width_product / 2)),
                                (result.width, result.height), target_resize_width_product, False, result)
    
    # (x, y) position of the top-left corner of the text
    text_position = (round(target_image_size[0] / 8), target_image_size[1] - 130)
    # Replace with the path to your TrueType font file if using a custom font
    font_path = "Trajan-Regular.ttf"
    max_width = round(target_image_size[0] * 6 / 8)
    max_height = 300
    best_font_size, _, _ = utils.find_best_font_size(punchline_text, max_width, max_height, font_path)
    result = utils.add_text(result, punchline_text, text_position, best_font_size, utils.hex_to_rgb(punchline_color), font_path)
    
    max_width = 200
    max_height = 50
    best_font_size, _, _ = utils.find_best_font_size(button_text, max_width, max_height, font_path)
    button_position = (round(target_image_size[0] / 2) - round(target_resize_width_product / 4), 
                       target_image_size[1] - 70)
    result = utils.add_button(result, font_path=font_path, button_position=button_position, 
                              button_color=utils.hex_to_rgb(button_color), text=button_text, font_size=best_font_size)
    
    return result
        