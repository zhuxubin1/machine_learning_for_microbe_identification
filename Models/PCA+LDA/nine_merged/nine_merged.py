import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import KernelPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline

from Utils.display import confusionPainting, scatter
from Utils.evaluate import model_metrics
from Utils.io import save_model, read_img, insert_into_table
from Utils.names import *

ROOT = "../../../Data/three_channel_combine"
TABLE = "./table"
MODEL = "./model"
IMAGE = "./image"
SCATTER = "./scatter"
VARIANCE = "./variance"
IDENTIFIER = "nine_merged"

if __name__ == "__main__":
    for concentration in ["10^4", "10^5", "10^6", "all"]:
        # read images and labels from filesv
        labels = ORGANISMS if concentration != "all" else ORGANISMS_WITH_BLANK
        labels = [name_to_abbr.get(x, x) for x in labels]

        X_train, y_train = read_img(f"{ROOT}/train", "Merged", concentration=concentration)
        X_test, y_test = read_img(f"{ROOT}/test", "Merged", concentration=concentration)
        print("X_train:", X_train.shape, "\n" + "X_test:", X_test.shape)

        # Build model and train
        pipeline = Pipeline([
            ("pca", KernelPCA(n_components=180)),
            ("lda", LinearDiscriminantAnalysis(n_components=2))
        ])
        param_grid = {
            'pca__n_components': range(180, 181, 1),
            'lda__solver': ['svd', 'eigen']
        }
        grid = GridSearchCV(pipeline, param_grid=param_grid, cv=10, n_jobs=-1, verbose=3)
        grid.fit(X_train, y_train)
        best_model = grid.best_estimator_
        save_model(best_model, f"{MODEL}/{IDENTIFIER}_{concentration}.pkl")

        # confusion matrix
        y_pred = best_model.predict(X_test)
        confusionPainting(y_pred, y_test, labels, plt.cm.Reds, output=f"{IMAGE}/{IDENTIFIER}_{concentration}.png")

        # LDA scatter
        X = np.concatenate((X_train, X_test))
        y = np.concatenate((y_train, y_test))
        X = best_model.transform(X)
        scatter(y, X, output=f"{SCATTER}/{IDENTIFIER}_{concentration}.csv")

        # LDA variance
        with open(f"{VARIANCE}/{IDENTIFIER}.txt", "a") as f:
            v = best_model.named_steps["lda"].explained_variance_ratio_
            f.write(f"{IDENTIFIER}_{concentration}\t{v[0]}\t{v[1]}\n")

        # model metrics
        Accuracy_score, Recall, F1_score, Precision_score = model_metrics(y_test, y_pred)
        cv = StratifiedKFold(n_splits=30)
        scores = cross_val_score(best_model, X_test, y_test, scoring='accuracy', n_jobs=-1, cv=cv)
        data = [3, 3, concentration, Accuracy_score, Recall, F1_score, Precision_score] + list(scores)
        insert_into_table(data, f"{TABLE}/{IDENTIFIER}_Accuracy.xlsx")
