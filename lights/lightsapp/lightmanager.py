import RPi.GPIO as GPIO
import time

class LightManager:
    instance = None

    def __init__(self):
        print("Init LightManager")
        GPIO.setmode(GPIO.BCM)
        self.pinBCMMap = {'a': 3, 'b': 2, 'c': 4, 'd': 14, 'e': 15, 'f': 17, 'g': 18, 'h': 27,
                          'i': 26, 'j': 20, 'k': 16, 'l': 19, 'm': 13, 'n': 12, 'o': 6, 'p': 22, 'q': 23,
                          'r': 21, 's': 24, 't': 10, 'u': 9, 'v': 25, 'w': 8, 'x': 11, 'y': 0, 'z': 5}

        for x in self.pinBCMMap.values():
            p = GPIO.setup(x, GPIO.OUT)
            GPIO.output(x, 0)

    @staticmethod
    def getInstance():
        if LightManager.instance is None:
            LightManager.instance = LightManager()
        return LightManager.instance

    def spell(self, text):
        print("Spelling %s" % text)
        text = ''.join([x for x in text.lower() if x in self.pinBCMMap])
        for i, letter in enumerate(text.lower()):
            GPIO.output(self.pinBCMMap[letter], 1)
            #pwms[pinBCMMap[letter]].ChangeDutyCycle(100)
            time.sleep(1.5)
            GPIO.output(self.pinBCMMap[letter], 0)

            # Add pause for repeated letters
            if i+1 < len(text) and text[i+1] == letter:
                time.sleep(0.5)

