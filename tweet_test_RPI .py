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
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(8, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(16, gpio.OUT,)

#initialize pygames for camera modules
pygame.init()
pygame.camera.init()

# setup the camera connected path
cam = pygame.camera.Camera("/dev/video0",(1840,680))

print('Click on the button to start up the program')

def tweetPicture():
    # input a tweet
    tweet = str(input("Update your tweet: "))
    time = 10
    print('Please wait for', time , ' seconds for picture to post tweet')
    sleep(time)
    gpio.output(16, 1)
    sleep(2)
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
        print('GETTING READY TO START UP')
        tweetPicture()
        gpio.output(16, 0)
        print('THANK YOU FOR USING TWITTER BOT')
        cam.stop()

#shut down the camera
gpio.cleanup()
