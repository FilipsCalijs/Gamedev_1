import pygame,sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption('НЕТ НИКОКИХ НОРМАЛЬНЫХ ИДЕЙ, ИЗ ЗА ЭТОГО ПУСЬ БУДЕТ ТАК')
WINDOW_SIZE = (1600,900 )
screen = pygame.display.set_mode(WINDOW_SIZE)


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()   
            sys.exit()

    pygame.display.update()
    clock.tick(60)#это кадры в сек или фпс


#скелет сайта
