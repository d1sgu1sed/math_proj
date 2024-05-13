import matplotlib
import matplotlib.pyplot as plt
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import numpy as np



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


def func(x):
    return -(4 * x + 18) ** 2

def main(page: ft.Page):
    matplotlib.use('agg')
    plt.grid(True)
    x = np.arange(-30, 30, 0.1)
    f1 = -(x - 2) ** 2
    plt.plot(x, f1)
    plt.axvline(x=biss(func, (-1, 5)))
    page.add(MatplotlibChart(plt, expand=True))

if __name__ == "__main__":
    s = input("Введите функцию: ")
    ft.app(target=main)