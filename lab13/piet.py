"""Mondrian Art Generator
Generates randomized compositions of colored rectangles in the style of Piet Mondrian.
Click the window to generate a new composition.
"""

import random
import pygame

# initialize pygame and screen settings
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mondrian Art Generator")

# define colors with white weighted heavily
COLORS = [
    pygame.Color("white"),
    pygame.Color("white"),
    pygame.Color("white"),
    pygame.Color("white"),
    pygame.Color("black"),
    pygame.Color("red"),
    pygame.Color("blue"),
    pygame.Color("yellow")
]

# padding and line width settings
X_PADDING = int(WIDTH * 0.05)
Y_PADDING = int(HEIGHT * 0.05)
LINE_WIDTH = 5

# recursive function to draw and split rectangles
def draw_and_split(rect, depth):
    pygame.draw.rect(screen, random.choice(COLORS), rect)
    pygame.draw.rect(screen, pygame.Color("black"), rect, LINE_WIDTH)

    if depth == 0:
        return
    if rect.width < 2 * X_PADDING or rect.height < 2 * Y_PADDING:
        return

    if rect.width > rect.height:
        x = random.randint(rect.left + X_PADDING, rect.right - X_PADDING)
        r1 = pygame.Rect(rect.left, rect.top, x - rect.left, rect.height)
        r2 = pygame.Rect(x, rect.top, rect.right - x, rect.height)
    else:
        y = random.randint(rect.top + Y_PADDING, rect.bottom - Y_PADDING)
        r1 = pygame.Rect(rect.left, rect.top, rect.width, y - rect.top)
        r2 = pygame.Rect(rect.left, y, rect.width, rect.bottom - y)

    draw_and_split(r1, depth - 1)
    draw_and_split(r2, depth - 1)

# function to draw the entire scene
def draw_scene():
    screen.fill(pygame.Color("white"))
    outer_rectangle = pygame.Rect(0, 0, WIDTH, HEIGHT)
    draw_and_split(outer_rectangle, 5)
    pygame.display.flip()

# initial draw
draw_scene()

# main event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            draw_scene()
