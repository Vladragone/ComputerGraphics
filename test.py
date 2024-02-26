    def findTriangles(self):
        cur = math.inf
        triangles = list(itertools.permutations(self.points, 3))
        for i in triangles:
            res = find_min_dif_square(i)
            if type(res) == complex:
                continue
            if res < cur:
                triangle = Triangle(i[0],i[1],i[2])
                cur = res
                cur_points = i
        if cur == math.inf:
            QMessageBox.warning(self, "Ошибка!", "Невозможно построить ни один треугольник")
        else:
            for i in range(3):
                x1, y1 = cur_points[i]
                x2, y2 = cur_points[(i + 1) % 3]
                self.graphWidget.plot([x1, x2], [y1, y2], pen='g')
            incircle = triangle.incircle

            # Находим центр и радиус вписанной окружности
            center = incircle.center

            # Находим уравнения биссектрис
            bis1 = Line(cur_points[0], center)
            bis2 = Line(cur_points[1], center)
            bis3 = Line(cur_points[2], center)

            # Находим уравнение прямой для каждой стороны треугольника
            side1 = Line(cur_points[0], cur_points[1])
            side2 = Line(cur_points[1], cur_points[2])
            side3 = Line(cur_points[0], cur_points[2])
            # Находим точку пересечения биссектрисы с стороной
            point1 = bis1.intersection(side2)
            point2 = bis2.intersection(side3)
            point3 = bis3.intersection(side1)


            # Построение биссектрис
            self.graphWidget.plot([cur_points[0][0], float(point1[0][0])], [cur_points[0][1], float(point1[0][1])], pen='r')
            self.graphWidget.plot([cur_points[1][0], float(point2[0][0])], [cur_points[1][1], float(point2[0][1])], pen='r')
            self.graphWidget.plot([cur_points[2][0], float(point3[0][0])], [cur_points[2][1], float(point3[0][1])], pen='r')
            QMessageBox.warning(self, "Задача решена!", f"Треугольник, у которого разница площадей минимальна - треугольник в вершинах {cur_points}")
            
