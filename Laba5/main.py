import sys 
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QGraphicsRectItem, QGraphicsTextItem 
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPen, QWheelEvent, QTransform
import math
import copy
class MyGraphicsView(QGraphicsView): 
    def __init__(self): 
        super(MyGraphicsView, self).__init__() 
        self.lines = [[1,1,10,10],[-3,2,6,7],[-5, -1, 2, 3],[10,10,11,0],[-4,-1,2,1], [-1, 0, -1, 8]] 
        self.clipping_rect = [-1, -1, 8, 6]
        self.polygon = [(-1,0), (-1,2), (4,-2),(2, -4)]
        self.scene = QGraphicsScene(self) 
        self.setScene(self.scene) 
        self.scale_factor = 2
        self.green_lines = []
        self.orange_lines = []
        self.poly_lines = []
        self.setRenderHint(QPainter.Antialiasing, True) 
        self.setSceneRect(QRectF(-100, -100, 200, 200))
        self.draw_axis_and_grid() 
        self.draw_polygon()
        self.fit_to_view() 
       
 
    def draw_axis_and_grid(self): 
        SIZE_X = (int)(self.width()/2)
        SIZE_Y = (int)(self.height()/2)
        step = (int)(self.scale_factor * 10)
        for i in range(0, SIZE_X, step):
            self.scene.addLine(i, -SIZE_Y, i, SIZE_Y, self.get_background_pen(Qt.gray)) 
            self.scene.addLine(-i, -SIZE_Y, -i, SIZE_Y, self.get_background_pen(Qt.gray)) 
        for i in range(0, SIZE_Y, step):
            self.scene.addLine(-SIZE_X, i, SIZE_X, i, self.get_background_pen(Qt.gray))
            self.scene.addLine(-SIZE_X, -i, SIZE_X, -i, self.get_background_pen(Qt.gray))

        self.scene.addLine(-SIZE_X, 0, SIZE_X, 0, self.get_background_pen(Qt.black)) 
        self.scene.addLine(0, -SIZE_Y, 0, SIZE_Y, self.get_background_pen(Qt.black)) 
         

    def get_background_pen(self, color):
        pen = self.scene.addLine(0, 0, 0, 0).pen() 
        pen.setColor(color) 
        return pen 
    
    def get_pen(self, color): 
        pen = self.scene.addLine(0, 0, 0, 0).pen() 
        pen.setColor(color) 
        pen.setWidth(3)
        return pen 
 
    def fit_to_view(self): 
        self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio) 
 
    def draw_lines(self): 
        for a in self.lines: 
            x1, y1, x2, y2 = a[0], a[1], a[2], a[3] 
            step = (int)(self.scale_factor * 10)
            self.scene.addLine(x1 * step, -y1 * step, x2 * step, -y2 * step, self.get_pen(Qt.blue)) 
    
    def draw_green_lines(self): 
        for a in self.green_lines: 
            x1, y1, x2, y2 = a[0], a[1], a[2], a[3] 
            step = (int)(self.scale_factor * 10)
            self.scene.addLine(x1 * step, -y1 * step, x2 * step, -y2 * step, self.get_pen(Qt.green)) 
    
    def draw_orange_lines(self): 
        for a in self.orange_lines: 
            x1, y1, x2, y2 = a[0], a[1], a[2], a[3] 
            step = (int)(self.scale_factor * 10)
            self.scene.addLine(x1 * step, -y1 * step, x2 * step, -y2 * step, self.get_pen(Qt.magenta)) 
    
    def draw_poly_lines(self): 
        for a in self.poly_lines: 
            x1, y1, x2, y2 = a[0], a[1], a[2], a[3] 
            step = (int)(self.scale_factor * 10)
            self.scene.addLine(x1 * step, -y1 * step, x2 * step, -y2 * step, self.get_pen(Qt.black)) 

    def draw_cuttingrect(self):
        step = (int)(self.scale_factor * 10)
        self.scene.addLine(self.clipping_rect[0] * step, -self.clipping_rect[1] * step, self.clipping_rect[0] * step, -self.clipping_rect[3] * step, self.get_pen(Qt.red))
        self.scene.addLine(self.clipping_rect[0] * step, -self.clipping_rect[1] * step, self.clipping_rect[2] * step, -self.clipping_rect[1] * step, self.get_pen(Qt.red))
        self.scene.addLine(self.clipping_rect[2] * step, -self.clipping_rect[1] * step, self.clipping_rect[2] * step, -self.clipping_rect[3] * step, self.get_pen(Qt.red))
        self.scene.addLine(self.clipping_rect[0] * step, -self.clipping_rect[3] * step, self.clipping_rect[2] * step, -self.clipping_rect[3] * step, self.get_pen(Qt.red))
    
    def draw_polygon(self):
        step = (int)(self.scale_factor * 10)
        for i in range(self.polygon.__len__()):
            if (i == self.polygon.__len__() - 1):
                x1 = self.polygon[i][0]
                y1 = self.polygon[i][1]
                x2 = self.polygon[0][0]
                y2 = self.polygon[0][1]
            else:
                x1 = self.polygon[i][0]
                y1 = self.polygon[i][1]
                x2 = self.polygon[i + 1][0]
                y2 = self.polygon[i + 1][1]

            self.scene.addLine(x1* step, -y1 * step, x2 * step, -y2 * step, self.get_pen(Qt.black))
            line = [x1, y1, x2, y2]
            self.poly_lines.append(line)
            

    def cohen_sutherland_clip(self, r, l):
        xmin, ymin, xmax, ymax, x1, y1, x2,  y2 = r[0], r[1], r[2],r[3], l[0], l[1], l[2],l[3]
        INSIDE = 0
        LEFT = 1
        RIGHT = 2
        BOTTOM = 4
        TOP = 8

        def compute_outcode(x, y):
            code = INSIDE
            if x < xmin:
                code |= LEFT
            elif x > xmax:
                code |= RIGHT
            if y < ymin:
                code |= BOTTOM
            elif y > ymax:
                code |= TOP
            return code

        def clip_segment(x1, y1, x2, y2):
            outcode1 = compute_outcode(x1, y1)
            outcode2 = compute_outcode(x2, y2)
            accept = False

            while True:
                if not (outcode1 | outcode2):
                    accept = True
                    break
                elif outcode1 & outcode2:
                    break
                else:
                    x, y = 0, 0
                    outcode = outcode1 if outcode1 else outcode2

                    if outcode & TOP:
                        x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                        y = ymax
                    elif outcode & BOTTOM:
                        x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                        y = ymin
                    elif outcode & RIGHT:
                        y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                        x = xmax
                    elif outcode & LEFT:
                        y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                        x = xmin

                    if outcode == outcode1:
                        x1, y1 = x, y
                        outcode1 = compute_outcode(x1, y1)
                    else:
                        x2, y2 = x, y
                        outcode2 = compute_outcode(x2, y2)

            if accept:
                return x1, y1, x2, y2
            else:
                return None

        return clip_segment(x1, y1, x2, y2)
    

    def draw_cohman_clip(self):
        for line in self.lines:
            result = self.cohen_sutherland_clip(self.clipping_rect, line)
            if (result != None):
                x1, y1, x2, y2 = result
                step = (int)(self.scale_factor * 10)
                self.scene.addLine(x1 * step, -y1 * step, x2 * step, -y2 * step, self.get_pen(Qt.green)) 
                green_line = [x1, y1, x2, y2]
                self.green_lines.append(green_line)

    def intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        X = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4))/((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        Y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4))/((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        return X, Y
    
    def sutherland_hodgman_clip(self, rectangle, polygon):
        result = []

        for i in range(rectangle.__len__()):
            if (i == rectangle.__len__() - 1):
                rect_x1, rect_y1, rect_x2, rect_y2 = rectangle[i][0], rectangle[i][1], rectangle[0][0], rectangle[0][1]
            else:
                rect_x1, rect_y1, rect_x2, rect_y2 = rectangle[i][0], rectangle[i][1], rectangle[i + 1][0], rectangle[i + 1][1]

            for j in range(polygon.__len__()):
                if (j == polygon.__len__() - 1):
                    poly_x1, poly_y1, poly_x2, poly_y2 = polygon[j][0], polygon[j][1], polygon[0][0], polygon[0][1]
                else:
                    poly_x1, poly_y1, poly_x2, poly_y2 = polygon[j][0], polygon[j][1], polygon[j + 1][0], polygon[j + 1][1]
                P1 = (rect_x2 - rect_x1) * (poly_y1 - rect_y1) - (rect_y2 - rect_y1) * (poly_x1 - rect_x1)
                P2 = (rect_x2 - rect_x1) * (poly_y2 - rect_y1) - (rect_y2 - rect_y1) * (poly_x2 - rect_x1)
                if (P1 <= 0 and P2 <=0):
                    result.append([poly_x2, poly_y2])
                elif (P1 > 0 and P2 <= 0):
                    X,Y = self.intersection(rect_x1, rect_y1, rect_x2, rect_y2, poly_x1, poly_y1, poly_x2, poly_y2)
                    result.append([X,Y])
                    result.append([poly_x2, poly_y2])
                elif (P1 <= 0 and P2 > 0):
                    X,Y = self.intersection(rect_x1, rect_y1, rect_x2, rect_y2, poly_x1, poly_y1, poly_x2, poly_y2)
                    result.append([X,Y])
            
            for j in range(result.__len__()):
                polygon[j] = result[j]
            result.clear()
        
        return polygon
    

    def draw_cut_polygon(self):
        polygon = self.polygon
        rectangle = [(self.clipping_rect[0], self.clipping_rect[1]), (self.clipping_rect[0], self.clipping_rect[3]), (self.clipping_rect[2], self.clipping_rect[3]), (self.clipping_rect[2], self.clipping_rect[1])]
        result = self.sutherland_hodgman_clip(rectangle, polygon)
        for i in range(result.__len__()):
            if (i == result.__len__() - 1):
                line = [result[i][0], result[i][1], result[0][0], result[0][1]]
            else:
                line = [result[i][0], result[i][1], result[i + 1][0], result[i + 1][1]]
            step = (int)(self.scale_factor * 10)
            self.scene.addLine(line[0] * step, -line[1] * step, line[2] * step, -line[3] * step, self.get_pen(Qt.magenta))
            self.orange_lines.append(line)
        

    def resizeEvent(self, event): 
        # Update the scene rectangle and redraw the grid when the window is resized 
        super(MyGraphicsView, self).resizeEvent(event)
        rect = QRectF(-100, -100, 200, 200) 
        self.setSceneRect(rect) 
        self.scene.clear() 
        self.draw_axis_and_grid() 
        self.draw_lines()
        
        self.draw_poly_lines()
        self.draw_cuttingrect()
        self.draw_green_lines()
        self.draw_orange_lines()
        # self.draw_cut_polygon()
        self.fit_to_view() 
 
    def wheelEvent(self, event: QWheelEvent): 
        # Handle wheel event for zooming 
        factor = 1.2 
        if event.angleDelta().y() > 0: 
            # Zoom in 
            # self.scale(factor, factor)   
            self.scale_factor *= factor
        else: 
            # Zoom out 
            self.scale_factor /= factor
        self.scene.clear() 
        self.draw_axis_and_grid() 
        self.draw_lines()

        self.draw_poly_lines()
        # self.draw_cut_polygon()
        self.draw_cuttingrect()
        # self.fit_to_view() 
        self.draw_green_lines()
        self.draw_orange_lines()


 
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
        layout.addWidget(self.graphics_view) 
 
        input_widget = QWidget(self) 
        layout.addWidget(input_widget) 
 
        input_layout = QVBoxLayout(input_widget) 

        cohman_button = QPushButton('Coham clip Method', self) 
        cohman_button.clicked.connect(self.slope_method_clicked) 
        input_layout.addWidget(cohman_button) 

        sutherland_hodgman_method_button = QPushButton('Sutherland Hodgman Method', self) 
        sutherland_hodgman_method_button.clicked.connect(self.dda_method_clicked) 
        input_layout.addWidget(sutherland_hodgman_method_button) 


    
    def slope_method_clicked(self):
        self.graphics_view.draw_cohman_clip()

    def dda_method_clicked(self):
        self.graphics_view.draw_cut_polygon()
   
    def add_segment(self): 
        coordinates = [float(line_edit.text()) for line_edit in self.line_edits] 
        x1, y1, x2, y2 = coordinates 
        step = (int)(self.graphics_view.scale_factor * 10)
        self.graphics_view.scene.addLine(x1 * step, -y1 * step, x2 * step, -y2 * step, self.graphics_view.get_pen(Qt.blue)) 
        self.graphics_view.fit_to_view() 
        a = [x1, y1, x2, y2] 
        self.graphics_view.lines.append(a) 
 
def main(): 
    app = QApplication(sys.argv) 
    window = MyMainWindow() 
    window.setGeometry(100, 100, 2000, 1000) 
    window.show() 
    sys.exit(app.exec()) 
 
if __name__ == '__main__': 
    main()
    