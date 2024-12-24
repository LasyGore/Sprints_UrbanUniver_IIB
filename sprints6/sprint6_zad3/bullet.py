import pygame
from pygame.math import Vector2


class Bullet(pygame.sprite.Sprite):
    """
    Класс для представления снаряда, который будет лететь в заданном направлении.

    С каждым снарядом связаны начальная и целевая позиции, урон, а также скорость.

    Attributes:
        game (Game): Ссылка на экземпляр игры.
        image (Surface): Изображение снаряда.
        rect (Rect): Объект rectangle для управления позиционированием снаряда.
        position (Vector2): Текущая позиция снаряда.
        target (Vector2): Целевая позиция для снаряда.
        speed (float): Скорость движения снаряда.
        damage (int): Урон, который наносит снаряд.
        velocity (Vector2): Вектор скорости снаряда.
    """

    def __init__(self, start_pos, target_pos, damage, game):
        """
        Инициализация снаряда.

        Args:
            start_pos (tuple): Начальная позиция снаряда (x, y).
            target_pos (tuple): Целевая позиция, куда должен лететь снаряд (x, y).
            damage (int): Урон, который будет наносить снаряд.
            game (Game): Ссылка на экземпляр игры, к которому принадлежит снаряд.
        """
        super().__init__()
        self.game = game
        self.image = pygame.image.load('assets/bullets/basic_bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.position = Vector2(start_pos)
        self.target = Vector2(target_pos)
        self.speed = 5
        self.damage = damage
        self.velocity = self.calculate_velocity()

    def calculate_velocity(self):
        """
        Вычисление вектора скорости снаряда в направлении цели.

        Returns:
            Vector2: Вектор скорости снаряда.
        """
        direction = (self.target - self.position).normalize()
        velocity = direction * self.speed
        return velocity

    def update(self):
        """
        Обновление позиции снаряда на каждом кадре и удаление его,
        если он достиг цели или вышел за пределы экрана.
        """
        self.position += self.velocity
        self.rect.center = self.position
        if self.position.distance_to(self.target) < 10 or not self.game.is_position_inside(self.position):
            self.kill()

    def is_position_inside(self, pos):
        """
        Проверка, находится ли заданная позиция внутри границ игрового экрана.

        Args:
            pos (Vector2): Позиция, которую нужно проверить.

        Returns:
            bool: True, если позиция находится внутри границ, иначе False.
        """
        return 0 <= pos.x <= self.game.settings.screen_width and 0 <= pos.y <= self.game.settings.screen_height
