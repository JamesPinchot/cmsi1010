import pygame
from dataclasses import dataclass

# screen setup
width, height = 800, 600
sky_color = (0, 255, 255)
sun_color = (255, 200, 0)
sun_position = (width - 100, 100)
sun_radius = 150
grass_color = (0, 128, 0)
grass_height = 100
grass_top = height - grass_height
grass_rectangle = (0, grass_top, width, grass_height)

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("alien invasion")
clock = pygame.time.Clock()

# ufo class
@dataclass
class ufo:
    x: float
    y: float
    width: int = 100
    height: int = 30
    color: tuple = (128, 128, 128)
    speed: float = 1

    def draw(self):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(
            screen,
            self.color,
            (self.x + self.width // 4, self.y - self.height // 3, self.width // 2, self.height)
        )

    def move(self):
        self.x += self.speed
        if self.x > width:
            self.x = -self.width

# ufo instances
ufos = [
    ufo(x=0, y=50),
    ufo(x=200, y=100, speed=3.5, width=80, height=20),
    ufo(x=400, y=150, color=(160, 160, 160), width=120, speed=3),
    ufo(x=600, y=200, speed=4)
]

# draw the scene
def draw_scene():
    screen.fill(sky_color)
    pygame.draw.circle(screen, sun_color, sun_position, sun_radius)
    pygame.draw.rect(screen, grass_color, grass_rectangle)

    for ship in ufos:
        ship.draw()
        ship.move()

    pygame.display.flip()
    clock.tick(60)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            raise SystemExit

    draw_scene()
