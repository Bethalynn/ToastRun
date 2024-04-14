
import pygame
import random

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill((255, 255, 255))

    def render(self, screen):
        screen.blit(self.surface, (0, 0))

class WelcomeScreen(Screen):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.font = pygame.font.Font(None, 72)
        self.big_font = pygame.font.Font(None, 36)

    def render(self, screen):
        super().render(screen)

        welcome_text = self.font.render("Dino Run", True, (0, 0, 0))
        welcome_rect = welcome_text.get_rect(center=(self.width // 2, self.height // 2 - 36))
        self.surface.blit(welcome_text, welcome_rect)

        start_text = self.big_font.render("To start, press SPACE", True, (0, 0, 0))
        start_rect = start_text.get_rect(center=(self.width // 2, self.height // 2 + 36))
        self.surface.blit(start_text, start_rect)

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the game window
        self.width, self.height = 800, 400
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Toast Run")

        # Set up colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # Set up the player
        self.player_width, self.player_height = 50, 50
        self.player_x = 50
        self.player_y = self.height - self.player_height
        self.player_vel_y = 0

        # Set up the objects
        self.object_width, self.object_height = 50, 50
        self.object_x = self.width
        self.object_y = self.height - self.object_height #  self.height - self.o bject_height
        self.object_color = self.RED

        # Set up game variables
        self.score = 0
        self.is_jumping = False

        # Load game fonts
        self.font = pygame.font.Font('actionj.ttf', 36)

        self.clock = pygame.time.Clock()

        # Set up lives
        self.lives = 3

        # Set up image
        self.image = pygame.image.load("CuteToast.png")
        self.image = pygame.transform.scale(self.image,(150, 150))

        self.imageKnife = pygame.image.load("cute knife.jpg")
        self.imageKnife = pygame.transform.scale(self.imageKnife,(100, 100))

        self.imageAvocado = pygame.image.load("cute avocado.webp")
        self.imageAvocado = pygame.transform.scale(self.imageAvocado,(100, 100))        

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.is_jumping:
                        self.player_vel_y = -20 # Increase jump height
                        self.is_jumping = True
                    if event.key == pygame.K_q:
                        self.game_over()
                        

            self.update_player()
            self.update_object()
            self.check_collision()
            self.check_pass()
            self.render()

            self.clock.tick(90) #random.randint(1,100))


        pygame.quit()

    def update_player(self):
        # Update player position
        self.player_y += self.player_vel_y
        self.player_vel_y += 1  # Apply gravity

        # Check for collision with the ground
        if self.player_y >= self.height - self.player_height:
            self.player_y = self.height - self.player_height
            self.player_vel_y = 0
            self.is_jumping = False

    def update_object(self):
        # Update object position
        self.object_x -= 5

    def check_collision(self):
        # Check for collision with the object
        if self.player_x + self.player_width > self.object_x and self.player_x < self.object_x + self.object_width \
                and self.player_y + self.player_height > self.object_y:
            if self.object_color == self.RED:
                self.lives-=1
                self.object_x = self.width
                self.object_y = self.height - self.object_height#random.randint(self.height - self.object_height - 50, self.height - self.object_height - 50)
                self.object_color = self.RED if random.random() < 0.8 else self.GREEN
                print(self.lives,"lives remaining")
                if self.lives<=0:
                    self.game_over()
            elif self.object_color == self.GREEN:
                self.score += 1
                self.object_x = self.width
                self.object_y = self.height - self.object_height #random.randint(self.height - self.object_height - 100, self.height - self.object_height - 50) # random.randint(50, self.height - self.object_height - 50)
                self.object_color = self.RED if random.random() < 0.8 else self.GREEN

    def check_pass(self):
        # Check if the object has passed the player
        if self.object_x + self.object_width < 0:
            self.object_x = self.width
            self.object_y = self.height - self.object_height #random.randint(50, self.height - self.object_height - 50)
            self.object_color = self.RED if random.random() < 0.5 else self.GREEN

    def render(self):
        # Clear the screen
        self.window.fill(self.WHITE)

        # Draw the player
        self.window.blit(self.image, (self.player_x-self.player_width, self.player_y-self.player_height-15))
        #pygame.draw.rect(self.window, self.BLACK, (self.player_x, self.player_y, self.player_width, self.player_height))

        # Draw the object
        if self.object_color == self.RED:
            self.window.blit(self.imageKnife, (self.object_x-self.object_width, self.object_y-self.object_height-15))
        elif self.object_color == self.GREEN:
            self.window.blit(self.imageAvocado, (self.object_x-self.object_width, self.object_y-self.object_height-15))#pygame.draw.rect(self.window, self.object_color, (self.object_x, self.object_y, self.object_width, self.object_height))


        # Display the score
        score_text = self.font.render("Score: " + str(self.score), True, self.BLACK)
        score_text2 = self.font.render("Lives remaining: " + str(self.lives), True, self.BLACK)
        self.window.blit(score_text2, (10, 40))
        self.window.blit(score_text, (10, 10))

        # Update the display
        pygame.display.update()

    def game_over(self):
        pygame.quit()

game = Game()
game.run()