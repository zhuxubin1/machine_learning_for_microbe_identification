"""
This script is used to generate the data needed to draw ROC curve.
"""
import numpy as np
import pandas as pd

from Utils.io import read_img, load_model
from Utils.names import *

ROOT = "../../../Data/split_Dichotomies_merged/"
MODEL = "./model"
IDENTIFIER = "Dichotomies_single"
PROBABILITY = "./probability"

for organism in ORGANISMS_WITH_BLANK:
    if organism == "xBlank":
        concentrations = ["all"]
    else:
        concentrations = ["10^4", "10^5", "10^6", "all"]
    for concentration in concentrations:
        new_root = f"{ROOT}/{organism}"
        X_test, y_test = read_img(f"{new_root}/test", "Merged", concentration=concentration)
        model = load_model(f"{MODEL}/{IDENTIFIER}_{organism}_{concentration}.pkl")
        proba: np.ndarray = model.predict_proba(X_test)
        result = np.hstack((y_test.reshape(-1, 1), proba[:, 0].reshape(-1, 1)))
        df = pd.DataFrame(result)
        df.iloc[:, 0] = df.iloc[:, 0].astype(np.uint8)
        df.to_csv(f"{PROBABILITY}/{IDENTIFIER}_{organism}_{concentration}.csv", index=False, header=False)
