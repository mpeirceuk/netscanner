import numpy as np
import matplotlib.pyplot as plt

def plot_mandelbrot(mandelbrot_set, xmin, xmax, ymin, ymax):
    plt.imshow(mandelbrot_set, extent=[xmin, xmax, ymin, ymax], cmap='hot', origin='lower')
    plt.colorbar(label='Iterations')
    plt.title('Mandelbrot Set')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.show()

def main():
    xmin, xmax = -2.0, 1.0
    ymin, ymax = -1.5, 1.5

    # Load pre-computed Mandelbrot set data
    mandelbrot_set = np.load('mandelbrot.npy')

    plot_mandelbrot(mandelbrot_set, xmin, xmax, ymin, ymax)

if __name__ == "__main__":
    main()
