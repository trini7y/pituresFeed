'''Created By Okeke Desmond
    date : 18 - 04 - 2019
    twitter: @okekedesmond
    github: @trini7y
'''
import pygame
import pygame.camera
from pygame.locals import *
from twython import Twython as Tw
from time import sleep
import RPi.GPIO as gpio
from api_details import *

# Setup the gpio on the raspberry pi 
gpio.setmode(gpio.BCM)
gpio.setup(8, gpio.IN)

#initialize pygames for camera modules
pygame.init()
pygame.camera.init()

# setup the camera connected path
cam = pygame.camera.Camera("/dev/video0",(1840,680))

def tweetPicture():
    # input a tweet
    tweet = str(input("Update your tweet: "))
    time = 10
    print('Please wait for', time , ' seconds')
    sleep(time)
    cam.start()
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
    
while True:
    input_value = gpio.input(8)
    if input_value == gpio.HIGH:
        sleep(5)
        tweetPicture()
    else:
        print('Nothing was pressed')
        tweetPicture()
        break


#shut down the camera
cam.stop()
