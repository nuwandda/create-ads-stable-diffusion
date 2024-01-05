from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import fastapi as _fapi

import schemas as _schemas
import services as _services
import io

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to AdCreative API"}


# Endpoint to test the backend
@app.get("/api")
async def root():
    return {"message": "Welcome to AdCreative API"}


@app.post("/api/generate-image/")
async def generate_image(imgPromptCreate: _schemas.ImageCreate = _fapi.Depends()):
    
    image = await _services.generate_image(imgPrompt=imgPromptCreate)

    memory_stream = io.BytesIO()
    image.save(memory_stream, format="PNG")
    memory_stream.seek(0)
    return StreamingResponse(memory_stream, media_type="image/png")


@app.post("/api/add_elements")
async def generate_image(addElements: _schemas.AddElements = _fapi.Depends()):
    
    image = await _services.add_elements(addElements=addElements)

    memory_stream = io.BytesIO()
    image.save(memory_stream, format="PNG")
    memory_stream.seek(0)
    return StreamingResponse(memory_stream, media_type="image/png")


@app.post("/api/create_ad")
async def generate_image(adCreate: _schemas.CreateAd = _fapi.Depends()):
    
    image = await _services.create_ad(adPrompt=adCreate)

    memory_stream = io.BytesIO()
    image.save(memory_stream, format="PNG")
    memory_stream.seek(0)
    return StreamingResponse(memory_stream, media_type="image/png")
