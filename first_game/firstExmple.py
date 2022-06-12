import pygame,sys
import random
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100,-16,2,512)#нужно чтоб звуки не задерживались
pygame.init()
pygame.mixer.set_num_channels(64)
pygame.display.set_caption('НЕТ НИКОКИХ НОРМАЛЬНЫХ ИДЕЙ, ИЗ ЗА ЭТОГО ПУСЬ БУДЕТ ТАК')
WINDOW_SIZE = (1600,900 )
screen = pygame.display.set_mode(WINDOW_SIZE)

display = pygame.Surface((300,200))

#загружает изображения игрока

stone_image = pygame.image.load('stone.png')
grass_image = pygame.image.load('grass.png')
dirt_image = pygame.image.load('dirt.png')
plant_image = pygame.image.load('plant.png').convert()
plant_image.set_colorkey((255,255,255))

tile_index = {1:grass_image,
              2:dirt_image,
              3:plant_image,
              4:stone_image}



TILE_SIZE = grass_image.get_width()

#крутит плитку дальше(просто менят позицию плитки на x+1 или x-1  )
true_scroll = [0,0]



global animation_frames
animation_frames = {}

CHUNK_SIZE = 8

def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing
            if target_y > 10:
                tile_type = 2 # dirt
            elif target_y == 10:
                tile_type = 1 # grass
            elif target_y == 9:
                if random.randint(1,5) == 1:#вероятность появление
                    tile_type = 3 # plant
                if random.randint(1,10) == 2:#для камнья
                    tile_type = 4
            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
    return chunk_data


def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((0,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        

animation_database = {}

animation_database['run'] = load_animation('player_animations/run',[7,7])
animation_database['idle'] = load_animation('player_animations/idle',[7,40])# здесь я исправил, было [7,7,40]


game_map = {}

jump_sound = pygame.mixer.Sound('jump.wav')
jump_sound_2 = pygame.mixer.Sound('jump_2.wav')
grass_sounds = [pygame.mixer.Sound('grass_0.wav'),pygame.mixer.Sound('grass_1.wav')]
jump_sound.set_volume(0.4)#звук валюм
grass_sounds[0].set_volume(0.4)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('music_1.wav')
pygame.mixer.music.play(-1)#парамитр отвичает за то сколько раз она бдует производиться после проигреша, если -1 то она будет идти бесконечно

player_action = 'idle'
player_frame = 0
player_flip = False

gras_sound_timer = 0

player_rect = pygame.Rect(100,100,10,16)#размеры и расположения игрока





                          #1 и 2 это позиция, 3 и 4 размеры
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]],[0.25,[120,70,70,400]],[0.25,[400,30,40,40]],[0.5,[560,10,55,320]],[0.5,[490,70,10,140]],[0.1,[600,80,140,400]]]
# следуйщии 2 дефа нужны для того чтоб проверяь стоит ли игрок на платформе или воздухе
def collision_test(rect, tiles): 
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top': False,'bottom': False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if  movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] <0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] <0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
moving_right = False
moving_left = False
vertical_momentum = 0
player_y_momentum = 0
air_timer = 0


while True:
    display.fill((146,244,255))

    if gras_sound_timer > 0:
        gras_sound_timer -= 1
        

    #чтоб скролл следовал за игроком

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/10     #152,то расположения игрока(по серидине, ноль это значит в гачале)
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/10     #10это промежуток отслежки камеры(она якобы движеться за игроком)
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    
    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(12,222,150),obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)
    tile_rects = []
    for y in range(3):#я так понял это генерация чанков
         for x in range(4):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x,target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))

                if tile[1] in [1,2]:#вещи, которые игрок не может пройти(они являються collision - грязь, трова)
                    tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16))
                    

    player_movement = [0,0]#скорость игрока
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
        if player_movement[0] != 0:
            if gras_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    player_img = pygame.transform.scale(player_img,(10,16))#визуальные размеры игрока
    player_img.set_colorkey((0,0,0))
    
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)#заглушить музыку
            if event.key == K_s:
                pygame.mixer.music.play(-1)#аново начать!
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display,WINDOW_SIZE)
    screen.blit(surf,(0,0))

    pygame.display.update()
    clock.tick(60)#это кадры в сек или фпс
