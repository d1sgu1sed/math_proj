import matplotlib
import matplotlib.pyplot as plt
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import numpy as np
import sympy as sp


def biss(func, bounds, eps=1e-5):
    a, b = bounds
    x0 = (a + b) / 2
    if func(a) * func(b) > 0:
        while abs(a - b) >= eps:
            if abs(func(x0)) > abs(func(x0 + eps)):
                a = x0
            else:
                b = x0
            x0 = (a + b) / 2
        return x0
    else:
        while abs(a - b) >= eps:
            if func(a) * func(x0) > 0:
                a = x0
            else:
                b = x0
            x0 = (a + b) / 2
        return x0


def get_func_str():
    x = sp.symbols('x')
    expr = sp.sympify(input_str)
    func = sp.lambdify(x, expr, "numpy")
    return func


def main(page: ft.Page):
    matplotlib.use('agg')
    plt.grid(True)

    #Получаем функцию и корень функции
    func = get_func_str()
    x_ans = biss(func, bounds, abs(int(eps))) if eps else biss(func, bounds)

    #Получаем границы для отрисовки
    x = np.arange(bounds[0] - 10, bounds[1] + 10, 0.1)
    plt.plot(x, func(x))

    #Рисуем начальные оси графика
    plt.axhline(0, color='green',linewidth=1.5)
    plt.axvline(0, color='green',linewidth=1.5)

    #Блок для отрисовки вертикальной оси от корня
    func_ans = func(x_ans)
    y_min, y_max = plt.ylim()
    normalized_y_start = (func_ans - y_min) / (y_max - y_min)

    plt.axvline(x=x_ans, 
                ymin = 0 if func_ans > 0 else normalized_y_start, 
                ymax = normalized_y_start if func_ans > 0 else 1, 
                color='k', linestyle='--', label=f'x = {x_ans}')
    
    x_min, x_max = plt.xlim()
    normalized_x_start = (x_ans - x_min) / (x_max - x_min)

    #Блок для отрисовки горизонтальной оси от корня
    plt.axhline(y=func_ans, 
                xmin=normalized_x_start if x_ans < 0 else 0, 
                xmax=1 if x_ans < 0 else normalized_x_start, 
                color='k', linestyle='--')

    #Отрисовываем корень на графике и нижний заголовок, выводим график
    plt.scatter([x_ans], [func_ans], color='red', zorder=5)
    plt.xlabel("x = {}          f(x) = {}".format(round(x_ans, 4), round(func(x_ans), 4)))
    # print(str(x_ans) + ':' + str(func(x_ans)))
    page.add(MatplotlibChart(plt, expand=True))

if __name__ == "__main__":
    input_str = input("Введите функцию: ")
    bounds = list(map(int, input('Введите границы для поиска(рациональные значения): ').split()))
    eps = input('Введите погрешность или нажмите Enter для стандартного значения(1e-5): ')
    ft.app(target=main)