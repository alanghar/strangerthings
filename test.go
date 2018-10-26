package main

import (
	"fmt"
	"time"
	"unicode"

	"github.com/stianeikeland/go-rpio"
)

var pinBCMMap = map[rune]int{
	'a': 2, 'b': 3, 'c': 4, 'd': 17, 'e': 27, 'f': 22, 'g': 10, 'h': 9, 'i': 11, 'j': 5,
	'k': 6, 'l': 13, 'm': 19, 'n': 26, 'o': 14, 'p': 15, 'q': 18, 'r': 23, 's': 24, 't': 25,
	'u': 8, 'v': 7, 'w': 12, 'x': 16, 'y': 20, 'z': 21,
}

var pinMap = map[rune]rpio.Pin{}

func getPinBCM(letter rune) int {
	return pinBCMMap[unicode.ToLower(letter)]
}

func getPin(letter rune) rpio.Pin {
	return pinMap[unicode.ToLower(letter)]
}

func light(pin rpio.Pin, brightness float64, duration time.Duration) {
	start := time.Now()

	sleepDuration := time.Duration(float64(time.Duration(100)*time.Millisecond) * (1. - brightness))

	for time.Since(start) < duration {
		pin.High()
		time.Sleep(time.Duration(10) * time.Millisecond)
		pin.Low()
		time.Sleep(sleepDuration)
	}
}

func main() {
	fmt.Println("hello world")
	if err := rpio.Open(); err != nil {
		panic(fmt.Sprint("got error", err.Error()))
	}
	defer rpio.Close()

	for letter, pinBCM := range pinBCMMap {
		pin := rpio.Pin(pinBCM)
		pin.Output()
		pinMap[letter] = pin
		pin.Low()
	}

	for {
		for _, pin := range pinMap {
			if _, ok := map[int]bool{17: true, 27: true, 22: true}[int(pin)]; !ok {
				continue
			}
			light(pin, 0.5, time.Duration(1)*time.Second)
		}
		//time.Sleep(time.Duration(2) * time.Second)
	}
}
