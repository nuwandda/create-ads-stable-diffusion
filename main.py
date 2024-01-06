import streamlit as st
from PIL import Image
import streamlit_services


def main():
    st.title("Welcome to AdCreative Demo App")

    # Upload images
    encoded_base_img = st.file_uploader("Upload Reference Image", type=["jpg", "jpeg", "png"])
    logo = st.file_uploader("Upload Logo (Transparent)", type=["png"])

    # Text input fields
    prompt = st.text_input("Prompt", "Enter text here")
    hex_color = st.text_input("HEX Color", "Enter text here")
    punchline_text = st.text_input("Punchline Text", "Enter text here")
    button_text = st.text_input("Button Text", "Enter text here")
    punchline_color = st.text_input("Punchline Color", "Enter text here")
    button_color = st.text_input("Button Color", "Enter text here")

    # Generate image
    if st.button("Generate"):
        if encoded_base_img is not None and logo is not None:
            init_image = Image.open(encoded_base_img)
            logo_image = Image.open(logo)
            result = streamlit_services.create_ad(init_image, logo_image, hex_color, prompt, punchline_text,
                                                  punchline_color, button_text, button_color)
            st.image(result, caption="Generated Ad", use_column_width=True)


if __name__ == "__main__":
    main()
