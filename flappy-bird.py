import pygame
import random

pygame.init()

score = 0
FONT = pygame.font.SysFont(None, 30)
TEXT = f"score: {score}"

pipes = []

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

PLAYER_X = 200
PLAYER_Y = SCREEN_HEIGHT/2
PLAYER_SIZE = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

MOMENTUM = False
INCREMENT = 0
JUMPS = 0.2
START_Y = 0
fps = 60
clock = pygame.time.Clock()


def write(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


screen.fill("#ffffff")
pygame.draw.circle(screen, "#000000", (PLAYER_X, PLAYER_Y), PLAYER_SIZE, PLAYER_SIZE)
write(TEXT, FONT, "#000000", 0, 0)
pygame.display.update() 
plus_score = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                MOMENTUM = True
                run = True
                iter = -2
                while run:
                    screen.fill("#ffffff")
                    TEXT = f"score: {score}"
                    write(TEXT, FONT, "#000000", 0, 0)
                    iter += 1
                    INCREMENT += JUMPS
                    for element in pipes:
                        if element[0]-150 < PLAYER_X+PLAYER_SIZE < element[0]:
                            if element[1] > PLAYER_Y-PLAYER_SIZE or PLAYER_Y+PLAYER_SIZE > element[2]:
                                run = False
                    
                    if len(pipes) > 0:
                        if pipes[0][0] < 200 and not plus_score:
                            plus_score = True
                            score += 1

                    if PLAYER_Y+PLAYER_SIZE < SCREEN_HEIGHT:
                        if MOMENTUM and START_Y > 80:
                            INCREMENT = 0
                            MOMENTUM = False
                            START_Y = 0
                        if MOMENTUM:
                            START_Y += 13
                            PLAYER_Y -= 13
                        else:
                            PLAYER_Y += (INCREMENT**2)
                    else:
                        run = False
                    PLAYER_Y = round(PLAYER_Y, 1)

                    if iter > 180 or iter == -1:
                        iter = 0
                        new_pipe = []
                        new_pipe.append(SCREEN_WIDTH+150)
                        new_pipe.append(random.randint(200, SCREEN_HEIGHT-200))
                        new_pipe.append(new_pipe[1]+175)
                        pipes.append(new_pipe)
                    
                    for element in pipes:
                        if element[0] > -10:
                            element[0] -=2
                            pipe_top = pygame.Rect(element[0], element[1], 150, element[1])
                            pipe_top.bottomright = (element[0], element[1])
                            pipe_bottom = pygame.Rect(element[0], element[2], 150, element[2])
                            pipe_bottom.topright = (element[0], element[2 ])
                            pygame.draw.rect(screen, "#000000", pipe_top)
                            pygame.draw.rect(screen, "#000000", pipe_bottom)
                        else:
                            plus_score = False
                            pipes.remove(element)

                    pygame.draw.circle(screen, "#000000", (PLAYER_X, PLAYER_Y), PLAYER_SIZE, PLAYER_SIZE)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                MOMENTUM = True
                                INCREMENT = 0

                    clock.tick(fps)
                    pygame.display.update()

                pygame.display.quit()
                print(score)