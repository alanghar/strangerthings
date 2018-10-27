import time
import sys
import datetime
import random
import RPi.GPIO as GPIO


def rampBrightnessLinear(pins, start_brightness, end_brightness, duration_sec):
    start = time.time()
    while datetime.timedelta(milliseconds=(time.time() - start)*1000.0) < datetime.timedelta(seconds=duration_sec):
        elapsed = time.time() - start
        if elapsed > duration_sec:
            continue
        for pin in pins:
            pin.ChangeDutyCycle(start_brightness + (elapsed / duration_sec)*(end_brightness - start_brightness))
        time.sleep(0.1)

GPIO.setmode(GPIO.BCM)

alphabet = 'abcdefghijklmnopqrstuvwxyz'

pinBCMMap = {'a': 3, 'b': 2, 'c': 4, 'd': 14, 'e': 15, 'f': 17, 'g': 18, 'h': 27,
             'i': 26, 'j': 20, 'k': 16, 'l': 19, 'm': 13, 'n': 12, 'o': 6, 'p': 22, 'q': 23,
             'r': 21, 's': 24, 't': 10, 'u': 9, 'v': 25, 'w': 8, 'x': 11, 'y': 0, 'z': 5}

# To fix:
# Why is letter 'u' so dim?
# Can I make J brighter? (It has my custom LED)
# Why does the LED in 'i' flicker or go dim?

pwms = {}

for x in pinBCMMap.values():
    p = GPIO.setup(x, GPIO.OUT)
    GPIO.output(x, 0)

#GPIO.cleanup()
#sys.exit()

# num = 28
# GPIO.setup(num, GPIO.OUT)
# p = GPIO.PWM(num, 10)
# p.start(100)


# for letter, pinNum in pinBCMMap.items():
#     freq = 10
#     duty = 0
#     GPIO.setup(pinNum, GPIO.OUT)
#     pwms[pinNum] = GPIO.PWM(pinNum, freq)
#     pwms[pinNum].start(duty)

while True:
    #for pinNum, pwm in pwms.items():
        #freq = random.randint(1, 50)
        #duty = random.random() * 100.0

        #pwms[pinNum].ChangeDutyCycle(duty)
        #pwms[pinNum].ChangeFrequency(freq)
    for letter in alphabet:
        GPIO.output(pinBCMMap[letter], 1)
        #pwms[pinBCMMap[letter]].ChangeDutyCycle(100)
        time.sleep(0.01)
        GPIO.output(pinBCMMap[letter], 0)
        #pwms[pinBCMMap[letter]].ChangeDutyCycle(0)

#    rampBrightnessLinear(pwms.values(), 0.0, 100.0, 3)
#    t = random.random() * 2
#    print("Sleeping %s" % t)
#    time.sleep(t)


GPIO.cleanup()
