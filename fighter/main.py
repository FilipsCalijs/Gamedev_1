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
#p = int(input("chose"))
#bg_image = pygame.image.load(rf"B:\promma\python\game\fighter\assets\images\background\background_{p}.jpg").convert_alpha()
bg_image = pygame.image.load(rf"B:\promma\python\game\fighter\assets\images\background\background_2.gif").convert_alpha()
#print(p)
#загружать spritesheets
warrior_sheet = pygame.image.load(rf"B:\promma\python\game\fighter\assets\images\warrior\Sprites\warrior.png").convert_alpha()
wizard_sheet = pygame.image.load(rf"B:\promma\python\game\fighter\assets\images\wizard\Sprites\wizard.png").convert_alpha()

victory_img = pygame.image.load(rf"B:\promma\python\game\fighter\assets\images\icons\victory.png").convert_alpha()


#найти количество кадров в анимции
WARRIOR_ANIMATION_STEPS = [10,8,1,7,7,3,7]
WIZARD_ANIMATION_STEPS = [8,8,1,8,8,3,7]
icon_wizzard = pygame.image.load(rf"B:\promma\python\game\fighter\assets\images\icons\wizard.png")
icon_wizzard = pygame.transform.scale(icon_wizzard, (90, 90))
icon_warrior = pygame.image.load(rf"B:\promma\python\game\fighter\assets\images\icons\warrior.png")
icon_warrior = pygame.transform.scale(icon_warrior, (100, 100))
clock = pygame.time.Clock()
FPS = 60

RED =(255,0,39)
BLUE = (55,141,255)
YELLOW =(255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,128,0)

intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0,0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#определять переменные бойцев
WARRIOR_SIZE =162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72,56]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112,107]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

count_font = pygame.font.Font(rf"B:\promma\python\game\fighter\assets\fonts\Fon.ttf",100)

score_font = pygame.font.Font(rf"B:\promma\python\game\fighter\assets\fonts\Fon.ttf",30)

def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#функция для прорисовки БГ
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDHT, SCREEN_HAIGHT))
  screen.blit(scaled_bg, (0, 0))

    
#функция для прорисовки атки бара здоровье
def draw_health_bar(health,x,y):
    ratio = health / 100
    pygame.draw.rect(screen,BLACK,(x - 2,y -2,404,34))
    pygame.draw.rect(screen,RED,(x,y,400,30))
    pygame.draw.rect(screen,GREEN,(x,y,400 * ratio,30))

