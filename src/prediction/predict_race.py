from PIL import Image, UnidentifiedImageError
import requests
import numpy as np
from deepface import DeepFace
from torch.utils.data import Dataset
from typing import Optional
class RacePredictor:
    """A race predictor for images with faces."""

    def __init__(self,
                 dataset: Optional[Dataset]):
        """Initialize the predictor."""
        self.dataset = dataset

    def __call__(self):
        """Identifies the images with one face and predicts the race of the person."""
        race_predicted = []
        for idx in range(len(self.dataset)):
            try:
                image = Image.open(requests.get(self.dataset.url[idx], stream=True, timeout=5).raw)
                img_array = np.array(image)
                
                ## DeepFace.analyze finds all faces in the image and predicts the race of each one
                predictions = DeepFace.analyze(img_array, actions="race")
                ratio_face_image = predictions[0]['region']['w'] * predictions[0]['region']['h'] / (image.height * image.width) * 100
                 ## We only want images with one face, and the face should cover between 10% and 25% of the image
                if(len(predictions) == 1 and ratio_face_image >= 10 and ratio_face_image <= 25):
                    race_predicted.append({
                        "id": self.dataset.ids[idx],
                        "text": self.dataset.text[idx],
                        "image": img_array,
                        "race": predictions[0]['dominant_race'],
                    })
            ## UnidentifiedImageError is raised in case the url is no longer available
            ## ValueError is raised in case the analyze function did not find any face
            ## ReadTimeout is raised in case the get operation to read the image timed out
            except (UnidentifiedImageError, requests.ReadTimeout, requests.ConnectionError, ValueError) as exception:
                print(str(exception))
        
        return race_predicted