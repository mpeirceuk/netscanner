import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scapy.all import *
import sqlite3

# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('sniffchannels.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS packets
                 (id INTEGER PRIMARY KEY, time FLOAT, src_ip TEXT, dst_ip TEXT, src_port INTEGER, dst_port INTEGER, 
                 protocol TEXT, mac_src TEXT, mac_dst TEXT, data BLOB, channel INTEGER)''')  # Added channel column
    conn.commit()
    conn.close()

# Function to update the plot with new data and store packet data in the database
def animate(i, xs, ys):
    # List of Wi-Fi channels to scan
    wifi_channels = range(1, 12)  # Scan channels 1 to 11

    # Initialize dictionary to store packet counts per channel
    pkts_count = {}

    # Sniff traffic on each channel
    for channel in wifi_channels:
        pkts = sniff(count=0, timeout=1, iface='wlan0mon', prn=lambda x: packet_handler(x, channel))

        # Count the number of packets
        pkts_count[channel] = len(pkts)

        # Store packet data in the database
        conn = sqlite3.connect('sniffchannels.db')
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
                # Include channel information in the database
                c.execute("INSERT INTO packets (time, src_ip, dst_ip, src_port, dst_port, protocol, mac_src, mac_dst, data, channel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                          (time, src_ip, dst_ip, src_port, dst_port, protocol, mac_src, mac_dst, data, channel))
        conn.commit()
        conn.close()

    # Update the plot
    xs.append(i)
    ys.append(pkts_count)
    xs = xs[-400:]
    ys = ys[-400:]

    ax.clear()
    ax.plot(xs, ys)
    plt.xlabel('Time (s)')
    plt.ylabel('Number of Packets')
    plt.title('Network Traffic Analysis')
    plt.grid(True)

# Packet handler function
def packet_handler(pkt, channel):
    pkt.channel = channel  # Add channel attribute to the packet

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
