import serial
import time

# Configure the serial port
ser = serial.Serial('/dev/ttyACM0', 115200)  # Replace '/dev/ttyACM0' with the appropriate port

# Wait for the serial connection to be established
time.sleep(2)

while True:
    if ser.in_waiting > 0:
        # Read the data from the serial port
        data = ser.readline().decode('utf-8').strip()
        
        # Check if the data contains the expected format
        if data.startswith("Distance: "):
            # Extract the values from the data string
            values = data.split("\t")
            distance = values[0].split(": ")[1]
            strength = values[1].split(": ")[1]
            temp = values[2].split(": ")[1]
            
            # Print the extracted values
            print("Distance:", distance, "cm")
            print("Strength:", strength)
            print("Temperature:", temp)
            print("---")
    
    # Add a small delay to avoid excessive CPU usage
    time.sleep(0.1)