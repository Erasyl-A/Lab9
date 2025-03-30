import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Кадров в секунду
clock = pygame.time.Clock()
FPS = 60

# Игрок
player = pygame.Rect(WIDTH // 2, HEIGHT - 60, 50, 50)
player_speed = 5

# Враг
enemy = pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50)
enemy_speed = 5

# Монеты
coins = []
coin_weights = [1, 2, 5]  # Возможные ценности монет

# Игровые переменные
score = 0
N = 10  # Количество монет до увеличения скорости врага
enemy_speed_increment = 2

# Шрифт
font = pygame.font.SysFont(None, 36)

# Основной игровой цикл
running = True
while running:
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Движение игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # Движение врага
    enemy.y += enemy_speed
    if enemy.y > HEIGHT:
        enemy.y = 0
        enemy.x = random.randint(0, WIDTH - enemy.width)

    # Генерация монет
    if random.randint(1, 30) == 1:  # Чем меньше число, тем чаще появляются
        coin = pygame.Rect(random.randint(0, WIDTH - 30), 0, 30, 30)
        weight = random.choice(coin_weights)
        coins.append((coin, weight))

    # Движение монет и сбор
    for coin, weight in coins[:]:
        coin.y += 4
        if coin.colliderect(player):
            score += weight
            coins.remove((coin, weight))
            # Увеличение скорости врага
            if score >= N:
                enemy_speed += enemy_speed_increment
                N += 10  # Следующий порог

        elif coin.y > HEIGHT:
            coins.remove((coin, weight))

    # Отрисовка
    screen.fill(WHITE)
    pygame.draw.rect(screen, (0, 0, 255), player)   # Игрок — синий
    pygame.draw.rect(screen, (255, 0, 0), enemy)    # Враг — красный

    # Отображение монет
    for coin, weight in coins:
        pygame.draw.circle(screen, (255, 215, 0), (coin.centerx, coin.centery), 15)
        weight_text = font.render(str(weight), True, BLACK)
        screen.blit(weight_text, (coin.x + 5, coin.y + 5))

    # Отображение счёта
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
