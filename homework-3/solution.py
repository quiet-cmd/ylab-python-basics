"""
geometric calculator
"""
from math import pi, atan, sin, cos, acos, asin, degrees, radians
import tkinter as tk
from tkinter import ttk
from tkinter import *


class Shape:
    def rounding(self):
        """Округляет все атрибуты до 3 знаков после запятой"""
        for key, value in self.__dict__.items():
            if self.__dict__[key]:
                self.__dict__[key] = round(value, 3)

    def deg_to_rad(self, name_list):
        """Первеодит градусы в радианы"""
        for name in name_list:
            if self.__dict__[name]:
                self.__dict__[name] = radians(self.__dict__[name])

    def rad_to_deg(self, name_list):
        """Переводит радианы в градусы"""
        for name in name_list:
            if self.__dict__[name]:
                self.__dict__[name] = degrees(self.__dict__[name])


class Circle(Shape):
    def __init__(self, radius=None, diameter=None, square=None, perimeter=None):
        """Зная 1 любой параметр можно найти все остальные параметры"""
        self.r = radius
        self.D = diameter
        self.S = square
        self.P = perimeter

    def calculate_radius(self):
        """Считает радиус круга"""
        if self.P:
            self.r = self.P / (2 * pi)
        elif self.S:
            self.r = (self.S / pi) ** 0.5
        elif self.D:
            self.S = (pi / 4) * self.D ** 2
            self.r = (self.S / pi) ** 0.5

    def circle_diameter(self):
        """диаметр через радиус"""
        return 2 * self.r

    def circle_perimeter(self):
        """окружность через радиус"""
        return 2 * pi * self.r

    def circle_area(self):
        """Площадь через радиус"""
        return pi * self.r ** 2

    def calculate_attributes(self):
        """Считает все параметры в конструкторе через радиус круга"""
        self.calculate_radius()
        if self.r:
            self.D = self.circle_diameter()
            self.S = self.circle_area()
            self.P = self.circle_perimeter()
            self.rounding()

    def attribute_description(self):
        text = f'''
        Радиус круга r {self.r}
        Площадь круга S {self.S}
        Диаметр круга d {self.D}
        Окружность круга P {self.P}'''
        return text


class Square(Shape):
    def __init__(self, side=None, diagonal=None, square=None, perimeter=None, radius_in=None, radius_des=None):
        """Зная 1 любой параметр можно найти все остальные параметры"""
        self.a = side
        self.d = diagonal
        self.S = square
        self.P = perimeter
        self.r = radius_in
        self.R = radius_des

    def calculate_side(self):
        """Считает сторону квадрата"""
        if self.d:
            self.a = self.d / (2 ** 0.5)
        elif self.S and self.a is None:
            self.a = self.S ** 0.5
        elif self.P:
            self.a = self.P / 4
        elif self.r:
            self.a = self.r * 2
        elif self.R and self.a is None:
            self.a = self.R * (2 ** 0.5)

    def calculate_attributes(self):
        """Считает все параметры в конструкторе через сторону квадрата"""
        self.calculate_side()
        if self.a:
            self.d = self.a * (2 ** 0.5)
            self.S = self.a ** 2
            self.P = 4 * self.a
            self.r = self.a / 2
            self.R = self.a / (2 ** 0.5)
            self.rounding()

    def attribute_description(self):
        text = f'''
        a - сторона {self.a}
        d - диагональ {self.d}
        S - площадь {self.S}
        P - периметр {self.P}
        r - радиус вписанной окружности {self.r}
        R - радиус описанной окружности {self.R}'''
        return text


