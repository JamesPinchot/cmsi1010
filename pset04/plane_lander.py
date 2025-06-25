import math
import random
from dataclasses import dataclass
import pygame

# setup
WIDTH, HEIGHT = 1024, 600
SKY_COLOR = (135, 240, 255)
GRASS_COLOR = (128, 255, 100)
RUNWAY_COLOR = (80, 80, 80)
RUNWAY_RECT = pygame.Rect(200, HEIGHT - 70, 600, 20)
GROUND_LEVEL = HEIGHT - 60
TREE_SPACING = 173
MAX_PLANE_SPEED = 23
CRUISING_ALTITUDE = 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("plane lander")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

score = 0


@dataclass
class Plane:
    x: int
    y: int
    state: str = "flying"
    speed: int = MAX_PLANE_SPEED
    rotation: float = 0
    color: tuple = (100, 100, 100)

    def draw(self):
        base_coords = [
            (-16, 0), (-13, 2), (-15, 7), (-12, 7), (-8, 2), (-1, 2),
            (-6, 6), (-5, 6), (8, 2), (16, 2), (19, -2), (8, -2),
            (-5, -8), (-6, -8), (-1, -2), (-13, -2)]
        rotated = base_coords if self.rotation == 0 else [
            (x * math.cos(self.rotation) - y * math.sin(self.rotation),
             x * math.sin(self.rotation) + y * math.cos(self.rotation))
            for x, y in base_coords]
        coords = [(WIDTH//2 + 4*x, self.y - 4*y) for x, y in rotated]
        pygame.draw.polygon(screen, self.color, coords)

    def move(self):
        global score

        if self.state != "stopped":
            self.x += self.speed % TREE_SPACING

        if self.state == "flying":
            pass
        elif self.state == "descending":
            self.y += self.speed * 0.1
            if self.y >= GROUND_LEVEL:
                self.check_runway_or_crash()
        elif self.state == "landing":
            self.y += self.speed * 0.1
            if self.y >= GROUND_LEVEL:
                self.state = "touching"
                self.y = GROUND_LEVEL
        elif self.state == "touching":
            pass
        elif self.state == "down":
            pass
        elif self.state == "braking":
            self.speed -= 0.1
            if self.speed <= 0:
                self.speed = 0
                self.state = "stopped"
                score += 1
        elif self.state == "starting":
            self.y = GROUND_LEVEL
            self.speed += 0.1
            if self.speed >= MAX_PLANE_SPEED:
                self.speed = MAX_PLANE_SPEED
        elif self.state == "rising":
            self.y -= self.speed * 0.1
            if self.y <= CRUISING_ALTITUDE:
                self.y = CRUISING_ALTITUDE
                self.state = "flying"
                self.rotation = 0

    def check_runway_or_crash(self):
        global score
        plane_center = (WIDTH//2) % WIDTH + self.x % WIDTH
        if RUNWAY_RECT.left <= plane_center <= RUNWAY_RECT.right:
            self.state = "touching"
            self.y = GROUND_LEVEL
        else:
            self.state = "crashed"
            self.color = (255, 0, 0)
            self.speed = 0
            self.y = GROUND_LEVEL
            score -= 1


plane = Plane(0, y=CRUISING_ALTITUDE)

# generate clouds
clouds = []
for _ in range(5):
    clouds.append([random.randint(0, WIDTH), random.randint(20, 150)])


def draw_tree(x, y):
    pygame.draw.rect(screen, (139, 69, 19), (x-5, y-20, 10, 20))
    pygame.draw.polygon(screen, (0, 128, 0), [(x-30, y-20), (x+30, y-20), (x, y-100)])


def draw_cloud(x, y):
    pygame.draw.ellipse(screen, (255, 255, 255), (x, y, 60, 30))
    pygame.draw.ellipse(screen, (255, 255, 255), (x + 20, y - 10, 60, 40))
    pygame.draw.ellipse(screen, (255, 255, 255), (x + 40, y, 60, 30))


def draw_scene():
    screen.fill(SKY_COLOR)

    # draw clouds
    for cloud in clouds:
        draw_cloud(cloud[0], cloud[1])
        cloud[0] -= 1
        if cloud[0] < -100:
            cloud[0] = WIDTH + random.randint(0, 300)
            cloud[1] = random.randint(20, 150)

    pygame.draw.rect(screen, GRASS_COLOR, (0, HEIGHT - 100, WIDTH, 100))
    pygame.draw.rect(screen, RUNWAY_COLOR, RUNWAY_RECT)

    x = -plane.x
    while x < WIDTH:
        draw_tree(x, HEIGHT - 100)
        x += TREE_SPACING

    plane.draw()
    plane.move()

    draw_hud()

    clock.tick(60)
    pygame.display.flip()


def draw_hud():
    speed_text = font.render(f"speed: {int(plane.speed)}", True, (0, 0, 0))
    screen.blit(speed_text, (10, 10))

    score_text = font.render(f"score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 30))

    instructions = [
        "controls:",
        "down = descend / lower nose",
        "up = raise nose / takeoff",
        "right = start moving",
        "return = brake"
    ]
    for i, line in enumerate(instructions):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (WIDTH - 320, 10 + i * 18))


# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and plane.state == "flying":
                plane.rotation = -0.2
                plane.state = "descending"
            elif event.key == pygame.K_UP and plane.state == "descending":
                plane.rotation = 0.2
                if plane.y < GROUND_LEVEL - 100:
                    plane.state = "rising"
                else:
                    plane.state = "landing"
            elif event.key == pygame.K_DOWN and plane.state == "touching":
                plane.rotation = 0
                plane.state = "down"
            elif event.key == pygame.K_RETURN and plane.state == "down":
                plane.state = "braking"
            elif event.key == pygame.K_RIGHT and plane.state == "stopped":
                plane.state = "starting"
            elif event.key == pygame.K_UP and plane.state == "starting" \
                    and plane.speed == MAX_PLANE_SPEED:
                plane.rotation = 0.1
                plane.state = "rising"
    draw_scene()
