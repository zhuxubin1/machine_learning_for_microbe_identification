"""
This script is used to demonstrate the result of using different grayscale values as feature extraction thresholds.
"""

import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QApplication, QSlider, QLabel, QVBoxLayout, QComboBox, QHBoxLayout
import pyqtgraph as pg


class Example(QWidget):
    def __init__(self):
        super().__init__()

        # ComboBox on the left
        self.cb_concentration = QComboBox()
        self.cb_concentration.addItems(["10^4", "10^5", "10^6"])
        self.cb_diameter = QComboBox()
        self.cb_diameter.addItems(["5nm", "13nm", "60nm"])
        self.cb_species = QComboBox()
        self.cb_species.addItems(["B.licheniformis", "E.cloacae", "E.coli", "E.faecalis", "L.monocytogenes",
                                  "S.aureus", "S.cerevisiae", "S.enterica", "S.marcescens"])

        self.cb_concentration.currentIndexChanged.connect(self.update_pic)
        self.cb_diameter.currentIndexChanged.connect(self.update_pic)
        self.cb_species.currentIndexChanged.connect(self.update_pic)

        hbox_cb = QHBoxLayout()
        hbox_cb.addWidget(self.cb_concentration)
        hbox_cb.addWidget(self.cb_diameter)
        hbox_cb.addWidget(self.cb_species)

        # Slider on the left
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 255)
        self.slider.setValue(255)
        self.slider.valueChanged.connect(self.thresholdChange)

        hbox_slider = QHBoxLayout()
        hbox_slider.addWidget(QLabel("threshold"))
        hbox_slider.addWidget(QLabel("0"))
        hbox_slider.addWidget(self.slider)
        hbox_slider.addWidget(QLabel("255"))

        # current threshold on the left
        self.label_current = QLabel("current threshold: 255")

        # image on the left
        self.pic = None
        self.pic_copy = None
        self.label_pic = QLabel()

        vbox_left = QVBoxLayout()
        vbox_left.addStretch(1)
        vbox_left.addLayout(hbox_cb)
        vbox_left.addLayout(hbox_slider)
        vbox_left.addWidget(self.label_current)
        vbox_left.addWidget(self.label_pic)
        vbox_left.addStretch(1)

        # line chart on the right
        pg.setConfigOptions(leftButtonPan=False)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.pw = pg.PlotWidget()
        self.plot_data = None

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_left, 1)
        hbox.addWidget(self.pw, 3)

        self.initHistogram()
        self.update_pic()
        self.setLayout(hbox)

    def update_pic(self):
        """
        Update the picture according to the current selection of ComboBox
        """
        concentration = self.cb_concentration.currentText()
        diameter = self.cb_diameter.currentText()
        species = self.cb_species.currentText()
        path = f"data/{species}_{diameter}_{concentration}.tif"

        self.pic = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        self.thresholdChange(self.slider.value())

    def initHistogram(self):
        """
        Initialize the line chart
        """
        self.pw.setLimits(xMin=0, yMin=0, xMax=256)
        hist = cv2.calcHist([self.pic], [0], None, [256], [0, 256]).ravel()
        hist = hist[1: 256]
        self.plot_data = self.pw.plot(hist, fillLevel=0, brush=(0, 0, 255, 80))

    def thresholdChange(self, value):
        """
        Update the picture and histogram when the threshold changes

        Args:
            value: the current threshold
        """

        self.label_current.setText(f"current threshold: {value}")

        self.pic_copy = self.pic.copy()
        self.pic_copy[self.pic_copy > value] = 0
        w, h = self.pic_copy.shape
        pixmap = QPixmap.fromImage(QImage(self.pic_copy, w, h, QImage.Format.Format_Grayscale8))
        self.label_pic.setPixmap(pixmap)

        hist = cv2.calcHist([self.pic_copy], [0], None, [256], [0, 256]).ravel()
        hist = hist[0: value + 1]
        hist[0] = 0
        self.plot_data.setData(hist)
        self.pw.setLimits(xMin=0, yMin=0, xMax=value + 1)


if __name__ == "__main__":
    app = QApplication([])
    ex = Example()
    ex.setWindowTitle("Threshold demonstration")
    ex.showMaximized()
    ex.show()
    app.exec()
