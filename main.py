import pygame
from sys import exit
from random import randint
 

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(str(current_time//100), False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)


def obstacle_movement(obstacle_list):
    movement_speed = 5 + ((pygame.time.get_ticks() - start_time)//1000)
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= movement_speed

            if obstacle_rect.bottom >= 300: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = True
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
sky_rect = sky_surf.get_rect(topleft = (0,0))
ground_surf = pygame.image.load('graphics/ground.png').convert()


# Obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]


obstacle_rect_list = []


player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0
start_time = 0 
player_jump_count = 2

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,randint(600,1500))

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_jump_count >0: 
                    player_gravity = -20
                    player_jump_count -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_jump_count >0:
                    player_gravity = -20
                    player_jump_count -= 1
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),190)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
            
            
        else: 
            if event.type == pygame.KEYDOWN:
                game_active = True
                start_time = pygame.time.get_ticks()
        
                


    if game_active:
        screen.blit(sky_surf,sky_rect)
        screen.blit(ground_surf,(0,300))

        display_score()
        
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: 
            player_rect.bottom = 300
            player_jump_count = 2
        player_animation()
        screen.blit(player_surf,player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill("Yellow")
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        


    pygame.display.update()
    clock.tick(60)