class Rectangle(Shape):
    def __init__(self, long=None, width=None, diagonal=None, alpha=None, beta=None, gamma=None, delta=None,
                 square=None, perimeter=None):
        """Можно вычислить все параметры зная: стороны, площадь и сторону, диагональ и сторону,
        перемитр и диагональ, угол между диагоналей"""
        self.a = width
        self.b = long
        self.d = diagonal
        self.gamma = gamma
        self.delta = delta
        self.beta = beta
        self.alpha = alpha
        self.S = square
        self.P = perimeter
        self.R = None

    def calculate_side(self):
        """Считает стороны прямоугольника"""
        if self.S and self.a:
            self.b = self.S / self.a
        elif self.S and self.b:
            self.a = self.S / self.b
        elif self.d and self.a:
            self.b = (self.d ** 2 - self.a ** 2) ** 0.5
        elif self.d and self.b:
            self.a = (self.d ** 2 - self.b ** 2) ** 0.5
        elif self.d and (self.beta or self.alpha):
            self.a = self.d * (sin(self.beta) if self.beta else sin(self.alpha))
            self.b = self.d * (cos(self.beta) if self.beta else cos(self.alpha))
        elif self.P and self.d:
            self.b = (self.P + (8 * self.d ** 2 - self.P ** 2) ** 0.5) / 4
            self.a = (self.P - (8 * self.d ** 2 - self.P ** 2) ** 0.5) / 4

    def calculate_attributes(self):
        """Считает все параметры в конструкторе через стороны прямоугольника"""
        self.deg_to_rad(['beta', 'alpha', 'gamma', 'delta'])
        self.calculate_side()
        if self.a and self.b:
            self.d = (self.a ** 2 + self.b ** 2) ** 0.5
            self.S = self.a * self.b
            self.P = 2 * (self.a + self.b)
            self.R = self.d / 2
            self.alpha = 2 * asin(self.a / self.d)
            self.beta = 2 * asin(self.b / self.d)
            self.gamma = self.beta / 2
            self.delta = self.alpha / 2

            self.rad_to_deg(['alpha', 'beta', 'delta', 'gamma'])
            self.rounding()

    def attribute_description(self):
        text = f'''
        Сторона a {self.a}
        Сторона b {self.b}
        Площадь прямоугольника S {self.S}
        Периметр прямоугольника P {self.P}
        Диагональ прямоугольника d {self.d}
        Угол между диагоналями α {self.alpha}
        Угол между диагоналями β {self.beta}
        Угол от деления диагональю γ {self.gamma}
        Угол от деления диагональю δ {self.delta}
        Радиус описанной окружности R {self.R}'''
        return text


class Trapezoid(Shape):
    def __init__(self, a=None, b=None, c=None, d=None):
        """Для обычной трапеции ожидаюся 4 стороны"""
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        # вычисляемо
        self.S = self.P = self.m = self.d1 = self.d2 = self.gamma = self.delta = self.beta = self.alpha = self.m =\
            self.h = None

    def general_formulas(self):
        """Общие формулы для разных видов трапеции"""
        self.m = (self.b + self.d) / 2
        self.P = self.a + self.b + self.c + self.d
        self.d1 = (self.c ** 2 + self.d * self.b - (self.d * (self.c ** 2 - self.a ** 2)) / (self.d - self.b)) ** 0.5
        self.d2 = (self.a ** 2 + self.d * self.b + (self.d * (self.c ** 2 - self.a ** 2)) / (self.d - self.b)) ** 0.5
        self.S = self.h * self.m

    def calculate_attributes(self):
        """Вычисление параметров для произвольной трапеции"""
        if self.a and self.b and self.c and self.d:
            self.h = (self.a ** 2 - (
                    ((self.d - self.b) ** 2 + self.a ** 2 - self.c ** 2) / (2 * (self.d - self.b))) ** 2) ** 0.5
            self.general_formulas()
            self.beta = degrees(asin(self.h / self.a))
            self.delta = degrees(asin(self.h / self.c))
            self.gamma = 180 - self.delta
            self.alpha = 180 - self.beta
            self.rounding()

    def attribute_description(self):
        text = f'''
        Площадь трапеции S {self.S}
        Высота трапеции h {self.h}
        Периметр трапеции P {self.P}
        Средняя линия трапеции m {self.m}
        Диагональ трапеции d1 {self.d1}
        Диагональ трапеции d2 {self.d2}
        Угол трапеции α {self.alpha}
        Угол трапеции β {self.beta}
        Угол трапеции γ {self.gamma}
        Угол трапеции δ {self.delta}'''
        return text


