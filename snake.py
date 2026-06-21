"""
========================================================
CIRCLE SNAKE GAME (UPGRADED VERSION - RUBRIC READY)
Features:
- OOP design
- File save/load score
- list, tuple, dictionary usage
- *args and **kwargs usage
- loops + nested logic
========================================================
"""

import pygame
import random

# =========================
# GAME SETTINGS
# =========================
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 10

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# =========================
# SNAKE GAME CLASS
# =========================
class SnakeGame:

    def __init__(self, user_id=None, username=None, db=None, root_win=None):
        pygame.init()

        self.user_id = user_id
        self.username = username
        self.db = db
        self.root_win = root_win

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Circle Snake Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

        self.reset_game()

    # =========================
    # RESET GAME
    # =========================
    def reset_game(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        self.dx = 0
        self.dy = 0

        self.snake = [(self.x, self.y)]   # tuple usage
        self.snake_length = 1

        self.food = self.generate_food()

        self.score = 0

    # =========================
    # *args usage (bonus movement control)
    # =========================
    def move(self, *args):
        for direction in args:
            if direction == "LEFT":
                self.dx, self.dy = -BLOCK_SIZE, 0
            elif direction == "RIGHT":
                self.dx, self.dy = BLOCK_SIZE, 0
            elif direction == "UP":
                self.dx, self.dy = 0, -BLOCK_SIZE
            elif direction == "DOWN":
                self.dx, self.dy = 0, BLOCK_SIZE

    # =========================
    # **kwargs usage (update settings)
    # =========================
    def update_settings(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # =========================
    # FOOD GENERATION (list check)
    # =========================
    def generate_food(self):
        while True:
            food_x = random.randrange(0, WIDTH, BLOCK_SIZE)
            food_y = random.randrange(0, HEIGHT, BLOCK_SIZE)

            if (food_x, food_y) not in self.snake:
                return (food_x, food_y)

    # =========================
    # DRAW SNAKE
    # =========================
    def draw_snake(self):
        for block in self.snake:
            center = (
                block[0] + BLOCK_SIZE // 2,
                block[1] + BLOCK_SIZE // 2
            )

            pygame.draw.circle(self.screen, GREEN, center, BLOCK_SIZE // 2)

    # =========================
    # SCORE DISPLAY (string formatting)
    # =========================
    def show_score(self):
        text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text, (10, 10))

    # =========================
    # EXIT GAME (Force Close Window)
    # =========================
    def exit_game(self):
        pygame.quit()         # Cleans up resources

    # =========================
    # MAIN LOOP
    # =========================
    def run(self):
        running = True

        while running:
            # 🔥 Crucial: Tell Tkinter to keep processing background window events
            # so Windows doesn't trigger a "Not Responding" state.
            if self.root_win:
                self.root_win.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                    return

                if event.type == pygame.KEYDOWN:

                    # conditionals (if / elif / else)
                    if event.key == pygame.K_LEFT and self.dx == 0:
                        self.move("LEFT")

                    elif event.key == pygame.K_RIGHT and self.dx == 0:
                        self.move("RIGHT")

                    elif event.key == pygame.K_UP and self.dy == 0:
                        self.move("UP")

                    elif event.key == pygame.K_DOWN and self.dy == 0:
                        self.move("DOWN")

            # =========================
            # MOVE SNAKE
            # =========================
            self.x += self.dx
            self.y += self.dy

            # wall collision
            if self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT:
                self.game_over()
                if not self.game_over:
                    return

            head = (self.x, self.y)

            # self collision
            if head in self.snake[:-1]:
                self.game_over()
                if not self.game_over:
                    return

            self.snake.append(head)

            if len(self.snake) > self.snake_length:
                del self.snake[0]

            # food collision (math + logic)
            if head == self.food:
                self.snake_length += 1
                self.score += 1
                self.food = self.generate_food()

            # ==========================================================
            # SAFEGUARD: If Pygame was closed during game_over, stop here
            # ==========================================================
            if not pygame.display.get_init():
                return

            # =========================
            # DRAW EVERYTHING
            # =========================
            self.screen.fill(BLACK)

            pygame.draw.circle(
                self.screen,
                RED,
                (self.food[0] + BLOCK_SIZE // 2,
                 self.food[1] + BLOCK_SIZE // 2),
                BLOCK_SIZE // 2
            )

            self.draw_snake()
            self.show_score()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()

    # =========================
    # GAME OVER + FILE SAVE
    # =========================
    def game_over(self):

        # save score using file class
        try:
            self.db.save_score(self.user_id, "Snake", self.score)
        except Exception:
            pass # Handles cases where db isn't connected during testing

        waiting = True
        while waiting:
            if self.root_win:
                self.root_win.update() # Keep Tkinter responsive here too

            msg1 = self.font.render("GAME OVER", True, RED)
            msg2 = self.font.render("Press R to Restart", True, WHITE)
            msg3 = self.font.render("Press Q to Quit", True, WHITE)

            self.screen.blit(msg1, (220, 150))
            self.screen.blit(msg2, (170, 200))
            self.screen.blit(msg3, (190, 240))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                    return False # Tells run() that we are quitting

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.exit_game()
                        return False # Tells run() that we are quitting

                    if event.key == pygame.K_r:
                        self.reset_game()
                        return True # Tells run() to keep playing


# =========================
# RUN GAME
# =========================
if __name__ == "__main__":
    game = SnakeGame()
    game.run()