import pygame
import pygame.freetype
from dataclasses import dataclass
import math
import random

# === Initialize ===
pygame.init()
pygame.freetype.init()

# === Screen ===
WIDTH, HEIGHT = 1024, 768
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("K'tah")
clock = pygame.time.Clock()

# === Colors ===
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
PURPLE = (80, 0, 80)
PLAYER_COLOR = (200, 200, 255)
ZOMBIE_COLOR = (80, 255, 0)
GHOUL_COLOR = (150, 0, 255)
DRAGON_COLOR = (255, 50, 50)
HEALTH_COLOR = (0, 200, 0)
SCARECROW_COLOR = (255, 200, 0)
BULLET_COLOR = (255, 255, 0)
PROJECTILE_COLOR = (255, 165, 0)
FIREBALL_COLOR = (255, 100, 0)
CONE_COLOR = (255, 50, 0)

# === Cooldowns (ms) ===
TELEPORT_COOLDOWN = 30000
SCARECROW_COOLDOWN = 45000
FREEZE_COOLDOWN = 120000
SHOOT_COOLDOWN = 1000
PLAYER_INVINCIBLE_DURATION = 1500

# === Dragon Cooldowns ===
DRAGON_FIREBALL_INTERVAL = 600
DRAGON_CONE_INTERVAL = 1500

# === Stats ===
BULLET_SPEED = 12
BULLET_DAMAGE_MOD = 1

# === Fonts ===
font = pygame.freetype.SysFont(None, 48)
ui_font = pygame.freetype.SysFont(None, 16)

# === Events ===
UNFREEZE = pygame.USEREVENT + 1
REMOVE_SCARECROW = pygame.USEREVENT + 2

# === Game State ===
frozen = False
scarecrow = None
game_over = False
game_won = False

# === Time Tracking ===
game_start_time = pygame.time.get_ticks()
best_time_seconds = 0
last_teleport = -TELEPORT_COOLDOWN
last_scarecrow = -SCARECROW_COOLDOWN
last_freeze = -FREEZE_COOLDOWN
last_player_hit = -PLAYER_INVINCIBLE_DURATION
last_shot_time = -SHOOT_COOLDOWN

# === Entities ===
bullets = []
projectiles = []
fireballs = []
cones = []
pickups = []

