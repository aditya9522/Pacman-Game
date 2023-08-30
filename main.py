import pygame
import random

# Initialize Pygame
pygame.init()

# Game variables
screen_width, screen_height = 640, 600
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60

# Create the game screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pac-Man Game")

# Loading images
pacman_image = pygame.image.load("assets/pacman.png")
pacman_image = pygame.transform.scale(pacman_image, (25, 25))

ghost_image = pygame.image.load("assets/ghost.png")
ghost_image = pygame.transform.scale(ghost_image, (20, 20))
dot_image = pygame.image.load("assets/dot.png")
dot_image = pygame.transform.scale(dot_image, (25, 25))

game_won = False


# creating classes for operating or creating objects (dots)
class Object:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        screen.blit(self.image, self.rect)

class PacMan(Object):
    def __init__(self, x, y):
        super().__init__(x, y, pacman_image)
        self.speed = 5

    def move(self, dx, dy, obstacles):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if self.is_valid_move(new_x, new_y, obstacles):
            self.x = new_x
            self.y = new_y
            self.rect.center = (self.x, self.y)

    def is_valid_move(self, new_x, new_y, obstacles):
        new_rect = self.image.get_rect(center=(new_x, new_y))
        for obstacle in obstacles:
            if obstacle.rect.colliderect(new_rect):
                return False
        return 0 <= new_x < screen_width and 0 <= new_y < screen_height

class Ghost(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.speed = 1

    def move(self, obstacles):
        new_x = self.x + random.choice([-1, 1]) * self.speed
        new_y = self.y + random.choice([-1, 1]) * self.speed
        if self.is_valid_move(new_x, new_y, obstacles):
            self.x = new_x
            self.y = new_y
            self.rect.center = (self.x, self.y)

    def move_towards_pacman(self, pacman, obstacles):
        dx = pacman.x - self.x
        dy = pacman.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            dx_normalized = dx / distance
            dy_normalized = dy / distance
            new_x = self.x + dx_normalized * self.speed
            new_y = self.y + dy_normalized * self.speed
            if self.is_valid_move(new_x, new_y, obstacles):
                self.x = new_x
                self.y = new_y
                self.rect.center = (self.x, self.y)

    def is_valid_move(self, new_x, new_y, obstacles):
        new_rect = self.image.get_rect(center=(new_x, new_y))
        for obstacle in obstacles:
            if obstacle.rect.colliderect(new_rect):
                return False
        return True


class Dot(Object):
    def __init__(self, x, y):
        super().__init__(x, y, dot_image)
        self.eaten = False

    def check_collision(self, pacman):
        distance = ((pacman.x - self.x) ** 2 + (pacman.y - self.y) ** 2) ** 0.5
        if distance < pacman.image.get_width() / 2 + self.image.get_width() / 2:
            self.eaten = True

class Obstacle(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, pygame.Surface((width, height)))
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect(topleft=(x, y))

obstacles = [
    Obstacle(0, 0, 20, screen_height),                   
    Obstacle(screen_width - 20, 0, 20, screen_height),          
    Obstacle(0, 0, screen_width, 20),                    
    Obstacle(0, screen_height - 20, screen_width, 20),          
    Obstacle(100, 100, screen_width-200, 20),  
    Obstacle(150, 150, screen_width-300, 20),  
    Obstacle(100, 150, 20, screen_height-300),  
    Obstacle(screen_width-120, 150, 20, screen_height-300),  
    Obstacle(screen_width-170, 200, 20, screen_height-400), 
    Obstacle(150, screen_height-170, screen_width-300, 20), 
    Obstacle(150, 200, 20, 200),   
    Obstacle(50, 50, screen_width-100, 20),
      
    Obstacle(50, screen_height-70, screen_width-100, 20),
    Obstacle(100, screen_height-120, screen_width-200, 20),  
    # Obstacle(50, 50, WIDTH-100, 20),
    
]

# Positioning the objects
pacman = PacMan(screen_width // 2, screen_height // 2)

ghosts = []
num_ghosts = 3
ghost_width = ghost_image.get_width()
ghost_height = ghost_image.get_height()

for _ in range(num_ghosts):
    while True:
        ghost_x = random.randint(ghost_width // 2, screen_width - ghost_width // 2)
        ghost_y = random.randint(ghost_height // 2, screen_height - ghost_height // 2)
        new_ghost = Ghost(ghost_x, ghost_y, ghost_image)
        
        overlaps_obstacle = any(obstacle.rect.colliderect(new_ghost.rect) for obstacle in obstacles)
        
        if not overlaps_obstacle:
            ghosts.append(new_ghost)
            break                
                
dots = []
num_dots = 10
for _ in range(num_dots):
    while True:
        dot_x = random.randint(dot_image.get_width() // 2, screen_width - dot_image.get_width() // 2)
        dot_y = random.randint(dot_image.get_height() // 2, screen_height - dot_image.get_height() // 2)
        new_dot = Dot(dot_x, dot_y)
        
        overlaps_obstacle = any(obstacle.rect.colliderect(new_dot.rect) for obstacle in obstacles)
        
        if not overlaps_obstacle:
            dots.append(new_dot)
            break

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def update_entities():
    for ghost in ghosts:
        ghost.move_towards_pacman(pacman, obstacles)

def check_collisions():
    global dots, game_won  
    dots_to_remove = []
    for ghost in ghosts:
        if ghost.rect.colliderect(pacman.rect):
            pygame.quit()
            exit()

    for i, dot in enumerate(dots):
        dot.check_collision(pacman)
        if dot.eaten:
            dots_to_remove.append(i)

    for index in reversed(dots_to_remove):
        dots.pop(index)

    if not dots:
        game_won = True

    for dot in dots:
        dot.check_collision(pacman)



def draw_screen():
    screen.fill(BACKGROUND_COLOR)
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()
    for dot in dots:
        dot.draw() 
    for obstacle in obstacles:
        obstacle.draw()
    pygame.display.flip()

    if game_won:
        font = pygame.font.Font(None, 36)
        text = font.render("You Win!", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

    pygame.display.flip()


clock = pygame.time.Clock()
running = True

# Main game loop
while running:
    handle_events()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman.move(-1, 0, obstacles)
    if keys[pygame.K_RIGHT]:
        pacman.move(1, 0, obstacles)
    if keys[pygame.K_UP]:
        pacman.move(0, -1, obstacles)
    if keys[pygame.K_DOWN]:
        pacman.move(0, 1, obstacles)
    
    for ghost in ghosts:
        ghost.move(obstacles)

    update_entities()
    check_collisions()
    draw_screen()
    clock.tick(FPS)

pygame.quit()
