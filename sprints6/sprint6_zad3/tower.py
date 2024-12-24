import pygame
from bullet import Bullet
import math


class Tower(pygame.sprite.Sprite):
    """
    Базовый класс для всех типов башен в игре.

    Attributes:
        position (Vector2): Позиция башни.
        game (Game): Ссылка на экземпляр игры.
        shoot_sound (Sound): Звук, воспроизводимый при выстреле.
        image (Surface): Изображение башни.
        rect (Rect): Объект прямоугольника для управления позиционированием башни.
        tower_range (int): Радиус действия башни.
        damage (int): Урон, который наносит башня.
        rate_of_fire (int): Скорострельность башни в миллисекундах.
        last_shot_time (int): Время последнего выстрела.
        level (int): Уровень башни.
        original_image (Surface): Исходное изображение башни для поворота.
    """

    def __init__(self, position, game):
        """
        Инициализация базовой башни.

        Args:
            position (tuple): Позиция башни (x, y).
            game (Game): Ссылка на экземпляр игры.
        """
        super().__init__()
        self.position = pygame.math.Vector2(position)
        self.game = game
        self.shoot_sound = self.game.shoot_sound  # Загружаем звук выстрела
        self.image = None
        self.rect = None
        self.tower_range = 0
        self.damage = 0
        self.rate_of_fire = 0
        self.last_shot_time = pygame.time.get_ticks()
        self.level = 1
        self.original_image = self.image

    def upgrade_cost(self):
        """
        Возвращает стоимость улучшения башни.

        Returns:
            int: Стоимость улучшения.
        """
        return 100 * self.level

    def draw(self, screen):
        """
        Отрисовывает башню на экране, а также текст уровня и стоимости улучшения.

        Args:
            screen (Surface): Поверхность экрана, на которую нужно отрисовать башню.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            level_text = self.game.font.render(f"Level: {self.level}", True, (255, 255, 255))
            upgrade_cost_text = self.game.font.render(f"Upgrade: ${self.upgrade_cost()}", True, (255, 255, 255))

            level_text_pos = (self.position.x, self.position.y + 20)
            upgrade_cost_pos = (self.position.x, self.position.y + 40)

            screen.blit(level_text, level_text_pos)
            screen.blit(upgrade_cost_text, upgrade_cost_pos)

    def update(self, enemies, current_time, bullets_group):
        """
        Обновляет состояние башни, проверяет возможность стрельбы и стреляет по врагу.

        Args:
            enemies (Group): Группа врагов.
            current_time (int): Текущее время в миллисекундах.
            bullets_group (Group): Группа снарядов.
        """
        if current_time - self.last_shot_time > self.rate_of_fire:
            target = self.find_target(enemies)
            if target:
                self.rotate_towards_target(target)
                self.shoot(target, bullets_group)
                self.last_shot_time = current_time

    def is_hovered(self, mouse_pos):
        """
        Проверяет, наведена ли мышь на башню.

        Args:
            mouse_pos (tuple): Позиция мыши (x, y).

        Returns:
            bool: True, если мышь наведена на башню, иначе False.
        """
        return self.rect.collidepoint(mouse_pos)

    def shoot(self, target, bullets_group):
        """
        Процесс стрельбы по врагу.

        Args:
            target (Enemy): Цель для стрельбы.
            bullets_group (Group): Группа, в которую будет добавлен новый снаряд.
        """
        self.shoot_sound.play()

    def rotate_towards_target(self, target):
        """
        Поворачивает башню в сторону цели.

        Args:
            target (Enemy): Цель, к которой башня должна повернуться.
        """
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        # Вычисляем угол в радианах
        angle_rad = math.atan2(dy, dx)
        # Преобразуем радианы в градусы
        angle_deg = math.degrees(angle_rad)
        angle_deg = -angle_deg - 90
        self.image = pygame.transform.rotate(self.original_image, angle_deg)
        self.rect = self.image.get_rect(center=self.position)

    def find_target(self, enemies):
        """
        Находит ближайшую цель для атаки.

        Args:
            enemies (Group): Группа врагов.

        Returns:
            Enemy: Найденный враг, если таковой имеется, иначе None.
        """
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = self.position.distance_to(enemy.position)
            if distance < min_distance and distance <= self.tower_range:
                nearest_enemy = enemy
                min_distance = distance
        return nearest_enemy

    def upgrade(self):
        """
        Улучшает уровень башни.
        """
        self.level += 1


class BasicTower(Tower):
    """
    Класс для базовой башни.

    Attributes:
        ... (расширенные от класса Tower)
    """

    def __init__(self, position, game):
        """
        Инициализация базовой башни.

        Args:
            position (tuple): Позиция башни (x, y).
            game (Game): Ссылка на экземпляр игры.
        """
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/basic_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 150
        self.damage = 20
        self.rate_of_fire = 1000

    def shoot(self, target, bullets_group):
        """
        Стреляет по цели, создавая новый снаряд.

        Args:
            target (Enemy): Цель для стрельбы.
            bullets_group (Group): Группа, в которую будет добавлен новый снаряд.
        """
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)
        self.shoot_sound.play()


class SniperTower(Tower):
    """
    Класс для снайперской башни.

    Attributes:
        ... (расширенные от класса Tower)
    """

    def __init__(self, position, game):
        """
        Инициализация снайперской башни.

        Args:
            position (tuple): Позиция башни (x, y).
            game (Game): Ссылка на экземпляр игры.
        """
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/sniper_tower.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 300
        self.damage = 40
        self.rate_of_fire = 2000

    def find_target(self, enemies):
        """
        Находит врага с наибольшим здоровьем в пределах радиуса атаки.

        Args:
            enemies (Group): Группа врагов.

        Returns:
            Enemy: Враг с наибольшим здоровьем, если таковой имеется, иначе None.
        """
        healthiest_enemy = None
        max_health = 0
        for enemy in enemies:
            if self.position.distance_to(enemy.position) <= self.tower_range and enemy.health > max_health:
                healthiest_enemy = enemy
                max_health = enemy.health
        return healthiest_enemy

    def shoot(self, target, bullets_group):
        """
        Стреляет по цели, создавая новый снаряд.

        Args:
            target (Enemy): Цель для стрельбы.
            bullets_group (Group): Группа, в которую будет добавлен новый снаряд.
        """
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)
        self.shoot_sound.play()


class MoneyTower(Tower):
    """
        Класс для башни, которая генерирует деньги за успешно отбитую атаку.

        Attributes:
            generated_money (int): Сумма денег, которую эта башня сгенерирует за волну.
        """

    def __init__(self, position, game):
        """
        Инициализация MoneyTower.

        Args:
            position (tuple): Позиция башни (x, y).
            game (Game): Ссылка на экземпляр игры.
        """
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/Money_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 0  # Эта башня не атакует, поэтому радиус 0
        self.damage = 0  # Урон не имеет значения для этой башни
        self.rate_of_fire = 0  # Нет задержки, это не боевой тип
        self.money_generation_rate = 5  # Сколько денег генерируется
        self.generation_interval = 500  # Интервал генерации в миллисекундах
        self.last_generation_time = pygame.time.get_ticks()

    def update(self, enemies, current_time, bullets_group):
        """
        Обновляет состояние башни, проверяя, должно ли произойти новое генерирование денег на основе текущего времени.
        Описание:
        enemies (Group): Группа врагов, с которыми взаимодействует башня.
        current_time (int): Текущее время в миллисекундах.
        bullets_group (Group): Группа пуль, выстреленных башней.
        """
        # Генерация денег с заданным интервалом
        if current_time - self.last_generation_time > self.generation_interval:
            self.generate_money()
            self.last_generation_time = current_time

    def generate_money(self):
        """
        Генерирует деньги для игрока, увеличивая его текущую сумму денег.
        """
        self.game.settings.starting_money += self.money_generation_rate
