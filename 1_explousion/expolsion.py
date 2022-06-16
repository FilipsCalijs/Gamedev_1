import pygame
from pygame.locals import *
pygame.init()
#стандартная структура

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((600,800))

bg = (50,50,50)

def draw_bg():
    screen.fill(bg)

#создать класс который вызывает Взрыв (exposion)
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):#кол-во картинок в спрайте
            img = pygame.image.load(f"img/exp{num}.png")
            img = pygame.transform.scale(img,(100,100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]                #позиция
        self.counter = 0
    def update(self):
        explosion_speed = 4 #скорость с которой он будет менять спрайт
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:#как он будет переключаться 
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        #если анимация закончена, переустановить индекс анимации
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()



explosion_group = pygame.sprite.Group()


run = True
while run:

    clock.tick(fps)

	#draw background
    draw_bg()

    explosion_group.draw(screen)
    explosion_group.update()


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()#узнаешь позицию мыши
            explosion = Explosion(pos[0],pos[1])#передаешь позицию в експлосион (а именно 0 это х а 1 это у)
            explosion_group.add(explosion)




    pygame.display.update()
        


pygame.quit()

