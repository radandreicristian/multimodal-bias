from prediction.predict_race import RacePredictor
from dataset.load_dataset import DataModule
from numpy import save, asarray

if __name__ == "__main__":
    image_dataset = DataModule().dataset
    race_predictor = RacePredictor(dataset = image_dataset)
    save("image_data.npy", asarray(race_predictor))