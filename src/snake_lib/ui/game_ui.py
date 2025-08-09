from typing import Final
import pygame

from snake_lib.models import Direction, Food, Snake
from loguru import logger as log

_GAME_BORDER_WIDTH: Final = 5
_GAME_SCORE_BAR_HEIGHT: Final = 30
_GAME_FPS = 25


class SnakeUI:
    """
    Represents the UI for the Snake game.
    """

    def __init__(
        self,
        width: int,
        height: int,
        border_width: int = _GAME_BORDER_WIDTH,
        score_bar_height: int = _GAME_SCORE_BAR_HEIGHT,
    ):
        self.width = width
        self.height = height
        self.border_width = border_width
        self.score_bar_height = score_bar_height
        self.surface, self.fps_controller = self._initialize_ui()

    def _initialize_ui(self) -> tuple[pygame.Surface, pygame.time.Clock]:
        """
        Initialize the game UI for the Snake game.
        This function sets up the game window and starts the main game loop.

        :return: A tuple containing the game window surface and the FPS controller.
        """
        _, num_errors = pygame.init()
        if num_errors > 0:
            raise RuntimeError(
                f"Failed to initialize pygame: {num_errors} errors occurred."
            )

        pygame.display.set_caption("Snake Game")

        window = pygame.display.set_mode(
            (
                self.width * 10 + 2 * self.border_width,
                self.height * 10 + 2 * self.border_width + self.score_bar_height,
            )
        )
        fps_controller = pygame.time.Clock()

        return window, fps_controller

    def draw_frame(self, snake: Snake, food: Food) -> None:
        """
        Draws the current frame of the game, including the snake, food, border, and score bar.

        :param snake: The Snake object representing the current state of the snake.
        :param food: The Food object representing the current position of the food.
        """
        self.surface.fill((0, 0, 0))
        self._draw_snake(snake)
        self._draw_food(food)
        self._draw_border()
        self._draw_score_bar(snake._length)
        pygame.display.flip()
        self.fps_controller.tick(_GAME_FPS)

    def _draw_snake(self, snake: Snake) -> None:
        """Draw the snake on the given surface."""
        x_offset = self.border_width
        y_offset = self.border_width
        for x, y in snake.get_positions():
            pygame.draw.rect(
                self.surface, "pink", (x * 10 + x_offset, y * 10 + y_offset, 10, 10)
            )

    def _draw_food(self, food: Food) -> None:
        """Draw the food on the given surface."""
        x_offset = self.border_width
        y_offset = self.border_width
        x, y = food.get_position()
        pygame.draw.rect(
            self.surface, "green", (x * 10 + x_offset, y * 10 + y_offset, 10, 10)
        )

    def _draw_border(self) -> None:
        """Draw the game border."""
        pygame.draw.rect(
            self.surface,
            "green",
            rect=pygame.Rect(
                0,
                0,
                self.width * 10 + 2 * self.border_width,
                self.height * 10 + 2 * self.border_width,
            ),
            width=self.border_width,
        )

    def _draw_score_bar(self, score: int) -> None:
        """Draw the score at the bottom of the game window."""
        font = pygame.font.Font(None, 28)
        score_text = font.render(f"Score: {score}", True, "green")
        self.surface.blit(score_text, (10, self.height * 10 + self.border_width + 10))

    def draw_game_over(self) -> None:
        font = pygame.font.Font(None, 74)
        game_over_text: pygame.Surface = font.render("GAME OVER", True, "red")
        text_rect = game_over_text.get_rect(
            center=(
                self.width * 5 + self.border_width,
                self.height * 5 + self.border_width,
            )
        )
        subtitle_font = pygame.font.Font(None, 36)
        retry_text = subtitle_font.render("Press any key to retry", True, "white")
        retry_text_rect = retry_text.get_rect(
            center=(
                self.width * 5 + self.border_width,
                self.height * 5 + self.border_width + 80,
            )
        )
        self.surface.blit(game_over_text, text_rect)
        self.surface.blit(retry_text, retry_text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)

    def close(self) -> None:
        """Close the game window and quit pygame."""
        pygame.quit()
        log.info("Game window closed.")


class UserInput:
    """
    Handles user input for the Snake game.
    """

    @staticmethod
    def check_for_any_key_down() -> bool:
        """Check if any key is pressed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log.info("Game window closed by user.")
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                return True
        return False

    @staticmethod
    def check_for_input() -> Direction | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log.info("Game window closed by user.")
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return Direction.UP
                elif event.key == pygame.K_DOWN:
                    return Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    return Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    return Direction.RIGHT
        return None
