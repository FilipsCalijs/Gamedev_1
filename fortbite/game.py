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
shoot = False

#загрузка изоброжений

bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

BG = (144,201,120)
RED = (255,0,0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

   
class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,scale,speed,ammo ):
        
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.jump = False
        self.ammo = ammo
        self.start_ammo = ammo
        self.in_air = True
        self.vel_y = 0
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0


        animation_types = ["Idle","Run","Jump","Death"]
        for animation in animation_types:
            #сбросить список изоброжений
            temp_list = []
            #кол-во файлов в папке
            num_of_frames = len(os.listdir(rf"B:\promma\python\game\fortbite\img\{self.char_type}\{animation}"))
            for i in range(num_of_frames):
            #f озночает. что если я добавлю мигурные скобки то помещю туда переменную
                img = pygame.image.load(rf"B:\promma\python\game\fortbite\img\{self.char_type}\{animation}\{i}.png").convert_alpha()
                #масштабирыванние
                img = pygame.transform.scale(img,(int(img.get_width() * scale),int(img.get_height()* scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
        self.image = self.animation_list[self.action][self.frame_index]
        #расположение игрока
        #важное!!!
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        self.update_animation()
        self.check_alive()
        #обновлять КД
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
    
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
            self.direction = 1

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


    def shoot(self):
            if self.shoot_cooldown == 0 and self.ammo > 0:
                self.shoot_cooldown = 20
                bullet = Bullet(player.rect.centerx + (0.6 * self.rect.size[0] * self.direction),self.rect.centery,self.direction )
                bullet_group.add(bullet)
                self.ammo -= 1 
        
        
    def draw(self):   #
         screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

    def update_animation(self):
        #обновление кадров
        ANIMATION_COOLDOWN = 100
        
         #если анимация подошла к концу, то вернутьсяк старту
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
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


    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #удалять пули
        self.rect.x += (self.direction * self.speed)
        #проверять если пуля ушла за экран
        if self.rect.right < 0  or self.rect.left > SCREEN_WIDTH:
            self.kill()

        #проверять сталкевония с персонажами
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                self.kill()
                player.health -= 5
                
                
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                self.kill()
                enemy.health -= 25
                
        
#создать группу спрйтов
bullet_group = pygame.sprite.Group()


        
    
player = Soldier("player",300,200,3,5,20)
player2 = Soldier("player",200,100,3,5,20)    
enemy = Soldier("enemy",200,245,3,5,1000)
run = True
while run:
    draw_bg()
    clock.tick(FPS)

    player.update()
    #player2.update_animation()

   
    player.draw()
    #player2.draw()
    player.update_animation()
    enemy.draw()
    enemy.update()

    bullet_group.update()
    bullet_group.draw(screen)
    
    if player.alive:
        if shoot:
            player.shoot()
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
            if event.key == pygame.K_SPACE:
                print("space")
                shoot = True   
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
            if event.key == pygame.K_SPACE:
                shoot = False
                print("stop")
    
    pygame.display.update()

pygame.quit()
