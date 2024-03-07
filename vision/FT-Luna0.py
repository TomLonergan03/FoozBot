import serial

ser = serial.Serial("/dev/ttyS0", 115200) #might not be this port, need to be changed, find serial port path
def read_data():
    while True:
        counter = ser.in_waiting #count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                print("TF-Luna python3 portion")
                distance = bytes_serial[2] + bytes_serial[3]*256
                strength = bytes_serial[4] + bytes_serial[5]*256
                temperature = bytes_serial[6] + bytes_serial[7]*256
                temperature = (temperature/8) - 256
                print("Distance:"+str(distance))
                print("Strength:"+str(strength))
                if temperature!= 0:
                    print("Chip Temperature:"+str(temperature))
                ser.reset_input_buffer()

if __name__ == "__main__":
    try:
        if ser.isOpen() == False:
            ser.open()
        read_data()
    except KeyboardInterrupt():
        if ser != None:
            ser.close()
            print ("program is interrupted by user")


            
