import serial
from platform import system
from itertools import repeat

LED_MATRIX_COLOR_DIFF = 30

class LedMatrix(object):
    def __init__(self, port_address):
        self.port_address = port_address

    def update_hardware(self,packet):
        print 'Sending : %s' % (packet.text,)
        red = packet.red
        green = packet.green
        blue = packet.blue
        if ord(red) <= 255 - LED_MATRIX_COLOR_DIFF:
            red = chr(ord(red)+LED_MATRIX_COLOR_DIFF)
        if ord(blue) <= 255 - LED_MATRIX_COLOR_DIFF:
            blue = chr(ord(blue)+LED_MATRIX_COLOR_DIFF)
        to_send = [red, green, blue, chr(packet.speed)]
        for letter in packet.text:
            to_send.append(letter)
        for _ in repeat(None, 141 - len(packet.text)):
            to_send.append('\n')
        self.port_address.write('*')
        if system() == "Darwin":
            self.port_address.write(to_send)
        else:
            self.port_address.write(str(bytearray(to_send)))


