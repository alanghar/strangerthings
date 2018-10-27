import RPi.GPIO as GPIO
import time
import re
from collections import deque
import threading

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

        self.spell_queue = deque()
        self.spell_queue_lock = threading.Lock()
        self.current_phrase = ''
        self.thread = threading.Thread(target=self.spellerThread)
        self.thread.start()

    def spellerThread(self):
        phrase = None
        while True:
            with self.spell_queue_lock:
                if self.spell_queue:
                    self.current_phrase = self.spell_queue.popleft()
                else:
                    self.current_phrase = ''

            if self.current_phrase:
                print("Spelling the phrase '%s'" % self.current_phrase)
                self.__spell(self.current_phrase)
            else:
                # Todo: Activate sparkles
                pass

            time.sleep(0.1)


    def enqueuePhrase(self, phrase):
        with self.spell_queue_lock:
            print("Enqueueing the phrase '%s'" % phrase)
            self.spell_queue.append(phrase)


    @staticmethod
    def getInstance():
        if LightManager.instance is None:
            LightManager.instance = LightManager()
        return LightManager.instance

    def setall(self, val):
        for letter, pin in self.pinBCMMap.items():
            GPIO.output(pin, val)

    def flash(self):
        for x in xrange(10):
            self.setall(1)

            time.sleep(0.02)

            self.setall(0)

            time.sleep(0.02)

        self.setall(1)
        time.sleep(0.7)
        self.setall(0)
        time.sleep(1)

    def __spell(self, text):
        text = ''.join([x for x in text.lower() if x in self.pinBCMMap or x == ' '])
        text = re.sub(r'\s+', ' ', text).strip()
        if not text:
            return

        self.flash()

        for i, letter in enumerate(text.lower()):
            if letter == ' ':
                time.sleep(1)
                continue
            GPIO.output(self.pinBCMMap[letter], 1)
            #pwms[pinBCMMap[letter]].ChangeDutyCycle(100)
            time.sleep(1.5)
            GPIO.output(self.pinBCMMap[letter], 0)

            # Add pause for repeated letters
            if i+1 < len(text) and text[i+1] == letter:
                time.sleep(0.5)

