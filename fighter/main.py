import pygame
from fighter import Fighter

pygame.init()
SCREEN_WIDHT = 1000
SCREEN_HAIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDHT,SCREEN_HAIGHT))
pygame.display.set_caption("Уличный Бой: I")
#картинка для заднего фона
#эта для мака
#bg_image = pygame.image.load(rf"/Users/Filip/Desktop/Programma/python/gamedev/fighter/assets/images/background/background.jpg").convert_alpha()
#Windows
bg_image = pygame.image.load(rf"B:\promma\python\game\fighter\assets\images\background\background.jpg").convert_alpha()
#загружать spritesheets
warrior_sheet = pygame.image.load(rf"B:\promma\python\game\fighter\assets\images\warrior\Sprites\warrior.png").convert_alpha()
wizard_sheet = pygame.image.load(rf"B:\promma\python\game\fighter\assets\images\wizard\Sprites\wizard.png").convert_alpha()



#найти количество кадров в анимции
WARRIOR_ANIMATION_STEPS = [10,8,1,7,7,3,7]
WIZARD_ANIMATION_STEPS = [8,8,1,8,8,3,7]

clock = pygame.time.Clock()
FPS = 60

RED =(255,0,0)
YELLOW =(255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,128,0)


#определять переменные бойцев
WARRIOR_SIZE =162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72,56]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112,107]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

#функция для прорисовки БГ
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image,((SCREEN_WIDHT,SCREEN_HAIGHT)))
    screen.blit(scaled_bg,(0,0))
    
#функция для прорисовки атки бара здоровье
def draw_health_bar(health,x,y):
    ratio = health / 100
    pygame.draw.rect(screen,BLACK,(x - 2,y -2,404,34))
    pygame.draw.rect(screen,RED,(x,y,400,30))
    pygame.draw.rect(screen,GREEN,(x,y,400 * ratio,30))
    
fighter_1 = Fighter(200,310,WARRIOR_DATA,warrior_sheet,WARRIOR_ANIMATION_STEPS,)
fighter_2 = Fighter(500,310,WIZARD_DATA, wizard_sheet,WIZARD_ANIMATION_STEPS)
run = True
while run:

    clock.tick(FPS)
    
    draw_bg()

    #статистика персонажа
    draw_health_bar(fighter_1.health,20,20)
    draw_health_bar(fighter_2.health,580,20)
    
    #двигоем бойцев
   
    fighter_1.move(SCREEN_WIDHT,SCREEN_HAIGHT,screen,fighter_2)
    

    #рисум бойцев
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()

