import pygame
from sys import exit
from random import randint, choice
 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Importing the animations
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100, 300))
        self.gravity = 0

    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        # Different types of enemies go here
        if type == "fly":
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = 190
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(850,1200),y_pos))

    
    def animate(self):
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x < -100: self.kill()

    def update(self):
        self.animate()
        self.rect.x -= 6
        self.destroy()


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(str(current_time//100), False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Runner')
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True

# Groups
player = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()

player.add(Player())


# Surfaces
sky_surf = pygame.image.load('graphics/Sky.png').convert()
sky_rect = sky_surf.get_rect(topleft = (0,0))
ground_surf = pygame.image.load('graphics/ground.png').convert()


# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,randint(600,1500))
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)
start_time = 0 


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active: 
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
            
        else: 
            if event.type == pygame.KEYDOWN:
                game_active = True
                start_time = pygame.time.get_ticks()
        
    # Active gameplay
    if game_active:
        screen.blit(sky_surf,sky_rect)
        screen.blit(ground_surf,(0,300))
        display_score()

        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

    # Gameover winodw, could be a menu window
    else:
        screen.fill("Yellow")
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        

    pygame.display.update()
    clock.tick(60)