# === Round ===
round_number = 1
background_cycle = [BROWN, BLACK, PURPLE]
last_pickup_type = None
# === Agent Base Class ===
@dataclass
class Agent:
    x: float
    y: float
    radius: int
    speed: float
    color: tuple
    health: int
    max_health: int

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        self.draw_health_bar()

    def draw_health_bar(self):
        bar_width = 40
        bar_height = 6
        health_ratio = max(self.health / self.max_health, 0)
        x = int(self.x - bar_width // 2)
        y = int(self.y - self.radius - 12)
        pygame.draw.rect(screen, (100, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(
            screen,
            HEALTH_COLOR if isinstance(self, Player) else (255, 0, 0),
            (x, y, int(bar_width * health_ratio), bar_height)
        )

    def is_collided_with(self, other):
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance < (self.radius + other.radius)


# === Player ===
@dataclass
class Player(Agent):
    def teleport(self, pos):
        self.x, self.y = pos

    def move_towards(self, target):
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.hypot(dx, dy)
        if distance > 3.0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed


# === Zombie ===
@dataclass
class Zombie(Agent):
    def move_towards(self, target):
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.hypot(dx, dy)
        if distance > 3.0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed


# === Ghoul ===
@dataclass
class Ghoul(Agent):
    last_shot_time: int = 0

    def move_towards(self, target):
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.hypot(dx, dy)
        if distance > 3.0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def maybe_fire(self, current_time, player):
        if current_time - self.last_shot_time > 4000:
            self.last_shot_time = current_time
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                return Projectile(
                    x=self.x,
                    y=self.y,
                    dx=(dx / dist) * 4,
                    dy=(dy / dist) * 4
                )
        return None


# === Dragon ===
@dataclass
class Dragon(Agent):
    last_fireball_time: int = 0
    last_cone_time: int = 0
    spawn_time: int = 0  # Wait 1 second before attacking

    def move_towards(self, target):
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.hypot(dx, dy)
        if distance > 3.0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def maybe_fireball(self, current_time, player):
        if current_time - self.spawn_time < 1000:
            return None
        if current_time - self.last_fireball_time > DRAGON_FIREBALL_INTERVAL:
            self.last_fireball_time = current_time
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                return Fireball(
                    x=self.x,
                    y=self.y,
                    dx=(dx / dist) * 6,
                    dy=(dy / dist) * 6
                )
        return None

    def maybe_cone(self, current_time, player):
        if current_time - self.spawn_time < 1000:
            return None
        if current_time - self.last_cone_time > DRAGON_CONE_INTERVAL:
            self.last_cone_time = current_time
            return Cone(
                x=self.x,
                y=self.y,
                angle=math.atan2(player.y - self.y, player.x - self.x),
                created_at=current_time
            )
        return None
# === Bullet ===
@dataclass
class Bullet:
    x: float
    y: float
    dx: float
    dy: float
    target: Agent

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(screen, BULLET_COLOR, (int(self.x), int(self.y)), 4)


# === Projectile (Ghoul Shot) ===
@dataclass
class Projectile:
    x: float
    y: float
    dx: float
    dy: float

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(screen, PROJECTILE_COLOR, (int(self.x), int(self.y)), 8)


# === Fireball (Dragon Shot) ===
@dataclass
class Fireball:
    x: float
    y: float
    dx: float
    dy: float

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(screen, FIREBALL_COLOR, (int(self.x), int(self.y)), 16)


# === Cone Attack (Dragon Cone) ===
@dataclass
class Cone:
    x: float
    y: float
    angle: float
    created_at: int

    def draw(self):
        length = 450
        spread = math.pi / 6
        left_angle = self.angle - spread
        right_angle = self.angle + spread

        points = [
            (self.x, self.y),
            (self.x + math.cos(left_angle) * length, self.y + math.sin(left_angle) * length),
            (self.x + math.cos(right_angle) * length, self.y + math.sin(right_angle) * length)
        ]

        pygame.draw.polygon(screen, CONE_COLOR, points)


# === Enemy Manager ===
class EnemyManager:
    def __init__(self):
        self.zombies = []
        self.ghouls = []
        self.dragon = None

    def all_enemies(self):
        enemies = self.zombies + self.ghouls
        if self.dragon:
            enemies.append(self.dragon)
        return enemies

    def add_zombie(self, zombie):
        self.zombies.append(zombie)

    def add_ghoul(self, ghoul):
        self.ghouls.append(ghoul)

    def set_dragon(self, dragon):
        self.dragon = dragon

    def remove_enemy(self, enemy):
        if enemy in self.zombies:
            self.zombies.remove(enemy)
        elif enemy in self.ghouls:
            self.ghouls.remove(enemy)
        elif enemy == self.dragon:
            self.dragon = None
# === UI Drawing Functions ===

def draw_cooldown_bar(current_time):
    bar_width = 120
    bar_height = 10
    spacing = 30
    bottom = HEIGHT - 15
    cooldowns = [
        ("Teleport", last_teleport, TELEPORT_COOLDOWN, (0, 200, 255)),
        ("Scarecrow", last_scarecrow, SCARECROW_COOLDOWN, (255, 200, 0)),
        ("Freeze", last_freeze, FREEZE_COOLDOWN, (0, 255, 150)),
    ]
    for i, (label, last_used, cooldown, color) in enumerate(cooldowns):
        x = 50 + i * (bar_width + spacing)
        elapsed = current_time - last_used
        ratio = min(elapsed / cooldown, 1.0)
        fill_width = int(bar_width * ratio)
        pygame.draw.rect(screen, (50, 50, 50), (x, bottom, bar_width, bar_height))
        pygame.draw.rect(screen, color, (x, bottom, fill_width, bar_height))
        ui_font.render_to(screen, (x, bottom - 15), label, (255, 255, 255))


def draw_player_health():
    bar_width = 200
    bar_height = 20
    x = WIDTH - bar_width - 20
    y = HEIGHT - 30
    ratio = max(player.health / player.max_health, 0)
    pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, HEALTH_COLOR, (x, y, int(bar_width * ratio), bar_height))
    ui_font.render_to(screen, (x, y - 15), "Player Health", (255, 255, 255))


def draw_timer_and_round(current_time):
    elapsed_ms = current_time - game_start_time
    seconds_total = elapsed_ms // 1000
    minutes = seconds_total // 60
    seconds = seconds_total % 60
    time_text = f"{minutes:02}:{seconds:02}"
    round_text = f"Round {round_number}"
    ui_font.render_to(screen, (20, 20), time_text, (255, 255, 255))
    ui_font.render_to(screen, (WIDTH - 120, 20), round_text, (255, 255, 255))


def draw_scene():
    background = background_cycle[((round_number - 1) // 5) % len(background_cycle)]
    screen.fill(background)

    for pickup in pickups:
        if pickup['type'] == 'health':
            pygame.draw.rect(screen, pickup['color'], pygame.Rect(pickup['x'] - 8, pickup['y'] - 8, 16, 16))
            ui_font.render_to(screen, (pickup['x'] - 15, pickup['y'] - 25), "Health", (255, 255, 255))
        elif pickup['type'] == 'speed':
            pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(pickup['x'] - 6, pickup['y'] - 10, 12, 20))
            ui_font.render_to(screen, (pickup['x'] - 20, pickup['y'] - 25), "Speed", (255, 255, 255))
        elif pickup['type'] == 'damage':
            points = [
                (pickup['x'], pickup['y'] - 12),
                (pickup['x'] - 8, pickup['y'] + 8),
                (pickup['x'] + 8, pickup['y'] + 8)
            ]
            pygame.draw.polygon(screen, (255, 255, 0), points)
            ui_font.render_to(screen, (pickup['x'] - 25, pickup['y'] - 25), "Damage", (255, 255, 255))
        elif pickup['type'] == 'firerate':
            hex_points = []
            for i in range(6):
                angle = math.radians(i * 60)
                x = pickup['x'] + 10 * math.cos(angle)
                y = pickup['y'] + 10 * math.sin(angle)
                hex_points.append((x, y))
            pygame.draw.polygon(screen, (255, 255, 255), hex_points)
            ui_font.render_to(screen, (pickup['x'] - 30, pickup['y'] - 25), "Fire Rate", (255, 255, 255))

    if scarecrow is not None:
        pygame.draw.circle(screen, SCARECROW_COLOR, scarecrow, 20)

    player.draw()

    for enemy in enemies.all_enemies():
        enemy.draw()

    for bullet in bullets:
        bullet.draw()

    for proj in projectiles:
        proj.draw()

    for fb in fireballs:
        fb.draw()

    for cone in cones:
        cone.draw()

    draw_cooldown_bar(pygame.time.get_ticks())
    draw_player_health()
    draw_timer_and_round(pygame.time.get_ticks())
    pygame.display.flip()


# === Start Menu ===
def start_menu():
    screen.fill((0, 0, 0))
    font.render_to(screen, (WIDTH // 2 - 180, HEIGHT // 2), "PRESS SPACE TO START", (255, 255, 255))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                waiting = False


# === Game Initialization ===
player = Player(
    x=WIDTH // 2,
    y=HEIGHT // 2,
    radius=20,
    speed=5,
    color=PLAYER_COLOR,
    health=100,
    max_health=100
)

enemies = EnemyManager()

# Spawn 4 zombies at corners
spawn_positions = [
    (20, 20),
    (WIDTH - 20, 20),
    (20, HEIGHT - 20),
    (WIDTH - 20, HEIGHT - 20)
]
for pos in spawn_positions:
    enemies.add_zombie(Zombie(
        x=pos[0],
        y=pos[1],
        radius=20,
        speed=2,
        color=ZOMBIE_COLOR,
        health=40,
        max_health=40
    ))

start_menu()
# === Main Game Loop ===
while True:
    current_time = pygame.time.get_ticks()

    # === Handle Events ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        elif event.type == pygame.MOUSEBUTTONDOWN and not (game_over or game_won):
            if current_time - last_teleport >= TELEPORT_COOLDOWN:
                player.teleport(event.pos)
                last_teleport = current_time

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and not frozen:
                if current_time - last_freeze >= FREEZE_COOLDOWN:
                    frozen = True
                    last_freeze = current_time
                    pygame.time.set_timer(UNFREEZE, 5000, loops=1)

            elif event.key == pygame.K_s and scarecrow is None:
                if current_time - last_scarecrow >= SCARECROW_COOLDOWN:
                    scarecrow = pygame.mouse.get_pos()
                    last_scarecrow = current_time
                    pygame.time.set_timer(REMOVE_SCARECROW, 5000, loops=1)

        elif event.type == UNFREEZE:
            frozen = False

        elif event.type == REMOVE_SCARECROW:
            scarecrow = None

    # === Player Movement ===
    if not (game_over or game_won):
        player.move_towards(pygame.mouse.get_pos())

    # === Auto Shooting ===
    if not (game_over or game_won):
        if current_time - last_shot_time >= SHOOT_COOLDOWN:
            targets = enemies.all_enemies()
            if targets:
                last_shot_time = current_time
                nearest = min(
                    targets,
                    key=lambda e: math.hypot(player.x - e.x, player.y - e.y)
                )
                dx = nearest.x - player.x
                dy = nearest.y - player.y
                dist = math.hypot(dx, dy)
                if dist != 0:
                    bullets.append(Bullet(
                        x=player.x,
                        y=player.y,
                        dx=(dx / dist) * BULLET_SPEED,
                        dy=(dy / dist) * BULLET_SPEED,
                        target=nearest
                    ))

    # === Pickup Collection ===
    for pickup in pickups[:]:
        if math.hypot(player.x - pickup['x'], player.y - pickup['y']) < player.radius:
            if pickup['type'] == 'health':
                player.max_health += 25
                player.health = player.max_health
            elif pickup['type'] == 'firerate':
                SHOOT_COOLDOWN = max(200, SHOOT_COOLDOWN - 100)
            elif pickup['type'] == 'speed':
                player.speed += 0.5
            elif pickup['type'] == 'damage':
                BULLET_DAMAGE_MOD += 1
            last_pickup_type = pickup['type']
            pickups.remove(pickup)

    # === Enemy Behavior ===
    if not frozen:
        for enemy in enemies.all_enemies():
            target = scarecrow or (player.x, player.y)
            enemy.move_towards(target)

            if enemy.is_collided_with(player):
                if current_time - last_player_hit >= PLAYER_INVINCIBLE_DURATION:
                    player.health -= 25
                    last_player_hit = current_time
                    if player.health <= 0:
                        game_over = True

        for ghoul in enemies.ghouls:
            proj = ghoul.maybe_fire(current_time, player)
            if proj:
                projectiles.append(proj)

        if enemies.dragon:
            fireball = enemies.dragon.maybe_fireball(current_time, player)
            cone = enemies.dragon.maybe_cone(current_time, player)
            if fireball:
                fireballs.append(fireball)
            if cone:
                cones.append({'cone': cone, 'start_time': current_time})

    # === Bullet Collision ===
    for bullet in bullets[:]:
        bullet.move()
        if bullet.target.health > 0 and math.hypot(bullet.x - bullet.target.x, bullet.y - bullet.target.y) < bullet.target.radius:
            bullet.target.health -= (bullet.target.max_health // 5) * BULLET_DAMAGE_MOD

            if bullet.target.health <= 0:
                is_dragon = bullet.target == enemies.dragon
                enemies.remove_enemy(bullet.target)

                if round_number == 15 and is_dragon:
                    game_won = True
                    win_time = current_time
                elif not enemies.all_enemies():
                    drop_types = ['health', 'firerate', 'speed', 'damage']
                    valid_drops = [d for d in drop_types if not (d == last_pickup_type and d in ['health', 'speed'])]
                    pickup_type = random.choice(valid_drops)
                    last_pickup_type = pickup_type

                    pickups.append({
                        'type': pickup_type,
                        'x': bullet.target.x,
                        'y': bullet.target.y,
                        'color': {
                            'health': (255, 0, 0),
                            'firerate': (0, 0, 255),
                            'speed': (0, 255, 0),
                            'damage': (255, 165, 0),
                        }[pickup_type]
                    })

                    if not game_won and 'pending_round_start' not in globals():
                        pending_round_start = current_time + 5000

            bullets.remove(bullet)

    # === Projectile Collision ===
    for proj in projectiles[:]:
        proj.move()
        if math.hypot(proj.x - player.x, proj.y - player.y) < player.radius:
            player.health -= 15
            projectiles.remove(proj)
            if player.health <= 0:
                game_over = True

    for fireball in fireballs[:]:
        fireball.move()
        if math.hypot(fireball.x - player.x, fireball.y - player.y) < player.radius + 10:
            player.health -= 35
            fireballs.remove(fireball)
            if player.health <= 0:
                game_over = True

    # === Cone Collision ===
    for cone_data in cones[:]:
        cone = cone_data['cone']
        start_time = cone_data['start_time']
        if current_time - start_time > 1000:
            cones.remove(cone_data)
        else:
            dx = player.x - cone.x
            dy = player.y - cone.y
            angle_to_player = math.atan2(dy, dx)
            angle_diff = abs((angle_to_player - cone.angle + math.pi) % (2 * math.pi) - math.pi)
            if angle_diff < math.pi / 6:
                dist = math.hypot(dx, dy)
                if dist < 450:
                    if current_time - last_player_hit >= PLAYER_INVINCIBLE_DURATION:
                        player.health -= 40
                        last_player_hit = current_time
                        if player.health <= 0:
                            game_over = True

    # === Check for Round Start ===
    if 'pending_round_start' in globals() and current_time >= pending_round_start:
        round_number += 1
        spawn_count = round_number + 3

        for i in range(spawn_count):
            edge = i % 4
            if edge == 0:
                spawn_x, spawn_y = 0, random.randint(0, HEIGHT)
            elif edge == 1:
                spawn_x, spawn_y = WIDTH, random.randint(0, HEIGHT)
            elif edge == 2:
                spawn_x, spawn_y = random.randint(0, WIDTH), 0
            else:
                spawn_x, spawn_y = random.randint(0, WIDTH), HEIGHT

            health_scale = 1 + (round_number // 5) * 0.6

            if round_number == 15:
                enemies.set_dragon(Dragon(
                    x=WIDTH - 100,
                    y=100,
                    radius=70,
                    speed=1.2,
                    color=DRAGON_COLOR,
                    health=int(8000 * health_scale),
                    max_health=int(8000 * health_scale),
                    spawn_time=current_time
                ))
            elif round_number >= 5 and random.randint(1, 5) == 1:
                enemies.add_ghoul(Ghoul(
                    x=spawn_x,
                    y=spawn_y,
                    radius=22,
                    speed=1.0,
                    color=GHOUL_COLOR,
                    health=int(60 * health_scale),
                    max_health=int(60 * health_scale)
                ))
            else:
                enemies.add_zombie(Zombie(
                    x=spawn_x,
                    y=spawn_y,
                    radius=20,
                    speed=1.5 + 0.1 * round_number,
                    color=ZOMBIE_COLOR,
                    health=int(40 * health_scale),
                    max_health=int(40 * health_scale)
                ))

        del pending_round_start

    # === Game Over Screen ===
    if game_over:
        survival_seconds = (current_time - game_start_time) // 1000
        if survival_seconds > best_time_seconds:
            best_time_seconds = survival_seconds

        minutes = best_time_seconds // 60
        seconds = best_time_seconds % 60
        best_text = f"BEST TIME: {minutes:02}:{seconds:02}"

        screen.fill((0, 0, 0))
        font.render_to(screen, (WIDTH // 2 - 100, HEIGHT // 2 - 30), "GAME OVER", (255, 0, 0))
        font.render_to(screen, (WIDTH // 2 - 130, HEIGHT // 2 + 20), best_text, (255, 255, 255))
        font.render_to(screen, (WIDTH // 2 - 180, HEIGHT // 2 + 70), "PRESS R TO RESTART OR ESC TO QUIT", (255, 255, 255))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.quit()
                        import os
                        os.system("python " + __file__)
                        raise SystemExit
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit

    # === Win Screen ===
    if game_won:
        elapsed_ms = win_time - game_start_time
        seconds_total = elapsed_ms // 1000
        minutes = seconds_total // 60
        seconds = seconds_total % 60
        win_text = f"TIME: {minutes:02}:{seconds:02}"

        screen.fill((0, 0, 0))
        font.render_to(screen, (WIDTH // 2 - 100, HEIGHT // 2 - 60), "YOU WIN!", (0, 255, 0))
        font.render_to(screen, (WIDTH // 2 - 120, HEIGHT // 2 - 10), win_text, (255, 255, 255))
        font.render_to(screen, (WIDTH // 2 - 180, HEIGHT // 2 + 40), "PRESS R TO RESTART OR ESC TO QUIT", (255, 255, 255))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.quit()
                        import os
                        os.system("python " + __file__)
                        raise SystemExit
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit

    # === Draw Everything ===
    draw_scene()

    # === Tick ===
    clock.tick(FPS)
