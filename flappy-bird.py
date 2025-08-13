import pygame
import random

pygame.init()

""" Game State Variables """
score = 0
END_FONT = pygame.font.SysFont(None, 60, True)   # Large font for end screen
FONT = pygame.font.SysFont(None, 30)             # Small font for HUD
TEXT = f"score: {score}"

""" Load saved top score """
TOP_SCORE = 1
with open("top-score.txt", "r") as file:
    TOP_SCORE = file.read()

""" Pipe data storage: list of [x, gap_start, gap_end] """
pipes = []

""" Screen and Player Setup """
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

PLAYER_X = 200
PLAYER_Y = SCREEN_HEIGHT/2
PLAYER_SIZE = 20

""" Main display and overlay surface """
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

""" Physics & Timing """
MOMENTUM = False       # True while player is jumping
START_Y = 0            # Jump arc counter
fps = 60
clock = pygame.time.Clock()


""" Utility: render text to screen """
def write(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


""" Initial Draw """
screen.fill("#ffffff")
pygame.draw.circle(screen, "#000000", (PLAYER_X, PLAYER_Y), PLAYER_SIZE, PLAYER_SIZE)
write(TEXT, FONT, "#000000", 0, 0)
pygame.display.update()

""" Control Flags """
plus_score = False     # Prevents double scoring on one pipe 
run = True             # Current round active 
runing = True          # Game process active ""

""" === Main Game Loop === """
while runing:
    """ End Screen """
    if not run:
        """ Update top score if beaten """
        if int(TOP_SCORE) < score:
            with open("top-score.txt", "w") as file:
                file.write(str(score))
            TOP_SCORE = score

        """ Draw semi-transparent overlay """
        screen.blit(canvas, (0, 0))
        canvas_element = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 300, 400)
        canvas_element.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        pygame.draw.rect(screen, (45, 45, 45, 230), canvas_element)

        """ Display current score and best """
        write(f"score: {score}", END_FONT, "#ffffff", SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2-100)
        write(f"best: {TOP_SCORE}", END_FONT, "#ffffff", SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2)
        pygame.display.update()

    """ Event Handling """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        elif event.type == pygame.KEYDOWN and run:
            if event.key == pygame.K_SPACE:
                """ Start jump + game loop if first press """
                MOMENTUM = True
                iter = -2

                """ === Round Loop === """
                while run:
                    screen.fill("#ffffff")
                    TEXT = f"score: {score}"
                    write(TEXT, FONT, "#000000", 0, 0)
                    iter += 1

                    """ Collision Detection """
                    for element in pipes:
                        if element[0]-150 < PLAYER_X < element[0]:
                            if not (element[1] < PLAYER_Y < element[2]):
                                run = False  # Hit pipe

                    """ Scoring """
                    if len(pipes) > 0:
                        if pipes[0][0] < 200 and not plus_score:
                            plus_score = True
                            score += 1

                    """ Player Movement """
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
                        run = False  # Hit ground
                    PLAYER_Y = round(PLAYER_Y, 1)

                    """ Pipe Spawning """
                    if iter > 90 or iter == -1:
                        iter = 0
                        new_pipe = [
                            SCREEN_WIDTH+150,
                            random.randint(200, SCREEN_HEIGHT-200)
                        ]
                        new_pipe.append(new_pipe[1]+180)  # gap_end
                        pipes.append(new_pipe)

                    """ Pipe Movement + Drawing """
                    for element in pipes:
                        if element[0] > -10:
                            element[0] -= 4
                            pipe_top = pygame.Rect(element[0], element[1], 120, element[1])
                            pipe_top.bottomright = (element[0], element[1])
                            pipe_bottom = pygame.Rect(element[0], element[2], 120, element[2])
                            pipe_bottom.topright = (element[0], element[2])
                            pygame.draw.rect(screen, "#000000", pipe_top)
                            pygame.draw.rect(screen, "#000000", pipe_bottom)
                        else:
                            plus_score = False
                            pipes.remove(element)

                    """ Draw Player """
                    pygame.draw.circle(screen, "#000000", (PLAYER_X, PLAYER_Y), PLAYER_SIZE, PLAYER_SIZE)

                    """ In-Loop Event Handling (jump mid-flight) """
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            runing = False
                            run = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                MOMENTUM = True

                    """ Frame Sync """
                    clock.tick(fps)
                    pygame.display.update()
