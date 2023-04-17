import pygame
import random
import math

BALL_SPEED = 10
BALL_SPEED_INCREMENT = 1
SCORES_PER_LEVEL = 2

ball_color = pygame.Color('red')
ball_speed = [5, 5]
ball_radius = 20

# declaring screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 20
PLAYER_SPEED = 5

###########
border_width = 10
border_color = pygame.Color('white')
border_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# declaring colours in game

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# creating player class

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.score = 0
        self.held_ball = None

    def move_left(self):
        self.x -= PLAYER_SPEED * 3

    def move_right(self):
        self.x += PLAYER_SPEED * 3

    def move_up(self):
        self.y -= PLAYER_SPEED * 3

    def move_down(self):
        self.y += PLAYER_SPEED * 3

    def hold_ball(self, ball):
        self.held_ball = ball

    def release_ball(self):
        ball = self.held_ball
        self.held_ball = None
        return ball

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BALL_RADIUS)


# defining the ball in class

class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.color = color
        self.held_by = None
        self.level = 1
        self.radius = radius
        self.speed_x = speed
        self.speed_y = speed

    def set_speed(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def is_held(self):
        return self.held_by is not None

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BALL_RADIUS)


# main loop

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

BORDER_WIDTH = 10
border_rects = [
    pygame.Rect(50, 0, SCREEN_WIDTH, BORDER_WIDTH),  # Top
    pygame.Rect(0, SCREEN_HEIGHT - BORDER_WIDTH, SCREEN_WIDTH, BORDER_WIDTH),  # Bottom
    pygame.Rect(0, 0, BORDER_WIDTH, SCREEN_HEIGHT),  # Left
    pygame.Rect(SCREEN_WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, SCREEN_HEIGHT),  # Right
]
border_color = pygame.Color('red')

for rect in border_rects:
    pygame.draw.rect(screen, border_color, rect)

players = [Player(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2, BLUE), Player(3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2, RED)]
ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 20, GREEN, 2)


def increase_level(t):
    ball.level += 1
    t += 5
    return t


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                players[0].move_left()
            elif event.key == pygame.K_d:
                players[0].move_right()
            elif event.key == pygame.K_w:
                players[0].move_up()
            elif event.key == pygame.K_s:
                players[0].move_down()
            elif event.key == pygame.K_LEFT:
                players[1].move_left()
            elif event.key == pygame.K_RIGHT:
                players[1].move_right()
            elif event.key == pygame.K_UP:
                players[1].move_up()
            elif event.key == pygame.K_DOWN:
                players[1].move_down()
            elif event.key == pygame.K_SPACE:
                if not ball.is_held():
                    for player in players:
                        distance = math.sqrt((player.x - ball.x) ** 2 + (player.y - ball.y) ** 2)
                        if distance <= BALL_RADIUS:
                            player.hold_ball(ball)
                            ball.held_by = player
                            break
                else:
                    ball.held_by.release_ball()

        # Check for collisions between players and ball
    for player in players:
        distance = math.sqrt((player.x - ball.x) ** 2 + (player.y - ball.y) ** 2)
        if distance <= BALL_RADIUS:
            player.score += 1
            ball.x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
            ball.y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            ball.held_by = None
        if distance > 800:
            ball.x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
            ball.y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            ball.held_by = None


    if not ball.is_held():
        ball.move(ball.speed_x, ball.speed_y)

        # Check for  walls
        if ball.x < BALL_RADIUS or ball.x > SCREEN_WIDTH - BALL_RADIUS:
            ball.speed_x *= -1
        if ball.y < BALL_RADIUS or ball.y > SCREEN_HEIGHT - BALL_RADIUS:
            ball.speed_y *= -1
        if ball.x < BALL_RADIUS:
            ball.x = BALL_RADIUS
        if ball.x > SCREEN_WIDTH - BALL_RADIUS:
            ball.x = SCREEN_WIDTH - BALL_RADIUS
        if ball.y < BALL_RADIUS:
            ball.y = BALL_RADIUS
        if ball.y > SCREEN_HEIGHT - BALL_RADIUS:
            ball.y = SCREEN_HEIGHT - BALL_RADIUS



    screen.fill(BLACK)

    BORDER_WIDTH = 10
    borderrects = [
        pygame.Rect(50, 0, SCREEN_WIDTH, BORDER_WIDTH),  # Top bordr
        pygame.Rect(0, SCREEN_HEIGHT - BORDER_WIDTH, SCREEN_WIDTH, BORDER_WIDTH),  # Bottom bordr
        pygame.Rect(0, 0, BORDER_WIDTH, SCREEN_HEIGHT),  # Left
        pygame.Rect(SCREEN_WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, SCREEN_HEIGHT),  # Right wal
    ]
    border_color = pygame.Color('blue')
    ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]

    for rect in borderrects:
        pygame.draw.rect(screen, border_color, rect)
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Move ball if it's not held
    if not ball.is_held():
        ball.move(0, 1)

    # Check if ball is being held and move it with the player
    for player in players:
        if player.held_ball is not None:
            ball.move(player.x - ball.x, player.y - ball.y)

    # Check for collisions between players and ball
    for player in players:
        distance = math.sqrt((player.x - ball.x) ** 2 + (player.y - ball.y) ** 2)
        if distance <= BALL_RADIUS:
            player.score += 1
            ball.x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
            ball.y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
            ball.held_by = None



    # Draw players and ball
    for player in players:
        player.draw(screen)
    ball.draw(screen)

    # Draw scores
    font = pygame.font.SysFont(None, 48)
    score_text = font.render(f"{players[0].score} - {players[1].score}", True, WHITE)
    screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) / 2, 10))

    pygame.display.update()
    clock.tick(60)
