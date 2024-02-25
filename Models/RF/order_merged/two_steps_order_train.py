from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

from Utils.io import read_img, save_model

# concentration: ['10^4', '10^5', '10^6', 'all']
concentration = 'all'

ROOT = "../../../Data/split_by_order"
TABLE = "./table"
MODEL = "./model"
IMAGE = "./image"
IDENTIFIER = "order_merged"

if __name__ == "__main__":
    # read images and labels from filesv
    X_train, y_train = read_img(f"{ROOT}/train", "Merged", concentration)
    X_test, y_test = read_img(f"{ROOT}/test", "Merged", concentration)
    print(X_train.shape)
    print(y_test.shape)

    # Build model and train
    # param_test = {"criterion": ['gini', 'entropy']}
    # param_test = {"max_depth": range(5, 32, 1)}
    # param_test = {"max_features": range(282, 342, 1)}
    # param_test = {"max_leaf_nodes": range(52,71, 1)}
    param_test = {"n_estimators": range(122, 141, 1)}
    grid = GridSearchCV(estimator=RandomForestClassifier(criterion='gini', max_depth=19, max_features=325,
                                                         max_leaf_nodes=53, n_estimators=122,
                                                         random_state=100, oob_score=True),
                        param_grid=param_test, cv=10, verbose=3, n_jobs=-1)  # 调参代码
    grid.fit(X_train, y_train)
    print(grid.cv_results_)
    print(grid.best_params_)
    best_model = grid.best_estimator_
    save_model(best_model, f"{MODEL}/{IDENTIFIER}_{concentration}.pkl")

    y_pred_rf = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred_rf)
    print(f"accuracy: {accuracy:.2%}")
