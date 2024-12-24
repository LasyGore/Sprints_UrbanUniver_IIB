import pygame
import sys
from settings import Settings
from level import Level
from grid import Grid
import time


class TowerDefenseGame:
    def __init__(self):
        """
        Главный класс игры Tower Defense.
        Управляет игровым процессом, отображает уровень, обрабатывает события и управление ресурсами игрока.
        Attributes:
        settings (Settings): Настройки игры.
        screen (Surface): Экран для отрисовки.
        clock (Clock): Объект для управления частотой кадров.
        background (Surface): Фоновое изображение для игры.
        shoot_sound (Sound): Звук выстрела.
        enemy_spawn_sound (Sound): Звук спавна врага.
        level (Level): Объект уровня, содержащий врагов и башни.
        grid (Grid): Объект сетки, управляющий позициями для башен.
        font (Font): Шрифт для отображения текста на экране.
        selected_tower_type (str): Тип выбранной игроком башни.
        is_game_over (bool): Флаг, указывающий на конец игры.

        Инициализация основных компонентов игры и загрузка ресурсов.
        """
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Tower Defense Game")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load(self.settings.background_image).convert()
        self.background = pygame.transform.scale(self.background,
                                                 (self.settings.screen_width, self.settings.screen_height))

        # Загрузка звуков
        self.shoot_sound = pygame.mixer.Sound(self.settings.shoot_sound)
        self.enemy_spawn_sound = pygame.mixer.Sound(self.settings.enemy_spawn_sound)  # Звук для спавна врага

        self.level = Level(self)
        self.grid = Grid(self)

        self.font = pygame.font.SysFont("Arial", 24)

        self.selected_tower_type = 'basic'
        self.is_game_over = False

    def game_over(self):
        """
        Устанавливает флаг завершения игры.
        """
        self.is_game_over = True

    def is_position_inside(self, pos):
        """
        Проверяет, находится ли заданная позиция внутри границ игрового экрана.

        Args:
            pos (Vector2): Позиция, которую нужно проверить.

        Returns:
            bool: True, если позиция находится внутри границ, иначе False.
        """
        return 0 <= pos.x <= self.settings.screen_width and 0 <= pos.y <= self.settings.screen_height

    def _check_events(self):
        """
        Обрабатывает события, такие как нажатия клавиш и клики мыши.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selected_tower_type = 'basic'
                    print("Selected basic tower.")
                elif event.key == pygame.K_2:
                    self.selected_tower_type = 'sniper'
                    print("Selected sniper tower.")
                elif event.key == pygame.K_3:
                    self.selected_tower_type = 'money'
                    print("Selected Money tower.")
                elif event.key == pygame.K_SPACE:
                    self.grid.toggle_positions()  # Переключаем отображение позиций при нажатии пробела

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.selected_tower_type:
                    mouse_pos = pygame.mouse.get_pos()
                    self.level.attempt_place_tower(mouse_pos, self.selected_tower_type)
                else:
                    print("Не выбран тип башни!")

    def _update_game(self):
        """
        Обновляет состояние игры, включая обновление уровня и сетки.
        """
        self.level.update()
        self.grid.update()

    def _draw_win_screen(self):
        """
        Отрисовывает экран победы, когда игрок выигрывает.
        """
        win_text = "You Win!"
        win_render = self.font.render(win_text, True, (255, 215, 0))
        win_rect = win_render.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2))
        self.screen.blit(win_render, win_rect)
        pygame.display.flip()  # Обновляем экран
        time.sleep(5)
        pygame.quit()
        exit()

    def _draw_game_over_screen(self):
        """
        Отрисовывает экран окончания игры, когда игрок проигрывает.
        """
        self.screen.fill((0, 0, 0))
        game_over_text = "Game Over!"
        game_over_render = self.font.render(game_over_text, True, (255, 0, 0))
        game_over_rect = game_over_render.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height /2))
        self.screen.blit(game_over_render, game_over_rect)
        pygame.display.flip()  # Обновляем экран
        time.sleep(3)
        pygame.quit()
        exit()

    def _draw(self):
        """
        Отрисовывает все элементы игры на экране, включая уровень, сетку и текст.
        """
        if self.is_game_over:
            self._draw_game_over_screen()
            # print('И здесь не отрисовывает, странно!')
        else:
            self.screen.blit(self.background, (0, 0))
            self.level.draw(self.screen)
            self.grid.draw()

            money_text = self.font.render(f"Money: ${self.settings.starting_money}", True, (255, 255, 255))
            tower_text = self.font.render(
                f"Selected Tower: {self.selected_tower_type if self.selected_tower_type else 'None'}", True,
                (255, 255, 255))
            waves_text = self.font.render(f"Waves Left: {len(self.level.waves) - self.level.current_wave}", True,
                                          (255, 255, 255))
            enemies_text = self.font.render(f"Enemies Left: {len(self.level.enemies)}", True, (255, 255, 255))

            self.screen.blit(money_text, (10, 10))
            self.screen.blit(tower_text, (10, 40))
            self.screen.blit(waves_text, (10, 70))
            self.screen.blit(enemies_text, (10, 100))

            if self.level.all_waves_complete:
                self._draw_win_screen()

            pygame.display.flip()

    def run_game(self):
        """
        Запускает главный цикл игры, обрабатывающий события и обновляющий состояние игры.
        """
        while True:
            self._check_events()
            self._update_game()

            if len(self.level.enemies) == 0 and not self.level.all_waves_complete:
                self.level.start_next_wave()

            self._draw()
            self.clock.tick(60)


if __name__ == '__main__':
    td_game = TowerDefenseGame()
    td_game.run_game()
