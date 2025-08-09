import enum
import random
from loguru import logger as log

GAME_WIDTH = 40
GAME_HEIGHT = 40


class Direction(enum.StrEnum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class MoveFailure(enum.Enum):
    WALL_HIT = "WALL_HIT"
    SNAKE_HIT = "SNAKE_HIT"


class MoveResult:
    def __init__(self, direction: Direction, new_head: tuple[int, int]):
        self.direction = direction
        self.new_head = new_head

    def __repr__(self):
        return f"MoveResult(direction={self.direction}, new_head={self.new_head})"


class Food:
    def __init__(self):
        self._position = _get_food_position()

    def get_position(self) -> tuple[int, int]:
        return self._position


class Snake:
    def __init__(self, initial_positions: list[tuple[int, int]] | None = None):
        if initial_positions is None:
            # Avoid mutable default arguments
            initial_positions = [(1, 1), (0, 0)]
        self._length = len(initial_positions)
        self._positions = initial_positions
        self._direction = Direction.RIGHT

    def move(self, direction) -> MoveResult | MoveFailure:
        """
        Move the snake in the specified direction, if the new direction is valid, otherwise
        continue moving in the current direction.

        A direction is valid only if it is not directly opposite to the current direction.
        If the move is successful, it returns a MoveResult with the new head position.
        If the move fails due to a collision, it returns a MoveFailure.
        """
        current_x, current_y = self._positions[0]
        new_head: tuple[int, int] | None = None
        if direction == Direction.UP:
            if self._direction != Direction.DOWN:
                self._direction = Direction.UP
                new_head = (current_x, current_y - 1)
        elif direction == Direction.DOWN:
            if self._direction != Direction.UP:
                self._direction = Direction.DOWN
                new_head = (current_x, current_y + 1)
        elif direction == Direction.LEFT:
            if self._direction != Direction.RIGHT:
                self._direction = Direction.LEFT
                new_head = (current_x - 1, current_y)
        elif direction == Direction.RIGHT:
            if self._direction != Direction.LEFT:
                self._direction = Direction.RIGHT
                new_head = (current_x + 1, current_y)
        else:
            raise ValueError(f"Invalid direction: {direction}")

        if not new_head:
            # If we get here, it means the move could not be made, so
            # we continue moving in the current direction
            return self.continue_moving()

        collision = self._move_head(new_head)
        if collision:
            return collision
        log.debug(
            f"Snake head moved to {new_head} pointing direction {self._direction}"
        )
        return MoveResult(self._direction, new_head)

    def continue_moving(self) -> MoveResult | MoveFailure:
        """Continue moving in the current direction without changing it.
        Returns a MoveResult with the new head position if successful.
        If the move fails due to a collision, it returns a MoveFailure.
        """
        current_x, current_y = self._positions[0]
        if self._direction == Direction.UP:
            new_head = (current_x, current_y - 1)
        elif self._direction == Direction.DOWN:
            new_head = (current_x, current_y + 1)
        elif self._direction == Direction.LEFT:
            new_head = (current_x - 1, current_y)
        elif self._direction == Direction.RIGHT:
            new_head = (current_x + 1, current_y)
        else:
            raise ValueError(f"Invalid direction: {self._direction}")

        collision = self._move_head(new_head)
        if collision:
            return collision
        log.debug(
            f"Snake continues moving to {new_head} in direction {self._direction}"
        )

        return MoveResult(self._direction, new_head)

    def _move_head(self, new_head: tuple[int, int]) -> MoveFailure | None:
        collision: MoveFailure | None = self._check_collisions(new_head)
        if collision:
            return collision
        self._positions.insert(0, new_head)
        if len(self._positions) > self._length:
            self._positions.pop()
        return None

    def grow(self) -> None:
        self._length += 1
        log.debug(f"Snake grew to length {self._length}")

    def get_positions(self) -> list[tuple[int, int]]:
        return self._positions

    def get_head(self) -> tuple[int, int]:
        return self._positions[0]

    def _check_collisions(self, new_head: tuple[int, int]) -> MoveFailure | None:
        if _wall_collision(new_head):
            log.error("Snake hit the wall!")
            return MoveFailure.WALL_HIT
        if (
            new_head in self._positions[1:]
        ):  # Check if the new head collides with the snake's body
            log.error("Snake hit itself!")
            log.debug(
                f"New head position {new_head} collides with body {self._positions[1:]}"
            )
            return MoveFailure.SNAKE_HIT
        return None


def _wall_collision(position: tuple[int, int]) -> bool:
    x, y = position
    return x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT


def _get_food_position() -> tuple[int, int]:
    x = random.randint(0, GAME_WIDTH - 1)
    y = random.randint(0, GAME_HEIGHT - 1)
    log.debug(f"Generated food position at ({x}, {y})")
    return (x, y)
