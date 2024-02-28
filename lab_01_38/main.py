import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QListWidget, QMessageBox
from pyqtgraph import PlotWidget
from pyqtgraph.Qt import QtCore
from find_triangle import *
import itertools


EPSILON = 1e-5

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("График с точками")
        self.setGeometry(100, 100, 800, 600)

        self.graphWidget = PlotWidget()
        
        layout = QVBoxLayout()
        layout.addWidget(self.graphWidget)

        # Создание поля для ввода координат точки
        self.pointLineEdit = QLineEdit()
        self.pointLineEdit.setPlaceholderText("Введите координаты точки (x, y)")
        layout.addWidget(self.pointLineEdit)

        # Создание кнопки для добавления точки
        self.addButton = QPushButton("Добавить точку")
        self.addButton.clicked.connect(self.addPoint)
        layout.addWidget(self.addButton)

        # Создание кнопки для удаления точки
        self.removeButton = QPushButton("Удалить выбранную точку")
        self.removeButton.clicked.connect(self.removePoints)
        layout.addWidget(self.removeButton)

        # Создание списка точек
        self.pointList = QListWidget()
        layout.addWidget(self.pointList)

        # Создание кнопки для редактирования координат точки
        self.editButton = QPushButton("Редактировать точку")
        self.editButton.clicked.connect(self.editPoint)
        layout.addWidget(self.editButton)

        # Создание кнопки для решения задачи
        self.solveButton = QPushButton("Решить задачу")
        self.solveButton.clicked.connect(self.findTriangles)
        layout.addWidget(self.solveButton)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.points = []

        self.graphWidget.scene().sigMouseClicked.connect(self.mouseClickEvent)

    def addPoint(self):
        text = self.pointLineEdit.text()
        try:
            x, y = map(float, text.split(','))
        except ValueError:
            self.pointLineEdit.clear()
            return

        for point in self.points:
            if abs(point[0] - x) < EPSILON and abs(point[1] - y) < EPSILON:
                QMessageBox.warning(self, "Ошибка!", "Такая точка уже есть на графике")
                return

        self.points.append((x, y))
        self.updatePlot()
        self.updatePointList()

        self.pointLineEdit.clear()

    def updatePlot(self):
        self.graphWidget.clear()

        self.graphWidget.plot([0, 0], [-1000, 1000], pen='k')
        self.graphWidget.plot([-1000, 1000], [0, 0], pen='k')

        for point in self.points:
            self.graphWidget.plot([point[0]], [point[1]], pen=None, symbol='o', symbolSize=10, symbolPen='b', symbolBrush='r')

        if self.points:
            x_values, y_values = zip(*self.points)
            min_x, max_x = min(x_values), max(x_values)
            min_y, max_y = min(y_values), max(y_values)
            self.graphWidget.setXRange(min_x - 1, max_x + 1)
            self.graphWidget.setYRange(min_y - 1, max_y + 1)

    def updatePointList(self):
        self.pointList.clear()

        for point in self.points:
            item = f"({point[0]}, {point[1]})"
            self.pointList.addItem(item)

    def mouseClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pos = event.pos()
            pos = self.graphWidget.plotItem.vb.mapSceneToView(pos)
            x, y = pos.x(), pos.y()
            self.points.append((x, y))
            self.updatePlot()
            self.updatePointList()

    def editPoint(self):
        selected_items = self.pointList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка!", "Вы не выбрали точку!")
            return
        selected_index = self.pointList.row(selected_items[0])
        selected_point = self.points[selected_index]

        text = self.pointLineEdit.text()
        try:
            new_x, new_y = map(float, text.split(','))
        except ValueError:
            self.pointLineEdit.clear()
            return

        for i, point in enumerate(self.points):
            if i != selected_index and abs(point[0] - new_x) < EPSILON and abs(point[1] - new_y) < EPSILON:
                QMessageBox.warning(self, "Ошибка!", "Такая точка уже есть на графике")
                return

        self.points[selected_index] = (new_x, new_y)
        self.updatePlot()
        self.updatePointList()

        self.pointLineEdit.clear()

    def removePoints(self):
        selected_items = self.pointList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка!", "Вы не выбрали точку!")
            return
        for item in selected_items:
            selected_index = self.pointList.row(item)
            del self.points[selected_index]
            self.pointList.takeItem(selected_index)
        self.updatePlot()

    def findTriangles(self):
        cur = math.inf
        triangles = list(itertools.permutations(self.points, 3))
        for i in triangles:
            res = find_min_dif_square(i)
            if type(res) == complex:
                continue
            if res < cur:
                cur = res
                cur_points = i
        if cur == math.inf:
            QMessageBox.warning(self, "Ошибка!", "Невозможно построить ни один треугольник")
        else:
            for i in range(3):
                x1, y1 = cur_points[i]
                x2, y2 = cur_points[(i + 1) % 3]
                self.graphWidget.plot([x1, x2], [y1, y2], pen='g')
            # Следующие 4 строки - команды для отрисовки бисскектрис. Занимает это продолжительное время (5-10 секунд), поэтому раскоментируйте, если это необходимо.
            """ 
            point1, point2, point3 = find_points_in_lines(cur_points)
            self.graphWidget.plot([cur_points[0][0], float(point1[0][0])], [cur_points[0][1], float(point1[0][1])], pen='r')
            self.graphWidget.plot([cur_points[1][0], float(point2[0][0])], [cur_points[1][1], float(point2[0][1])], pen='r')
            self.graphWidget.plot([cur_points[2][0], float(point3[0][0])], [cur_points[2][1], float(point3[0][1])], pen='r')
            """
            QMessageBox.warning(self, "Задача решена!", f"Треугольник, у которого разница площадей минимальна - треугольник в вершинах {cur_points}")
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
