# Time     : 2024/2/11 9:31
# Project  : Importance Assessment.py
# FileName : 瀑布图.py
# Author   : ZXB

import glob
import os
import pickle

import cv2
import numpy as np
import shap
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

concentration = ['10^4', '10^5', '10^6', 'all']


def read_img(path, c):  # path: M_data
    cate = [os.path.join(path, x) for x in os.listdir(path)]  # cate: [path/类型1,path/类型2...]
    imgs = []
    labels = []
    if c == 'all':
        image_name = f"/*.tif"
    else:
        image_name = f"/*{c}*.tif"

    for idx, folder in enumerate(cate):  # folder: 类型1, 类型2, ...

        for im in glob.glob(folder + image_name):  # im: xxxx.tif 命名的图片
            # print('reading the images:%s' % (im))
            img = cv2.imread(im, cv2.IMREAD_UNCHANGED)
            imgs.append(img)
            labels.append(idx)
    return imgs, labels


def trans_to_oneline(img):
    # hist_list = []
    # for i in range(3):
    #     hist = cv2.calcHist([img], [i], None, [256], [0, 255])
    #     hist_225 = hist[:225, ]
    #     hist_list.append(hist_225.ravel().astype(np.uint16))
    # return np.hstack(hist_list)
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # hist_225 = hist[:225, ]
    return hist.ravel()


def trans_oneline(img):
    hist_list = []
    for index in range(3):
        hist = img[index].ravel()
        hist_list.append(hist.astype(np.uint16))
    return np.hstack(hist_list)


if __name__ == "__main__":

    img_dir = f"D:/new_data/test_1/image_RF_FJ_1_0125"

    for i in concentration:
        X_train_i, y_train_i = read_img(img_dir + '/' + "X_train", i)
        X_test_i, y_test_i = read_img(img_dir + '/' + "X_test", i)

        label_encoder = LabelEncoder()
        y_train = label_encoder.fit_transform(y_train_i)
        X_train = np.row_stack([trans_to_oneline(img) for img in X_train_i])

        y_test = label_encoder.fit_transform(y_test_i)
        X_test = np.row_stack([trans_to_oneline(img) for img in X_test_i])

        X = np.concatenate((X_train, X_test), axis=0)
        y = np.concatenate((y_train, y_test), axis=0)
        print(X_train.shape)
        print(y_test.shape)

        model_dir = f"model/{i}_model.pkl"
        with open(model_dir, 'rb') as file:
            model_rf = pickle.load(file)

        model_rf.fit(X_train, y_train)

        # 使用SHAP解释模型
        explainer = shap.Explainer(model_rf, X_train)
        shap_values = explainer.shap_values(X_test)

        # 选择要绘制依赖图的特征索引（这里选择第一个特征作为示例）
        feature_index = 225

        # 遍历每个类别的 SHAP 值并绘制依赖图
        for j, shap_values_for_class in enumerate(shap_values):
            plt.figure(figsize=(10, 6))  # 创建新的图表
            shap.dependence_plot(
                feature_index,  # 要展示的特征索引
                shap_values_for_class,  # 当前类别的 SHAP 值
                X_test,  # 测试数据集
                interaction_index=None,  # 可以指定交互作用的特征索引，这里我们不指定
                title=f'Dependence for feature {feature_index} and class {i}'  # 设置图表标题
            )
            plt.show()

