from snake_game.game_logic import run_game_loop
from loguru import logger as log


def main():
    log.info("Starting the Snake Game")
    run_game_loop()
