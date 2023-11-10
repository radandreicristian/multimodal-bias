from dataset.load_dataset import TrainDataModule
from PIL import Image, UnidentifiedImageError
import requests
import numpy as np
from deepface import DeepFace
from typing import Any, Dict

class RacePrediction():
    def __init__(self):
        self.train_dataset = TrainDataModule().train_dataset

    def predict(self):
        race_predicted = []
        for idx in range(len(self.train_dataset)):
            try:
                image = Image.open(requests.get(self.train_dataset.url[idx], stream=True).raw)
                img_array = np.array(image)
                
                ## DeepFace.analyze finds all faces in the image and predicts the race of each one
                predictions = DeepFace.analyze(img_array, actions="race")
                ratio_face_image = predictions[0]['region']['w'] * predictions[0]['region']['h'] / (image.height * image.width) * 100
                 ## We only want images with one face, and the face should cover between 10% and 25% of the image
                if(len(predictions) == 1 and ratio_face_image >= 10 and ratio_face_image <= 25):
                    race_predicted.append({
                        "id": self.train_dataset.ids[idx],
                        "text": self.train_dataset.text[idx],
                        "image": img_array,
                        "race": predictions[0]['dominant_race'],
                    })
            ## UnidentifiedImageError is raised in case the url is no longer available
            ## ValueError is raised in case the analyze function did not find any face
            except (UnidentifiedImageError, ConnectionError, ValueError):
                pass
        
        return race_predicted