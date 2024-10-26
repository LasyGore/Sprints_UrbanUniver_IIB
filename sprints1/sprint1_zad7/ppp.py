import matplotlib.pyplot as plt
import numpy as np

ggg='fivethirtyeight'
# Пример данных
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Использование стиля
plt.style.use(ggg)

plt.plot(x, y)
plt.title("Пример графика с использованием стиля 'fivethirtyeight'")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()