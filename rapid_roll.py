"""
========================================================
RAPID ROL
========================================================
"""

import pygame
import random

# =========================
# GAME SETTINGS
# =========================
WIDTH, HEIGHT = 400, 600
FPS = 45

COLORS = {
    "bg": (255, 255, 255),
    "player": (80, 150, 255),
    "platform": (0, 255, 100),
    "text": (0, 0, 0)
}

PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 10
PLATFORM_COUNT = 10

GRAVITY = 0.3
JUMP_STRENGTH = -10

# =========================
# PLATFORM CLASS
# =========================
class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

# =========================
# MAIN GAME CLASS
# =========================
class RapidRoll:

    def __init__(self, user_id=None, username=None, db=None):
        pygame.init()
        self.user_id = user_id
        self.username = username
        self.db = db

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rapid Roll")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 40)

        self.reset_game()

    # =========================
    # RESET GAME
    # =========================
    def reset_game(self):

        # =========================
        # PLAYER
        # =========================
        self.player = pygame.Rect(0, 0, 30, 30)
        self.velocity_y = 0
        self.score = 0

        # =========================
        # PLATFORMS
        # =========================
        self.platforms = []

        # Starting platform
        start_x = WIDTH // 2 - PLATFORM_WIDTH // 2
        start_y = HEIGHT - 100

        self.platforms.append(Platform(start_x, start_y))

        # Put player exactly on top of starting platform
        self.player.centerx = start_x + PLATFORM_WIDTH // 2
        self.player.bottom = start_y

        # Remaining random platforms
        for i in range(1, PLATFORM_COUNT):
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            y = start_y - (i * 80)

            self.platforms.append(Platform(x, y))

        # =========================
        # GAME STATE
        # =========================
        self.game_over_state = False
        self.score_saved = False

    # =========================
    # CREATE PLATFORMS
    # =========================
    def create_platforms(self):
        self.platforms = []

        # First platform directly under player
        start_x = self.player.centerx - PLATFORM_WIDTH // 2
        start_y = self.player.bottom + 20

        self.platforms.append(Platform(start_x, start_y))

        # Remaining platforms
        for i in range(1, PLATFORM_COUNT):
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            y = i * 80
            self.platforms.append(Platform(x, y))

    # =========================
    # MOVE PLATFORMS
    # =========================
    def move_platforms(self):
        for p in self.platforms:
            p.rect.y += 3

            if p.rect.top > HEIGHT:
                p.rect.x = random.randint(0, WIDTH - PLATFORM_WIDTH)
                p.rect.y = -20
                self.score += 1

    # =========================
    # COLLISION CHECK
    # =========================
    def check_collision(self):
        for p in self.platforms:
            if self.player.colliderect(p.rect) and self.velocity_y > 0:
                self.player.bottom = p.rect.top
                self.velocity_y = JUMP_STRENGTH

    # =========================
    # GAME OVER CHECK
    # =========================
    def is_game_over(self):
        return self.player.top > HEIGHT

    # =========================
    # DRAW FUNCTIONS
    # =========================
    def draw(self):
        self.screen.fill(COLORS["bg"])

        pygame.draw.ellipse(self.screen, COLORS["player"], self.player)

        for p in self.platforms:
            pygame.draw.rect(self.screen, COLORS["platform"], p.rect)

        text = self.font.render(f"Score: {self.score}", True, COLORS["text"])
        self.screen.blit(text, (10, 10))

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))
        self.screen.blit(overlay, (0, 0))

        msg1 = self.big_font.render("GAME OVER", True, (0, 0, 0))
        msg2 = self.font.render("Press R to Restart", True, (0, 0, 0))
        msg3 = self.font.render("Press Q to Quit", True, (0, 0, 0))

        self.screen.blit(msg1, (80, 220))
        self.screen.blit(msg2, (90, 300))
        self.screen.blit(msg3, (100, 340))

    # =========================
    # GAME LOOP
    # =========================
    def run(self):

        running = True

        while running:

            self.clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                # =========================
                # GAME OVER CONTROLS
                # =========================
                if self.game_over_state:
                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_r:
                            self.reset_game()

                        elif event.key == pygame.K_q:
                            pygame.quit()
                            return

                # =========================
                # NORMAL CONTROLS
                # =========================
                else:
                    pass  # movement handled below

            # =========================
            # GAME LOGIC
            # =========================
            if not self.game_over_state:

                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT]:
                    self.player.x -= 5

                if keys[pygame.K_RIGHT]:
                    self.player.x += 5

                # wrap
                if self.player.left < 0:
                    self.player.right = WIDTH

                if self.player.right > WIDTH:
                    self.player.left = 0

                # physics
                self.velocity_y += GRAVITY
                self.player.y += self.velocity_y

                # collision
                self.check_collision()

                # platforms
                self.move_platforms()

                # check game over
                if self.is_game_over():
                    self.game_over_state = True

                    if self.db and not self.score_saved:
                        self.db.save_score(self.user_id, "Rapid Roll", self.score)
                        self.score_saved = True

            # =========================
            # DRAW
            # =========================
            self.draw()

            if self.game_over_state:
                self.draw_game_over()

            pygame.display.update()

        pygame.quit()
        return


# =========================
# START GAME
# =========================
if __name__ == "__main__":
    game = RapidRoll()
    game.run()