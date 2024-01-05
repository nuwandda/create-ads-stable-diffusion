import pydantic as _pydantic
from fastapi import UploadFile


class ImageCreate(_pydantic.BaseModel):
    prompt: str
    encoded_base_img: UploadFile
    hex_color: str = '#F8BFD4'
    
    
class AddElements(_pydantic.BaseModel):
    generated_image: UploadFile
    logo: UploadFile
    punchline_text: str
    button_text: str
    punchline_color: str
    button_color: str
    
    
class CreateAd(_pydantic.BaseModel):
    prompt: str
    encoded_base_img: UploadFile
    hex_color: str = '#F8BFD4'
    logo: UploadFile
    punchline_text: str
    button_text: str
    punchline_color: str
    button_color: str
