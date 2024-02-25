import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

from Utils.display import scatter, confusionPainting
from Utils.evaluate import model_metrics
from Utils.io import save_model, read_img, insert_into_table
from Utils.names import *

ROOT = "../../../Data"
TABLE = "./table"
MODEL = "./model"
IMAGE = "./image"
SCATTER = "./scatter"
VARIANCE = "./variance"
IDENTIFIER = "order_merged"

if __name__ == "__main__":
    for order in ["Bacillales", "Enterobacteriales"]:
        for concentration in ["10^6", "10^5", "10^4", "all"]:
            # read images and labels from files
            X_train, y_train = read_img(f"{ROOT}/split_in_{order}/train", "Merged", concentration)
            X_test, y_test = read_img(f"{ROOT}/split_in_{order}/test", "Merged", concentration)
            labels = os.listdir(f"{ROOT}/train")
            if concentration != "all":
                labels.remove("xBlank")
            labels = [name_to_abbr.get(x, x) for x in labels]
            print("X_train:", X_train.shape, "\n" + "X_test:", X_test.shape)

            # Build model and train
            model = Pipeline([
                ("pca", PCA(n_components=50)),
                ("lda", LinearDiscriminantAnalysis(n_components=2))
            ])
            model.fit(X_train, y_train)
            save_model(model, f"{MODEL}/{IDENTIFIER}_{order}_{concentration}.pkl")

            # confusion matrix
            y_pred = model.predict(X_test)
            confusionPainting(y_pred, y_test, labels, plt.cm.Reds,
                              output=f"{IMAGE}/{IDENTIFIER}_{order}_{concentration}.png")

            # LDA scatter
            X = np.concatenate((X_train, X_test))
            y = np.concatenate((y_train, y_test))
            X = model.transform(X)
            scatter(y, X, output=f"{SCATTER}/{IDENTIFIER}_{order}_{concentration}.csv")

            # LDA variance
            with open(f"{VARIANCE}/{IDENTIFIER}_{order}.txt", "a") as f:
                v = model.named_steps["lda"].explained_variance_ratio_
                f.write(f"{IDENTIFIER}_{order}_{concentration}\t{v[0]}\t{v[1]}\n")

            # model metrics
            Accuracy, Recall, F1_score, Precision = model_metrics(y_test, y_pred)
            cv = StratifiedKFold(n_splits=30)
            scores = cross_val_score(model, X_test, y_test, scoring='accuracy', n_jobs=-1, cv=cv)
            data = [3, 3, concentration, Accuracy, Recall, F1_score, Precision] + list(scores)
            insert_into_table(data, f"{TABLE}/{IDENTIFIER}_{order}_Accuracy.xlsx")