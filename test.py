#Функция, которая проверяет функцию find_min_dif_square
from find_triangle import find_min_dif_square
def check_find_min_dif_square():
    points = [(0, 0), (0, 3), (4, 0)]
    res = find_min_dif_square(points)
    print(res)

check_find_min_dif_square()
