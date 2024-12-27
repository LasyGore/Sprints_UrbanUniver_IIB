import pygame
from pygame.math import Vector2


class Enemy(pygame.sprite.Sprite):
    """
    Класс для представления врага, который будет двигаться по заданному пути.

    С каждым врагом связаны параметры скорости, здоровья, путь движения и изображение.

    Attributes:
        image (Surface): Изображение врага.
        rect (Rect): Объект rectangle для управления позиционированием врага.
        game (Game): Ссылка на экземпляр игры.
        path (list): Список координат пути, по которому движется враг.
        path_index (int): Индекс текущей точки на пути.
        speed (float): Скорость передвижения врага.
        health (int): Общее здоровье врага.
        position (Vector2): Текущая позиция врага.
        reward: награда за уничтожение.
    """

    def __init__(self, path, speed=2, health=20, image_path=None, game=None, reward=20):
        """
        Инициализация врага.

        Args:
            path (list): Список координат, по которым будет двигаться враг.
            speed (float): Скорость передвижения врага (по умолчанию 2).
            health (int): Общее здоровье врага (по умолчанию 10).
            image_path (str): Путь к изображению врага.
            game (Game): Ссылка на экземпляр игры, к которому принадлежит враг.
        """
        super().__init__()
        self.image = pygame.Surface((30, 40))  # Это можно удалить, если изображение загружается сразу ниже
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.game = game
        self.path = path
        self.path_index = 0
        self.speed = speed
        self.health = health
        self.reward = reward
        self.position = Vector2(path[0])
        self.rect.center = self.position

    def take_damage(self, amount):
        """
        Наносит урон врагу и проверяет на смерть.

        Args:
            amount (int): Количество урона, которое будет нанесено врагу.
        """
        self.health -= amount
        if self.health <= 0:
            print('kill')
            self.on_death()  # Удаляет врага из игры

    def on_death(self):
        """
        Действия при смерти врага. Увеличивает деньги игрока и удаляет врага.
        """
        if self.game:  # Проверяем, есть ли ссылка на игру
            self.game.settings.starting_money += self.reward  # Увеличиваем деньги игрока
            print(f"Enemy killed! Player rewarded with ${self.reward}. "
                  f"Total money: ${self.game.settings.starting_money}")
        self.kill()  # Удаляем врага из игры

    def update(self):
        """
        Обновление положения врага на каждом кадре.
        Передвигает врага к следующей точке на пути и проверяет, достиг ли он конца пути.
        Если достиг, вызывается метод game_over() и враг уничтожается.
        """
        if self.path_index < len(self.path) - 1:
            start_point = Vector2(self.path[self.path_index])
            end_point = Vector2(self.path[self.path_index + 1])
            direction = (end_point - start_point).normalize()

            self.position += direction * self.speed
            self.rect.center = self.position

            if self.position.distance_to(end_point) < self.speed:
                self.path_index += 1

            if self.path_index >= len(self.path) - 1:
                self.game.game_over()  # Вызов метода game_over() из класса игры
                print('__ДОШЛИ ДО КОНЦА ПУТИ__')
                self.kill()  # Удаляет врага из игры


class FastEnemy(Enemy):
    """
    Класс для создания врагов более быстрых, чем в базовом классе, но с низким здоровьем
    """
    def __init__(self, path, game):
        super().__init__(path=path, speed=3, health=10,
                         image_path='assets/enemies/fast_enemy.png', game=game, reward=50)


class StrongEnemy(Enemy):
    """
    Класс для создания врагов более медленных, но с высоким здоровьем
    """
    def __init__(self, path, game):
        super().__init__(path=path, speed=1, health=100,
                         image_path='assets/enemies/strong_enemy.png', game=game, reward=100)


class BossEnemy(Enemy):
    """
    Класс для создания очень медленных врагов, но с очень высоким здоровьем
    """
    def __init__(self, path, game):
        super().__init__(path=path, speed=0.5, health=300,
                         image_path='assets/enemies/boss_enemy.png', game=game, reward=200)
