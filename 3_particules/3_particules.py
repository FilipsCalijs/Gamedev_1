import pygame, sys, random

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Частитсы")
screen = pygame.display.set_mode((500,500),0,32)

particles = []



while True:

    screen.fill((43,43,43))
    mx, my = pygame.mouse.get_pos()
                              #3 значение это скорость по х оси, а 4 это таймер ([месторосположение,формы,таймер])
    particles.append([[mx, my], [random.randint(1,20) /10 - 1, -2], random.randint(4,6)])

    for particle in particles:
            particle[0][0] += particle[1][0]
            #по иси х(250) добовляем скорость
            particle[0][1] += particle[1][1]
            #по иси y(250) добовляем четвертый аргумент
            particle[2] -= 0.1
            # это по моему таймер(отщет времени)
            particle[1][1] += 0.005
            pygame.draw.circle(screen, (0, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                particles.remove(particle)
                
    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    pygame.display.update()
    mainClock.tick(60)
                

                
                
#свойства честиц(partclies)
#обычно крутьиться где то рядом
#обычно меняеться раз в какоето время
#и обычно исчезает через каоета время

#из за этого лучше использовать [месторосположение,формы,таймер]