class Rhombus(Shape):
    def __init__(self, a=None, alpha=None, beta=None, d1=None, d2=None, height=None, perimeter=None,
                 square=None, r=None):
        """ожидатся сторона и высота, площадь и угол, площадь и диагональ, сторона и угол, диагонали
        площадь и сторона, диагонали и сторону, радиус и сторону, радиус и угол"""
        self.a = a
        self.beta = beta
        self.alpha = alpha
        self.h = height
        self.d1 = d1
        self.d2 = d2
        self.S = square
        self.P = perimeter
        self.r = r

    def calculate_side(self):
        """Расчет стороны и высоты ромба"""
        if self.S and (self.alpha or self.beta):
            self.a = (self.S / sin(radians(self.alpha if self.alpha else self.beta))) ** 0.5
            self.h = self.S / self.a
        elif self.S and (self.d1 or self.d2):
            d = self.d1 if self.d1 else self.d2
            self.a = (d ** 2 + (2 * self.S / d) ** 2) ** 0.5 / 2
            self.h = self.S / self.a
        elif self.a and (self.alpha or self.beta):
            self.h = self.a * sin(radians(self.alpha if self.alpha else self.beta))
        elif self.d1 and self.d2:
            self.a = (self.d1 ** 2 + self.d2 ** 2) ** 0.5 / 2
            self.h = self.d1 * self.d2 / (self.d1 ** 2 + self.d2 ** 2) ** 0.5
        elif self.S and self.a:
            self.h = self.S / self.a
        elif self.a and self.d1:
            d2 = (4 * self.a ** 2 - self.d1 ** 2) ** 0.5
            self.h = self.d1 * d2 / (self.d1 ** 2 + d2 ** 2) ** 0.5
        elif self.a and self.d2:
            d1 = (4 * self.a ** 2 - self.d2 ** 2) ** 0.5
            self.h = self.d2 * d1 / (self.d2 ** 2 + d1 ** 2) ** 0.5
        elif self.r and (self.a or self.alpha):
            self.a = self.a if self.a else 2 * self.r / sin(radians(self.alpha))
            self.h = 2 * self.r

    def calculate_attributes(self):
        """Считает все параметры в конструкторе через сторону и высоту ромба"""
        self.calculate_side()
        if self.a and self.h:
            self.P = 4 * self.a
            self.S = self.a * self.h if not self.S else self.S
            self.r = self.h / 2
            self.alpha = degrees(asin(self.h / self.a))
            self.beta = 180 - self.alpha
            self.d2 = 2 * self.a * sin(radians(self.alpha / 2))
            self.d1 = 2 * self.a * cos(radians(self.alpha / 2))
            self.rounding()

    def attribute_description(self):
        text = f'''
        Площадь ромба S {self.S}
        Периметр ромба P {self.P}
        Угол ромба α {self.alpha}
        Угол ромба β {self.beta}
        Диагональ ромба d1 {self.d1}
        Диагональ ромба d2 {self.d2}
        Радиус вписанной окружности r {self.r}'''
        return text


class Triangle(Shape):
    def __init__(self, a=None, b=None, c=None, beta=None, alpha=None, gamma=None):
        """Обычный треугольник, для расчетов необходимо ввести 3 стороны,
        два угла и сторону, две стороны и угол"""
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        # Вычисляемо
        self.P = self.S = self.r = self.R = self.h_a = self.h_b = self.h_c = self.m_a = self.m_b = self.m_c = None

    def calculate_side(self):
        """Расчет сторон треугольника"""
        if self.alpha and self.beta and self.c:
            gamma = 180 - self.alpha - self.beta
            self.a = self.c * sin(radians(gamma)) / sin(radians(self.beta))
            self.b = self.cos_theorem(self.c, self.a, self.alpha)
        elif self.alpha and self.beta and self.a:  # не точно
            gamma = 180 - self.alpha - self.beta
            self.b = self.a * sin(radians(self.alpha + gamma)) / sin(radians(self.alpha))
            self.c = self.cos_theorem(self.a, self.b, self.beta)
        elif self.alpha and self.c and self.a:
            self.b = self.cos_theorem(self.c, self.a, self.alpha)
        elif self.gamma and self.b and self.c:
            self.a = self.cos_theorem(self.b, self.c, self.gamma)
        elif self.beta and self.a and self.b:
            self.c = self.cos_theorem(self.a, self.b, self.beta)

    def cos_theorem(self, b, c, gamma):
        """3 сторона треугольника"""
        return (b ** 2 + c ** 2 - (2 * b * c * cos(radians(gamma)))) ** 0.5

    def height(self, a, alpha):
        """Высота угла через угол и сторону"""
        return a * sin(radians(alpha))

    def calculate_attributes(self):
        """Считает все параметры в конструкторе через стороны треугольника"""
        self.calculate_side()
        if self.a and self.c and self.b:
            self.P = self.a + self.b + self.c
            self.r = (self.a + self.b - self.c) / 2
            self.R = self.c / 2
            self.alpha = degrees(acos((self.a ** 2 + self.c ** 2 - self.b ** 2) / (2 * self.a * self.c)))
            self.beta = degrees(acos((self.a ** 2 + self.b ** 2 - self.c ** 2) / (2 * self.a * self.b)))
            self.gamma = degrees(acos((self.b ** 2 + self.c ** 2 - self.a ** 2) / (2 * self.c * self.b)))
            self.S = 0.5 * self.a * self.c * sin(radians(self.alpha))
            self.m_a, self.m_b, self.m_c, = 0.5 * self.a, 0.5 * self.b, 0.5 * self.c
            self.h_a = self.height(self.b, self.beta)
            self.h_b = self.height(self.c, self.gamma)
            self.h_c = self.height(self.a, self.alpha)
            self.rounding()

    def attribute_description(self):
        text = f'''
        Площадь треугольника S {self.S}
        Периметр треугольника P {self.P}
        Угол треугольника α {self.alpha}
        Угол треугольника β {self.beta}
        Угол треугольника γ {self.gamma}
        Высота треугольника ha {self.h_a}
        Высота треугольника hb {self.h_b}
        Высота треугольника hc {self.h_c}
        Медиана треугольника ma {self.m_a}
        Медиана треугольника mb {self.m_b}
        Медиана треугольника mc {self.m_c}
        Радиус вписанной окружности r {self.r}
        Радиус описанной окружности R {self.R}
        Средняя линия треугольника mla {self.m_a}
        Средняя линия треугольника mlb {self.m_b}
        Средняя линия треугольника mlc {self.m_c}'''
        return text


