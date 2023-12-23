import sys 
from PySide6.QtWidgets import QApplication, QGroupBox, QMainWindow, QGraphicsScene, QGraphicsView, QSizePolicy, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel, QLineEdit, QPushButton, QGraphicsRectItem, QGraphicsTextItem, QGraphicsEllipseItem
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QWheelEvent, QTransform
import math
class MyGraphicsView(QGraphicsView): 
    def __init__(self): 
        super(MyGraphicsView, self).__init__() 
        self.lines = [] 
        self.pixels = []
        self.circles = []
        self.scene = QGraphicsScene(self) 
        self.setScene(self.scene) 
        self.scale_factor = 2
        self.setRenderHint(QPainter.Antialiasing, True) 
        self.setSceneRect(QRectF(-100, -100, 200, 200)) 
 
        self.draw_axis_and_grid() 
        self.fit_to_view() 
       
 
    def draw_axis_and_grid(self): 

        SIZE_X = (int)(self.width()/2)
        SIZE_Y = (int)(self.height()/2)
        step = (int)(self.scale_factor * 10)
        for i in range(0, SIZE_X, step):
            self.scene.addLine(i, -SIZE_Y, i, SIZE_Y, self.get_pen(Qt.gray)) 
            self.scene.addLine(-i, -SIZE_Y, -i, SIZE_Y, self.get_pen(Qt.gray)) 
        for i in range(0, SIZE_Y, step):
            self.scene.addLine(-SIZE_X, i, SIZE_X, i, self.get_pen(Qt.gray))
            self.scene.addLine(-SIZE_X, -i, SIZE_X, -i, self.get_pen(Qt.gray))

        self.scene.addLine(-SIZE_X, 0, SIZE_X, 0, self.get_pen(Qt.black)) 
        self.scene.addLine(0, -SIZE_Y, 0, SIZE_Y, self.get_pen(Qt.black)) 
         
    def get_pen(self, color): 
        pen = self.scene.addLine(0, 0, 0, 0).pen() 
        pen.setColor(color) 
        return pen 
 
    def fit_to_view(self): 
        self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio) 
 
    def draw_lines(self): 
        for a in self.lines: 
            x1, y1, x2, y2 = a[0], a[1], a[2], a[3] 
            step = (int)(self.scale_factor * 10)
            self.scene.addLine(x1 * step, -y1 * step, x2 * step, -y2 * step, self.get_pen(Qt.blue)) 
    
    def draw_circles(self):
        for circle in self.circles:
            x0, y0, r = circle[0], circle[1], circle[2]
            step = (int)(self.scale_factor * 10)
            circle = QGraphicsEllipseItem(x0 * step - r * step, -(y0 * step + r * step), 2 * r * step, 2 * r * step)
            self.scene.addItem(circle)


    def put_pixel(self, X, Y):
        x = (int)(self.scale_factor * 10) * X
        y = (int)(self.scale_factor * 10) * Y
        rect_item = QGraphicsRectItem(x, -y, (int)(self.scale_factor * 10), (int)(self.scale_factor * 10))
        rect_item.setBrush(Qt.gray)  
        self.scene.addItem(rect_item)

    def raw_to_1_octant(self, line):
        x1, y1, x2, y2 = line[0], line[1], line[2], line[3]
        if ((x2 > x1 and y2 < y1) or (x2 < x1 and y2 < y1)):
            x1, x2, y1, y2 = x2, x1, y2, y1               
        x2_centered, y2_centered = x2 - x1, y2 - y1
        dx = x1
        dy = y1
        slope = (y2 - y1)/ (x2 - x1)
        octant = 1
        if (slope > 1):
            x2_new = y2_centered
            y2_new = x2_centered
            octant = 2
        elif(slope <= -1):
            x2_new = y2_centered
            y2_new = -x2_centered
            octant = 3
        elif(slope > -1 and slope < 0):
            x2_new = -x2_centered
            y2_new = y2_centered
            octant = 4
        else:
            y2_new, x2_new = y2_centered, x2_centered
            
        slope = y2_new/ x2_new
        return slope, x2_new, y2_new, octant, dy, dx

    def get_coordinates(self, octant, x, y):
        if (octant == 1):
            return x, int(y) + 1
        if (octant == 2):
           return int(y), x + 1
        if (octant == 3):
            return -(int(y) + 1), x + 1
        if (octant == 4):
            return -x - 1, int(y) + 1

    def draw_slope_method(self):
        for line in self.lines:
            slope, x2_new, y2_new, octant, dy, dx = self.raw_to_1_octant(line)
          
            for x in range(0, (int)(x2_new) + 1):
                y = int(slope * x)
                X,Y = self.get_coordinates(octant, x, y)
                X += dx
                Y += dy
                self.put_pixel(X,Y)
                pixel = [X,Y]
                self.pixels.append(pixel)
        self.draw_lines()
    
    def draw_dda_method(self):
        for line in self.lines:
            slope, x2_new, y2_new, octant, dy, dx = self.raw_to_1_octant(line)
            y = 0
            for x in range(0, (int)(x2_new) + 1):                
                X,Y = self.get_coordinates(octant, x, y)
                X += dx
                Y += dy
                self.put_pixel(X,Y)
                raster = [X,Y]
                self.pixels.append(raster)
                y += slope
        self.draw_lines()
    
    def draw_bresenhem_method(self):
        for line in self.lines:
            slope, x2_new, y2_new, octant, dy, dx = self.raw_to_1_octant(line)
            y = 0
            x = 0
            Dx = x2_new
            Dy = y2_new
            E = Dy/Dx - 0.5

            X,Y = self.get_coordinates(octant, x, y)
            X += dx
            Y += dy
                
            self.put_pixel(X,Y)
            raster = [X,Y]
            self.pixels.append(raster)
            
            for x in range(1, (int)(x2_new) + 1):
                if (E >= 0):
                    y += 1
                    E += Dy/Dx - 1
                else:
                    E += Dy/Dx

                X,Y = self.get_coordinates(octant, x, y)
                X += dx
                Y += dy

                self.put_pixel(X,Y)
                raster = [X,Y]
                self.pixels.append(raster)
        self.draw_lines()

    def circle_bresenhem_method(self):
        for circle in self.circles:
            x0, y0, r = circle[0], circle[1], circle[2]
            x = 0
            y = r
            E = 3 - 2 * r
            self.put_pixel(x + x0, y + 1 + y0)
            self.put_pixel(x + x0, -y + y0)
            self.put_pixel(y + x0, x + 1 + y0)
            self.put_pixel(y + x0, -x + y0)
            self.put_pixel(-x - 1 + x0, y + 1 + y0)
            self.put_pixel(-y - 1 + x0, x + 1 + y0)
            self.put_pixel(-y - 1 + x0, -x + y0)
            self.put_pixel(-x - 1 + x0, -y + y0)
        
            self.pixels.append([x + x0, y + 1 + y0])
            self.pixels.append([x + x0, -y + y0])
            self.pixels.append([y + x0, x + 1 + y0])
            self.pixels.append([y + x0, -x + y0])
            self.pixels.append([-x - 1 + x0, y + 1 + y0])
            self.pixels.append([-y - 1 + x0, x + 1 + y0])
            self.pixels.append([-y - 1 + x0, -x + y0])
            self.pixels.append([-x - 1 + x0, -y + y0])

            while (x < y):
                if (E >= 0):
                    E += 4 * (x - y) + 10
                    x += 1
                    y -= 1
                else:
                    E += 4 * x + 6
                    x += 1
                self.put_pixel(x + x0, y + 1 + y0)
                self.put_pixel(x + x0, -y + y0)
                self.put_pixel(y + x0, x + 1 + y0)
                self.put_pixel(y + x0, -x + y0)
                self.put_pixel(-x - 1 + x0, y + 1 + y0)
                self.put_pixel(-y - 1 + x0, x + 1 + y0)
                self.put_pixel(-y - 1 + x0, -x + y0)
                self.put_pixel(-x - 1 + x0, -y + y0)

                self.pixels.append([x + x0, y + 1 + y0])
                self.pixels.append([x + x0, -y + y0])
                self.pixels.append([y + x0, x + 1 + y0])
                self.pixels.append([y + x0, -x + y0])
                self.pixels.append([-x - 1 + x0, y + 1 + y0])
                self.pixels.append([-y - 1 + x0, x + 1 + y0])
                self.pixels.append([-y - 1 + x0, -x + y0])
                self.pixels.append([-x - 1 + x0, -y + y0])

    def draw_rasters(self):
        for pixel in self.pixels:
            x,y = pixel[0], pixel[1]
            self.put_pixel(x,y)
            # X = (int)(self.scale_factor * 10) * x
            # Y = (int)(self.scale_factor * 10) * y
            # rect_item = QGraphicsRectItem(X, -Y, (int)(self.scale_factor * 10), (int)(self.scale_factor * 10))
            # rect_item.setBrush(Qt.gray) 
            # self.scene.addItem(rect_item)

            
    def resizeEvent(self, event): 
        super(MyGraphicsView, self).resizeEvent(event) 
        rect = QRectF(-100, -100, 200, 200) 
        self.setSceneRect(rect) 
        self.scene.clear() 
        self.draw_axis_and_grid() 
        self.draw_rasters()
        self.draw_lines()
        self.draw_circles()
        self.fit_to_view() 
 
    def wheelEvent(self, event: QWheelEvent): 
        factor = 1.2 
        if event.angleDelta().y() > 0: 
            self.scale_factor *= factor
        else: 
            self.scale_factor /= factor
        self.scene.clear() 
        self.draw_axis_and_grid() 
        self.draw_rasters()
        self.draw_lines()
        self.draw_circles()

    def delete_All(self):
        self.scene.clear() 
        self.draw_axis_and_grid() 
        self.lines.clear()
        self.pixels.clear()
        self.circles.clear()

 
