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
PLAYER_SIZE = 20   # Bird radius

""" Main display and overlay surface """
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

""" Physics & Timing """
time_falling = 0
time_jumping = 0
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
runing = True          # Game process active

""" === Main Game Loop === """
while runing:
    """ End Screen """
    if not run:
        """ Make ball fall to the ground when dead"""
        if PLAYER_Y < SCREEN_HEIGHT:
            screen.fill("#ffffff")
            pipe_rects = []  # store active pipe rects
            for element in pipes:
                # Top pipe rect
                pipe_top = pygame.Rect(element[0], 0, 120, element[1])
                pipe_top.topright = (element[0], 0)
                # Bottom pipe rect
                pipe_bottom = pygame.Rect(element[0], element[2], 120, SCREEN_HEIGHT - element[2])
                pipe_bottom.topright = (element[0], element[2])

                pygame.draw.rect(screen, "#000000", pipe_top)
                pygame.draw.rect(screen, "#000000", pipe_bottom)

                pipe_rects.append(pipe_top)
                pipe_rects.append(pipe_bottom)

            PLAYER_Y += 15 
            pygame.draw.circle(screen, "#000000", (PLAYER_X, PLAYER_Y), PLAYER_SIZE, PLAYER_SIZE)

        """ Update top score if beaten """
        if int(TOP_SCORE) < score:
            with open("top-score.txt", "w") as file:
                file.write(str(score))
            TOP_SCORE = score

        """ Draw semi-transparent overlay """
        screen.blit(canvas, (0, 0))
        canvas_element = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 300, 400)
        canvas_element.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        pygame.draw.rect(screen, (45, 45, 45, 230), canvas_element, border_radius=20)

        """ Display current score and best """
        write(f"score: {score}", END_FONT, "#ffffff", SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2-100)
        write(f"best: {TOP_SCORE}", END_FONT, "#ffffff", SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2)
        clock.tick(fps) 
        pygame.display.update()

    """ Event Handling """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        elif event.type == pygame.KEYDOWN and run:
            if event.key == pygame.K_SPACE:
                """ Start jump + game loop if first press """
                MOMENTUM = True
                iteration = -2

                """ === Round Loop === """
                while run:
                    screen.fill("#ffffff")
                    TEXT = f"score: {score}"
                    write(TEXT, FONT, "#000000", 0, 0)
                    iteration += 1

                    """ Pipe Spawning """
                    if iteration > 90 or iteration == -1:
                        iteration = 0
                        new_pipe = [
                            SCREEN_WIDTH+120,
                            random.randint(100, SCREEN_HEIGHT-310)
                        ]
                        new_pipe.append(new_pipe[1]+210)  # gap_end
                        pipes.append(new_pipe)

                    """ Pipe Movement + Drawing """
                    pipe_rects = []  # store active pipe rects
                    for element in pipes:
                        if element[0] > -120:
                            element[0] -= 4

                            # Top pipe rect
                            pipe_top = pygame.Rect(element[0], 0, 120, element[1])
                            pipe_top.topright = (element[0], 0)
                            # Bottom pipe rect
                            pipe_bottom = pygame.Rect(element[0], element[2], 120, SCREEN_HEIGHT - element[2])
                            pipe_bottom.topright = (element[0], element[2])

                            pygame.draw.rect(screen, "#000000", pipe_top)
                            pygame.draw.rect(screen, "#000000", pipe_bottom)

                            pipe_rects.append(pipe_top)
                            pipe_rects.append(pipe_bottom)
                        else:
                            plus_score = False
                            pipes.remove(element)

                    """ Collision Detection """
                    for element in pipes:
                        if element[0]-120+PLAYER_SIZE < PLAYER_X < element[0]-PLAYER_SIZE:
                            if not (element[1]+PLAYER_SIZE < PLAYER_Y < element[2]-PLAYER_SIZE):
                                run = False  # Hit pipe

                    """ Scoring """
                    if len(pipes) > 0:
                        if pipes[0][0] < 200 and not plus_score:
                            plus_score = True
                            score += 1

                    """ Player Movement """
                    if PLAYER_Y+PLAYER_SIZE < SCREEN_HEIGHT:
                        if MOMENTUM and START_Y > 140:
                            MOMENTUM = False
                            START_Y = 0
                            time_jumping += 1
                        if MOMENTUM:
                            time_jumping += 1
                            time_falling = 0
                            if time_jumping < 40:
                                START_Y += 12
                                PLAYER_Y -= 12
                            elif time_jumping < 80:
                                START_Y += 14
                                PLAYER_Y -= 14
                            else:
                                time_falling += 1
                                START_Y += 16
                                PLAYER_Y -= 16
                        else:
                            time_jumping = 0
                            if time_falling < 30:
                                PLAYER_Y += 8
                            elif time_falling < 60:
                                PLAYER_Y += 10
                            else:
                                PLAYER_Y += 12
                    else:
                        run = False  # Hit ground
                    PLAYER_Y = round(PLAYER_Y, 1)

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
                                START_Y = 0

                    """ Frame Sync """
                    clock.tick(fps)
                    pygame.display.update()
