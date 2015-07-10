from glob import glob
from platform import system
import serial

BAUD_RATE = 115200
TIMEOUT = 0

def get_available_ports():
    if system() == "Darwin":
        port_address = '/dev/tty.*'
    else:
        port_address = '/dev/tty[A-Za-z]*'
    return glob(port_address) 

def get_matrix_port():
    current_ports = get_available_ports()
    print 'Available Ports are : \n%s\n' % (current_ports,)
    
    potential_ports = []
    for port in current_ports:
        if system() == "Darwin" and 'Bluetooth' not in port or system() != "Darwin" and 'ACM' in port:
            potential_ports.append(port) 
    print '\nMatrix Port: \n%s\n' % (potential_ports[0],)
    return serial.Serial(potential_ports[0], BAUD_RATE, timeout=TIMEOUT, writeTimeout=TIMEOUT)

def main():
    print get_matrix_port()

if __name__ == "__main__":
    main()
