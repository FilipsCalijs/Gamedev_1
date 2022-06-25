#ОБЫЧНО КОНСТАНТЫ ПИШУТЬСЯ С БОЛЬШИМ РЕГИСТРОМ

import pygame
import os

pygame.init()

#поставить фпс

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Fortbite Season 0")

#определять перемнные действий персонажа
clock = pygame.time.Clock()
FPS = 60

#игровые парамитры
GRAVITY = 0.55

moving_right = False
moving_left = False

#загрузка изоброжений



BG = (144,201,120)
RED = (255,0,0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

   
class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,scale,speed):
        
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.jump = False
        self.in_air = True
        self.vel_y = 0
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0


        animation_types = ["Idle","Run","Jump"]
        for animation in animation_types:
            #сбросить список изоброжений
            temp_list = []
            #кол-во файлов в папке
            num_of_frames = len(os.listdir(rf"B:\promma\python\game\fortbite\img\{self.char_type}\{animation}"))
            for i in range(num_of_frames):
            #f озночает. что если я добавлю мигурные скобки то помещю туда переменную
                img = pygame.image.load(rf"B:\promma\python\game\fortbite\img\{self.char_type}\{animation}\{i}.png")
                #масштабирыванние
                img = pygame.transform.scale(img,(int(img.get_width() * scale),int(img.get_height()* scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
        self.image = self.animation_list[self.action][self.frame_index]
        #расположение игрока
        #важное!!!
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def move(self, moving_left, moving_right): 
        #нужны для проверки с столкновением 
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = -1

        #прыжок
            
        if self.jump == True and self.in_air == False:
           self.vel_y = -11 
           self.jump = False
           self.in_air = True
        #незабыть про гравитацию
                    
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #ПРОВЕРЯТЬ СТАЛКНОВЕНИЕ С ПОЛОМ
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
    

        
        #обновлять позицию
        self.rect.x += dx
        self.rect.y += dy
    def draw(self):   #
         screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

    def update_animation(self):
        #обновление кадров
        ANIMATION_COOLDOWN = 100
        
         #если анимация подошла к концу, то вернутьсяк старту
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        #обновлять картинку взависимости от текущего кадра
        self.image = self.animation_list[self.action][self.frame_index]
       
        
        
        #роверяем, если достаточно времени прошло с предыдущего упдайта
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
    def update_action(self,new_action):
        #проверять если новое действие другое чем предыдущее
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        
player = Soldier("player",300,200,3,5)
player2 = Soldier("player",200,100,3,5)    
enemy = Soldier("enemy",100,90,3,5)
run = True
while run:
    draw_bg()
    clock.tick(FPS)

    player.update_animation()
    #player2.update_animation()
    
    player.draw()
    #player2.draw()
    player.update_animation()
    enemy.draw()
    if player.alive:
        if player.in_air :
            player.update_action(2)# 2 озночает активацию прыжка
        elif moving_left or moving_right:
            player.update_action(1)# 1 озночает активацию бега
            #player2.update_action(1)
        else:
            player.update_action(0)# 0 озночает активацию стояние
            # player2.update_action(1)
    else:
        pass
    player.move(moving_left, moving_right)
    #player2.move(moving_left, moving_right)
    
    
   
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
        #клавиши и действия от них 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True 
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
            
        #клавиши и действия когда отпускаешь клавишу  
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False   
    
    pygame.display.update()

pygame.quit()
