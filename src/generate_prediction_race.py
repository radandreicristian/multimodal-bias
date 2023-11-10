from prediction.predict_race import RacePrediction
from numpy import save, asarray

if __name__ == "__main__":
    race_predicted = RacePrediction().predict()
    save("image_data.npy", asarray(race_predicted))