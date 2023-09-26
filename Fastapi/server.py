from fastapi import FastAPI, UploadFile, File
from fastapi.encoders import jsonable_encoder
import tensorflow as tf
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = tf.keras.models.load_model("gfgModel.h5")
classname = ["Early Blight", "Late Blight", "Healthy"]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    # Check if the image has 4 channels (RGBA) and convert it to 3 channels (RGB)
    if image.shape[-1] == 4:
        image = image[:, :, :3]
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    img = read_file_as_image(await file.read())

    img = cv2.resize(img, (256, 256))
    img = np.array(img)
    img = np.expand_dims(img, 0)
    prediction = model.predict(img)

    max_index = np.argmax(prediction[0])
    confidence = float(np.max(prediction[0]))  # Convert to native Python float

    result = classname[max_index]
    response_content = {
        "class": result,
        "confidence": confidence
    }

    # Convert response_content to a JSON-serializable format
    json_response = jsonable_encoder(response_content)
    return json_response
