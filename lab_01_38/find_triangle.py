from sympy import Triangle, Line
import math
def area_triangle(a, b, c):
    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c))**0.5
    return area

def find_biss(side1, side2, side3, p):
    l_a = (2 * (side2 * side3 * p * (p - side1)) ** 0.5) / (side2 + side3)
    l_b = (2 * (side1 * side3 * p * (p - side2)) ** 0.5) / (side1 + side3)
    l_c = (2 * (side1 * side2 * p * (p - side3)) ** 0.5) / (side1 + side2)
    return l_a, l_b, l_c

def find_part_of_biss(l_a, l_b, l_c, side1, side2, side3):
    l_a_second = l_a / ((side2 + side3) / side1 + 1)
    l_a_first = l_a - l_a_second
    l_b_second = l_b / ((side1 + side3) / side2 + 1)
    l_b_first = l_b - l_b_second
    l_c_second = l_c / ((side1 + side2) / side3 + 1)
    l_c_first = l_c - l_c_second
    return l_a_first, l_a_second, l_b_first, l_b_second, l_c_first, l_c_second

def find_part_of_sides(side1, side2, side3):
    side1_second = side1 / (side3 / side2 + 1)
    side1_first = side1 - side1_second
    side2_second = side2 / (side1 / side3 + 1)
    side2_first = side2 - side2_second
    side3_second = side3 / (side1 / side2 + 1)
    side3_first = side3 - side3_second
    return side1_first, side1_second, side2_first, side2_second, side3_first, side3_second


def check_triangle(side1, side2, side3):
    if side1 + side2 > side3 and side1 + side3 > side2 and side2 + side3 > side1:
        return False
    return True

    
def find_min_dif_square(points):



    # Вычисляем длины сторон треугольника по его вершинам
    side1 = math.hypot(points[0][0] - points[1][0], points[0][1] - points[1][1])
    side2 = math.hypot(points[1][0] - points[2][0], points[1][1] - points[2][1])
    side3 = math.hypot(points[0][0] - points[2][0], points[0][1] - points[2][1])

    rc = check_triangle(side1, side2, side3)
    if rc:
        return math.inf
    
    p = (side1 + side2 + side3) / 2
    # Вычисляем длины биссектрис треугольника
    l_a, l_b, l_c = find_biss(side1, side2, side3, p)
    
    # Вычисляем длину первой и второй части каждой биссектрисы относительно точки пересечения
    l_a_first, l_a_second, l_b_first, l_b_second, l_c_first, l_c_second = find_part_of_biss(l_a, l_b, l_c, side1, side2, side3)

    # Вычисляем длину первой и второй части каждой стороны относительно точки, куда падает биссектриса
    side1_first, side1_second, side2_first, side2_second, side3_first, side3_second = find_part_of_sides(side1, side2, side3)

    # Считаем каждую площадь
    s1 = area_triangle(l_c_second, side3_first, l_b_first)
    s2 = area_triangle(l_c_second, side3_second, l_a_first)
    s3 = area_triangle(l_b_second, side2_second, l_a_first)
    s4 = area_triangle(l_b_second, side2_first, l_c_first)
    s5 = area_triangle(l_a_second, side1_second, l_c_first)
    s6 = area_triangle(l_a_second, side1_first, l_b_first)

    return max(s1,s2,s3,s4,s5,s6) - min(s1,s2,s3,s4,s5,s6)

def find_points_in_lines(cur_points):

    triangle = Triangle(cur_points[0], cur_points[1], cur_points[2])
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
    return point1, point2, point3
