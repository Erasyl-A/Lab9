import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Размер экрана
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Шрифт
font = pygame.font.SysFont(None, 36)

# Скорость игры (чем больше, тем быстрее)
clock = pygame.time.Clock()
FPS = 10

# Направления движения
directions = {
    "UP": (0, -CELL_SIZE),
    "DOWN": (0, CELL_SIZE),
    "LEFT": (-CELL_SIZE, 0),
    "RIGHT": (CELL_SIZE, 0)
}

# Змейка
snake = [(100, 100)]
snake_dir = "RIGHT"

# Еда: (позиция, вес, время_создания)
foods = []

# Порог времени (в секундах), после которого еда исчезает
FOOD_LIFETIME = 5

# Общий счёт
score = 0

# Основной игровой цикл
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление змейкой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_dir != "DOWN":
        snake_dir = "UP"
    elif keys[pygame.K_DOWN] and snake_dir != "UP":
        snake_dir = "DOWN"
    elif keys[pygame.K_LEFT] and snake_dir != "RIGHT":
        snake_dir = "LEFT"
    elif keys[pygame.K_RIGHT] and snake_dir != "LEFT":
        snake_dir = "RIGHT"

    # Новая голова змейки
    dx, dy = directions[snake_dir]
    new_head = (snake[0][0] + dx, snake[0][1] + dy)

    # Проверка на выход за границу
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        running = False  # Конец игры при столкновении

    snake.insert(0, new_head)  # Добавляем новую голову

    # Проверка еды
    ate_food = False
    current_time = time.time()
    for food in foods[:]:
        pos, weight, spawn_time = food
        if current_time - spawn_time > FOOD_LIFETIME:
            foods.remove(food)  # Еда исчезает
        elif new_head == pos:
            score += weight
            ate_food = True
            foods.remove(food)
            break

    if not ate_food:
        snake.pop()  # Удаляем хвост, если не ели

    # Случайное появление еды
    if random.randint(1, 20) == 1:
        fx = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        fy = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        weight = random.choice([1, 3, 5])
        foods.append(((fx, fy), weight, time.time()))

    # Отрисовка еды
    for pos, weight, _ in foods:
        pygame.draw.rect(screen, RED, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        text = font.render(str(weight), True, WHITE)
        screen.blit(text, (pos[0] + 2, pos[1] + 2))

    # Отрисовка змейки
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Отображение счёта
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
