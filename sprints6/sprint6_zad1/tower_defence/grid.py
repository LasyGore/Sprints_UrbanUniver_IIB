import pygame


class Grid:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        #self.screen = game.screen
        self.available_spots = self.settings.tower_positions
        self.towers = []
        self.show_positions = False  # Отображение позиций башен по умолчанию выключено

    def update(self):
        pass

    def toggle_positions(self):
        self.show_positions = not self.show_positions  # Переключение состояния

    def draw(self):
        if self.show_positions:  # Проверяем, нужно ли отображать позиции
            for spot in self.available_spots:
                color = (0, 255, 0) if self.is_spot_available(spot) else (255, 0, 0)
                pygame.draw.circle(self.game.screen, color, spot, 15, 2)

    def place_tower(self, tower=None):
        # Остальной код класса не меняется...
        grid_pos = self.get_grid_position(tower.position)
        if grid_pos in self.available_spots and not any(tower.rect.collidepoint(grid_pos) for tower in self.towers):
            self.towers.append(tower)
            return True
        return False

    def remove_tower(self, tower):
        if tower in self.towers:
            self.towers.remove(tower)

    def get_grid_position(self, mouse_pos):
        """
        Получаем координаты клетки сетки по положению мыши

        Args:
            mouse_pos (tuple): координаты мыши (x, y).

        Returns:
            tuple: центр нажатой клетки сетки.
        """
        grid_x = mouse_pos[0] // 64 * 64 + 32
        grid_y = mouse_pos[1] // 64 * 64 + 32
        return grid_x, grid_y

    def is_spot_available(self, grid_pos):
        return grid_pos in self.available_spots and all(not tower.rect.collidepoint(grid_pos) for tower in self.towers)
