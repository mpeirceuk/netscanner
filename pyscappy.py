import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scapy.all import *


# Function to update the plot with new data
def animate(i, xs, ys):
    # Read the number of packets in the last second
    pkts = sniff(count=0, timeout=1)
    xs.append(i)
    ys.append(len(pkts))

    # Limit the number of data points shown to improve performance
    xs = xs[-400:]
    ys = ys[-400:]

    # Update the plot
    ax.clear()
    ax.plot(xs, ys)
    plt.xlabel('Time (s)')
    plt.ylabel('Number of Packets')
    plt.title('Network Traffic Analysis')
    plt.grid(True)


# Initialize lists to store data
xs = []
ys = []

# Set up the plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)

# Start sniffing traffic
plt.show()
