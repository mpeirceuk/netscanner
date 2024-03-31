import numpy as np

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def generate_mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    mandelbrot_set = np.zeros((height, width), dtype=int)

    for i in range(height):
        for j in range(width):
            c = complex(x[j], y[i])
            mandelbrot_set[i, j] = mandelbrot(c, max_iter)

    return mandelbrot_set

def main():
    xmin, xmax = -1.0, 0.5
    ymin, ymax = -1.5, 1.0
    width, height = 1000, 1000  # Reduced resolution
    max_iter = 2000  # Reduced maximum iterations

    mandelbrot_set = generate_mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)

    np.save('mandelbrot.npy', mandelbrot_set)
    print("Mandelbrot set data saved to mandelbrot.npy")

if __name__ == "__main__":
    main()