class MyMainWindow(QMainWindow): 
    def __init__(self): 
        super(MyMainWindow, self).__init__() 
        self.lines = [] 
        self.init_ui() 
 
    def init_ui(self): 
        main_widget = QWidget(self) 
        self.setCentralWidget(main_widget) 
 
        layout = QHBoxLayout(main_widget) 
 
        self.graphics_view = MyGraphicsView() 
        layout.addWidget(self.graphics_view, 2) 
 
        input_widget = QWidget(self) 
        layout.addWidget(input_widget, 1) 
        input_layout = QVBoxLayout(input_widget) 

        segment_group_box = QGroupBox("Segment Parameters")
        segment_group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        segment_grid_layout = QGridLayout()
        segment_labels = ['X1:', 'Y1:', 'X2:', 'Y2:']
        circle_labels = ['X0', 'Y0', 'R']
        self.segment_line_edits = [QLineEdit() for _ in range(4)] 
        self.circle_line_edits = [QLineEdit() for _ in range(3)] 
        i, j = 0, 0
        for label, line_edit in zip(segment_labels, self.segment_line_edits):         
            segment_grid_layout.addWidget(QLabel(label), i, j) 
            segment_grid_layout.addWidget(line_edit, i, j + 1) 
            i += 1
            j = 0
        segment_group_box.setLayout(segment_grid_layout)
        input_layout.addWidget(segment_group_box)

        circle_group_box = QGroupBox("Circle Parameters")
        circle_group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        circel_grid_layout = QGridLayout()
        i, j = 0, 0
        for label, line_edit in zip(circle_labels, self.circle_line_edits): 
            circel_grid_layout.addWidget(QLabel(label), i, j) 
            circel_grid_layout.addWidget(line_edit, i, j + 1)  
            i += 1
            j = 0

        circle_group_box.setLayout(circel_grid_layout)       
        input_layout.addWidget(circle_group_box)

        add_clear_group_box = QGroupBox("Add/Clear")
        add_clear_group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        add_clear_layout = QHBoxLayout()
        add_button = QPushButton('Add Segment', self) 
        add_button.clicked.connect(self.add_segment) 
        clear_button = QPushButton('Clear', self) 
        clear_button.clicked.connect(self.clear_clicked) 
        add_circle_button = QPushButton('Add Circle', self) 
        add_circle_button.clicked.connect(self.add_circle) 
 
        add_clear_layout.addWidget(add_button)
        add_clear_layout.addWidget(add_circle_button)
        add_clear_layout.addWidget(clear_button)
        add_clear_group_box.setLayout(add_clear_layout)
        input_layout.addWidget(add_clear_group_box)

        methods_group_box = QGroupBox("Methods")
        methods_group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        methods_layout = QVBoxLayout()

        slope_method_button = QPushButton('Slope Method', self) 
        slope_method_button.clicked.connect(self.slope_method_clicked) 

        dda_method_button = QPushButton('DDA Method', self) 
        dda_method_button.clicked.connect(self.dda_method_clicked)  

        bresenhem_button = QPushButton('Bresenehem Method', self) 
        bresenhem_button.clicked.connect(self.bresenhem_method_clicked) 

        bresenhem_circle_button = QPushButton('Bresenehem for circle Method', self) 
        bresenhem_circle_button.clicked.connect(self.bresenhem_circle_method_clicked) 

        methods_layout.addWidget(slope_method_button)
        methods_layout.addWidget(dda_method_button)
        methods_layout.addWidget(bresenhem_button)
        methods_layout.addWidget(bresenhem_circle_button)
        methods_group_box.setLayout(methods_layout)
        input_layout.addWidget(methods_group_box)
   
    def slope_method_clicked(self):
        self.graphics_view.draw_slope_method()

    def dda_method_clicked(self):
        self.graphics_view.draw_dda_method()
    
    def bresenhem_method_clicked(self):
        self.graphics_view.draw_bresenhem_method()
    
    def bresenhem_circle_method_clicked(self):
        self.graphics_view.circle_bresenhem_method()
    
    def clear_clicked(self):
        self.graphics_view.delete_All()

    def add_circle(self):
        coordinates = [float(line_edit.text()) for line_edit in self.circle_line_edits] 
        x0, y0, r = coordinates 
        circle_coordinates = [x0, y0, r]
        self.graphics_view.circles.append(circle_coordinates)
        self.graphics_view.draw_circles()
        

    def add_segment(self): 
        coordinates = [float(line_edit.text()) for line_edit in self.segment_line_edits] 
        x1, y1, x2, y2 = coordinates 
        step = (int)(self.graphics_view.scale_factor * 10)
        self.graphics_view.scene.addLine(x1 * step, -y1 * step, x2 * step, -y2 * step, self.graphics_view.get_pen(Qt.blue)) 
        
        a = [x1, y1, x2, y2] 
        self.graphics_view.lines.append(a) 
 
def main(): 
    app = QApplication(sys.argv) 
    window = MyMainWindow() 
    window.setGeometry(100, 100, 1000, 500) 
    window.show() 
    sys.exit(app.exec()) 
 
if __name__ == '__main__': 
    main()
    