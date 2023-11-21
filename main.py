import pygame
from sys import exit
 

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(str(current_time//100), False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = True
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()


snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (700,300))

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0
start_time = 0 
player_jump_count = 2


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
                snail_rect.left = 800
                start_time = pygame.time.get_ticks()


    if game_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))

        display_score()
        screen.blit(snail_surf,snail_rect)
        snail_rect.x -= 5
        if snail_rect.right <= 0: snail_rect.left = 800
        
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        print(player_gravity)
        if player_rect.bottom >= 300: 
            player_rect.bottom = 300
            player_gravity = 0
            player_jump_count = 2
        screen.blit(player_surf,player_rect)

        # Collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill("Yellow")



    pygame.display.update()
    clock.tick(60)