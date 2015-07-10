class Packet(object):

    def __init__(self, speed, color, text):
        self.length = len(text)
        self.speed = speed
        self.red, self.green, self.blue = color
        self.text = text
        