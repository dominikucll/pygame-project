import pygame
from sys import exit


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

score_surf = test_font.render("My game", False, (64,64,64))
score_rect = score_surf.get_rect(center = (400,50))


snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (700,300))

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0


def is_touching_floor():
    return player_rect.bottom >= 300


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos) and is_touching_floor(): 
                player_gravity = -20
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and is_touching_floor():
                player_gravity = -20
        if event.type == pygame.KEYUP:
            print("Key up")


    screen.blit(sky_surf,(0,0))
    screen.blit(ground_surf,(0,300))
    pygame.draw.rect(screen, "#c0e8ec",score_rect)
    pygame.draw.rect(screen, "#c0e8ec",score_rect,10)
    screen.blit(score_surf,score_rect)
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
    screen.blit(player_surf,player_rect)


    pygame.display.update()
    clock.tick(60)