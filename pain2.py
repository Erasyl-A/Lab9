import pygame
import math

# Инициализация Pygame
pygame.init()

# Создание экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Начальные значения
drawing = False
start_pos = None
current_shape = "square"  # по умолчанию
shapes = []  # список всех нарисованных фигур: (shape, start, end)

# Шрифт
font = pygame.font.SysFont(None, 24)

# Основной цикл
running = True
while running:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Выбор фигуры клавишами 1-4
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_shape = "square"
            elif event.key == pygame.K_2:
                current_shape = "right_triangle"
            elif event.key == pygame.K_3:
                current_shape = "equilateral_triangle"
            elif event.key == pygame.K_4:
                current_shape = "rhombus"

        # Начало рисования
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = pygame.mouse.get_pos()

        # Завершение рисования
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = pygame.mouse.get_pos()
            shapes.append((current_shape, start_pos, end_pos))

    # Отрисовка всех сохранённых фигур
    for shape, start, end in shapes:
        x1, y1 = start
        x2, y2 = end

        if shape == "square":
            side = min(abs(x2 - x1), abs(y2 - y1))
            rect = pygame.Rect(x1, y1, side, side)
            pygame.draw.rect(screen, BLACK, rect, 2)

        elif shape == "right_triangle":
            points = [start, (x1, y2), (x2, y2)]
            pygame.draw.polygon(screen, RED, points, 2)

        elif shape == "equilateral_triangle":
            # Центр и сторона
            side = abs(x2 - x1)
            height = side * math.sqrt(3) / 2
            points = [
                (x1, y2),
                (x1 + side, y2),
                (x1 + side / 2, y2 - height)
            ]
            pygame.draw.polygon(screen, (0, 0, 255), points, 2)

        elif shape == "rhombus":
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            dx = abs(x2 - x1) // 2
            dy = abs(y2 - y1) // 2
            points = [
                (center_x, y1),
                (x2, center_y),
                (center_x, y2),
                (x1, center_y)
            ]
            pygame.draw.polygon(screen, (0, 150, 0), points, 2)

    # Подсказка текущей фигуры
    text = font.render(f"Current shape: {current_shape}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
