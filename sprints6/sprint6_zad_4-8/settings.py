import random
from level import LevelBase


class Settings:
    """
    Класс, который содержит все настройки для игры Tower Defense.

    Attributes:
        screen_width (int): Ширина игрового окна.
        screen_height (int): Высота игрового окна.
        bg_color (tuple): Цвет фона в формате RGB.
        rows (int): Количество рядов в сетке.
        cols (int): Количество колонок в сетке.
        grid_size (tuple): Размер клетки сетки.
        tower_cost (int): Стоимость установки башни.
        tower_upgrade_cost (int): Стоимость улучшения башни.
        tower_sell_percentage (float): Процент возвращаемых средств при продаже башни.
        enemy_path (list): Путь, по которому идут враги.
        tower_sprites (dict): Путь к изображениям спрайтов башен.
        enemy_sprite (str): Путь к изображению спрайта врага.
        bullet_sprite (str): Путь к изображению спрайта снаряда.
        background_image (str): Путь к изображению фона игры.
        shoot_sound (str): Путь к звуку выстрела.
        enemy_spawn_sound (str): Путь к звуку спавна врага.
        upgrade_sound (str): Путь к звуку улучшения башни.
        sell_sound (str): Путь к звуку продажи башни.
        enemy_hit_sound (str): Путь к звуку попадания по врагу.
        background_music (str): Путь к файлу фоновой музыки.
        starting_money (int): Начальная сумма денег игрока.
        lives (int): Количество жизней игрока.
        tower_positions (list): Список координат доступных для размещения башен.
    """

    def __init__(self):
        """
        Инициализация всех настроек игры Tower Defense.
        """
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.rows = 10
        self.cols = 15
        self.grid_size = (64, 64)

        self.tower_costs = {
            'basic': 100,
            'sniper': 150,
            'money': 200,
        }

        self.tower_upgrade_cost = 150
        self.tower_sell_percentage = 0.75
        self.enemy_path = [(50, 400), (300, 400), (300, 200), (600, 200), (600, 600), (900, 600), (900, 300), (1150, 300)]
        self.tower_sprites = {
            'basic': 'assets/towers/basic_tower.png',
            'sniper': 'assets/towers/sniper_tower.png',
            'money': 'assets/towers/Money_tower.png'
        }
        self.enemy_sprite = 'assets/enemies/basic_enemy.png'
        self.bullet_sprite = 'assets/bullets/basic_bullet.png'
        self.background_image = 'assets/backgrounds/game_background.png'
        #self.background_image = 'assets/backgrounds/bg.jpeg'

        self.shoot_sound = 'assets/sounds/odinochnyiy-pistoletnyiy-vyistrel.wav'
        self.enemy_spawn_sound = 'assets/sounds/okey-lets-gou-lets-go.wav'  # Звук для спавна врага
        self.upgrade_sound = 'assets/sounds/upgrade.wav'
        self.sell_sound = 'assets/sounds/sell.wav'
        self.enemy_hit_sound = 'assets/sounds/enemy_hit.wav'
        self.background_music = 'assets/sounds/background_music.mp3'

        self.starting_money = 3000
        self.lives = 20

        self.tower_positions = [
            (x * self.grid_size[0] + self.grid_size[0] // 2,
             y * self.grid_size[1] + self.grid_size[1] // 2)
            for x in range(1, self.cols) for y in range(3, self.rows)
        ]
