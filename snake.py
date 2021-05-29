import pygame
import time
import random
import sys

pygame.init()

# variables for colors and dimensions
colors = {
    "board": (153, 153, 85),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "yellow": (255, 255, 102),
    "red": (213, 50, 80),
    "green": (0, 255, 0),
    "blue": (50, 153, 213),
    "step5": (255, 221, 0),
    "step4": (255, 187, 0),
    "step3": (255, 136, 0),
    "step2": (255, 102, 0),
    "step1": (255, 51, 0)
}
dimensions = {
    "gamewidth": 800,
    "gameheight": 600,
    "blocksize": 10
}

topedge = dimensions["gameheight"] / 15

# pygame and animation-related
snakespeed = 15
fontstyle = pygame.font.SysFont("bahnschrift", 25)
clock = pygame.time.Clock()
dis = pygame.display.set_mode((dimensions["gamewidth"], dimensions["gameheight"]))

pygame.display.set_caption("Snake Game")

# scoring
def scoring(score):
    value = fontstyle.render("Score: " + str(score), True, colors["black"])

    dis.blit(value, [0, 0])

# draw the snake on the board
def snake(snakeblock, snakelist):
    # color code based on how hungry snake is
    for x in snakelist:
        if len(snakelist) == 1:
            snakecolor = colors["red"]
        if len(snakelist) >= 2 and len(snakelist) <= 4:
            snakecolor = colors["step1"]
        elif len(snakelist) > 4 and len(snakelist) <= 6:
            snakecolor = colors["step2"]
        elif len(snakelist) > 6 and len(snakelist) <= 8:
            snakecolor = colors["step3"]
        elif len(snakelist) > 8 and len(snakelist) <= 10:
            snakecolor = colors["step4"]
        elif len(snakelist) > 10:
            snakecolor = colors["step5"]

        pygame.draw.rect(dis, colors["black"], [x[0], x[1], snakeblock, snakeblock], 2)
        pygame.draw.rect(dis, snakecolor, [x[0] + 1, x[1] + 1, snakeblock - 1, snakeblock - 1])

# generate and return the coordinates of the snack
def snack():
    snackx = round(random.randrange(0, dimensions["gamewidth"] - dimensions["blocksize"]) / 10.0) * 10.0
    snacky = round(random.randrange(topedge, dimensions["gameheight"] - dimensions["blocksize"]) / 10.0) * 10.0

    return snackx, snacky

def message(msg, color):
    mesg = fontstyle.render(msg, True, color)

    dis.blit(mesg, [dimensions["gamewidth"] / 6, dimensions["gameheight"] / 3])

def gameloop():
    gameover = False
    gameclose = False

    # start snake in the center of the board
    x1 = dimensions["gamewidth"] / 2
    y1 = dimensions["gameheight"] / 2

    deltax1 = 0
    deltay1 = 0

    snakelist = []
    snakelength = 1

    # get random coordinates of snack
    snackinfo = snack()
    snackx = snackinfo[0]
    snacky = snackinfo[1]

    while not gameover:
        while gameclose == True:
            dis.fill(colors["board"])

            scoring(snakelength - 1)
            message("Game over! Press Q to quit or C to play again", colors["red"])
            
            pygame.display.update()

            # quit or start another game at game over
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameover = True
                        gameclose = False
                    if event.key == pygame.K_c:
                        gameloop()

        # snake control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    deltax1 = -10
                    deltay1 = 0
                elif event.key == pygame.K_RIGHT:
                    deltax1 = 10
                    deltay1 = 0
                elif event.key == pygame.K_UP:
                    deltax1 = 0
                    deltay1 = -10
                elif event.key == pygame.K_DOWN:
                    deltax1 = 0
                    deltay1 = 10

        # snake hits wall
        if x1 >= dimensions["gamewidth"] or x1 < 0 or y1 >= dimensions["gameheight"] or y1 < topedge:
            gameclose = True

        x1 += deltax1
        y1 += deltay1
        
        dis.fill(colors["board"])

        pygame.draw.rect(dis, colors["step5"], [0, 0, dimensions["gamewidth"], topedge])

        # draw the snake's food
        pygame.draw.rect(dis, colors["green"], [snackx, snacky, dimensions["blocksize"], dimensions["blocksize"]], 2)
        pygame.draw.rect(dis, colors["yellow"], [snackx + 1, snacky + 1, dimensions["blocksize"] - 1, dimensions["blocksize"] - 1])
        
        snakehead = []
        snakehead.append(x1)
        snakehead.append(y1)
        snakelist.append(snakehead)

        if len(snakelist) > snakelength:
            del snakelist[0]

        for x in snakelist[:-1]:
            if x == snakehead:
                gameclose = True

        snake(dimensions["blocksize"], snakelist)
        scoring(snakelength - 1)

        pygame.display.update()

        # snake eats snack
        if x1 == snackx and y1 == snacky:
            snackinfo = snack()
            snackx = snackinfo[0]
            snacky = snackinfo[1]

            snakelength += 1

        clock.tick(snakespeed)

    pygame.quit()

    quit()

gameloop()