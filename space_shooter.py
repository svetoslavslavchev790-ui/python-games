import pygame
import sys
import random

# --- Настройки ---
WIDTH, HEIGHT = 600, 800
FPS = 60

# Цветове
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 30, 30)
GREEN = (30, 220, 30)
BLUE = (30, 144, 255)
YELLOW = (255, 255, 0)

# Размери на кораба / враговете / куршумите
PLAYER_SIZE = (50, 40)
ENEMY_SIZE = (50, 40)
BULLET_SIZE = (5, 15)


def spawn_enemy():
    """Създава нов враг на произволна позиция."""
    x = random.randint(0, WIDTH - ENEMY_SIZE[0])
    y = -ENEMY_SIZE[1]
    speed = random.randint(3, 7)
    return pygame.Rect(x, y, ENEMY_SIZE[0], ENEMY_SIZE[1]), speed


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 28)
    big_font = pygame.font.SysFont("arial", 64)

    # Играч
    player = pygame.Rect(
        WIDTH // 2 - PLAYER_SIZE[0] // 2,
        HEIGHT - PLAYER_SIZE[1] - 20,
        PLAYER_SIZE[0],
        PLAYER_SIZE[1],
    )
    player_speed = 6

    # Куршуми
    bullets = []

    # Врагове
    enemies = []
    enemy_spawn_delay = 40
    enemy_timer = 0

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

                if game_over and event.key == pygame.K_r:
                    # рестарт
                    return main()

                if not game_over and event.key == pygame.K_SPACE:
                    # стрелба
                    bullets.append(
                        pygame.Rect(
                            player.centerx - BULLET_SIZE[0] // 2,
                            player.top - BULLET_SIZE[1],
                            BULLET_SIZE[0],
                            BULLET_SIZE[1],
                        )
                    )

        if not game_over:
            # управление на играча
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += player_speed

            # обновяване на куршумите
            for bullet in bullets[:]:
                bullet.y -= 10
                if bullet.bottom < 0:
                    bullets.remove(bullet)

            # обновяване на враговете
            enemy_timer += 1
            if enemy_timer >= enemy_spawn_delay:
                enemy_timer = 0
                enemies.append(spawn_enemy())

            for enemy, speed in enemies[:]:
                enemy.y += speed

                # враг стига до долу = GAME OVER
                if enemy.bottom >= HEIGHT:
                    game_over = True

                # проверка за удар между куршум и враг
                for bullet in bullets[:]:
                    if enemy.colliderect(bullet):
                        bullets.remove(bullet)
                        enemies.remove((enemy, speed))
                        score += 1
                        break

            # проверка за сблъсък играч-враг
            for enemy, speed in enemies:
                if enemy.colliderect(player):
                    game_over = True

        # --- Рисуване ---
        screen.fill(BLACK)

        # играч
        pygame.draw.rect(screen, BLUE, player)

        # куршуми
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

        # врагове
        for enemy, speed in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # точки
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # game over
        if game_over:
            over = big_font.render("GAME OVER", True, RED)
            info = font.render("Press R to restart", True, WHITE)
            screen.blit(
                over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 100)
            )
            screen.blit(
                info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2)
            )

        pygame.display.flip()


if __name__ == "__main__":
    main()
