import serial

def connect_to_rev2(location='/dev/ttyUSB1', baud=4800):
    print 'creating serial connection'
    return serial.Serial(location, baud)
# ser = serial.Serial('/dev/ttyUSB1', 4800)

