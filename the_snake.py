from random import randint

import pygame as pg

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Константы цветов
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
DEFAULT_BODY_COLOR = (255, 255, 255)

# Скорость игры
SPEED = 20

# Начальная позиция по умолчанию
DEFAULT_POSITION = (0, 0)

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Змейка")
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, color=DEFAULT_BODY_COLOR):
        """Инициализация игрового объекта."""
        self.position = DEFAULT_POSITION
        self.body_color = color

    def draw_cell(self, position):
        """Рисуем одну клетку."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Заготовка для отрисовки игрового объекта."""
        pass


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__(SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сбрасываем змейку в начальное положение."""
        self.positions = [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        ]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.length = 1

    def draw(self):
        """Рисуем змейку."""
        for position in self.positions:
            self.draw_cell(position)

    def get_head_position(self):
        """Возвращаем координаты головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновление направления змейки."""
        self.next_direction = new_direction

    def move(self):
        """Перемещаем змейку."""
        self.direction = self.next_direction
        head_x, head_y = self.positions[0]
        new_head = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        if new_head in self.positions:
            self.reset()
            return

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        """Увеличиваем длину змейки на 1."""
        self.length += 1


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, snake_positions=None):
        """Инициализация яблока."""
        super().__init__(APPLE_COLOR)
        if snake_positions is None:
            self.snake_positions = snake_positions
        else:
            self.snake_positions = []

    def randomize_position(self, snake_positions):
        """Случайная позиция яблока."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in self.snake_positions:
                self.position = new_position
                break

    def draw(self):
        """Рисуем яблоко."""
        self.draw_cell(self.position)


def handle_keys(snake):
    """Обработка нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """Главная функция."""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
