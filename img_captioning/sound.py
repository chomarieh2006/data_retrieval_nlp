from pygame import mixer
import time

def alarm():
    mixer.init()
    sound = mixer.Sound("Tornado_Siren_II-Delilah-747233690.mp3")
    sound.play()

    delay