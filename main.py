import pygame
import sys
import random

# --- Настройки на играта ---
WIDTH, HEIGHT = 800, 600
FPS = 60
GAME_TIME_SECONDS = 30  # колко секунди да трае играта

# Цветове (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 100)

def create_button():
    """Създава бутон на произволна позиция."""
    w, h = 120, 60
    x = random.randint(0, WIDTH - w)
    y = random.randint(0, HEIGHT - h)
    return pygame.Rect(x, y, w, h)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TapGame Desktop")
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("arial", 48)
    font_small = pygame.font.SysFont("arial", 28)

    score = 0
    time_left = GAME_TIME_SECONDS
    button_rect = create_button()
    game_over = False

    while True:
        dt = clock.tick(FPS) / 1000.0  # секунди между кадрите

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if game_over:
                    # R = restart, Q = quit
                    if event.key == pygame.K_r:
                        score = 0
                        time_left = GAME_TIME_SECONDS
                        button_rect = create_button()
                        game_over = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game_over and button_rect.collidepoint(event.pos):
                    score += 1
                    button_rect = create_button()

        # Обновяване на таймера
        if not game_over:
            time_left -= dt
            if time_left <= 0:
                time_left = 0
                game_over = True

        # --- Рендиране ---
        screen.fill(WHITE)

        # Заглавие
        title_surf = font_big.render("TapGame Desktop", True, BLACK)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 20))

        # Точки
        score_surf = font_small.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surf, (20, 80))

        # Оставащо време
        time_surf = font_small.render(f"Time: {int(time_left)} s", True, BLACK)
        screen.blit(time_surf, (20, 120))

        if not game_over:
            # Бутон TAP
            pygame.draw.rect(screen, BLUE, button_rect, border_radius=10)
            btn_text = font_small.render("TAP", True, WHITE)
            screen.blit(
                btn_text,
                (
                    button_rect.centerx - btn_text.get_width() // 2,
                    button_rect.centery - btn_text.get_height() // 2,
                ),
            )
        else:
            # GAME OVER
            over_surf = font_big.render("GAME OVER", True, RED)
            screen.blit(
                over_surf,
                (WIDTH // 2 - over_surf.get_width() // 2, HEIGHT // 2 - 80),
            )

            final_score_surf = font_small.render(
                f"Final score: {score}", True, BLACK
            )
            screen.blit(
                final_score_surf,
                (
                    WIDTH // 2 - final_score_surf.get_width() // 2,
                    HEIGHT // 2 - 20,
                ),
            )

            info_surf = font_small.render(
                "Press R to restart or Q to quit", True, GREEN
            )
            screen.blit(
                info_surf,
                (
                    WIDTH // 2 - info_surf.get_width() // 2,
                    HEIGHT // 2 + 30,
                ),
            )

        pygame.display.flip()


if __name__ == "__main__":
    main()
