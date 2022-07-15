import pygame

class Fighter():
    
    def __init__(self,x,y,data,sprite_sheet,animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = False
        self.animation_list = self.load_images(sprite_sheet,animation_steps)
        self.action = 0#0 - стоояние,1 - бег, 2 - прыжок, 3 - атака 4 - атака2 5 - удар 6 - смерть
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x,y,80,180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100


    def load_images(self,sprite_sheet,animation_steps):
        
        animation_list = []
        for y, animation in  enumerate(animation_steps):
            temp_img_list = []
            #звлечь изоброжения из спрайта
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size,y * self.size,self.size,self.size)
                temp_img_list.append(pygame.transform.scale(temp_img,(self.size * self.image_scale,self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        
        return animation_list

    def move(self,screen_width,screen_height,surface,target):
        SPEED = 10

        
        #это мои дельта-переменные, то есть это изменяемые переменные
        GRAVITY = 1
        dx = 0
        dy = 0
        #получить ключить
        key = pygame.key.get_pressed()
        #если ты нажмешь чтото на клавиатуре, это зарегистрирует его в этой переменной

        #может делать действия в том случае,если в дастоящее время атакует 
        if self.attacking == False:
            #движение
                if key[pygame.K_a]:
                    dx = - SPEED

                if key[pygame.K_d]:
                    dx = SPEED
            #Прыжок - если хочешь оставить двойные прыжки см здесь:remove "and self.jump == False"
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -20
                    self.jump = True
            #Атака
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface,target)
                #определить,какой тип атаки был использован
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2


        self.vel_y += GRAVITY
        dy +=self.vel_y
        #игрок остоеться на экране(не уходит за рамки)
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            #и это тоже тогда надо будет удалить!
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
        #это чтоб не проходить через барьер сверху
        if self.rect.top + dy < 0:
            dy = - self.rect.top
        #проверять смотрит ли игроки друг на друга
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        


        self.rect.x += dx
        self.rect.y += dy

    #Значит как будет работать атака
    #так как оба эти бойцы будут исп. рукопашное оружие,я буду проверять,
    #достаточно ли длизок противник в пределах достигаймости, чтоб это сделать я
    #   я слздам атакущий Прямоугольник, который будет проверять столкновениес с врагом

    def attack(self,surface,target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),self.rect.y,2 * self.rect.width,self.rect.height)
        
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
        pygame.draw.rect(surface,(0,255,0),attacking_rect)
    def draw(self,surface):
        img = pygame.transform.flip(self.image, self.flip,False)
        #рисуем красные квадраты
        pygame.draw.rect(surface,(255,0,0),self.rect)
        surface.blit(img,(self.rect.x - (self.offset[0] * self.image_scale),self.rect.y - (self.offset[1] * self.image_scale)))
print("all work corectly, change your py file to the main")
