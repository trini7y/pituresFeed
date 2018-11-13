import pygame
import pygame.camera
from pygame.locals import *
from twython import Twython as Tw
from time import sleep
import RPi.GPIO as gpio
from api_details import *

# Setup the gpio on the raspberry pi
gpio.setmode(gpio.BCM)
gpio.setup(6, gpio.IN)
# input a tweet 
tweet = str(input("Update your tweet: "))

#initialize pygames for camera modules
pygame.init()
pygame.camera.init()

# setup the camera connected path
cam = pygame.camera.Camera("/dev/video0",(1840,680))

while True:
    input_value = gpio.input(6)
    if input_value == False:
        sleep(5)
        cam.start()
        print("Upload successful")
    break
        
#get the image taken by the camera
image = cam.get_image()
#save image
pygame.image.save(image,'webcam.jpg')

#twitter api
api = Tw(apiKey,apiSecret,accessToken,accessTokenSecret)

#open saved image
photo = open('webcam.jpg' , 'rb')
pygame.event.pump()

#uploads it to twitter
Tw.update_status_with_media(api, media=photo, status=tweet)

#shut down the camera
cam.stop()
               