class Sphere(Circle):
    def __init__(self, radius=None, diameter=None, square=None, perimeter=None, v=None):
        super().__init__(radius, diameter, square, perimeter)
        self.V = v

    def calculate_attributes(self):
        """Считаем атрибуты сферы через радиус"""
        if self.V:
            self.r = (3 * self.V / (4 * pi)) ** (1 / 3)
        super().calculate_attributes()
        if self.r:
            self.V = 4 / 3 * pi * self.r ** 3
            self.S *= 4
            self.rounding()

    def attribute_description(self):
        text = Circle.attribute_description(self)
        text += f"""
        Объем шара V {self.V}"""
        return text


class Cube(Square):
    def __init__(self, side=None, side_diagonal=None, side_square=None, side_perimeter=None, radius_in=None,
                 radius_des=None, main_diagonal=None, surface_square=None, main_square=None, main_perimeter=None,
                 v=None):
        super().__init__(side, side_diagonal, surface_square, side_perimeter, radius_in, radius_des)
        self.side_square = side_square
        self.main_diagonal = main_diagonal
        self.main_square = main_square
        self.main_perimeter = main_perimeter
        self.V = v

    def calculate_cube_side(self):
        """Считаем сторону"""
        if self.V:
            self.a = self.V ** (1 / 3)
        elif self.main_perimeter:
            self.a = self.main_perimeter / 12
        elif self.main_diagonal:
            self.a = self.main_diagonal * (3 ** 0.5)
        elif self.main_square:
            self.a = (self.main_square / 6) ** 0.5
        elif self.side_square:
            self.a = self.side_square ** 0.5
        elif self.S:
            self.a = self.S ** 0.5 / 2
        elif self.R:
            self.a = 2 * self.R / 3 ** 0.5

    def calculate_attributes(self):
        """Считаем атрибуты куба через стороны"""
        self.calculate_cube_side()
        super().calculate_attributes()
        if self.a:
            self.side_square = self.a ** 2
            self.main_diagonal = self.a * 3 ** 0.5
            self.main_square = self.side_square * 4
            self.main_perimeter = 12 * self.a
            self.V = self.a ** 3
            self.R = self.main_diagonal / 2
            self.rounding()

    def attribute_description(self):
        text = Square.attribute_description(self)
        text += f"""
        Объем куба V {self.V}
        Длина ребер куба P {self.main_perimeter}
        Диагональ стороны куба d1 {self.main_diagonal}
        Площадь куба S {self.main_square}
        Площадь стороны S {self.side_square}"""
        return text


