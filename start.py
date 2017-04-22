#!/usr/bin/python3

# deamon scrript for piface controll and display


import sys
from time import sleep
import termios

# install python-modules
import contexlib

# install install python{,3}-pifacecad
import pifacecad

# install omxplayer-wrapper
from omxplayer import OMXPlayer

player = None
mode = None

radioStations = {
    "Radio Mars":"http://frekvenca.eu:8000/radiomars.mp3",
    "FM4":"http://mp3stream1.apasf.apa.at:8000/;listen.pls"
}

currentStation = None

# update current screen text on piface button pressed
# screen is 2 x 24 ?
def update_pin_text(event):
    event.chip.lcd.set_cursor(13, 0)
    event.chip.lcd.write(str(event.pin_num))

    # write mode to screen

    # write mode screenValue to screen

    

def play_mp3(event):
    print("Play mp3")

    global player
    global mode

    if player is not None:
        print("Already playing - quit")
        player.quit()
        player = None
        mode = None
    else:
        print("Start player")
        player = OMXPlayer('/home/pi/mp3/Beck.mp3')
        player.pause()
        mode = "MP3"
        player.play()
        print("Play")


# action play radio
# when in radio mode and pressed radio is stopped
def play_radio(event):
    print("Play radio")
      

    global player
    global mode
    global currentStation

    
    if player is not None:
        print("Already playing - quit")
        player.quit()
        player = None
        mode = None
    else:
        print("Start online radio player")

        for key, value in radioStations.items():
            player = OMXPlayer(value)

            print(key)
            currentStation = key
            
            break
            
        player.pause()

        mode = "radio"
        player.play()
        print("Play")


# previous button on piface control
def previousAction(event):
    print("Previous")
    
    global mode 
    global currentStation
    
    if mode == 'radio':

        previousStationUrl = None
        previusStation = None
        
        for key, value in radioStations.items():

            if key == currentStation:
                break;

            previousStationUrl = value
            previousStation = key


        currentStation = previousStation
        player = OMXPlayer(previousStationUrl)

        print(currentStation)

        
# next button on piface control        
def nextAction(event):
    print("Next")

    global player
    global mode
    global currentStation

    nextStationUrl = None
    nextStation = None

    found = False
    
    if mode == 'radio':

        for key, value in radioStations.items():

            if found == True:
                nextStationUrl = value
                nextStation = key
                break;
            
            if key == currentStation:
                found = True


        player.stop()            
        currentStation = nextStation
        player.load(nextStationUrl)
        player.play()
    
        print(currentStation)
        
piface = pifacecad.PiFaceCAD()  # initialize a PiFace Control and Display board
    
# basic buttuns handling
listener = pifacecad.SwitchEventListener(chip=piface)

#for i in range(1,8):
#    listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)

listener.register(0, pifacecad.IODIR_FALLING_EDGE, play_mp3)
listener.register(1, pifacecad.IODIR_FALLING_EDGE, play_radio)

listener.register(6, pifacecad.IODIR_FALLING_EDGE, previousAction)
listener.register(7, pifacecad.IODIR_FALLING_EDGE, nextAction)


listener.activate()

