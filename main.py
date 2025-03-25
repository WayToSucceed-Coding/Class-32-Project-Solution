import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Save The Spaceship")

# Load images
background = pygame.image.load("bg.png")
spaceship = pygame.image.load("spaceship.png")
meteor_img = pygame.image.load("meteor.png")
star_img = pygame.image.load("star.png")
welcome_bg = pygame.image.load("welcome_bg.png")
restart_bg=pygame.image.load("restart_bg.png")

# Resize images
spaceship = pygame.transform.scale(spaceship, (100, 100))
meteor_img = pygame.transform.scale(meteor_img, (100, 100))
star_img = pygame.transform.scale(star_img, (100, 100))

#Load Sound
star_hit=pygame.mixer.Sound('star_hit.mp3')
meteor_hit=pygame.mixer.Sound('meteor_hit.mp3')

class SpaceObject:
    def __init__(self, type):
        self.x = random.randint(0, WIDTH - 100)
        self.y = -50
        self.speed_y = random.randint(3, 7)
        self.type = type
        self.collided=False

    def draw(self):
        if self.type == 'meteor':
            screen.blit(meteor_img, (self.x, self.y))
        else:
            screen.blit(star_img, (self.x, self.y))

    def move(self):
        self.y += self.speed_y

# Game loop
running = True

# Spaceship position
spaceship_x = WIDTH // 2
spaceship_y = HEIGHT - 100

objects = []

spawn_interval = 2000  # Initial interval (2 seconds)
min_spawn_interval = 500  # Minimum interval (0.5 seconds)
difficulty_timer = pygame.time.get_ticks()
last_spawn_time = 0

score=0
lives=3

game_state = 'start'

font=pygame.font.Font(None,36)

def reset():
    global game_state,score,lives

    game_state='play'
    score=0
    lives=3

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_state == 'start':
            game_state = 'play'

        if event.type == pygame.MOUSEMOTION and game_state == 'play':
            x, y = event.pos
            if 0 <= x <= WIDTH - 100:
                spaceship_x = x

        if event.type==pygame.KEYDOWN and event.key==pygame.K_r and game_state=='end':
            reset()

    if game_state == 'start':
        screen.blit(welcome_bg, (0, 0))

    elif game_state == 'play':
        screen.blit(background, (0, 0))  # Draw background
        screen.blit(spaceship, (spaceship_x, spaceship_y))  # Draw spaceship

        current_time = pygame.time.get_ticks()

        if current_time - last_spawn_time > spawn_interval or last_spawn_time == 0:
            type = random.choice(['meteor', 'star'])
            objects.append(SpaceObject(type))
            last_spawn_time = current_time

        if current_time - difficulty_timer > 15000 and spawn_interval > min_spawn_interval:
            spawn_interval -= 500
            difficulty_timer = current_time  # Reset difficulty timer

        # Remove objects that move off-screen
        objects = [obj for obj in objects if not (obj.y > HEIGHT or obj.collided)]

        # Draw and move objects
        for obj in objects:
            obj.draw()
            obj.move()

            if not obj.collided:

                spaceship_rect=pygame.Rect(spaceship_x+25,spaceship_y+25,50,50)
                obj_rect=pygame.Rect(obj.x+25,obj.y+25,50,50)

                # pygame.draw.rect(screen, (255, 0, 0), spaceship_rect, 2)  # Red for spaceship
                # pygame.draw.rect(screen, (0, 255, 0), obj_rect, 2)     # Green for objects

                if spaceship_rect.colliderect(obj_rect):
                    obj.collided=True
                    if obj.type=='star':
                        score+=1
                        star_hit.play()
                    else:
                        lives-=1
                        meteor_hit.play()
                    break 


        score_text=font.render(f"Score: {score}",True,(255,255,255))
        lives_text=font.render(f"Lives: {lives}",True,(255,255,255))

        screen.blit(score_text,(10,10))
        screen.blit(lives_text,(WIDTH-150,10))
               

        if lives==0:
            game_state='end'
    else:
        screen.blit(restart_bg,(0,0))    

    pygame.display.update()

pygame.quit()
