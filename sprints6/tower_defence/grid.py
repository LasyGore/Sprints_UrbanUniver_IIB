import pygame


class Grid:
    """
    Класс, представляющий игровую сетку, на которой могут быть размещены башни.

    Attributes:
        game (Game): Ссылка на экземпляр игры.
        settings (Settings): Ссылков на настройки игры.
        available_spots (list): Список доступных позиций для размещения башен.
        towers (list): Список установленных башен.
        show_positions (bool): Флаг, определяющий необходимость отображения доступных позиций для башен.
    """

    def __init__(self, game):
        """
        Инициализация сетки.

        Args:
            game (Game): Ссылка на экземпляр игры.
        """
        self.game = game
        self.settings = game.settings
        self.available_spots = self.settings.tower_positions
        self.towers = []
        self.show_positions = False  # Отображение позиций башен по умолчанию выключено

    def update(self):
        """
        Обновление состояния сетки. Может использоваться для логики на каждом кадре.
        """
        pass

    def toggle_positions(self):
        """
        Переключение состояния отображения доступных позиций для башен.
        """
        self.show_positions = not self.show_positions

    def draw(self):
        """
        Отображение доступных позиций для установки башен на экране.

        Если show_positions установлено в True, то на экране будут нарисованы
        круги в доступных позициях, которые будут зелеными, если они доступны,
        и красными, если заняты другими башнями.
        """
        if self.show_positions:  # Проверяем, нужно ли отображать позиции
            for spot in self.available_spots:
                color = (0, 255, 0) if self.is_spot_available(spot) else (255, 0, 0)
                pygame.draw.circle(self.game.screen, color, spot, 15, 2)

    def place_tower(self, tower=None):
        """
        Размещение башни на сетке.

        Args:
            tower (Tower): Объект башни, которую нужно разместить.

        Returns:
            bool: True, если башня успешно размещена; иначе False.
        """
        grid_pos = self.get_grid_position(tower.position)
        if grid_pos in self.available_spots and not any(tower.rect.collidepoint(grid_pos) for tower in self.towers):
            self.towers.append(tower)
            return True
        return False

    def remove_tower(self, tower):
        """
        Удаление башни из сетки.

        Args:
            tower (Tower): Башня, которую нужно удалить.
        """
        if tower in self.towers:
            self.towers.remove(tower)

    def get_grid_position(self, mouse_pos):
        """
        Получаем координаты клетки сетки по положению мыши.

        Args:
            mouse_pos (tuple): координаты мыши (x, y).

        Returns:
            tuple: центр нажатой клетки сетки.
        """
        grid_x = mouse_pos[0] // 64 * 64 + 32
        grid_y = mouse_pos[1] // 64 * 64 + 32
        return grid_x, grid_y

    def is_spot_available(self, grid_pos):
        """
        Проверка доступности заданной позиции для размещения башни.

        Args:
            grid_pos (tuple): Координаты позиции (x, y) для проверки.

        Returns:
            bool: True, если позиция доступна для размещения башни; иначе False.
        """
        return grid_pos in self.available_spots and all(not tower.rect.collidepoint(grid_pos) for tower in self.towers)
