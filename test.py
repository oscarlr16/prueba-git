import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.interpolate import CubicSpline

def fibonacci(n):
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

# Número de términos de Fibonacci a mostrar
n_terms = 10
fib_sequence = fibonacci(n_terms)

fig, ax = plt.subplots()
ax.set_xlim(0, n_terms - 1)
ax.set_ylim(0, max(fib_sequence) + 5)
ax.set_xlabel("Índice")
ax.set_ylabel("Valor de Fibonacci")
ax.set_title("Animación de la Secuencia de Fibonacci con Scatter y Catmull-Rom")

x_data, y_data = [], []
scat = ax.scatter([], [])
line, = ax.plot([], [], 'r-', alpha=0.6)

def catmull_rom_interpolation(x, y):
    if len(x) < 4:
        return x, y  # No se puede hacer interpolación con menos de 4 puntos
    
    # Asegurar que los valores de x sean estrictamente crecientes
    sorted_indices = np.argsort(x)
    x_sorted = np.array(x)[sorted_indices]
    y_sorted = np.array(y)[sorted_indices]
    
    cs = CubicSpline(x_sorted, y_sorted, bc_type='clamped')
    x_interp = np.linspace(min(x_sorted), max(x_sorted), 100)
    y_interp = cs(x_interp)
    return x_interp, y_interp

def update(frame):
    if frame not in x_data:  # Evitar valores duplicados
        x_data.append(frame)
        y_data.append(fib_sequence[frame])
    
    scat.set_offsets(np.c_[x_data, y_data])
    
    if len(x_data) > 3:
        x_interp, y_interp = catmull_rom_interpolation(x_data, y_data)
        line.set_data(x_interp, y_interp)
    
    return scat, line

ani = animation.FuncAnimation(fig, update, frames=n_terms, interval=500, repeat=False)

plt.show()
