from cmath import sqrt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget, QPushButton, QLineEdit, QGridLayout, QGroupBox, QSlider
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import gluLookAt
from math import tan, pi
import math
import numpy as np

class OpenGLWidget(QOpenGLWidget):
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0) 
        self.xRot = 0
        self.yRot = 0
        self.ptrMousePosition = None
        self.zoom_factor = 1.0  
        self.setFocusPolicy(Qt.StrongFocus)
        self.T1 = []
        self.T2 = []
        self.T3 = []
        self.T4 = []
        self.Q1 = []
        self.Q2 = []
        self.Q3 = []
        self.Q4 = []
        self.R1 = []
        self.R2 = []
        self.started = False

        self.T1Orth = []
        self.T2Orth = []
        self.T3Orth = []
        self.T4Orth = []
        self.Q1Orth = []
        self.Q2Orth = []
        self.Q3Orth = []
        self.Q4Orth = []
        self.R1Orth = []
        self.R2Orth = []

        

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        aspect_ratio = self.width() / self.height()
        near_plane = 1.0
        far_plane = 100.0
        fov = 45.0 * self.zoom_factor  
        f = 1 / tan((fov / 2) * (pi / 180))
        glFrustum(-aspect_ratio * near_plane, aspect_ratio * near_plane,
                  -near_plane, near_plane, near_plane, far_plane)
        gluLookAt(5, 5, 10, 0, 0, 0, 0, 1, 0)
        glRotatef(self.xRot, 1, 0, 0)
        glRotatef(self.yRot, 0, 1, 0)
        self.drawAxis()
        if (not self.started):
            self.drawStartLetter()
            self.started = True
        else:
            self.drawLetter()
        
        if (len(self.T1Orth) != 0):
            self.drawOrtho()

    def drawAxis(self):
        glLineWidth(3.0)

        width, height = self.width(), self.height()
       

        glColor4f(1.0, 0.0, 0.0, 1.0)
        glBegin(GL_LINES)
        glVertex3f(100.0 * self.zoom_factor, 0.0, 0.0)
        glVertex3f(-100.0 *  self.zoom_factor, 0.0, 0.0)
        glEnd()

        glColor4f(0.0, 1.0, 0.0, 1.0)
        glBegin(GL_LINES)
        glVertex3f(0.0, 100.0 * self.zoom_factor, 0.0)
        glVertex3f(0.0, -100.0 * self.zoom_factor, 0.0)
        glEnd()

        glColor4f(0.0, 0.0, 1.0, 1.0)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 100.0 * self.zoom_factor)
        glVertex3f(0.0, 0.0, -100.0 * self.zoom_factor)
        glEnd()

        glColor4f(0.0, 0.0, 0.0, 0.0)
        for i in range(-100, 110):
            k = 5
            one = 0.5
            glBegin(GL_LINES)
            glVertex3f(i * self.zoom_factor, -one / k * self.zoom_factor, 0.0)
            glVertex3f(i *  self.zoom_factor, one / k * self.zoom_factor, 0.0)
            glVertex3f(-one / k * self.zoom_factor, i * self.zoom_factor, 0.0)
            glVertex3f(one / k * self.zoom_factor, i * self.zoom_factor, 0.0)
            glVertex3f(0.0, one / k * self.zoom_factor, i * self.zoom_factor)
            glVertex3f(0.0, -one / k * self.zoom_factor, i * self.zoom_factor)
            glEnd()
    

    def drawStartTriangleStrip(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, r1, r2, minus):
        verticies = []
        glBegin(GL_TRIANGLE_STRIP)
        glColor4f(0.0, 0.0, 0.0, 1.0) 
        num_segments = 100
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)
        verticies.append([x1, y1, z1])
        verticies.append([x2, y2, z2])
        r = 0
        for i in range(1, num_segments + 2):
            if (i % 2 == 1):
                r = r1
            else:
                r = r2
            angle =  3 * math.pi * i / (2 * num_segments)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            if (minus):
                glVertex3f(x0 - x, y0 - y, z0)
                verticies.append([x0 - x, y0 - y, z0])

            else:
                glVertex3f(x0 + x, y0 + y, z0)
                verticies.append([x0 + x, y0 + y, z0])
            
        glEnd()
        return verticies

    def drawStartQuadStrip(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, r, minus):
        verticies = []
        glBegin(GL_QUAD_STRIP)
        glColor4f(1.0, 1.0, 0.0, 1.0) 
        num_segments = 100
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)
        verticies.append([x1, y1, z1])
        verticies.append([x2, y2, z2])
        for i in range(0, num_segments + 2):
            angle = 3 * math.pi * i / (2 * num_segments)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            if (minus):
                glVertex3f(x0 - x, y0 - y, 0)
                glVertex3f(x0 - x, y0 - y, 1)
                verticies.append([x0 - x, y0 - y, 0])
                verticies.append([x0 - x, y0 - y, 1])
            else:
                glVertex3f(x0 + x, y0 + y, 0)
                glVertex3f(x0 + x, y0 + y, 1)
                verticies.append([x0 + x, y0 + y, 0])
                verticies.append([x0 + x, y0 + y, 1])
        glEnd() 

        return verticies


    def drawStartLetter(self):
        #S1
        self.T1 = self.drawStartTriangleStrip(2, 5, 0, 4, 5, 0, 3, 5, 0, 2, 1, False)
        self.T2 = self.drawStartTriangleStrip(2, 2, 0, 0, 2, 0, 1, 2, 0, 2, 1, True)

        #S2
        self.T3 = self.drawStartTriangleStrip(2, 5, 1, 4, 5, 1, 3, 5, 1, 2, 1, False)
        self.T4 = self.drawStartTriangleStrip(2, 2, 1, 0, 2, 1, 1, 2, 1, 2, 1, True)

        #QuadStrips
        self.Q1 = self.drawStartQuadStrip(2, 5, 0, 4, 5, 0, 4, 5, 1, 2, False)
        self.Q2 = self.drawStartQuadStrip(2, 5, 0, 3, 5, 0, 3, 5, 1, 1, False)
    
        self.Q3 = self.drawStartQuadStrip(2, 2, 0, 0, 2, 0, 0, 2, 1, 2, True)
        self.Q4 = self.drawStartQuadStrip(2, 2, 0, 1, 2, 0, 1, 2, 1, 1, True)
        
        glBegin(GL_QUAD_STRIP)
        glColor4f(1.0, 0.0, 1.0, 1.0) 
        glVertex3f(3, 5, 0)
        glVertex3f(3, 5, 1)
        glVertex3f(4, 5, 0)
        glVertex3f(4, 5, 1)       
        glEnd() 

        self.R1 = [[3, 5, 0], [3, 5, 1], [4, 5, 0], [4, 5, 1]]
        print(self.R1)
        glBegin(GL_QUAD_STRIP)
        glColor4f(1.0, 0.0, 1.0, 1.0)
        glVertex3f(0, 2, 0)
        glVertex3f(1, 2, 0)
        glVertex3f(0, 2, 1)
        glVertex3f(1, 2, 1)     
        glEnd() 

        

        self.R2 = [[0,2,0], [1, 2, 0], [0, 2, 1], [1, 2, 1]]

    def drawTriangleStrip(self, verticies, color = 0):      
        glBegin(GL_TRIANGLE_STRIP)
        glColor4f(color, 0.0, 0.0, 1.0) 
        for i in range(len(verticies)):
            x, y, z = verticies[i][0], verticies[i][1], verticies[i][2]
            glVertex3f(x * self.zoom_factor, y * self.zoom_factor, z * self.zoom_factor)           
        glEnd()
    
    def drawQuadStrip(self, verticies, color=0):
        glBegin(GL_QUAD_STRIP)
        glColor4f(color, 0.0, 0.0, 1.0)  #
        for i in range(len(verticies)):
            x, y, z = verticies[i][0], verticies[i][1], verticies[i][2]
            glVertex3f(x * self.zoom_factor, y * self.zoom_factor, z * self.zoom_factor)           
        glEnd()

    def drawLetter(self):

        self.drawTriangleStrip(self.T1)
        self.drawTriangleStrip(self.T2)
        self.drawTriangleStrip(self.T3)
        self.drawTriangleStrip(self.T4)

        self.drawQuadStrip(self.Q1)
        self.drawQuadStrip(self.Q2)
        self.drawQuadStrip(self.Q3)
        self.drawQuadStrip(self.Q4)

        glBegin(GL_QUAD_STRIP)
        glColor4f(1.0, 0.0, 1.0, 1.0)  
        glVertex3f(self.R1[0][0] * self.zoom_factor, self.R1[0][1] * self.zoom_factor, self.R1[0][2] * self.zoom_factor)
        glVertex3f(self.R1[1][0] * self.zoom_factor, self.R1[1][1] * self.zoom_factor, self.R1[1][2] * self.zoom_factor)
        glVertex3f(self.R1[2][0] * self.zoom_factor, self.R1[2][1] * self.zoom_factor, self.R1[2][2] * self.zoom_factor)
        glVertex3f(self.R1[3][0] * self.zoom_factor, self.R1[3][1] * self.zoom_factor, self.R1[3][2] * self.zoom_factor)       
        glEnd() 

        glBegin(GL_QUAD_STRIP)
        glColor4f(1.0, 0.0, 1.0, 1.0)
        glVertex3f(self.R2[0][0] * self.zoom_factor, self.R2[0][1] * self.zoom_factor, self.R2[0][2] * self.zoom_factor)
        glVertex3f(self.R2[1][0] * self.zoom_factor, self.R2[1][1] * self.zoom_factor, self.R2[1][2] * self.zoom_factor)
        glVertex3f(self.R2[2][0] * self.zoom_factor, self.R2[2][1] * self.zoom_factor, self.R2[2][2] * self.zoom_factor)
        glVertex3f(self.R2[3][0] * self.zoom_factor, self.R2[3][1] * self.zoom_factor, self.R2[3][2] * self.zoom_factor)       
        glEnd() 


    def drawOrtho(self):

        self.drawTriangleStrip(self.T1Orth, 1)
        self.drawTriangleStrip(self.T2Orth, 1)
        self.drawTriangleStrip(self.T3Orth, 1)
        self.drawTriangleStrip(self.T4Orth, 1)

        self.drawQuadStrip(self.Q1Orth, 1)
        self.drawQuadStrip(self.Q2Orth, 1)
        self.drawQuadStrip(self.Q3Orth, 1)
        self.drawQuadStrip(self.Q4Orth, 1)

        glBegin(GL_QUAD_STRIP)
        glColor4f(1.0, 0.0, 0, 1.0)  # Set color to black
        glVertex3f(self.R1Orth[0][0] * self.zoom_factor, self.R1Orth[0][1] * self.zoom_factor, self.R1Orth[0][2] * self.zoom_factor)
        glVertex3f(self.R1Orth[1][0] * self.zoom_factor, self.R1Orth[1][1] * self.zoom_factor, self.R1Orth[1][2] * self.zoom_factor)
        glVertex3f(self.R1Orth[2][0] * self.zoom_factor, self.R1Orth[2][1] * self.zoom_factor, self.R1Orth[2][2] * self.zoom_factor)
        glVertex3f(self.R1Orth[3][0] * self.zoom_factor, self.R1Orth[3][1] * self.zoom_factor, self.R1Orth[3][2] * self.zoom_factor)       
        glEnd() 

        glBegin(GL_QUAD_STRIP)
        glColor4f(1.0, 0.0, 0, 1.0)  # Set color to black
        glVertex3f(self.R2Orth[0][0] * self.zoom_factor, self.R2Orth[0][1] * self.zoom_factor, self.R2Orth[0][2] * self.zoom_factor)
        glVertex3f(self.R2Orth[1][0] * self.zoom_factor, self.R2Orth[1][1] * self.zoom_factor, self.R2Orth[1][2] * self.zoom_factor)
        glVertex3f(self.R2Orth[2][0] * self.zoom_factor, self.R2Orth[2][1] * self.zoom_factor, self.R2Orth[2][2] * self.zoom_factor)
        glVertex3f(self.R2Orth[3][0] * self.zoom_factor, self.R2Orth[3][1] * self.zoom_factor, self.R2Orth[3][2] * self.zoom_factor)       
        glEnd()
    
    def multiply_2d_array_by_scalar(self, a, factor):
        for i in range(len(a)):
            a[i][0] *= factor
            a[i][1] *= factor
            a[i][2] *= factor


    def scale(self, factor):
        self.multiply_2d_array_by_scalar(self.T1, factor)
        self.multiply_2d_array_by_scalar(self.T2, factor)
        self.multiply_2d_array_by_scalar(self.T3, factor)
        self.multiply_2d_array_by_scalar(self.T4, factor)
        self.multiply_2d_array_by_scalar(self.Q1, factor)
        self.multiply_2d_array_by_scalar(self.Q2, factor)
        self.multiply_2d_array_by_scalar(self.Q3, factor)
        self.multiply_2d_array_by_scalar(self.Q4, factor)
        self.multiply_2d_array_by_scalar(self.R1, factor)
        self.multiply_2d_array_by_scalar(self.R2, factor)

        self.update()

    def normalize_vector(self, vector):
        den = sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])
        den = den.real
        vector[0] /= den
        vector[1] /= den
        vector[2] /= den
        return vector
    
    def move_2d_array_by_length(self, a, vector, length):
        vector = self.normalize_vector(vector)
        for i in range(len(a)):        
            a[i][0] += vector[0] * length
            a[i][1] += vector[1] * length
            a[i][2] += vector[2] * length

    def move(self, vector, length):
        
        self.move_2d_array_by_length(self.T1, vector, length)
        self.move_2d_array_by_length(self.T2, vector, length)
        self.move_2d_array_by_length(self.T3, vector, length)
        self.move_2d_array_by_length(self.T4, vector, length)

        self.move_2d_array_by_length(self.Q1, vector, length)
        self.move_2d_array_by_length(self.Q2, vector, length)
        self.move_2d_array_by_length(self.Q3, vector, length)
        self.move_2d_array_by_length(self.Q4, vector, length)

        self.move_2d_array_by_length(self.R1, vector, length)
        self.move_2d_array_by_length(self.R2, vector, length)
        self.update()

    def rotate_point_around_axis(self, point, rotation_matrix):
        point_np = np.array([point[0], point[1], point[2]])
        rotated_point= np.dot(rotation_matrix, point_np)
        return rotated_point


    def rotate_2d_array(self, a, angle, axis):
        angle_rad = np.radians(angle)
        for i in range(len(a)):   
            rotation_matrix = np.empty((3, 3))     
            if (axis == 'x'):
                rotation_matrix = np.array([
                    [1, 0, 0],
                    [0, np.cos(angle_rad), -np.sin(angle_rad)],
                    [0, np.sin(angle_rad), np.cos(angle_rad)],
                    ])
            elif (axis == 'y'):
                rotation_matrix = np.array([
                    [np.cos(angle_rad), 0, np.sin(angle_rad)],
                    [0, 1, 0],
                    [-np.sin(angle_rad), 0, np.cos(angle_rad)],
                    ])
            else:
                rotation_matrix = np.array([
                    [np.cos(angle_rad), -np.sin(angle_rad), 0],
                    [np.sin(angle_rad), np.cos(angle_rad), 0],
                    [0, 0, 1],
                    ])
            

            a[i]= self.rotate_point_around_axis(a[i], rotation_matrix)



    def rotate(self, angle, axis):
        self.rotate_2d_array(self.T1, angle, axis)
        self.rotate_2d_array(self.T2, angle, axis)
        self.rotate_2d_array(self.T3, angle, axis)
        self.rotate_2d_array(self.T4, angle, axis)

        self.rotate_2d_array(self.Q1, angle, axis)
        self.rotate_2d_array(self.Q2, angle, axis)
        self.rotate_2d_array(self.Q3, angle, axis)
        self.rotate_2d_array(self.Q4, angle, axis)

        self.rotate_2d_array(self.R1, angle, axis)
        self.rotate_2d_array(self.R2, angle, axis)
        self.update()

    def ortho_xy(self, a):
        result = []
        for vertex in a:
            result.append([vertex[0], vertex[1], 0])
        return result

    def ortho_yz(self, a):
        result = []
        for vertex in a:
            result.append([0, vertex[1], vertex[2]])
        return result

    def ortho_xz(self, a):
        result = []
        for vertex in a:
            result.append([vertex[0], 0, vertex[2]])
        return result

    def ortho(self, plane):
        if (plane == 'xy'):
            self.T1Orth = self.ortho_xy(self.T1)
            self.T2Orth = self.ortho_xy(self.T2)
            self.T3Orth = self.ortho_xy(self.T3)
            self.T4Orth = self.ortho_xy(self.T4)
            self.Q1Orth = self.ortho_xy(self.Q1)
            self.Q2Orth = self.ortho_xy(self.Q2)
            self.Q3Orth = self.ortho_xy(self.Q3)
            self.Q4Orth = self.ortho_xy(self.Q4)
            self.R1Orth = self.ortho_xy(self.R1)
            self.R2Orth = self.ortho_xy(self.R2)
        elif (plane == 'xz'):
            self.T1Orth = self.ortho_xz(self.T1)
            self.T2Orth = self.ortho_xz(self.T2)
            self.T3Orth = self.ortho_xz(self.T3)
            self.T4Orth = self.ortho_xz(self.T4)
            self.Q1Orth = self.ortho_xz(self.Q1)
            self.Q2Orth = self.ortho_xz(self.Q2)
            self.Q3Orth = self.ortho_xz(self.Q3)
            self.Q4Orth = self.ortho_xz(self.Q4)
            self.R1Orth = self.ortho_xz(self.R1)
            self.R2Orth = self.ortho_xz(self.R2)
        elif (plane == 'yz'):
            self.T1Orth = self.ortho_yz(self.T1)
            self.T2Orth = self.ortho_yz(self.T2)
            self.T3Orth = self.ortho_yz(self.T3)
            self.T4Orth = self.ortho_yz(self.T4)
            self.Q1Orth = self.ortho_yz(self.Q1)
            self.Q2Orth = self.ortho_yz(self.Q2)
            self.Q3Orth = self.ortho_yz(self.Q3)
            self.Q4Orth = self.ortho_yz(self.Q4)
            self.R1Orth = self.ortho_yz(self.R1)
            self.R2Orth = self.ortho_yz(self.R2)

        self.update()

    def clearOrtho(self):
        self.T1Orth = []
        self.T2Orth = []
        self.T3Orth = []
        self.T4Orth = []
        self.Q1Orth = []
        self.Q2Orth = []
        self.Q3Orth = []
        self.Q4Orth = []
        self.R1Orth = []
        self.R2Orth = []
        self.update()

    def restore(self):
        self.drawStartLetter()
        self.clearOrtho()
        self.update()





    def mousePressEvent(self, event):
        self.ptrMousePosition = event.pos()

    def mouseReleaseEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        if self.ptrMousePosition is not None:
            self.xRot += 1 / pi * (event.y() - self.ptrMousePosition.y())
            self.yRot += 1 / pi * (event.x() - self.ptrMousePosition.x())
            self.ptrMousePosition = event.pos()
            self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            print('+')
            self.zoom_factor *= 1.1 
        elif event.key() == Qt.Key_Minus:
            print('-')
            self.zoom_factor /= 1.1 

        self.update()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D Graph Application")

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        input_widget = QWidget(self) 
        main_layout.addWidget(input_widget, 1) 
        input_layout = QVBoxLayout(input_widget) 
        
        label = QLabel("3D Graph")
        label.setAlignment(Qt.AlignCenter)

        group_box = QGroupBox("Methods")        
        group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        gridlayout = QGridLayout()
        self.scale_button = QPushButton("Scale")
        self.scale_button.clicked.connect(self.scale)
        self.scale_line_edit = QLineEdit()
        gridlayout.addWidget(label, 0, 0)
        gridlayout.addWidget(self.scale_button, 1, 0)
        gridlayout.addWidget(self.scale_line_edit, 1, 1)
        self.move_button = QPushButton('Move')
        self.move_button.clicked.connect(self.move)
        vector_label = QLabel('vector:')
        length_label = QLabel('length:')
        self.vector_line_edit = QLineEdit()
        self.length_line_edit = QLineEdit()
        

        self.rotate_x_button = QPushButton("Rotate around x axis: ")
        self.rotate_y_button = QPushButton("Rotate around y axis: ")
        self.rotate_z_button = QPushButton("Rotate around z axis: ")
        self.rotate_x_button.clicked.connect(self.rotate_x)
        self.rotate_y_button.clicked.connect(self.rotate_y)
        self.rotate_z_button.clicked.connect(self.rotate_z)

        self.rotate_x_line_edit = QLineEdit()
        self.rotate_y_line_edit = QLineEdit()
        self.rotate_z_line_edit = QLineEdit()


        self.ortho_xy_button = QPushButton("Ortho xy plane")
        self.ortho_yz_button = QPushButton("Ortho yz plane")
        self.ortho_xz_button = QPushButton("Ortho xz plane")
        self.ortho_xy_button.clicked.connect(self.ortho_xy)
        self.ortho_yz_button.clicked.connect(self.ortho_yz)
        self.ortho_xz_button.clicked.connect(self.ortho_xz)

        self.clear_ortho_button = QPushButton("Clear Ortho Projection")
        self.clear_ortho_button.clicked.connect(self.clear_ortho_proj)


        self.restore_letter_button = QPushButton("Restore letter")
        self.restore_letter_button.clicked.connect(self.restore_letter)
        gridlayout.addWidget(self.move_button, 2, 0)
        gridlayout.addWidget(vector_label, 3, 0)
        gridlayout.addWidget(self.vector_line_edit, 3, 1)
        gridlayout.addWidget(length_label, 4, 0)
        gridlayout.addWidget(self.length_line_edit, 4, 1)
        gridlayout.addWidget(self.rotate_x_button, 6, 0)
        gridlayout.addWidget(self.rotate_x_line_edit, 6, 1)
        gridlayout.addWidget(self.rotate_y_button, 7, 0)
        gridlayout.addWidget(self.rotate_y_line_edit, 7, 1)
        gridlayout.addWidget(self.rotate_z_button, 8, 0)
        gridlayout.addWidget(self.rotate_z_line_edit, 8, 1)

        gridlayout.addWidget(self.ortho_xy_button, 9, 0)
        gridlayout.addWidget(self.ortho_yz_button, 10, 0)
        gridlayout.addWidget(self.ortho_xz_button, 11, 0)

        gridlayout.addWidget(self.clear_ortho_button, 12, 0)
        gridlayout.addWidget(self.restore_letter_button, 13, 0)


        group_box.setLayout(gridlayout)
        input_layout.addWidget(group_box)
        



        self.opengl_widget = OpenGLWidget()
        main_layout.addWidget(self.opengl_widget, 2)

        self.setCentralWidget(central_widget)

    def scale(self):
        factor = float(self.scale_line_edit.text())
        self.opengl_widget.scale(factor)

    def move(self):
        number_strings = self.vector_line_edit.text().split(', ')
        vector = [float(number) for number in number_strings]
        length = int(self.length_line_edit.text())
        self.opengl_widget.move(vector, length)
    
    def rotate_x(self):
        angle = float(self.rotate_x_line_edit.text())
        self.opengl_widget.rotate(angle, 'x')

    def rotate_y(self):
        angle = float(self.rotate_y_line_edit.text())
        self.opengl_widget.rotate(angle, 'y')

    def rotate_z(self):
        angle = float(self.rotate_z_line_edit.text())
        self.opengl_widget.rotate(angle, 'z')

    def ortho_xy(self):
        self.opengl_widget.ortho('xy')

    def ortho_yz(self):
        self.opengl_widget.ortho('yz')

    def ortho_xz(self):
        self.opengl_widget.ortho('xz')

    def clear_ortho_proj(self):
        self.opengl_widget.clearOrtho()

    def restore_letter(self):
        self.opengl_widget.restore()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(1000, 800)
    window.show()
    app.exec_()
