import pygame
from loguru import logger as log

from lib.snake_lib import (
    GAME_HEIGHT,
    GAME_WIDTH,
    Direction,
    Food,
    MoveFailure,
    MoveResult,
    Snake,
)

GAME_FPS = 25
GAME_SCORE_BAR_HEIGHT = 30
GAME_BORDER_WIDTH = 5


_, num_errors = pygame.init()
if num_errors > 0:
    raise RuntimeError(f"Failed to initialize pygame: {num_errors} errors occurred.")

pygame.display.set_caption("Snake Game")

window = pygame.display.set_mode(
    (
        GAME_WIDTH * 10 + 2 * GAME_BORDER_WIDTH,
        GAME_HEIGHT * 10 + 2 * GAME_BORDER_WIDTH + GAME_SCORE_BAR_HEIGHT,
    )
)
fps_controller = pygame.time.Clock()


def run_game_loop() -> None:
    """
    Main game loop that runs the snake game.
    Runs iterations of the game until user closes the window.
    """
    while True:
        _run_game_iteration()

        # Display Game Over Message
        _draw_game_over(window)
        pygame.display.flip()
        pygame.time.delay(1000)
        while True:
            retry = _check_for_any_key_down()
            if retry:
                log.info("Retrying the game...")
                break


def _check_for_any_key_down() -> bool:
    """Check if any key is pressed."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            log.info("Game window closed by user.")
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            return True
    return False


def _check_for_input() -> Direction | None:
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


def _run_game_iteration() -> None:
    """Run a single iteration of the game loop."""
    log.info("Starting a new game iteration.")
    snake = Snake()
    food = Food()

    while True:
        log.debug("Running game loop iteration.")
        input: Direction | None = _check_for_input()
        if input:
            log.info(f"Input received: {input}")
            result = snake.move(input)
        else:
            result = snake.continue_moving()
        if isinstance(result, MoveFailure):
            log.info(f"GAME OVER: {result}")
            break
        elif isinstance(result, MoveResult):
            log.debug(f"Move successful: {result}")

        if snake.get_head() == food.get_position():
            log.info("Snake ate the food!")
            snake.grow()
            food = Food()

        window.fill((0, 0, 0))
        _draw_snake(snake, window)
        _draw_food(food, window)
        _draw_border(window)
        _draw_score_bar(window, snake._length)
        pygame.display.flip()
        fps_controller.tick(GAME_FPS)


def _draw_snake(snake: Snake, surface: pygame.Surface) -> None:
    """Draw the snake on the given surface."""
    x_offset = GAME_BORDER_WIDTH
    y_offset = GAME_BORDER_WIDTH
    for x, y in snake.get_positions():
        pygame.draw.rect(
            surface, "pink", (x * 10 + x_offset, y * 10 + y_offset, 10, 10)
        )


def _draw_food(food: Food, surface: pygame.Surface) -> None:
    """Draw the food on the given surface."""
    x_offset = GAME_BORDER_WIDTH
    y_offset = GAME_BORDER_WIDTH
    x, y = food.get_position()
    pygame.draw.rect(surface, "green", (x * 10 + x_offset, y * 10 + y_offset, 10, 10))


def _draw_border(surface: pygame.Surface) -> None:
    """Draw the game border."""
    pygame.draw.rect(
        surface,
        "green",
        rect=pygame.Rect(
            0,
            0,
            GAME_WIDTH * 10 + 2 * GAME_BORDER_WIDTH,
            GAME_HEIGHT * 10 + 2 * GAME_BORDER_WIDTH,
        ),
        width=GAME_BORDER_WIDTH,
    )


def _draw_score_bar(surface: pygame.Surface, score: int) -> None:
    """Draw the score at the bottom of the game window."""
    font = pygame.font.Font(None, 28)
    score_text = font.render(f"Score: {score}", True, "green")
    surface.blit(score_text, (10, GAME_HEIGHT * 10 + GAME_BORDER_WIDTH + 10))


def _draw_game_over(surface: pygame.Surface) -> None:
    font = pygame.font.Font(None, 74)
    game_over_text: pygame.Surface = font.render("GAME OVER", True, "red")
    text_rect = game_over_text.get_rect(
        center=(GAME_WIDTH * 5 + GAME_BORDER_WIDTH, GAME_HEIGHT * 5 + GAME_BORDER_WIDTH)
    )
    subtitle_font = pygame.font.Font(None, 36)
    retry_text = subtitle_font.render("Press any key to retry", True, "white")
    retry_text_rect = retry_text.get_rect(
        center=(
            GAME_WIDTH * 5 + GAME_BORDER_WIDTH,
            GAME_HEIGHT * 5 + GAME_BORDER_WIDTH + 80,
        )
    )
    window.blit(game_over_text, text_rect)
    window.blit(retry_text, retry_text_rect)