fighter_1 = Fighter(1,200,310,WARRIOR_DATA,warrior_sheet,WARRIOR_ANIMATION_STEPS,)
fighter_2 = Fighter(2,700,310,WIZARD_DATA, wizard_sheet,WIZARD_ANIMATION_STEPS)
run = True
while run:

    clock.tick(FPS)
    
    draw_bg()
    draw_text(str("Га'таон:" + (str(score[0]))),score_font,BLACK,int(SCREEN_WIDHT-865)-3,(SCREEN_HAIGHT / 8)-3)
    draw_text(str("Га'таон:"+ (str(score[0]))),score_font,BLACK,int(SCREEN_WIDHT-865)-3,(SCREEN_HAIGHT / 8)+3)
    draw_text(str("Га'таон:"+ (str(score[0]))),score_font,BLACK,int(SCREEN_WIDHT-865)+3,(SCREEN_HAIGHT / 8)+3)
    draw_text(str("Га'таон:"+ (str(score[0]))),score_font,BLACK,int(SCREEN_WIDHT-865)+3,(SCREEN_HAIGHT / 8)-3)
    draw_text(str("Га'таон:"+ (str(score[0]))),score_font,YELLOW,int(SCREEN_WIDHT-865),SCREEN_HAIGHT / 8)

    
    draw_text(str(str(score[1])+":Иог-Сот"),score_font,BLACK,int(SCREEN_WIDHT-390)-3,(SCREEN_HAIGHT / 8)-3)
    draw_text(str(str(score[1])+":Иог-Сот"),score_font,BLACK,int(SCREEN_WIDHT-390)+3,(SCREEN_HAIGHT / 8)-3)
    draw_text(str(str(score[1])+":Иог-Сот"),score_font,BLACK,int(SCREEN_WIDHT-390)-3,(SCREEN_HAIGHT / 8)+3)
    draw_text(str(str(score[1])+":Иог-Сот"),score_font,BLACK,int(SCREEN_WIDHT-390)+3,(SCREEN_HAIGHT / 8)+3)
    draw_text(str(str(score[1])+":Иог-Сот"),score_font,YELLOW,int(SCREEN_WIDHT-390),(SCREEN_HAIGHT / 8))
    
    #статистика персонажа
    draw_health_bar(fighter_1.health,20,20)
    draw_health_bar(fighter_2.health,580,20)


    if intro_count <= 0:
        fighter_1.move(SCREEN_WIDHT,SCREEN_HAIGHT,screen,fighter_2,round_over)
        fighter_2.move(SCREEN_WIDHT,SCREEN_HAIGHT,screen,fighter_1,round_over)
    else:
        draw_text(str(intro_count),count_font,BLACK,int((SCREEN_WIDHT / 2)-34),(SCREEN_HAIGHT / 4)+ 6)
        draw_text(str(intro_count),count_font,BLACK,int((SCREEN_WIDHT / 2)-34),(SCREEN_HAIGHT / 4)- 6)
        draw_text(str(intro_count),count_font,BLACK,int((SCREEN_WIDHT / 2)-46),(SCREEN_HAIGHT / 4)+ 6)
        draw_text(str(intro_count),count_font,BLACK,int((SCREEN_WIDHT / 2)-46),(SCREEN_HAIGHT / 4)- 6)
        draw_text(str(intro_count),count_font,RED,int((SCREEN_WIDHT / 2)-40),SCREEN_HAIGHT / 4)
        #updae count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
        
    #двигоем бойцев
   
    
    #fighter_2.move(610,600,screen,fighter_1)

    #обновлять бойцев
    fighter_1.update()
    fighter_2.update()
    

    #нарисовать иконки игроков
    screen.blit(icon_wizzard, (int(SCREEN_WIDHT-110),SCREEN_HAIGHT / 11))
    screen.blit(icon_warrior, (20,SCREEN_HAIGHT / 11))

    draw_text(str("P2"),score_font,BLACK,int(SCREEN_WIDHT-90)-3,(SCREEN_HAIGHT / 4.5)-3)
    draw_text(str("P2"),score_font,BLACK,int(SCREEN_WIDHT-90)+3,(SCREEN_HAIGHT / 4.5)-3)
    draw_text(str("P2"),score_font,BLACK,int(SCREEN_WIDHT-90)-3,(SCREEN_HAIGHT / 4.5)+3)
    draw_text(str("P2"),score_font,BLACK,int(SCREEN_WIDHT-90)+3,(SCREEN_HAIGHT / 4.5)+3)
    draw_text(str("P2"),score_font,BLUE,int(SCREEN_WIDHT-90),(SCREEN_HAIGHT / 4.5))

    draw_text(str("P1"),score_font,BLACK,int(SCREEN_WIDHT-955)-3,(SCREEN_HAIGHT / 4.5)-3)
    draw_text(str("P1"),score_font,BLACK,int(SCREEN_WIDHT-955)+3,(SCREEN_HAIGHT / 4.5)-3)
    draw_text(str("P1"),score_font,BLACK,int(SCREEN_WIDHT-955)-3,(SCREEN_HAIGHT / 4.5)+3)
    draw_text(str("P1"),score_font,BLACK,int(SCREEN_WIDHT-955)+3,(SCREEN_HAIGHT / 4.5)+3)
    draw_text(str("P1"),score_font,RED,int(SCREEN_WIDHT-955),(SCREEN_HAIGHT / 4.5))


    #рисум бойцев
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    
    #роверять если проиграл
    if round_over == False:
        if fighter_1.alive == False:
            score[1] +=1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] +=1
            print(score)
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img,(360,150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 4
            fighter_1 = Fighter(1,200,310,WARRIOR_DATA,warrior_sheet,WARRIOR_ANIMATION_STEPS)
            fighter_2 = Fighter(2,700,310,WIZARD_DATA, wizard_sheet,WIZARD_ANIMATION_STEPS)


        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()

