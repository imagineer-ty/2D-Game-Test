
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = BLUE
PLAYER_SPEED = 5
PLAYER_JUMP_STRENGTH = 12
GRAVITY = 0.5

# Platform settings
PLATFORM_COLOR = GREEN
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x

        # Check for collisions with platforms
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in platform_hit_list:
            if self.change_x > 0:
                self.rect.right = platform.rect.left
            elif self.change_x < 0:
                self.rect.left = platform.rect.right

        self.rect.y += self.change_y

        # Check for collisions with platforms
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in platform_hit_list:
            if self.change_y > 0:
                self.rect.bottom = platform.rect.top
                self.on_ground = True
                self.change_y = 0
            elif self.change_y < 0:
                self.rect.top = platform.rect.bottom
                self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY

        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.change_y = -PLAYER_JUMP_STRENGTH
            self.on_ground = False

    def go_left(self):
        self.change_x = -PLAYER_SPEED

    def go_right(self):
        self.change_x = PLAYER_SPEED

    def stop(self):
        self.change_x = 0

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Create platforms
platform1 = Platform(200, 500)
platform2 = Platform(400, 400)
platform3 = Platform(600, 300)
platforms.add(platform1, platform2, platform3)
all_sprites.add(platform1, platform2, platform3)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            elif event.key == pygame.K_RIGHT:
                player.go_right()
            elif event.key == pygame.K_SPACE:
                player.jump()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
            elif event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()

    # Update all sprites
    all_sprites.update()

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Flip the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
