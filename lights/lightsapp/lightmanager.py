import RPi.GPIO as GPIO
import time
import random
import datetime
import re
from collections import deque
import threading

class LightManager:
    instance = None

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pinBCMMap = {'a': 3, 'b': 2, 'c': 4, 'd': 14, 'e': 15, 'f': 17, 'g': 18, 'h': 27,
                          'i': 26, 'j': 20, 'k': 16, 'l': 19, 'm': 13, 'n': 12, 'o': 6, 'p': 22, 'q': 23,
                          'r': 21, 's': 24, 't': 10, 'u': 9, 'v': 25, 'w': 8, 'x': 11, 'y': 0, 'z': 5}

        self.pwms = {}
        for letter, pin in self.pinBCMMap.items():
            p = GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
            self.pwms[letter] = GPIO.PWM(pin, 100)
            self.pwms[letter].start(0)

        self.sparkle_pause_count = 0
        self.sparkle_pause_lock = threading.Lock()
        self.spell_queue = deque()
        self.spell_queue_lock = threading.Lock()
        self.current_phrase = ''
        self.thread = threading.Thread(target=self.spellerThread)
        self.thread.start()
        self.pwmthreads = []
        for letter in self.pwms.keys():
            t = threading.Thread(target=self.sparkleThread, args=(letter,))
            self.pwmthreads.append(t)
            t.start()

    def sparkleThread(self, letter):
        while True:
            if self.current_phrase:
                with self.sparkle_pause_lock:
                    #print("Incrementing pause count to %s" % (self.sparkle_pause_count+1))
                    self.sparkle_pause_count += 1
                while self.current_phrase:
                    time.sleep(0.3)
                with self.sparkle_pause_lock:
                    #print("Decrementing pause count to %s" % (self.sparkle_pause_count-1))
                    self.sparkle_pause_count -= 1

            sleeptime =  (0.3 + (random.random() * 3))
            if(random.random() > 0.3):
                self.pwms[letter].ChangeDutyCycle(0)
                self.sleepUnless(sleeptime, lambda: not self.current_phrase)
            else:
                brightness_start = random.random() * 100
                brightness_end = random.random() * 100
                self.rampBrightnessLinear(self.pwms[letter], brightness_start, brightness_end, sleeptime)

    def spellerThread(self):
        phrase = None
        while True:
            with self.spell_queue_lock:
                if self.spell_queue:
                    self.current_phrase = self.spell_queue.popleft()
                    while self.sparkle_pause_count != len(self.pwms.keys()):
                        time.sleep(0.05)
                    print("sparkle count complete")

                    for letter, pin in self.pinBCMMap.items():
                        self.pwms[letter].stop()
                        GPIO.setup(pin, GPIO.OUT)
                        GPIO.output(pin, 0)

                else:
                    if self.current_phrase:
                        for letter, pin in self.pinBCMMap.items():
                            self.pwms[letter] = GPIO.PWM(pin, 100)
                            self.pwms[letter].start(0)
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

    def sleepUnless(self, duration_sec, conditional):
        start = time.time()
        while conditional() and datetime.timedelta(milliseconds=(time.time() - start)*1000.0) < datetime.timedelta(seconds=duration_sec) and not self.current_phrase:
            elapsed = time.time() - start
            if elapsed > duration_sec:
                continue
            time.sleep(0.05)

    def rampBrightnessLinear(self, pwm, start_brightness, end_brightness, duration_sec):
        start = time.time()
        while datetime.timedelta(milliseconds=(time.time() - start)*1000.0) < datetime.timedelta(seconds=duration_sec) and not self.current_phrase:
            elapsed = time.time() - start
            if elapsed > duration_sec:
                continue
            pwm.ChangeDutyCycle(start_brightness + (elapsed / duration_sec)*(end_brightness - start_brightness))
            time.sleep(0.05)

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
            time.sleep(1.5 + (random.random() - 0.5))
            GPIO.output(self.pinBCMMap[letter], 0)

            # Add pause for repeated letters
            if i+1 < len(text) and text[i+1] == letter:
                time.sleep(0.5)

