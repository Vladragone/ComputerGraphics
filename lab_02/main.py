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
        self.setGeometry(100, 100, 1000, 1000)
        
        self.graphWidget = PlotWidget()
        #self.graphWidget.setFixedSize(600, 600)    
        layout = QVBoxLayout()
        layout.addWidget(self.graphWidget)

        # Создание поля для переноса
        self.moveEdit = QLineEdit()
        self.moveEdit.setPlaceholderText("Введите координаты для переноса (x,y)")
        layout.addWidget(self.moveEdit)

        # Создание кнопки для перенсоа
        self.moveButton = QPushButton("Перенести")
        self.moveButton.clicked.connect(self.movePoint)
        layout.addWidget(self.moveButton)

        # Создание поля для масштабирования
        self.scaleEdit = QLineEdit()
        self.scaleEdit.setPlaceholderText("Введите коэффицент масштабирования")
        layout.addWidget(self.scaleEdit)

        # Создание кнопки для масштабирования
        self.scaleButton = QPushButton("Масштабировать")
        self.scaleButton.clicked.connect(self.scalePoint)
        layout.addWidget(self.scaleButton)

        # Создание поля для угла поворота
        self.rotateAngleEdit = QLineEdit()
        self.rotateAngleEdit.setPlaceholderText("Введите угол поворота")
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

        self.upEllipseA = 15
        self.upEllipseB = 15

        self.downEllipseA = 10
        self.downEllipseB = 10
        
        self.circleCenter = [0, 16]
        self.circleRadius = 1

        self.angle = 0
        

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
        a = self.downEllipseA
        b = self.downEllipseB
        t = [math.radians(i) for i in range(55, 130, 3)]
        x = [centerEllipse[0] + a * math.cos(angle) for angle in t]
        y = [centerEllipse[1] + b * math.sin(angle) for angle in t]
        mas = list(zip(x,y))
        mas = [self.rotate(p, centerEllipse, self.angle) for p in mas]
        x, y = zip(*mas)
        dots = [[x[0], y[0]], [x[-1], y[-1]]]
        self.graphWidget.plot(x, y, pen='r', symbolSize=0, connect='all')

        
        rightEllipse = self.upEllipse[2]
        upEllipse = self.upEllipse[1]
        centerEllipse = self.upEllipse[0]
        
        a = self.upEllipseA
        b = self.upEllipseB
        t = [math.radians(i) for i in range(67, 115)]

        x = [centerEllipse[0] + a * math.cos(angle) for angle in t]
        y = [centerEllipse[1] + b * math.sin(angle) for angle in t]

        mas = list(zip(x,y))
        mas = [self.rotate(p, centerEllipse, self.angle) for p in mas]
        x, y = zip(*mas)
        
        self.graphWidget.plot(x, y, pen='r', symbolSize=0, connect='all')

        new_dots = [[x[0], y[0]], [x[-1], y[-1]]]
        for dot, new_dot in zip(dots, new_dots):
            x = [dot[0], new_dot[0]]
            y = [dot[1], new_dot[1]]
            self.graphWidget.plot(x, y, pen='r')

        min_x = min(self.clockCenter[0], self.circleCenter[0])
        max_x = max(self.clockCenter[0], self.circleCenter[0])
        for point in itertools.chain(self.clockArrows, self.clockLegs, self.clockLines, self.downEllipse, self.upEllipse):
            if isinstance(point[0], list):
                min_x = min(min_x, min(point[0]))
                max_x = max(max_x, max(point[0]))
            else:
                min_x = min(min_x, point[0])
                max_x = max(max_x, point[0])

        min_y = min(self.clockCenter[1], self.circleCenter[1])
        max_y = max(self.clockCenter[1], self.circleCenter[1])
        for point in itertools.chain(self.clockArrows, self.clockLegs, self.clockLines, self.downEllipse, self.upEllipse):
            if isinstance(point[1], list):
                min_y = min(min_y, min(point[1]))
                max_y = max(max_y, max(point[1]))
            else:
                min_y = min(min_y, point[1])
                max_y = max(max_y, point[1])

        self.graphWidget.setXRange(min_x - self.clockRadius, max_x + self.clockRadius)
        self.graphWidget.setYRange(min_y - self.clockRadius, max_y + self.clockRadius)
        
    def movePoint(self):
        text = self.moveEdit.text()
        try:
            x, y = map(float, text.split(','))
        except ValueError:
            QMessageBox.warning(self, "Ошибка!", "Вы ввели некорректные точки!")
            return
        self.clockCenter[0] += x
        self.clockCenter[1] += y

        self.circleCenter[0] += x
        self.circleCenter[1] += y

        for arrow in self.clockArrows:
            arrow[0][0] += x
            arrow[0][1] += y
            arrow[1][0] += x
            arrow[1][1] += y

        for arrow in self.clockLegs:
            arrow[0][0] += x
            arrow[0][1] += y
            arrow[1][0] += x
            arrow[1][1] += y

        for line in self.clockLines:
            line[0][0] += x
            line[0][1] += y
            line[1][0] += x
            line[1][1] += y

        for ellipse in [self.downEllipse, self.upEllipse]:
            ellipse[0][0] += x
            ellipse[0][1] += y
            ellipse[1][0] += x
            ellipse[1][1] += y
            ellipse[2][0] += x
            ellipse[2][1] += y       
        
        self.drawPicture()

    def scalePoint(self):
        text = self.scaleEdit.text()
        try:
            scale_factor = float(text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка!", "Вы ввели не число!")
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
            self.upEllipseA *= scale_factor
            self.upEllipseB *= scale_factor
            self.downEllipseA *= scale_factor
            self.downEllipseB *= scale_factor
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
            self.upEllipseA /= scale_factor
            self.upEllipseB /= scale_factor
            self.downEllipseA /= scale_factor
            self.downEllipseB /= scale_factor

        self.drawPicture()

    def rotatePoint(self):
        try:
            angle = float(self.rotateAngleEdit.text())
            point = list(map(int, self.rotatePointEdit.text().split(',')))
        except:
            QMessageBox.warning(self, "Ошибка!", "Вы ввели некорректные параметры!")
            return
        
        # Rotate clock hands
        for arrow in self.clockArrows:
            arrow[0], arrow[1] = self.rotate(arrow[0], point, angle), self.rotate(arrow[1], point, angle)
        
        # Rotate clock lines
        for pointer in self.clockLines:
            pointer[0], pointer[1] = self.rotate(pointer[0], point, angle), self.rotate(pointer[1], point, angle)
        
        # Rotate clock legs
        for legs in self.clockLegs:
            legs[0], legs[1] = self.rotate(legs[0], point, angle), self.rotate(legs[1], point, angle)

        # Rotate ellipses
        self.downEllipse = [self.rotate(p, point, angle) for p in self.downEllipse]
        self.upEllipse = [self.rotate(p, point, angle) for p in self.upEllipse]
        
        # Rotate circle
        self.circleCenter = self.rotate(self.circleCenter, point, angle)

        self.clockCenter = self.rotate(self.clockCenter, point, angle)
        self.angle += angle
        # Redraw the picture
        self.drawPicture()

    def rotate(self, point, origin, angle):
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(math.radians(angle)) * (px - ox) - math.sin(math.radians(angle)) * (py - oy)
        qy = oy + math.sin(math.radians(angle)) * (px - ox) + math.cos(math.radians(angle)) * (py - oy)
        return [qx, qy]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

