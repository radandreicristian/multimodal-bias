from prediction.predict_race import RacePredictor
from dataset.load_dataset import DataModule
from numpy import save, asarray

if __name__ == "__main__":
    image_dataset = DataModule().dataset
    race_predictor = RacePredictor(dataset = image_dataset)
    race_prediction = race_predictor()
    save("image_data.npy", asarray(race_prediction))