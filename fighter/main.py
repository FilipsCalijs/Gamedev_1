import pygame
pygame.init

#CREATE GAME WINDOW
SCREEN_WIDTH = 1000
CREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, CREEN_HEIGHT))
pygame.display.set_caption("Street Fighter")

bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image,(SCREEN_WIDTH, CREEN_HEIGHT))
    screen.blit(scaled_bg,(0,0))

run = True
while run:


    #BG
    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    #оьновлять дислей
    

    pygame.display.update()


    pygame.display.flip()

pygame.quit()
