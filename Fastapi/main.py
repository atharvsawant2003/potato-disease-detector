from fastapi import FastAPI
from enum import Enum
import tensorflow 
import numpy as np
import keras
import cv2
from fastapi import  File, UploadFile

app=FastAPI()

model = tensorflow.keras.models.load_model("gfgModel.h5")
classname=["Early Blight","Late Blight","Healthy"]

img = cv2.imread('healthy.png')
print(img.shape)
img = cv2.resize(img, (256, 256))

img=np.array(img)
img=np.expand_dims(img,0)

arr=model.predict(img)

arr = np.array(arr)

# Find the index of the maximum value
max_index = np.argmax(arr)

result=classname[max_index]
print(result)
# class availabelecusines(str,Enum):
#      indian="indian"
#      pakistan="pakistan"

# food_items={
#   "indian":["vadapav","bhel"],
#   "pakistan":["no food","kimma"]
# }





# @app.get("/get_item/{name}")
# async def Hello(name:availabelecusines):
#     return food_items.get(name)
  
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# return f"welcome{name}"