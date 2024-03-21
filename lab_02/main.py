import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QListWidget, QMessageBox
from pyqtgraph import PlotWidget
from pyqtgraph.Qt import QtCore
import itertools
import math
import os

EPSILON = 1e-5

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("График с точками")
        self.setGeometry(100, 100, 800, 600)

        self.graphWidget = PlotWidget()
        
        layout = QVBoxLayout()
        layout.addWidget(self.graphWidget)

        # Создание поля для переноса
        self.moveEdit = QLineEdit()
        self.moveEdit.setPlaceholderText("Введите координаты переноса (x,y)")
        layout.addWidget(self.moveEdit)

        # Создание кнопки для перенсоа
        self.moveButton = QPushButton("Перенести")
        self.moveButton.clicked.connect(self.movePoint)
        layout.addWidget(self.moveButton)

        # Создание поля для масштабирования
        self.scaleEdit = QLineEdit()
        self.scaleEdit.setPlaceholderText("Введите коэффицент масштабирования (x,y)")
        layout.addWidget(self.scaleEdit)

        # Создание кнопки для масштабирования
        self.scaleButton = QPushButton("Масштабировать")
        self.scaleButton.clicked.connect(self.scalePoint)
        layout.addWidget(self.scaleButton)

        # Создание поля для угла поворота
        self.rotateAngleEdit = QLineEdit()
        self.rotateAngleEdit.setPlaceholderText("Введите угол поворота (x,y)")
        layout.addWidget(self.rotateAngleEdit)

        # Создание поля для точки поворота
        self.rotatePointEdit = QLineEdit()
        self.rotatePointEdit.setPlaceholderText("Введите точку вокруг которой будет поворот (x,y)")
        layout.addWidget(self.rotatePointEdit)
        
        # Создание кнопки для поворота
        self.rotateButton = QPushButton("Повернуть")
        self.rotateButton.clicked.connect(self.rotatePoint)
        layout.addWidget(self.rotateButton)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


        self.clockCenter = [0, 0]
        self.clockRadius = 5

        self.clockArrows = [[[0, 0], [0, 2.5]], [[0, 0], [2.5, 0]]]

        self.clockLines = [[[0, 5], [0, 4]], [[5, 0], [4, 0]], [[0, -5], [0, -4]], [[-5, 0], [-4, 0]]]

        self.clockLegs = [[[-3, -4], [-5, -6]], [[3, -4], [5, -6]]]

        self.downEllipse = [[0, 0], [0, 10], [10, 0]]
        self.upEllipse = [[0, 0], [0, 15], [15, 0]]

        self.circleCenter = [0, 16]
        self.circleRadius = 1

        
        
        self.drawPicture()

    def drawPicture(self):
        
        self.graphWidget.clear()

        self.graphWidget.plot([0, 0], [-1000, 1000], pen='k')
        self.graphWidget.plot([-1000, 1000], [0, 0], pen='k')

        t = [i for i in range(0, 629, 6)]
        r = self.clockRadius
        x = [self.clockCenter[0] + r * math.cos(math.radians(param)) for param in t]
        y = [self.clockCenter[1] + r * math.sin(math.radians(param)) for param in t]
        
        self.graphWidget.plot(x, y, pen='r', ssymbolSize=0, connect = 'all')

        t = [i for i in range(0, 629, 6)]
        r = self.circleRadius
        x = [self.circleCenter[0] + r * math.cos(math.radians(param)) for param in t]
        y = [self.circleCenter[1] + r * math.sin(math.radians(param)) for param in t]

        self.graphWidget.plot(x, y, pen='r', ssymbolSize=0, connect = 'all')
      
        
        x = self.clockCenter[0]
        y = self.clockCenter[1]
        r = self.clockRadius
        for arrow in self.clockArrows:
            x_values = [arrow[0][0], arrow[1][0]]
            y_values = [arrow[0][1], arrow[1][1]]
            self.graphWidget.plot(x_values, y_values, pen='r')
        
        for pointer in self.clockLines:
            x_values = [pointer[0][0], pointer[1][0]]
            y_values = [pointer[0][1], pointer[1][1]]
            self.graphWidget.plot(x_values, y_values, pen='r')

        for legs in self.clockLegs:
            x_values = [legs[0][0], legs[1][0]]
            y_values = [legs[0][1], legs[1][1]]
            self.graphWidget.plot(x_values, y_values, pen='r')       

        rightEllipse = self.downEllipse[2]
        upEllipse = self.downEllipse[1]
        centerEllipse = self.downEllipse[0]
        
        a = abs(rightEllipse[0] - centerEllipse[0])
        b = abs(upEllipse[1] - centerEllipse[1])

        t = [math.radians(i) for i in range(55, 130, 3)]

        x = [centerEllipse[0] + a * math.cos(angle) for angle in t]
        y = [centerEllipse[1] + b * math.sin(angle) for angle in t]
        dots = [[x[0], y[0]], [x[-1], y[-1]]]
        self.graphWidget.plot(x, y, pen='r', symbolSize=0, connect='all')
        
        x = self.clockCenter[0]
        y = self.clockCenter[1]
        r = self.clockRadius
        
        rightEllipse = self.upEllipse[2]
        upEllipse = self.upEllipse[1]
        centerEllipse = self.upEllipse[0]
        
        a = abs(rightEllipse[0] - centerEllipse[0])
        b = abs(upEllipse[1] - centerEllipse[1])

        t = [math.radians(i) for i in range(67, 115)]

        x = [centerEllipse[0] + a * math.cos(angle) for angle in t]
        y = [centerEllipse[1] + b * math.sin(angle) for angle in t]
        self.graphWidget.plot(x, y, pen='r', symbolSize=0, connect='all')

        new_dots = [[x[0], y[0]], [x[-1], y[-1]]]
        for dot, new_dot in zip(dots, new_dots):
            x = [dot[0], new_dot[0]]
            y = [dot[1], new_dot[1]]
            self.graphWidget.plot(x, y, pen='r')

            
    def movePoint(self):
        text = self.moveEdit.text()
        try:
            x, y = map(float, text.split(','))
        except ValueError:
            return
        self.circleCenter[0] += x
        self.circleCenter[1] += y
        self.drawPicture()

    def scalePoint(self):
        text = self.scaleEdit.text()
        try:
            scale_factor = float(text)
        except ValueError:
            return
        if scale_factor >= 0:
            # Масштабирование центра окружности
            self.clockCenter[0] *= scale_factor
            self.clockCenter[1] *= scale_factor
            self.circleCenter[0] *= scale_factor
            self.circleCenter[1] *= scale_factor
            
            # Масштабирование радиуса окружности
            self.clockRadius *= scale_factor
            self.circleRadius *= scale_factor
            # Масштабирование стрелок часов            
            for arrow in self.clockArrows:
                arrow[0][0] *= scale_factor
                arrow[0][1] *= scale_factor
                arrow[1][0] *= scale_factor
                arrow[1][1] *= scale_factor

            for arrow in self.clockLegs:
                arrow[0][0] *= scale_factor
                arrow[0][1] *= scale_factor
                arrow[1][0] *= scale_factor
                arrow[1][1] *= scale_factor

            # Масштабирование линий часов
            for line in self.clockLines:
                line[0][0] *= scale_factor
                line[0][1] *= scale_factor
                line[1][0] *= scale_factor
                line[1][1] *= scale_factor

            # Масштабирование нижнего и верхнего эллипсов
            for ellipse in [self.downEllipse, self.upEllipse]:
                ellipse[0][0] *= scale_factor
                ellipse[0][1] *= scale_factor
                ellipse[1][0] *= scale_factor
                ellipse[1][1] *= scale_factor
                ellipse[2][0] *= scale_factor
                ellipse[2][1] *= scale_factor
        else:
            scale_factor = - scale_factor
            # Масштабирование центра окружности
            self.clockCenter[0] /= scale_factor
            self.clockCenter[1] /= scale_factor
            self.circleCenter[0] /= scale_factor
            self.circleCenter[1] /= scale_factor

            # Масштабирование радиуса окружности
            self.clockRadius /= scale_factor
            self.circleRadius /= scale_factor

            # Масштабирование стрелок часов
            for arrow in self.clockArrows:
                arrow[0][0] /= scale_factor
                arrow[0][1] /= scale_factor
                arrow[1][0] /= scale_factor
                arrow[1][1] /= scale_factor
                
            for arrow in self.clockLegs:
                arrow[0][0] /= scale_factor
                arrow[0][1] /= scale_factor
                arrow[1][0] /= scale_factor
                arrow[1][1] /= scale_factor

            # Масштабирование линий часов
            for line in self.clockLines:
                line[0][0] /= scale_factor
                line[0][1] /= scale_factor
                line[1][0] /= scale_factor
                line[1][1] /= scale_factor

            # Масштабирование нижнего и верхнего эллипсов
            for ellipse in [self.downEllipse, self.upEllipse]:
                ellipse[0][0] /= scale_factor
                ellipse[0][1] /= scale_factor
                ellipse[1][0] /= scale_factor
                ellipse[1][1] /= scale_factor
                ellipse[2][0] /= scale_factor
                ellipse[2][1] /= scale_factor       

        self.drawPicture()

    def rotatePoint(self):
        print("halo")
        text_angle = self.rotateAngleEdit.text()
        text_point = self.rotatePointEdit.text()
        try:
            angle = float(text_angle)
            point_x, point_y = map(float, text_point.split(','))
        except ValueError:
            return

        # Поворот центра окружности
        self.circleCenter[0], self.circleCenter[1] = self._rotate_point(self.circleCenter[0], self.circleCenter[1], point_x, point_y, angle)

        # Поворот стрелок часов
        for arrow in self.clockArrows:
            
            arrow[0][0], arrow[0][1] = self._rotate_point(arrow[0][0], arrow[0][1], point_x, point_y, angle)
            arrow[1][0], arrow[1][1] = self._rotate_point(arrow[1][0], arrow[1][1], point_x, point_y, angle)

          # Поворот линий часов
        for line in self.clockLines:
            line[0][0], line[0][1] = self._rotate_point(line[0][0], line[0][1], point_x, point_y, angle)
            line[1][0], line[1][1] = self._rotate_point(line[1][0], line[1][1], point_x, point_y, angle)

        # Поворот нижнего и верхнего эллипсов
        for ellipse in [self.downEllipse, self.upEllipse]:
            ellipse[0][0], ellipse[0][1] = self._rotate_point(ellipse[0][0], ellipse[0][1], point_x, point_y, angle)
            ellipse[1][0], ellipse[1][1] = self._rotate_point(ellipse[1][0], ellipse[1][1], point_x, point_y, angle)
            ellipse[2][0], ellipse[2][1] = self._rotate_point(ellipse[2][0], ellipse[2][1], point_x, point_y, angle)

        self.drawPicture()

    def _rotate_point(self, x, y, point_x, point_y, angle):
      x -= point_x
      y -= point_y
      new_x = x * math.cos(math.radians(angle)) - y * math.sin(math.radians(angle))
      new_y = x * math.sin(math.radians(angle)) + y * math.cos(math.radians(angle))
      new_x += point_x
      new_y += point_y
      return new_x, new_y

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

