import pygame
import sys
import random

# --- Настройки ---
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10  # скорост на змията

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 30, 30)
GRAY = (40, 40, 40)

def random_food_position(snake):
    """Връща произволна позиция за храната, която не е върху змията."""
    while True:
        pos = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )
        if pos not in snake:
            return pos

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 24)
    big_font = pygame.font.SysFont("arial", 48)

    # Начално състояние
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)  # движение надясно
    food = random_food_position(snake)
    score = 0
    game_over = False

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if game_over:
                    if event.key == pygame.K_r:
                        # рестарт
                        snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                        direction = (1, 0)
                        food = random_food_position(snake)
                        score = 0
                        game_over = False
                    continue

                # смяна на посоката
                if event.key in (pygame.K_UP, pygame.K_w):
                    if direction != (0, 1):  # да не обърнем наобратно
                        direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if direction != (0, -1):
                        direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if direction != (1, 0):
                        direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if direction != (-1, 0):
                        direction = (1, 0)

        if not game_over:
            # местим змията
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # проверка за удар в стена
            if (
                new_head[0] < 0
                or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0
                or new_head[1] >= GRID_HEIGHT
            ):
                game_over = True
            # проверка за удар в себе си
            elif new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)  # нова глава отпред

                # проверка за храна
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                else:
                    snake.pop()  # махаме опашката, ако не е яла

        # --- Рисуване ---
        screen.fill(BLACK)

        # решетка (по желание)
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        # змия
        for i, (x, y) in enumerate(snake):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GREEN if i == 0 else (0, 150, 0)  # главата по-светла
            pygame.draw.rect(screen, color, rect)

        # храна
        fx, fy = food
        food_rect = pygame.Rect(
            fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(screen, RED, food_rect)

        # точки
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        if game_over:
            over_text = big_font.render("GAME OVER", True, RED)
            info_text = font.render("Press R to restart or ESC to quit", True, WHITE)
            screen.blit(
                over_text,
                (
                    WIDTH // 2 - over_text.get_width() // 2,
                    HEIGHT // 2 - 60,
                ),
            )
            screen.blit(
                info_text,
                (
                    WIDTH // 2 - info_text.get_width() // 2,
                    HEIGHT // 2,
                ),
            )

        pygame.display.flip()


if __name__ == "__main__":
    main()
