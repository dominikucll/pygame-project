import pygame
from sys import exit
from random import randint
 

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(str(current_time//100), False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)


def obstacle_movement(obstacle_list):
    movement_speed = 5 + (pygame.time.get_ticks() - start_time)//10000
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= movement_speed

            if obstacle_rect.bottom >= 300: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []


def collisions(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if obstacle_rect.colliderect(player_rect):
                return True


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
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

obstacle_rect_list = []


player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0
start_time = 0 
player_jump_count = 2

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,randint(600,1500))


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
        else: 
            if event.type == pygame.KEYDOWN:
                game_active = True
                start_time = pygame.time.get_ticks()
        
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),190)))
                


    if game_active:
        screen.blit(sky_surf,sky_rect)
        screen.blit(ground_surf,(0,300))

        display_score()
        
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: 
            player_rect.bottom = 300
            player_gravity = 0
            player_jump_count = 2
        screen.blit(player_surf,player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        if collisions(obstacle_rect_list): 
            game_active = False
            obstacle_rect_list.clear()

    else:
        screen.fill("Yellow")


    pygame.display.update()
    clock.tick(60)