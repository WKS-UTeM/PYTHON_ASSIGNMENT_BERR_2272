import pygame
import random

# =========================
# GAME SETTINGS
# =========================
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 4
CELL_SIZE = 100
CELL_PADDING = 10
GRID_PADDING = 10

FPS = 60

COLORS = {
    "bg": (187, 173, 160),
    "empty": (205, 193, 180),
    "text": (119, 110, 101)
}

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# =========================
# MAIN GAME CLASS
# =========================
class Game2048:

    def __init__(self, user_id=None, username=None, db=None, root_win=None):
        pygame.init()

        self.user_id = user_id
        self.username = username
        self.db = db
        self.root_win = root_win

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048 Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.score_font = pygame.font.SysFont("Arial", 25, bold=True)

        self.reset_game()

    # =========================
    # RESET GAME
    # =========================
    def reset_game(self):
        self.board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0

        self.add_new_tile()
        self.add_new_tile()

    # =========================
    # *args usage
    # =========================
    def spawn_tiles(self, *args):
        for _ in args:
            self.add_new_tile()

    # =========================
    # **kwargs usage
    # =========================
    def update_settings(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # =========================
    # ADD TILE
    # =========================
    def add_new_tile(self):
        empty = [(r, c)
                 for r in range(GRID_SIZE)
                 for c in range(GRID_SIZE)
                 if self.board[r][c] == 0]

        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = 2

    # =========================
    # SCORE DISPLAY
    # =========================
    def show_score(self):
        text = self.score_font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))

    # =========================
    # DRAW
    # =========================
    def draw(self):
        self.screen.fill(COLORS["bg"])

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):

                value = self.board[r][c]

                x = c * (CELL_SIZE + CELL_PADDING) + GRID_PADDING
                y = r * (CELL_SIZE + CELL_PADDING) + GRID_PADDING + 40

                pygame.draw.rect(
                    self.screen,
                    TILE_COLORS.get(value, (60, 58, 50)),
                    (x, y, CELL_SIZE, CELL_SIZE),
                    border_radius=8
                )

                if value != 0:
                    text = self.font.render(str(value), True, COLORS["text"])
                    rect = text.get_rect(center=(x + CELL_SIZE // 2,
                                                 y + CELL_SIZE // 2))
                    self.screen.blit(text, rect)

        self.show_score()

    # =========================
    # LOGIC
    # =========================
    def compress(self, row):
        new_row = [x for x in row if x != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    # =========================
    # MOVEMENTS
    # =========================
    def move_left(self):
        changed = False

        for i in range(GRID_SIZE):
            original = self.board[i][:]

            row = self.compress(self.board[i])
            row = self.merge(row)
            row = self.compress(row)

            self.board[i] = row

            if original != row:
                changed = True

        return changed

    def reverse(self):
        for row in self.board:
            row.reverse()

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_right(self):
        self.reverse()
        changed = self.move_left()
        self.reverse()
        return changed

    def move_up(self):
        self.transpose()
        changed = self.move_left()
        self.transpose()
        return changed

    def move_down(self):
        self.transpose()
        changed = self.move_right()
        self.transpose()
        return changed

    # =========================
    # GAME OVER CHECK
    # =========================
    def is_game_over(self):
        for row in self.board:
            if 0 in row:
                return False

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 1):
                if self.board[r][c] == self.board[r][c + 1]:
                    return False

        for r in range(GRID_SIZE - 1):
            for c in range(GRID_SIZE):
                if self.board[r][c] == self.board[r + 1][c]:
                    return False

        return True

    # =========================
    # GAME OVER SCREEN
    # =========================
    def game_over_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))

        self.screen.blit(overlay, (0, 0))

        msg1 = self.font.render("GAME OVER", True, (0, 0, 0))
        msg2 = self.score_font.render("Press R to Restart", True, (0, 0, 0))
        msg3 = self.score_font.render("Press Q to Quit", True, (0, 0, 0))

        self.screen.blit(msg1, (150, 180))
        self.screen.blit(msg2, (140, 240))
        self.screen.blit(msg3, (160, 280))

    # =========================
    # RUN LOOP
    # =========================
    def run(self):
        running = True
        game_over = False

        while running:

            if self.root_win:
                self.root_win.update()

            self.clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN and not game_over:

                    moved = False

                    if event.key == pygame.K_LEFT:
                        moved = self.move_left()

                    elif event.key == pygame.K_RIGHT:
                        moved = self.move_right()

                    elif event.key == pygame.K_UP:
                        moved = self.move_up()

                    elif event.key == pygame.K_DOWN:
                        moved = self.move_down()

                    if moved:
                        self.add_new_tile()

                    if self.is_game_over():
                        game_over = True
                        self.db.save_score(self.user_id, "2048", self.score)

                elif event.type == pygame.KEYDOWN and game_over:

                    if event.key == pygame.K_r:
                        self.reset_game()
                        game_over = False

                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return

            self.draw()

            if game_over:
                self.game_over_screen()

            pygame.display.update()

        pygame.quit()
        return


# =========================
# START GAME
# =========================
if __name__ == "__main__":
    game = Game2048()
    game.run()