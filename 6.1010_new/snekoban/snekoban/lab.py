"""
6.101 Lab:
Snekoban Game
"""

# import json # optional import for loading test_levels
# import typing # optional import
# import pprint # optional import

# NO ADDITIONAL IMPORTS!

# Mapping of directions to their row/column vector movements
DIRECTION_VECTOR = {
    "up": (-1, 0),  # move one row up
    "down": (+1, 0),  # move one row down
    "left": (0, -1),  # move one column left
    "right": (0, +1),  # move one column right
}


def make_new_game(level_description):
    """
    Create a new game state from a level description.

    Parameters
    ----------
    level_description : list[list[list[str]]]
        A 2D board where each cell contains a list of objects
        such as 'player', 'wall', 'computer', 'target'.

    Returns
    dict
        A game representation containing:
         'player': tuple(row, col)
         'wall': set of wall positions
         'computer': set of computer positions
         'target': set of target positions
        'dimension': (rows, cols)
    This function does not mutate the input level_description.
    """
    result = {
        "wall": set(),
        "target": set(),
        "computer": set(),
        "dimension": (len(level_description), len(level_description[0])),
    }
    # Iterate through the grid to populate walls, targets, computers, and player
    for row in range(len(level_description)):
        for col in range(len(level_description[row])):
            for item in level_description[row][col]:
                if item == "player":
                    result["player"] = (row, col)
                else:
                    result[item].add((row, col))

    return result


def victory_check(game):
    """
    Check if the game has been won.

    Parameters
    game : dict
        Game representation as returned by make_new_game.

    Returns
    bool
        True if all computers are on target cells, False otherwise.
    Returns False if there are no computers or targets.
    This function does not mutate the input game.
    """
    if len(game["target"]) == 0:
        return False
    return game["target"] == game["computer"]


def step_help(game, direction, para_extra):
    """
    Helper function to compute a single game step in a given direction.
    Parameters
    game : dict
        Current game state.
    direction : str
        Direction to move: 'up', 'down', 'left', 'right'.
    para_extra : str
        If 'extra', also return new_player and new_computer positions.

    Returns
    dict or tuple
        New game state (and optionally new player/computer positions)
        depending on para_extra.

    This function does not mutate the input game.
    """
    # Copy the computer positions and player position
    new_game = {"computer": set(i for i in game["computer"]), "player": game["player"]}

    # Compute new player position based on direction
    new_player = (
        game["player"][0] + DIRECTION_VECTOR[direction][0],
        game["player"][1] + DIRECTION_VECTOR[direction][1],
    )

    # Default new computer position (used if a computer is pushed)
    new_computer = (-1, -1)

    # Check if player can move to new cell (not a wall)
    if new_player not in game["wall"]:
        if new_player in game["computer"]:
            # Compute position to push the computer
            new_computer = (
                new_player[0] + DIRECTION_VECTOR[direction][0],
                new_player[1] + DIRECTION_VECTOR[direction][1],
            )
            # Check if computer can be pushed (not into wall or other computer)
            if (new_computer not in game["wall"]) and new_computer not in game[
                "computer"
            ]:
                new_game["computer"].remove(new_player)
                new_game["computer"].add(new_computer)
                new_game["player"] = new_player
        else:
            # No computer blocking, just move player
            new_game["player"] = new_player

    # Return extended info if requested
    return (new_game, new_player, new_computer) if para_extra == "extra" else new_game


def step_game(game, direction):
    """
    Perform a single step in the game in the given direction.

    Parameters
    game : dict
        Current game state.
    direction : str
        One of 'up', 'down', 'left', 'right'.

    Returns
    dict
        New game state after the move.
    Does not mutate the input game.
    """
    new_game = step_help(game, direction, 0)

    # Preserve basic elements
    new_game["wall"] = game["wall"]
    new_game["target"] = game["target"]
    new_game["dimension"] = game["dimension"]

    return new_game


def dump_game(game):
    """
    Convert a game representation back to a level description.

    Parameters
    game : dict
        Current game state.

    Returns
    list[list[list[str]]]
        Level description suitable for make_new_game.
    Useful for debugging or GUI display. Does not mutate the input game.
    """
    result = [
        [[] for col in range(game["dimension"][1])]
        for row in range(game["dimension"][0])
    ]
    for key, value in game.items():
        if key == "player":
            result[value[0]][value[1]].append(key)
        else:
            if key != "dimension":
                for tuples in value:
                    result[tuples[0]][tuples[1]].append(key)
    return result


def possible_states(game):
    """
    Generate all possible next states from the current game.

    Parameters
    game : dict
        Current game state.

    Returns
    list[tuple[str, dict]]
        List of tuples (direction, new_game) for each valid move.
    Ignores moves that push a computer into another computer.
    """
    result = []

    for dir in DIRECTION_VECTOR:
        result_dir, new_player, new_computer = step_help(game, dir, "extra")
        if new_player != game["player"]:
            if new_computer not in game["computer"]:
                result.append((dir, result_dir))
    return result


def dead_lock_states(game):
    """
    Detect deadlock situations where a computer cannot reach a target.

    Parameters
    game : dict
        Current game state.

    Returns
    bool
        True if there is a deadlock, False otherwise.
    A deadlock occurs if a computer is stuck against walls and cannot move
    to a target.
    """
    for tuples in game["computer"]:
        if tuples in game["target"]:
            return False  # Already on a target
        if tuples in game["wall"]:
            return True
        # Check corners formed by walls (classic deadlock)
        for i in (-1, 1):
            for j in (-1, 1):
                if (tuples[0] + i, tuples[1]) in game["wall"] and (
                    tuples[0],
                    tuples[1] + j,
                ) in game["wall"]:
                    return True

    return False


def solve_puzzle(game):
    """
    Solve the Snekoban puzzle using breadth-first search.

    Parameters
    game : dict
        Initial game state.

    Returns
    list[str] or None
        Shortest list of moves to reach victory, or None if unsolvable.
    Uses BFS and avoids revisiting states.
    Detects deadlock states to prune search space.
    """
    if victory_check(game):
        return []

    # Initialize BFS
    possible = possible_states(game)

    # Check if immediate victory is possible
    for tuples in possible:
        if tuples[1]["computer"] == game["target"]:
            return [tuples[0]]

    paths = [[tuples] for tuples in possible]
    visited = set()
    visited.update(
        [(tuples[1]["player"], frozenset(tuples[1]["computer"])) for tuples in possible]
    )

    # BFS loop
    while paths:
        path_track = paths.pop(0)
        path_last = tuple(i for i in path_track[-1])
        path_last[1]["target"] = game["target"]
        path_last[1]["wall"] = game["wall"]

        # Skip deadlock states
        if not dead_lock_states(path_last[1]):
            neighbours = possible_states(path_last[1])
            for neighbour in neighbours:
                state_key = (
                    neighbour[1]["player"],
                    frozenset(neighbour[1]["computer"]),
                )
                if state_key not in visited:
                    visited.add(state_key)
                    path_small = path_track + [neighbour]
                    if neighbour[1]["computer"] == game["target"]:
                        return [tuples[0] for tuples in path_small]
                    paths.append(path_small)

    return None


if __name__ == "__main__":
    pass
