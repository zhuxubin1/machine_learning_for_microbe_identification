import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

root = "../wave_length_data"
target = "SMA_5_106.txt"
for txt in os.listdir("precise"):
    if txt != target:
        continue
    txtFile = os.path.join("precise", txt)
    # 峰值
    datas = pd.read_table(txtFile, header=None)
    # 原始数据
    df = pd.read_excel(os.path.join(root, txt.removesuffix(".txt") + ".xlsx"), header=None)

    fig, ax = plt.subplots(8, 8, figsize=(20, 20))

    for index, row in df.iterrows():
        peak = datas.iloc[index, 1]
        i = index // 8
        j = index % 8
        ax[i, j].plot(row)
        ax[i, j].plot(peak, row[peak], "x", color="red")
        ax[i, j].set_xticks([])
        ax[i, j].set_yticks([])
    plt.show()
