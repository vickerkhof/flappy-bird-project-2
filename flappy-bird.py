import pygame
import random

pygame.init()

score = 0
END_FONT = pygame.font.SysFont(None, 60, True)
FONT = pygame.font.SysFont(None, 30)
TEXT = f"score: {score}"

TOP_SCORE = 1
with open("top-score.txt", "r") as file:
    TOP_SCORE = file.read()

pipes = []

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

PLAYER_X = 200
PLAYER_Y = SCREEN_HEIGHT/2
PLAYER_SIZE = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

MOMENTUM = False
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
runing = True
while runing:
        if not run:
            if int(TOP_SCORE) < score:
                with open("top-score.txt", "w") as file:
                    file.write(str(score))
                TOP_SCORE = score
            screen.blit(canvas, (0, 0))
            canvas_element = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 300, 400)
            canvas_element.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            pygame.draw.rect(canvas, (45, 45, 45, 230), canvas_element)
            write(f"score: {score}", END_FONT, "#ffffff", SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2-100)
            write(f"best: {TOP_SCORE}", END_FONT, "#ffffff", SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2)
            pygame.display.update() 
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
            elif event.type == pygame.KEYDOWN and run:
                if event.key == pygame.K_SPACE:
                    MOMENTUM = True
                    iter = -2
                    while run:
                        screen.fill("#ffffff")
                        TEXT = f"score: {score}" 
                        write(TEXT, FONT, "#000000", 0, 0)
                        iter += 1
                        for element in pipes:
                            if element[0]-150 < PLAYER_X < element[0]:
                                if not (element[1] < PLAYER_Y < element[2]):
                                    run = False
                        
                        if len(pipes) > 0:
                            if pipes[0][0] < 200 and not plus_score:
                                plus_score = True
                                score += 1

                        if PLAYER_Y+PLAYER_SIZE < SCREEN_HEIGHT:
                            if MOMENTUM and START_Y > 120:
                                MOMENTUM = False
                                START_Y = 0
                            if MOMENTUM:
                                START_Y += 12
                                PLAYER_Y -= 12
                            else:
                                PLAYER_Y += 8
                        else:
                            run = False
                        PLAYER_Y = round(PLAYER_Y, 1)

                        if iter > 90 or iter == -1:
                            iter = 0
                            new_pipe = []
                            new_pipe.append(SCREEN_WIDTH+150)
                            new_pipe.append(random.randint(200, SCREEN_HEIGHT-200))
                            new_pipe.append(new_pipe[1]+180)
                            pipes.append(new_pipe)
                        
                        for element in pipes:
                            if element[0] > -10:
                                element[0] -=4
                                pipe_top = pygame.Rect(element[0], element[1], 120, element[1])
                                pipe_top.bottomright = (element[0], element[1])
                                pipe_bottom = pygame.Rect(element[0], element[2], 120, element[2])
                                pipe_bottom.topright = (element[0], element[2 ])
                                pygame.draw.rect(screen, "#000000", pipe_top)
                                pygame.draw.rect(screen, "#000000", pipe_bottom)
                            else:
                                plus_score = False
                                pipes.remove(element)

                        pygame.draw.circle(screen, "#000000", (PLAYER_X, PLAYER_Y), PLAYER_SIZE, PLAYER_SIZE)

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                runing = False
                                run = False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    MOMENTUM = True

                        clock.tick(fps)
                        pygame.display.update()

