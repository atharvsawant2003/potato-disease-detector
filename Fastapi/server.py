from flask import Flask, request, jsonify,session
from flask_cors import CORS  # Import the CORS extension
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import os
import psycopg2
from dotenv import load_dotenv

CREATE_ROOMS_TABLE = (
    "CREATE TABLE IF NOT EXISTS userinfo (id SERIAL PRIMARY KEY, Username TEXT UNIQUE,Email Text,Password TEXT);"
)



INSERT_User = (
    "INSERT INTO userinfo ( Username, Email,Password) VALUES ( %s, %s,%s);"
)

Check_User=("SELECT * FROM userinfo WHERE Username LIKE %s AND Password LIKE %s ")


url="postgres://zaieepvh:VDMHqTBNiwi_wxmqfHvZKwrYMjBtsMPD@rain.db.elephantsql.com/zaieepvh"

connection=psycopg2.connect(url)

with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE)  

app = Flask(__name__)
CORS(app)  # This enables CORS for the entire Flask application
app.secret_key = os.urandom(24)

@app.post("/signup")
def signup():
    data = request.get_json()
    username = data["username"]
    password=data["password"]
    email=data["email"]
    with connection:
      with connection.cursor() as cursor:
        cursor.execute(INSERT_User,(username,email,password))
        # cursor.execute(Check_User,(username,pass))
        # users=cursor.fetchall()
        # # print(users)
        # session['user_id']=users[0][0]
        
    return {"message":f"New user is registered named {username}"},201


@app.post("/login")
def login():
    data = request.get_json()
    username = data["username"]
    password=data["password"]
    with connection:
      with connection.cursor() as cursor:
        cursor.execute(Check_User,(username,password))
        users=cursor.fetchall()
        
        # print(users[0][0])
        
        if(len(users)>0):
            session['user_id']=users[0][0]
        
            return {"message":f"Your are Sucessfully login"}
        else:
            return {"message":"please login again wrong info"}


model = tf.keras.models.load_model("gfgModel.h5")
classname = ["Early Blight", "Late Blight", "Healthy"]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    if image.shape[-1] == 4:
        image = image[:, :, :3]
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    img = read_file_as_image(file.read())
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

    return jsonify(response_content)

if __name__ == '__main__':
    app.run()
