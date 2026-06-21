"""
========================================================
TETRIS GAME
========================================================
"""

import pygame
import random

# =========================
# GAME SETTINGS
# =========================
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30

COLS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE

FPS = 10

COLORS = {
    "bg": (0, 0, 0),
    "grid": (60, 60, 60),
    "text": (255, 255, 255),
    "game_over": (255, 0, 0)
}

BLACK = (0, 0, 0)
GRAY = (60, 60, 60)

TILE_COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (160, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (0, 120, 255),
    (255, 140, 0)]

# =========================
# SHAPES (with comments)
# =========================
SHAPES = [

    # I Shape (Straight line)
    [
        [[1,1,1,1]],        # Horizontal
        [[1],[1],[1],[1]]   # Vertical
    ],

    # O Shape (Square)
    [
        [[1,1],
         [1,1]]
    ],

    # T Shape
    [
        [[0,1,0],
         [1,1,1]],

        [[1,0],
         [1,1],
         [1,0]],

        [[1,1,1],
         [0,1,0]],

        [[0,1],
         [1,1],
         [0,1]]
    ],

    # S Shape
    [
        [[0,1,1],
         [1,1,0]],

        [[1,0],
         [1,1],
         [0,1]]
    ],

    # Z Shape
    [
        [[1,1,0],
         [0,1,1]],

        [[0,1],
         [1,1],
         [1,0]]
    ],

    # L Shape
    [
        [[1,0,0],
         [1,1,1]],

        [[1,1],
         [1,0],
         [1,0]],

        [[1,1,1],
         [0,0,1]],

        [[0,1],
         [0,1],
         [1,1]]
    ],

    # J Shape (mirror of L)
    [
        [[0,0,1],
         [1,1,1]],

        [[1,0],
         [1,0],
         [1,1]],

        [[1,1,1],
         [1,0,0]],

        [[1,1],
         [0,1],
         [0,1]]
    ]
]

fall_time = 5
# =========================
# PIECE CLASS
# =========================
class Piece:
    def __init__(self):
        self.shape_set = random.choice(SHAPES)
        self.rotation = 0
        self.shape = self.shape_set[self.rotation]
        self.color = random.choice(TILE_COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape_set)
        self.shape = self.shape_set[self.rotation]

# =========================
# MAIN GAME CLASS
# =========================
class TetrisGame:

    def __init__(self, user_id=None, username=None, db=None):
        pygame.init()
        self.user_id = user_id
        self.username = username
        self.db = db

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 40)

        self.reset_game()

    def reset_game(self):
        self.grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.piece = Piece()
        self.drop_time = 0
        self.game_over_state = False
        self.score_saved = False   # ✅ prevent duplicate save

    def valid_move(self, piece, dx=0, dy=0, shape=None):
        if shape is None:
            shape = piece.shape

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = piece.x + x + dx
                    ny = piece.y + y + dy

                    if nx < 0 or nx >= COLS or ny >= ROWS:
                        return False
                    if ny >= 0 and self.grid[ny][nx] != BLACK:
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.piece.y + y][self.piece.x + x] = self.piece.color

    def clear_lines(self):
        new_grid = []
        lines = 0

        for row in self.grid:
            if BLACK in row:
                new_grid.append(row)
            else:
                lines += 1

        for _ in range(lines):
            new_grid.insert(0, [BLACK for _ in range(COLS)])

        self.grid = new_grid

        if lines == 1:
            self.score += 10
        elif lines == 2:
            self.score += 30
        elif lines == 3:
            self.score += 50
        elif lines == 4:
            self.score += 70
        elif lines >= 5:
            self.score += 100

    def is_game_over(self):
        return any(self.grid[0][x] != BLACK for x in range(COLS))

    # =========================
    # DRAW FUNCTIONS
    # =========================
    def draw_grid(self):
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.rect(
                    self.screen,
                    self.grid[y][x],
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
                pygame.draw.rect(
                    self.screen,
                    GRAY,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1
                )

    def draw_piece(self):
        for y, row in enumerate(self.piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        self.piece.color,
                        ((self.piece.x + x) * BLOCK_SIZE,
                         (self.piece.y + y) * BLOCK_SIZE,
                         BLOCK_SIZE,
                         BLOCK_SIZE)
                    )

    def draw_score(self):
        text = self.font.render(f"Score: {self.score}", True, COLORS["text"])
        self.screen.blit(text, (10, 10))

    # =========================
    # GAME OVER SCREEN
    # =========================
    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))

        self.screen.blit(overlay, (0, 0))

        msg1 = self.big_font.render("GAME OVER", True, COLORS["game_over"])
        msg2 = self.font.render("Press R to Restart", True, (0, 0, 0))
        msg3 = self.font.render("Press Q to Quit", True, (0, 0, 0))

        self.screen.blit(msg1, (40, 220))
        self.screen.blit(msg2, (50, 300))
        self.screen.blit(msg3, (70, 340))

    # =========================
    # GAME LOOP
    # =========================
    def run(self):

        running = True

        while running:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)
            self.drop_time += 1

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
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.piece, dx=-1):
                            self.piece.x -= 1

                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.piece, dx=1):
                            self.piece.x += 1

                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.piece, dy=1):
                            self.piece.y += 1

                    elif event.key == pygame.K_r:
                        # Rotate piece during gameplay
                        next_rot = (self.piece.rotation + 1) % len(self.piece.shape_set)
                        next_shape = self.piece.shape_set[next_rot]

                        if self.valid_move(self.piece, shape=next_shape):
                            self.piece.rotate()



            # =========================
            # AUTO DROP
            # =========================
            if not self.game_over_state:

                if self.drop_time > fall_time:
                    if self.valid_move(self.piece, dy=1):
                        self.piece.y += 1
                    else:
                        self.lock_piece()
                        self.clear_lines()
                        self.piece = Piece()

                        if self.is_game_over():
                            self.game_over_state = True

                            # ✅ save score ONCE
                            if self.db and not self.score_saved:
                                self.db.save_score(self.user_id, "Tetris", self.score)
                                self.score_saved = True

                    self.drop_time = 0

            # =========================
            # DRAW
            # =========================
            self.draw_grid()
            self.draw_piece()
            self.draw_score()

            if self.game_over_state:
                self.draw_game_over()

            pygame.display.update()

        pygame.quit()
        return


# =========================
# START GAME
# =========================
if __name__ == "__main__":
    game = TetrisGame()
    game.run()