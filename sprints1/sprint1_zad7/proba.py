import numpy as np
import matplotlib.pyplot as plt

# функция y = sin(x)
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

# нарисовать график в виде отдельных точек, в форме "0"
plt.plot(x, y, 'ro')

# сохранить рисунок в формат SVG
plt.savefig('matplotlib_sin_x_red_dots.svg')

# показать интерактивное окно с графиком
plt.show()