from random import random
import time
import numpy as np
import matplotlib.pyplot as plt


def func(x, a, b, c):
    return a * (b + random()) * x ** 2 + b * x + c


num_iters = 10000

start = time.time()
for i in range(num_iters):
    x = np.linspace(0, 4, 50)

    y = func(x, 2.5, 1.3, 0.5)

    rng = np.random.default_rng()

    y_noise = 0.2 * rng.normal(size=x.size)

    y = y + y_noise

    result = np.polyfit(x, y, 6)

end = time.time()
period = (end - start) / num_iters
print(str(round(period, 8)) + " seconds per cycle")
print(str(round(1 / period)) + " per second")
print(str(round((end - start), 2)) + " seconds total")

plt.scatter(x, y, label='data')
x = list(x)
n = 10
for i in range(n):
    x.append(n + i)
plt.plot(x, np.polyval(result, x), 'r-', label='fit')
plt.show()


"""
def func(x, a, b, c):
    return a * x ** 2 + b * x + c


x = np.linspace(0, 4, 50)

y = func(x, 2.5, 1.3, 0.5)

rng = np.random.default_rng()

y_noise = 0.2 * rng.normal(size=x.size)

y = y + y_noise

result = np.polyfit(x, y, 3)

plt.scatter(x, y, label='data')
x = np.concatenate((x, np.linspace(4, 8, 50)))
plt.plot(x, np.polyval(result, x), 'r-', label='fit')
plt.show()
"""
