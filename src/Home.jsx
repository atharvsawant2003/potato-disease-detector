import React, { useState } from 'react';
import axios from 'axios';
import  

function ImageUploader() {
  const [selectedImage, setSelectedImage] = useState(null);
  const[result,setresult]=useState("");
  const[confi,setconfi]=useState("");
  const [imagePreview, setImagePreview] = useState("");

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
    if (file) {
      setSelectedImage(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      alert('Please select an image first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
     
      console.log('Image uploaded successfully:', response.data); 
      setresult(response.data.class)
      setconfi(response.data.confidence)

    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div>
      <h2>Image Uploader</h2>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      <button onClick={handleUpload}>Upload Image</button>

      {selectedImage && (
        <div>
          <h3>Preview:</h3>
          <img src={imagePreview} alt="Selected" width="200" />
        </div>
      )}
      <div id='result'>Disease:{result}<br/>
                        Confidence:{confi}</div>
    </div>
  );
}

export default ImageUploader;
