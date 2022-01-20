#!/usr/bin/env python

import random
import time
import os
import signal
import datetime


from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, rotate=1)


WORDS = {
  "a":["0 0"],
  "_five":["0 2","1 2","2 2","3 2"],
  "_ten":["1 0","3 0","4 0"],
  "_quarter":["0 1","1 1","2 1","3 1","4 1","5 1","6 1"],
  "_twenty":["1 0","2 0","3 0","4 0","5 0","6 0"],
  "_half":["4 2","5 2","6 2","7 2"],
  "past":["1 3","2 3","3 3","4 3"],
  "to":["4 3","5 3"],
  "one":["1 7","4 7","7 7"],
  "two":["0 6","1 6","1 7"],
  "three":["3 5","4 5","5 5","6 5","7 5"],
  "four":["0 7","1 7","2 7","3 7"],
  "five":["0 4","1 4","2 4","3 4"],
  "six":["0 5","1 5","2 5"],
  "seven":["0 5","4 6","5 6","6 6","6 7"],
  "eight":["3 4","4 4","5 4","6 4","7 4"],
  "nine":["4 7","5 7","6 7","7 7"],
  "ten":["7 4","7 5","7 6"],
  "eleven":["2 6","3 6","4 6","5 6","6 6","7 6"],
  "twelve":["0 6","1 6","2 6","3 6","5 6","6 6"]
};


def isInternet():
  print ("Check Internet!")  
  host_up = True if os.system("ping -c 1 " + "heise.de" ) is 0 else False
  if (not host_up):
    device.contrast(40)  
    msg = "No Internet ... No Internet ... No Internet"
    show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT), scroll_delay=0.05)
    device.contrast(4)  


def receiveSignal(signalNumber, frame):
  print("Received:", signalNumber)
  animation()
  raise SystemExit('Exiting')
  return


def animation():
# while True:
  for z in range(30):
    with canvas(device) as draw:
      for i in range(4):
        x = random.randint(0, device.width)
        y = random.randint(0, device.height)
        draw.point((x, y), fill="red")
    time.sleep(0.05)


def printWords (words):
  with canvas(device) as draw:
    for name in words:  
      word = WORDS[name]
      for i in range(len(word)):
        pos = word[i].split()
        x = int(pos[0])
        y = int(pos[1])
        draw.point((x, y), fill="green")


def timeToWords(h,m):
  mins = ["","_five","_ten","_quarter","_twenty","_twenty _five","_half"]
  hours = ["", "one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve"]
  words = ""
  midx = round(m/5)
  hidx = h

  if (midx > 6):
    if (midx == 12):
      midx = 0
    hidx += 1

  hidx = hidx % 12

  if (hidx == 0):
    hidx = 12    

  if (midx != 0):
    if (midx <= 6):
      words = mins[midx] + " past " + hours[hidx]
    else:  
      words = mins[12-midx] + " to " + hours[hidx]
  else:
    words = hours[hidx]  

  #print("Time: %d:%d   hdix: %d  midx: %d " % (h, m, hidx, midx))
  #print(words)

  return words.split()

# Main 

signal.signal(signal.SIGTERM, receiveSignal)

now = datetime.datetime.now()
exactHour=now.hour

animation()

n = 0
while True:
  now = datetime.datetime.now()

  if (exactHour != now.hour):
    exactHour = now.hour
    animation()

  words = timeToWords(now.hour, now.minute)
  printWords(words)

#  n += 1
#  if( n == 150 ): 
#    n = 0    
#    isInternet() 
      
  time.sleep(4.00)
 
  print (n)
