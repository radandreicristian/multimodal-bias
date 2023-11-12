from PIL import Image, UnidentifiedImageError
import requests
import numpy as np
from deepface import DeepFace
from torch.utils.data import Dataset
from typing import Optional, Any, Dict
class RacePredictor():
    def __init__(self,
                 dataset: Optional[Dataset]):
        race_predicted = []
        for idx in range(len(dataset)):
            try:
                image = Image.open(requests.get(dataset.url[idx], stream=True).raw)
                img_array = np.array(image)
                
                ## DeepFace.analyze finds all faces in the image and predicts the race of each one
                predictions = DeepFace.analyze(img_array, actions="race")
                ratio_face_image = predictions[0]['region']['w'] * predictions[0]['region']['h'] / (image.height * image.width) * 100
                 ## We only want images with one face, and the face should cover between 10% and 25% of the image
                if(len(predictions) == 1 and ratio_face_image >= 10 and ratio_face_image <= 25):
                    race_predicted.append({
                        "id": dataset.ids[idx],
                        "text": dataset.text[idx],
                        "image": img_array,
                        "race": predictions[0]['dominant_race'],
                    })
            ## UnidentifiedImageError is raised in case the url is no longer available
            ## ValueError is raised in case the analyze function did not find any face
            except (UnidentifiedImageError, ConnectionError, ValueError) as exception:
                print(str(exception))
        
        return race_predicted