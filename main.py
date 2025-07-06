import pygame
import random
import sys

pygame.init()

# Display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Plane Fighting Game")

# Fonts
font = pygame.font.SysFont(None, 36)

# Clock
clock = pygame.time.Clock()

# Load and scale images
player_image = pygame.image.load("HeroPlane.png")
player_image = pygame.transform.scale(player_image, (80, 60))

enemy_image = pygame.image.load("EnemyPlane.png")
enemy_image = pygame.transform.scale(enemy_image, (80, 60))

bullet_image = pygame.Surface((8, 20))
bullet_image.fill((255, 0, 0))  # Red

# Score
score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 20
        self.speed = 5
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.defeated = False

    def update(self):
        if self.defeated:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        max_x = max(1, screen_width - self.rect.width)
        self.rect.x = random.randint(0, max_x)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

    def update(self):
        if player.defeated:
            return
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.reset()

    def reset(self):
        max_x = max(1, screen_width - self.rect.width)
        self.rect.x = random.randint(0, max_x)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Initialize player and sprite groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

enemies = pygame.sprite.Group()
for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

bullets = pygame.sprite.Group()

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not player.defeated:
        all_sprites.update()

        # Bullet hits enemy
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for _ in hits:
            score += 1
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Enemy hits player
        if pygame.sprite.spritecollideany(player, enemies):
            player.defeated = True

    # Draw sprites
    all_sprites.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen_width - 150, 10))

    # Game over message
    if player.defeated:
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
