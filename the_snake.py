from random import choice, randint

import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20
# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """#Класс объекта игрового поля:"""

    def __init__(self) -> None:
        """Начальная позиция."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

        self.body_color = None
    """Рисуем объект"""

    def draw(self):
        """Метод отображения объекта."""
        pass


class Apple(GameObject):
    """Класс яблока:"""

    def __init__(self, snake_positions=[], body_color=None):
        """Инициализация яблока."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(snake_positions)

    """Новая позиция яблока."""

    def randomize_position(self, snake_positions):
        """Обновляем позицию яблока."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self):
        """Рисуем яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


"""Класс змейки."""


class Snake(GameObject):
    """Инициализация змейки."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        # Случайное направление(изначально).
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = RIGHT
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.last = None

    def get_head_position(self):
        """Возвращаем координаты головы змейки."""
        return self.positions[0]
    """Обновление направления змейки."""

    def update_direction(self, new_direction):
        """Обновление направления змейки."""
        opposite = {
            UP: DOWN,
            DOWN: UP,
            LEFT: RIGHT,
            RIGHT: LEFT
        }
        if new_direction != opposite.get(self.direction):
            self.next_direction = new_direction

    def reset(self):
        """Сбрасываем змейку в начальное положение"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction

    def move(self):
        """Перемещаем змейку и проверяем столкновение"""
        self.direction = self.next_direction
        head_x, head_y = self.positions[0]

        new_head = (
            head_x + self.direction[0] * GRID_SIZE,
            head_y + self.direction[1] * GRID_SIZE,
        )

        if head_x < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, head_y)
        elif head_x >= SCREEN_WIDTH:
            new_head = (0, head_y)

        if head_y < 0:
            new_head = (head_x, SCREEN_HEIGHT - GRID_SIZE)
        elif head_y >= SCREEN_HEIGHT:
            new_head = (head_x, 0)

        if new_head in self.positions:
            self.reset()
            return

        """Добавляем новую голову в начало списка."""
        self.positions.insert(0, new_head)

        """Удаляем хвост змейки."""
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def grow(self):
        """Увеличиваем длину змейки на 1."""
        self.length += 1


def handle_keys(game_object):
    """обработка нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция."""
    # Инициализация PyGame:
    pygame.init()

    """Создаем змейку и яблоко:"""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.move()

        """Проверка на столкновение змейки с яблоком."""
        if snake.positions[0] == apple.position:
            snake.grow()  # Увеличиваем длину змейки на 1.
            apple = Apple(snake.positions)  # Создаем новое яблоко.

        """Отображение игрового поля."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()

        for pos in snake.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, snake.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        pygame.display.update()


if __name__ == "__main__":
    main()
