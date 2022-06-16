import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("background in 3d")

#найти игровые переменные
scroll = 0
#загружаем и ставим картинку с ground

ground_image = pygame.image.load("ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

## создоем список с нашими изоброжениями и загружаем его сюда
bg_images = []
for i in range(1,6):
    bg_image = pygame.image.load(f'plx-{i}.png').convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

def draw_bg():
    for x in range(10):#это повторяет картинку с лева и с права
        speed = 1
        for i in bg_images:
            screen.blit(i,((x * bg_width)- scroll * speed,0))
            speed += 0.1 

def draw_ground():
    for x in range(25):
        screen.blit(ground_image, ((x * ground_width) - scroll * 1.5, SCREEN_HEIGHT - ground_height))

run = True
while run:
    clock.tick(FPS)


    #рисовать мир
    draw_bg()
    draw_ground()

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 5
    if key[pygame.K_RIGHT] and scroll < 3000:
        scroll += 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
