import pygame
import time
import os

pygame.init()
pygame.mixer.init()
print('Mixer inited')

try:
    pygame.mixer.music.load('/tmp/test.mp3')
    print('Loaded')
    pygame.mixer.music.play()
    print('Playing')
    time.sleep(3)
except Exception as e:
    print(f'Error: {e}')