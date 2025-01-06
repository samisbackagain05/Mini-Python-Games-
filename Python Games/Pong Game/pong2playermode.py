import pygame
import sys
import random
import argparse

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
GRAY = (169, 169, 169)
TURQUOISE = (64, 224, 208)
LIME = (0, 255, 0)
VIOLET = (238, 130, 238)
GOLD = (255, 215, 0)
SLATEBLUE = (106, 90, 205)
TEAL = (0, 128, 128)
TOMATO = (255, 99, 71)
SALMON = (250, 128, 114)
PEACHPUFF = (255, 218, 185)
LIGHTCORAL = (240, 128, 128)
SEASHELL = (255, 245, 238)
MINTCREAM = (245, 255, 250)
LIGHTYELLOW = (255, 255, 224)
LIGHTGREEN = (144, 238, 144)
LAVENDER = (230, 230, 250)
INDIGO = (75, 0, 130)
CHARTREUSE = (127, 255, 0)
CRIMSON = (220, 20, 60)
FUCHSIA = (255, 0, 255)
DODGERBLUE = (30, 144, 255)
PALEVIOLETRED = (219, 112, 147)
MIDNIGHTBLUE = (25, 25, 112)
SLATEGRAY = (112, 128, 144)
STEELBLUE = (70, 130, 180)
LIGHTSTEELBLUE = (176, 224, 230)
CORAL = (255, 127, 80)
DARKORANGE = (255, 140, 0)
MINT = (189, 252, 201)
SEAGREEN = (46, 139, 87)
NAVY = (0, 0, 128)
OLIVE = (128, 128, 0)
TAN = (210, 180, 140)
DARKGOLDENROD = (184, 134, 11)
SADDLEBROWN = (139, 69, 19)
WHEAT = (245, 222, 179)

# Ball class to handle the ball movement and reset
class Ball:
    def __init__(self, center_x, center_y, radius, color, display_width, display_height):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color
        self.speed_x = 5 * random.choice([1, -1])
        self.speed_y = 5 * random.choice([1, -1])
        self.display_width = display_width
        self.display_height = display_height

    def update(self):
        # Update ball's position
        self.center_x += self.speed_x
        self.center_y += self.speed_y

        # Ball collision with top and bottom
        if self.center_y - self.radius <= 0 or self.center_y + self.radius >= self.display_height:
            self.speed_y *= -1

    def reset(self):
        self.center_x = self.display_width // 2
        self.center_y = self.display_height // 2
        self.speed_x = 5 * random.choice([1, -1])
        self.speed_y = 5 * random.choice([1, -1])

    def draw(self, screen):
        pygame.draw.circle(screen, DODGERBLUE, (self.center_x, self.center_y), self.radius)


# Paddle class to handle player paddles
class Paddle:
    def __init__(self, x, y, width, height, color, display_width, display_height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.display_width = display_width
        self.display_height = display_height
        self.speed_y = 0

    def move(self):
        # Move the paddle
        self.rect.y += self.speed_y
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.display_height:
            self.rect.bottom = self.display_height

    def draw(self, screen):
        pygame.draw.rect(screen, CRIMSON, self.rect)

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y


# Game class to handle game logic
class PongGame:
    def __init__(self, screen_width, screen_height, max_score, fps):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_score = max_score
        self.fps = fps
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()

        self.ball = Ball(screen_width // 2, screen_height // 2, 10, PURPLE, screen_width, screen_height)
        self.player1 = Paddle(10, screen_height // 2 - 40, 10, 80, BLUE, screen_width, screen_height)
        self.player2 = Paddle(screen_width - 20, screen_height // 2 - 40, 10, 80, RED, screen_width, screen_height)

        pygame.font.init()  # Ensure the font module is initialized

    def show_instructions(self):
        # Display instructions and controls
        font = pygame.font.Font(None, 36)
        instructions = [
            "Welcome to Pong Game!",
            "Player 1 controls: W (Up), S (Down)",
            "Player 2 controls: Arrow Up (Up), Arrow Down (Down)",
            "Goal: Score by getting the ball past the opponent",
            "Press SPACE to start the game"
        ]

        self.screen.fill(BLACK)
        y_offset = 100
        for line in instructions:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 40

        pygame.display.flip()

        # Wait for SPACE key to start
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
                    self.game_loop()  # Start the game

    def game_loop(self):
        player1_score = 0
        player2_score = 0
        game_over = False

        self.ball.reset()
        self.player1.reset(10, self.screen_height // 2 - 40)
        self.player2.reset(self.screen_width - 20, self.screen_height // 2 - 40)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player1.speed_y = -5
                    if event.key == pygame.K_s:
                        self.player1.speed_y = 5
                    if event.key == pygame.K_UP:
                        self.player2.speed_y = -5
                    if event.key == pygame.K_DOWN:
                        self.player2.speed_y = 5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        self.player1.speed_y = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.player2.speed_y = 0

            # Move paddles and ball
            self.player1.move()
            self.player2.move()
            self.ball.update()

            # Ball-paddle collision
            if self.ball.center_x - self.ball.radius <= self.player1.rect.right and \
               self.ball.center_y >= self.player1.rect.top and \
               self.ball.center_y <= self.player1.rect.bottom:
                self.ball.speed_x *= -1

            if self.ball.center_x + self.ball.radius >= self.player2.rect.left and \
               self.ball.center_y >= self.player2.rect.top and \
               self.ball.center_y <= self.player2.rect.bottom:
                self.ball.speed_x *= -1

            # Score points
            if self.ball.center_x - self.ball.radius <= 0:
                player2_score += 1
                self.ball.reset()

            if self.ball.center_x + self.ball.radius >= self.screen_width:
                player1_score += 1
                self.ball.reset()

            # Draw everything
            self.screen.fill(BLACK)
            self.ball.draw(self.screen)
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)

            # Draw the score
            font = pygame.font.Font(None, 36)
            player1_score_text = font.render(f"Player 1: {player1_score}", True, BLUE)
            player2_score_text = font.render(f"Player 2: {player2_score}", True, RED)
            self.screen.blit(player1_score_text, (self.screen_width // 2 - 100, 20))
            self.screen.blit(player2_score_text, (self.screen_width // 2 + 50, 20))

            # Check for game over
            if player1_score >= self.max_score:
                game_over = True
                winner_text = font.render("Player 1 Wins!", True, WHITE)
                self.screen.blit(winner_text, (self.screen_width // 2 - winner_text.get_width() // 2, self.screen_height // 2))
                pygame.display.flip()
                pygame.time.delay(2000)

            if player2_score >= self.max_score:
                game_over = True
                winner_text = font.render("Player 2 Wins!", True, WHITE)
                self.screen.blit(winner_text, (self.screen_width // 2 - winner_text.get_width() // 2, self.screen_height // 2))
                pygame.display.flip()
                pygame.time.delay(2000)

            pygame.display.flip()
            self.clock.tick(self.fps)


def main():
    parser = argparse.ArgumentParser(description="Pong Game")
    parser.add_argument("-dw", "--width", type=int, default=800, help="Width of the display (default 800)")
    parser.add_argument("-dh", "--height", type=int, default=600, help="Height of the display (default 600)")
    parser.add_argument("--fps", type=int, default=60, help="Framerate (default 60)")
    parser.add_argument("--max_score", type=int, default=10, help="Max score to win (default 10)")
    args = parser.parse_args()

    # Initialize the game with parameters
    pong_game = PongGame(screen_width=args.width, screen_height=args.height, max_score=args.max_score, fps=args.fps)

    # Show instructions before the game
    pong_game.show_instructions()


if __name__ == "__main__":
    main()
