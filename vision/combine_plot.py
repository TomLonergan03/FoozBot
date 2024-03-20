import serial
import time
import numpy as np
import matplotlib.pyplot as plt

# Arduino serial communication setup
arduino_ser = serial.Serial('/dev/ttyACM0', 115200)  # Replace '/dev/ttyACM0' with the appropriate port
time.sleep(2)  # Wait for the serial connection to be established

# TF-Luna Mini LiDAR serial communication setup
tfluna_ser = serial.Serial("/dev/ttyS0", 115200, timeout=0)
if tfluna_ser.isOpen() == False:
    tfluna_ser.open()

# Set the distance threshold for detecting spikes (in cm)
threshold = 50

# Plotting setup
plot_pts = 100
fig, axs = plt.subplots(2, 1, figsize=(8, 8))

# Axis formatting for Arduino sensor
axs[0].set_xlabel('Sample', fontsize=12)
axs[0].set_ylabel('Distance (cm)', fontsize=12)
axs[0].set_xlim([0.0, plot_pts])
axs[0].set_ylim([0.0, 500.0])
axs[0].set_title('Arduino Sensor')

# Axis formatting for TF-Luna Mini LiDAR
axs[1].set_xlabel('Sample', fontsize=12)
axs[1].set_ylabel('Distance (cm)', fontsize=12)
axs[1].set_xlim([0.0, plot_pts])
axs[1].set_ylim([0.0, 800.0])
axs[1].set_title('TF-Luna Mini LiDAR')

fig.tight_layout()
fig.canvas.draw()
ax_bgnds = [fig.canvas.copy_from_bbox(ax.bbox) for ax in axs]
lines = [ax.plot(np.zeros((plot_pts,)), linewidth=2.0)[0] for ax in axs]
fig.show()

# Data arrays for updating values
dist_arrays = [np.zeros((plot_pts,)), np.zeros((plot_pts,))]

print('Starting Ranging...')
while True:
    # Read data from Arduino sensor
    if arduino_ser.in_waiting > 0:
        data = arduino_ser.readline().decode('utf-8').strip()
        if data.startswith("Distance: "):
            values = data.split("\t")
            distance_str = values[0].split(": ")[1]
            distance = float(distance_str[:-2])  # Remove the unit "cm" from the string
            dist_arrays[0] = np.roll(dist_arrays[0], -1)
            dist_arrays[0][-1] = distance
            if distance <= threshold:
                print(f"Spike detected on Arduino sensor: {distance} cm")

    # Read data from TF-Luna Mini LiDAR
    counter = tfluna_ser.in_waiting
    bytes_to_read = 9
    if counter > bytes_to_read - 1:
        bytes_serial = tfluna_ser.read(bytes_to_read)
        tfluna_ser.reset_input_buffer()
        if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
            distance = (bytes_serial[2] + bytes_serial[3] * 256) / 100.0
            dist_arrays[1] = np.roll(dist_arrays[1], -1)
            dist_arrays[1][-1] = distance
            if distance <= threshold:
                print(f"Spike detected on TF-Luna Mini LiDAR: {distance} cm")

    # Update plot
    for i in range(2):
        fig.canvas.restore_region(ax_bgnds[i])
        lines[i].set_ydata(dist_arrays[i])
        axs[i].draw_artist(lines[i])
        fig.canvas.blit(axs[i].bbox)
    fig.canvas.flush_events()

    time.sleep(0.01)  # Small delay to avoid excessive CPU usage

arduino_ser.close()
tfluna_ser.close()