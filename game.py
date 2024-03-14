import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALLOON_RADIUS = 30
BALLOON_SPEED = 2
TIMER_FONT_SIZE = 36
SCORE_FONT_SIZE = 24
TOTAL_SECONDS = 120  # 2 minutes

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Balloon Popper')

# Fonts
timer_font = pygame.font.SysFont(None, TIMER_FONT_SIZE)
score_font = pygame.font.SysFont(None, SCORE_FONT_SIZE)

# Variables
score = 0
balloons_popped = 0
balloons_missed = 0
timer = TOTAL_SECONDS
clock = pygame.time.Clock()

# Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALLOON_RADIUS * 2, BALLOON_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (BALLOON_RADIUS, BALLOON_RADIUS), BALLOON_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - BALLOON_RADIUS * 2)
        self.rect.y = SCREEN_HEIGHT

    def update(self):
        self.rect.y -= BALLOON_SPEED
        if self.rect.y < -BALLOON_RADIUS * 2:
            global balloons_missed
            balloons_missed += 1
            self.kill()

# Group for balloons
balloon_group = pygame.sprite.Group()

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Timer
    minutes = timer // 60
    seconds = timer % 60
    timer_text = timer_font.render(f'Time: {minutes:02}:{seconds:02}', True, BLACK)
    screen.blit(timer_text, (10, 10))
    if timer <= 0:
        running = False

    # Decrement timer every frame
    timer -= 1 / 60  # Decrement by 1 second (1/60 seconds per frame)

    # Score
    score_text = score_font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 50))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for balloon in balloon_group:
                    if balloon.rect.collidepoint(event.pos):
                        score += 2
                        balloons_popped += 1
                        balloon.kill()

    # Generate balloons
    if random.randint(1, 100) == 1:
        new_balloon = Balloon()
        balloon_group.add(new_balloon)

    # Update balloons
    balloon_group.update()
    balloon_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# End game
print(f'Final Score: {score}')
print(f'Balloons Popped: {balloons_popped}')
print(f'Balloons Missed: {balloons_missed}')

pygame.quit()
sys.exit()
