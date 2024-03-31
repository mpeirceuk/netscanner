import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scapy.all import *
import sqlite3

# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('packadmin.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS packets
                 (id INTEGER PRIMARY KEY, time FLOAT, src_ip TEXT, dst_ip TEXT, src_port INTEGER, dst_port INTEGER, 
                 protocol TEXT, mac_src TEXT, mac_dst TEXT, data BLOB)''')
    conn.commit()
    conn.close()

# Function to update the plot with new data and store packet data in the database
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

    # Store packet data in the database
    conn = sqlite3.connect('packadmin.db')
    c = conn.cursor()
    for pkt in pkts:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            if TCP in pkt:
                src_port = pkt[TCP].sport
                dst_port = pkt[TCP].dport
                protocol = "TCP"
            elif UDP in pkt:
                src_port = pkt[UDP].sport
                dst_port = pkt[UDP].dport
                protocol = "UDP"
            else:
                src_port = 0
                dst_port = 0
                protocol = "Other"
            time = pkt.time
            mac_src = pkt.src
            mac_dst = pkt.dst
            data = bytes(pkt)
            c.execute("INSERT INTO packets (time, src_ip, dst_ip, src_port, dst_port, protocol, mac_src, mac_dst, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (time, src_ip, dst_ip, src_port, dst_port, protocol, mac_src, mac_dst, data))
    conn.commit()
    conn.close()

# Initialize lists to store data
xs = []
ys = []

# Initialize the database
initialize_database()

# Set up the plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)

# Start sniffing traffic
plt.show()
