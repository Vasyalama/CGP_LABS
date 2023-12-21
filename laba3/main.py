import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QWidget, QGroupBox, QFormLayout, QLineEdit, QWidget, QSizePolicy, QGridLayout
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import cv2
import numpy as np
from scipy.ndimage import minimum_filter, maximum_filter

class ImageProcessor(QWidget):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.image_label.setScaledContents(True)


        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)

        
    

        self.sharpen_button = QPushButton("Apply High-Pass Filter", self)
        self.sharpen_button.clicked.connect(self.apply_high_pass_filter)


        self.niblack_button = QPushButton("Apply Niblack Binarization", self)
        self.niblack_button.clicked.connect(self.apply_niblack_binarization)

        self.adaptiveThresh_button = QPushButton("Apply Adaptive Threshold", self)
        self.adaptiveThresh_button.clicked.connect(self.apply_adaptive_threshold)


        self.reset_button = QPushButton("Reset Image", self)
        self.reset_button.clicked.connect(self.reset_image)


        self.bernsen_group_box = QGroupBox("Bernsen Parameters", self)
        self.bernsen_group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grid_layout = QGridLayout()

        self.half_size_label = QLabel("Half-Size")
        self.contrast_threshold_label = QLabel("Contrast Threshold")

        self.half_size_edit = QLineEdit(self)
        self.contrast_threshold_edit = QLineEdit(self)

        self.apply_custom_bernsen_button = QPushButton("Apply Bernsen Binarization", self)
        self.apply_custom_bernsen_button.clicked.connect(self.apply_custom_bernsen_binarization)

        grid_layout.addWidget(self.half_size_label, 0, 0)
        grid_layout.addWidget(self.contrast_threshold_label, 1, 0)
        grid_layout.addWidget(self.half_size_edit, 0, 1)
        grid_layout.addWidget(self.contrast_threshold_edit, 1, 1)
        grid_layout.addWidget(self.apply_custom_bernsen_button, 0, 2, 2, 1)
        self.bernsen_group_box.setLayout(grid_layout)

        # self.bernsen_layout = QFormLayout(self.bernsen_group_box)
        # self.bernsen_layout.addRow("Half Size:", self.half_size_edit)
        # self.bernsen_layout.addRow("Contrast Threshold:", self.contrast_threshold_edit)
        # self.bernsen_layout.addWidget(self.apply_custom_bernsen_button)

        self.layout = QGridLayout(self)
        
        self.layout.addWidget(self.load_button, 0, 0)
        self.layout.addWidget(self.reset_button, 0, 1)
        self.layout.addWidget(self.sharpen_button, 1, 0, 1, 2)
        self.layout.addWidget(self.bernsen_group_box, 2, 0, 1, 2)
        self.layout.addWidget(self.niblack_button, 3, 0, 1, 2)
        self.layout.addWidget(self.adaptiveThresh_button, 4, 0, 1, 2)        
        self.layout.addWidget(self.image_label, 5, 0, 1, 2)

        # self.layout.setRowStretch(0,0)
        # self.layout.setRowStretch(1,0)
        # self.layout.setRowStretch(2,0)
        # self.layout.setRowStretch(3,0)
        # self.layout.setRowStretch(4,0)
        

        # self.central_widget = QWidget(self)
        # self.central_widget.setLayout(self.layout)

        self.loaded_image = None
        self.original_image = None

    def load_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.loaded_image = cv2.imread(file_path)
            self.original_image = self.loaded_image.copy()
            self.display_image()

    def display_image(self):
        if self.loaded_image is not None:
            height, width, channel = self.loaded_image.shape
            bytes_per_line = 3 * width

            q_image = QImage(self.loaded_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            q_image = q_image.rgbSwapped()

            pixmap = QPixmap.fromImage(q_image)
            if (width > height):
                pixmap = pixmap.scaledToWidth(int(self.image_label.width()))
            else:
                pixmap = pixmap.scaledToHeight(int(self.image_label.height()))
            self.image_label.setPixmap(pixmap)

    def apply_high_pass_filter(self):
        if self.loaded_image is not None:
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
            sharpened_image = cv2.filter2D(self.loaded_image, -1, kernel)
            self.loaded_image = sharpened_image
            self.display_image()


    def bernsen(image, window=(15, 15), contrast_threshold=15):

        image = image.astype(float)

        kernel = np.ones(window, np.uint8)
        max_values = cv2.dilate(image, kernel)
        min_values = cv2.erode(image, kernel)
        
        local_threshold = (max_values + min_values)/2
        local_difference = max_values - min_values

        mask = local_difference < contrast_threshold

        
        output = np.zeros_like(image)
        output[mask] = 1
        output[image > local_threshold - 7]  = 1


        mean = cv2.boxFilter(image, -1, ksize=window, normalize=True)
        # print(mean)

        # local_contrast = cv2.dilate(image, np.ones(window)) - cv2.erode(image, np.ones(window))
        # print(local_contrast)
        # mask = local_contrast < contrast_threshold
        # print(mask)
        # output = np.zeros_like(image)
        # print(output)
        # output[np.logical_and(mask, image >= local_contrast)] = 1

        # print(output)
        # output[~mask] = (image[~mask] >= mean[~mask])
        # print(output)
        return output


    def apply_custom_bernsen_binarization(self):
        if self.loaded_image is not None:

            half_size = int(self.half_size_edit.text())
            contrast_threshold_user = int(self.contrast_threshold_edit.text())

            
            gray_image = cv2.cvtColor(self.loaded_image, cv2.COLOR_BGR2GRAY)
            output = ImageProcessor.bernsen(gray_image, window = (half_size, half_size), contrast_threshold = contrast_threshold_user)
            output_image = (output * 255).astype(np.uint8)
            self.loaded_image = cv2.cvtColor(output_image, cv2.COLOR_GRAY2BGR)
            self.display_image()
 
    def apply_niblack_binarization(self):
        window_size=15
        k=-0.2
        gray_image = cv2.cvtColor(self.loaded_image, cv2.COLOR_BGR2GRAY)
        gray_image_array = gray_image.astype(float)

        mean_image = cv2.boxFilter(gray_image_array, -1, ksize=(window_size, window_size))
        mean = mean_image.astype(float)

        meanSquare = cv2.boxFilter(gray_image_array*gray_image_array, -1, ksize=(window_size, window_size))
        deviation = (meanSquare - mean*mean)**0.5

        output = np.zeros_like(gray_image_array)

        output[gray_image_array > mean + k * deviation - 7] = 1

        # for y in range(self.loaded_image.shape[0]):
        #     for x in range(self.loaded_image.shape[1]):
        #         neighborhood_y_start = max(0, y - half)
        #         neighborhood_y_end = min(gray_image.shape[0] - 1, y + half)
        #         neighborhood_x_start = max(0, x - half)
        #         neighborhood_x_end = min(gray_image.shape[1] - 1, x + half)

        #         neighborhood = gray_image[neighborhood_y_start:neighborhood_y_end + 1, neighborhood_x_start:neighborhood_x_end + 1]

        #         mean_intensity = np.mean(neighborhood)
        #         stddev_intensity = np.std(neighborhood)

        #         threshold = mean_intensity + k * stddev_intensity

        #         binary_image[y, x] = 255 if gray_image[y, x] > threshold else 0
        output_image = (output * 255).astype(np.uint8)
        self.loaded_image = cv2.cvtColor(output_image, cv2.COLOR_GRAY2BGR)
        self.display_image()

    def reset_image(self):
        if self.original_image is not None:
            self.loaded_image = self.original_image.copy()
            self.display_image()
    
    def apply_adaptive_threshold(self):
        if self.loaded_image is not None:
            gray_image = cv2.cvtColor(self.loaded_image, cv2.COLOR_BGR2GRAY)
            
            binary_image = cv2.adaptiveThreshold(
                gray_image, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                31,  
                10  
            )

            self.loaded_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
            self.display_image()

    def resizeEvent(self, event):
        self.display_image()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.layout = QHBoxLayout(self)
        for i in range(2):
            imageProcessor = ImageProcessor()
            self.layout.addWidget(imageProcessor)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        
        

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Image Processor")
    window.setGeometry(0, 0, 1000, 500)
    window.show()
    sys.exit(app.exec())
