from loguru import logger as log

from snake_lib.models import (
    GAME_HEIGHT,
    GAME_WIDTH,
    Direction,
    Food,
    MoveFailure,
    MoveResult,
    Snake,
)
from snake_lib.ui.game_ui import SnakeUI, UserInput


def run_game_loop() -> None:
    """
    Main game loop that runs the snake game.
    Runs iterations of the game until user closes the window.
    """
    ui_controller = SnakeUI(GAME_WIDTH, GAME_HEIGHT)
    while True:
        _run_game_iteration(ui_controller)

        # Display Game Over Message
        ui_controller.draw_game_over()
        while True:
            retry = UserInput.check_for_any_key_down()
            if retry:
                log.info("Retrying the game...")
                break


def _run_game_iteration(ui_controller: SnakeUI) -> None:
    """Run a game of Snake. Terminates when the snake collides with itself or the wall."""
    log.info("Starting a new game iteration.")
    snake = Snake()
    food = Food()

    while True:
        log.debug("Running game loop iteration.")
        input: Direction | None = UserInput.check_for_input()
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

        # TODO: move this into a game logic lib
        if snake.get_head() == food.get_position():
            log.info("Snake ate the food!")
            snake.grow()
            food = Food()

        ui_controller.draw_frame(snake, food)