class Parallelepiped(Shape):
    def __init__(self, a=None, b=None, c=None, d4=None):
        self.a = a
        self.b = b
        self.c = c
        self.d4 = d4
        # вычисляемо
        self.alpha = self.d3 = self.S1 = self.S2 = self.S3 = self.P = self.V = \
            self.d2 = self.d1 = self.surface_S = self.main_S = None

    def calculate_side(self):
        """Поиск сторон параллелепипеда"""
        if self.a and self.c and self.d4:
            self.b = self.side(self.a, self.c, self.d4)
        elif self.a and self.b and self.d4:
            self.c = self.side(self.a, self.b, self.d4)
        elif self.b and self.c and self.d4:
            self.a = self.side(self.b, self.c, self.d4)

    def side(self, a, c, d4):
        """Расчитывает сторону по 2 сторонам и главной диагонали"""
        return (d4 ** 2 - (a ** 2 + c ** 2)) ** 0.5

    def diagonal(self, a, c):
        """Расчитываем диагональ через стороны"""
        return (a ** 2 + c ** 2) ** 0.5

    def square(self, a, c):
        """Расчитываем малые площади через стороны"""
        return a * c

    def calculate_attributes(self):
        """Вычисление параметров для параллелепипеда"""
        self.calculate_side()
        if self.a and self.b and self.c:
            self.P = 4 * (self.a + self.b + self.c)
            self.surface_S = 2 * self.a * self.c + 2 * self.a * self.b
            self.main_S = 2 * (self.a * self.b + self.b * self.c + self.a * self.c)
            self.V = self.a * self.b * self.c
            self.d1 = self.diagonal(self.a, self.c)
            self.d2 = self.diagonal(self.a, self.b)
            self.d3 = self.diagonal(self.b, self.c)
            self.d4 = (self.a ** 2 + self.c ** 2 + self.b ** 2) ** 0.5
            self.alpha = degrees(atan(self.a / self.d3))
            self.S1 = self.square(self.a, self.c)
            self.S2 = self.square(self.a, self.b)
            self.S3 = self.square(self.c, self.b)
            self.rounding()

    def attribute_description(self):
        text = f'''
        Площадь параллелепипеда S {self.main_S}
        Площадь боковой поверхности S {self.surface_S}
        Объем параллелепипеда V {self.V}
        Длина ребер параллелепипеда P {self.P}
        Диагональ стороны d1 {self.d1}
        Диагональ стороны d2 {self.d2}
        Диагональ стороны d3 {self.d3}
        Диагональ параллелепипеда d4 {self.d4}
        Площадь стороны S1 {self.S1}
        Площадь стороны S2 {self.S2}
        Площадь стороны S3 {self.S3}
        Угол α {self.alpha}'''
        return text


class Cylinder(Shape):
    def __init__(self, r=None, diameter=None, diagonal=None, v=None, base_S=None, h=None):
        self.r = r
        self.h = h
        self.V = v
        self.diagonal = diagonal
        self.D = diameter
        self.base_S = base_S
        self.P = self.R = self.r_in = self.P = self.main_S = self.surface_S = self.axial_S = None

    def calculate_radius_height(self):
        """Поиск радиуса и высоты"""
        if self.r and self.V:
            self.h = self.V / (2 * pi * self.r)
            print("self.r and self.V")
        elif self.r and self.diagonal:
            self.h = (self.diagonal ** 2 - (2 * self.r) ** 2) ** 0.5
            print("self.r and self.diagonal")
        elif self.h and self.base_S:
            self.r = (self.base_S / pi) ** 0.5
            print("self.h and self.base_S")
        elif self.h and self.diagonal:
            self.r = (self.diagonal ** 2 - self.h ** 2) ** 0.5 / 2
            print("self.h and self.diagonal")
        elif self.D and self.h:
            self.r = self.D / 2
            print("self.D and self.h")
        elif self.D and self.V:
            self.r = self.D / 2
            self.h = 4 * self.V / (pi * self.D ** 2)
            print("self.D and self.V")
        elif self.D and self.diagonal:
            self.r = self.D / 2
            self.h = (self.diagonal ** 2 - self.D ** 2) ** 0.5
            print("self.D and self.diagonal")

    def calculate_attributes(self):
        """Вычисление параметров для цилиндра через радиус и высоту"""
        self.calculate_radius_height()
        if self.r and self.h:
            self.D = 2 * self.r
            self.P = 2 * pi * self.r
            self.surface_S = self.h * self.P
            self.base_S = self.surface_S * 2
            self.axial_S = self.h * self.D
            self.main_S = self.surface_S + 2 * self.base_S
            self.V = pi * self.r ** 2 * self.h
            self.diagonal = (self.D ** 2 + self.h ** 2) ** 0.5
            self.r_in = self.r
            self.R = self.diagonal / 2
            self.rounding()

    def attribute_description(self):
        text = f'''
        Объем цилиндра V {self.V}
        Площадь цилиндра S {self.main_S}
        Площадь боковой поверхности S {self.surface_S}
        Площадь основания S {self.base_S}
        Площадь осевого сечения S {self.axial_S}
        Диагональ осевого сечения d {self.diagonal}
        Окружность основания P {self.P}
        Диаметр основания D {self.D}
        Радиус описанной сферы R {self.R}
        радиус вписанной сферы r1 {self.r_in}'''
        return text


class Cone(Shape):
    def __init__(self, r=None, diameter=None, l=None, h=None, v=None, base_S=None, alpha=None):
        self.r = r
        self.h = h
        self.V = v
        self.l = l
        self.D = diameter
        self.base_S = base_S
        self.alpha = alpha
        self.r_in = self.r_des = self.main_S = self.surface_S = self.axial_S = self.beta = self.P = None

    def calculate_radius_generators(self):
        """Поиск радиуса и образующей"""
        if self.r and self.h:
            self.l = (self.h ** 2 + self.r ** 2) ** 0.5
        elif self.l and self.h:
            self.r = (self.l ** 2 - self.h ** 2) ** 0.5
        elif self.V and self.h:
            base_S = 3 * self.V / self.h
            self.r = (base_S / pi) ** 0.5
            self.l = (self.h ** 2 + self.r ** 2) ** 0.5
        elif self.alpha and self.l:
            b = round((180 - self.alpha) / 2, 2)
            self.r = cos(radians(b)) * self.l
        elif self.alpha and self.r:
            b = round((180 - self.alpha) / 2, 2)
            self.l = self.r / cos(radians(b))
        elif self.base_S and self.l:
            self.r = (self.base_S / pi) ** 0.5
        elif self.base_S and self.h:
            self.r = (self.base_S / pi) ** 0.5
            self.l = (self.h ** 2 + self.r ** 2) ** 0.5

    def calculate_attributes(self):
        """Вычисление параметров для конуса через радиус и образующею конуса"""
        self.calculate_radius_generators()
        if self.r and self.l:
            self.D = 2 * self.r
            self.P = 2 * pi * self.r
            self.base_S = pi * self.r ** 2
            self.h = (self.l ** 2 - self.r ** 2) ** 0.5
            self.beta = degrees(acos(self.r / self.l))
            self.alpha = 180 - 2 * self.beta
            self.surface_S = pi * self.r * self.l
            self.main_S = self.surface_S + self.base_S
            self.axial_S = self.r * self.h
            self.V = 1 / 3 * self.base_S * self.h
            self.r_in = self.h * self.r / (self.l + self.r)
            self.r_des = self.l ** 2 / (2 * self.h)
            self.rounding()

    def attribute_description(self):
        text = f'''
        Высота конуса h {self.h}
        Диаметр конуса d {self.D}
        Объем конуса V {self.V}
        Площадь конуса S {self.main_S}
        Площадь боковой поверхности S {self.surface_S}
        Площадь основания S {self.base_S}
        Площадь осевого сечения S {self.axial_S}
        Угол раствора конуса α {self.alpha}
        Угол наклона образующей β {self.beta}
        Радиус вписанной сферы r1 {self.r_in}
        Радиус описанной сферы R {self.r_des}
        Периметр конуса P {self.P}'''
        return text


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.photo_label = Label(image=None)
        self.button_frame = Frame(self)
        self.model = None
        self.result = Label(text=None)
        # Сентябрь горит, студент плачет, но он не смог поступить иначе
        self.shapes = {'Круг': {'photo': 'circle.png', 'model': Circle(), 'Радиус круга r': 'r',
                                'Площадь круга S': 'S', 'Диаметр круга d': 'D', 'Окружность круга P': 'P'},
                       'Квадрат': {'photo': 'square.png', 'model': Square(), 'Сторона': 'a', 'Площадь': 'S',
                                   'Диагональ': 'd', 'Периметр': 'P', 'Радиус вписанной окружности': 'r',
                                   'Радиус описанной окружности': 'R'},
                       'Прямоугольник': {'photo': 'rectangle.png', 'model': Rectangle(), 'Сторона a': 'a',
                                         'Сторона b': 'b', 'Площадь': 'S', 'Диагональ': 'd', 'Периметр': 'P',
                                         'Альфа': 'alpha', 'Бета': 'beta', 'Гамма': 'gamma', 'Дельта': 'delta'},
                       'Трапеция': {'photo': 'trapezoid.png', 'model': Trapezoid(),
                                    'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd'},
                       'Ромб': {'photo': 'rhombus.png', 'model': Rhombus(), 'Сторона': 'a', 'угол альфа': 'alpha',
                                'угол бета': 'beta', 'высота': 'h', 'диагональ': 'd', 'периметр': 'P',
                                'площадь': 'S', 'радиус': 'r'},
                       'Треугольник': {'photo': 'triangle.png', 'model': Triangle(), 'Сторона a': 'a',
                                       'Сторона v': 'b', 'Сторона c': 'c', 'Угол alpha': 'alpha',
                                       'Угол beta': 'beta', 'Угол gamma': 'gamma'},
                       'Сфера': {'photo': 'sphere.png', 'model': Sphere(), 'Радиус круга r': 'r',
                                 'Площадь круга S': 'S', 'Диаметр круга d': 'D',
                                 'Окружность круга P': 'P', 'объем': 'v'},
                       'Куб': {'photo': 'cube.png', 'model': Cube(), 'Сторона': 'a', 'Площадь поверхности': 'S',
                               'Диагональ d1': 'd', 'Периметр стороны': 'P', 'Радиус вписанной окружности': 'r',
                               'Радиус описанной окружности': 'R', 'Площадь стороны': 'side_square',
                               'Диагональ d2': 'main_diagonal', 'Площадь куба': 'main_square',
                               'Периметр куба': 'main_perimeter',
                               "объем": 'v'},
                       'параллелепипед': {'photo': 'parallelepiped.png', 'model': Parallelepiped(), 'Сторона a': 'a',
                                          'Сторона b': 'b', 'Сторона c': 'c', 'Диагональ d4': 'd4'},
                       'цилиндр': {'photo': 'cylinder.png', 'model': Cylinder(), 'Радиус вращения': 'r',
                                   'Высота ': 'h', 'Объем цилиндра V': 'V', 'Диагональ осевого сечения d': 'diagonal',
                                   'Диаметр': 'D', 'Площадь основания S': 'base_S'},
                       'Конус': {'photo': 'cone.png', 'model': Cone(), 'Радиус основания конуса r': 'r',
                                 'Высота конуса h': 'h', 'Объем конуса V ': 'v', 'Образующая конуса l': 'l',
                                 'Диаметр конуса d': 'D', 'Площадь основания S ': 'base_S',
                                 'Угол раствора конуса α': 'alpha'}
                       }

        self.shape_cmb = ttk.Combobox(self, values=list(list(self.shapes.keys())))
        self.shape_cmb.bind("<<ComboboxSelected>>", self.shape_choose)
        self.shape_cmb.pack(padx=10, pady=5, expand=True)

    def shape_choose(self, *args):
        """Обновляем фото по списку и обновляем список опций"""
        self.shape = self.shape_cmb.get()
        photo = PhotoImage(file=f"img/{self.shapes[self.shape]['photo']}")
        self.photo_label.config(image=photo)
        self.photo_label.image = photo
        self.photo_label.pack(side=tk.LEFT)
        self.options()

    def clear_options(self):
        """Удаляет поле ввода и текст параметров"""
        for item in self.button_frame.pack_slaves():
            item.destroy()

    def click_button(self):
        """Активирует калькулятор"""
        list = self.button_frame.pack_slaves()
        shapes = self.shapes[self.shape]
        self.model = self.shapes[self.shape]['model']
        for i in range(1, len(list) - 1, 2):
            key, value = shapes[list[i - 1].cget("text")], list[i].get()
            self.model.__dict__[key] = float(value) if value != '' else None
        self.model.calculate_attributes()
        result = self.model.attribute_description()
        self.result.config(text=result)
        self.result.pack()

    def options(self):
        """Создает поле ввода, текст и кнопку"""
        shapes = list(self.shapes[self.shape].keys())
        self.clear_options()
        for i in range(2, len(shapes)):
            l = Label(self.button_frame, text=shapes[i])
            e = Entry(self.button_frame, bd=5)
            l.pack()
            e.pack()

        button = Button(self.button_frame, text='рассчитать', command=self.click_button)
        button.pack()
        self.button_frame.pack()


app = App()
app.mainloop()
