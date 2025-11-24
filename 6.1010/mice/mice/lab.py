#!/usr/bin/env python3
"""
6.101 Lab:
Mice-sleeper
"""

# import typing  # optional import
# import pprint  # optional import
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game, all_keys=False):
    """
    Prints a human-readable version of a game (provided as a dictionary)

    By default uses only "board", "dimensions", "state", "visible" keys (used
    by doctests). Setting all_keys=True shows all game keys.
    """
    if all_keys:
        keys = sorted(game)
    else:
        keys = ("board", "dimensions", "state", "visible")
        # Use only default game keys. If you modify this you will need
        # to update the docstrings in other functions!

    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(nrows, ncolumns, num_mice, num_power_cells):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
        nrows (int): Number of rows
        ncolumns (int): Number of columns
        num_mice (int): The number of mice to be added to the board

    Returns:
        A game state dictionary

    >>> dump(new_game_2d(2, 4, 3))
    board:
         [0, 0, 0, 0]
         [0, 0, 0, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
         [False, False, False, False]
         [False, False, False, False]
    """
    return new_game_nd((nrows, ncolumns), num_mice, num_power_cells)  # Delegate to N-D version


def place_mice_2d(game, num_mice, disallowed):
    """
    Add mice to the given game, subject to limitations on where they may be
    placed.  The first num_mice valid locations from an appropriate
    random_coordinates generator should be used.

    Parameters:
        game (dict): game state
        num_mice (int): the number of mice to be added
        disallowed (set): a set of (r, c) locations where mice cannot be placed

    This function works by mutating the given game, and it always returns None

    >>> g = new_game_2d(2, 2, 2)
    >>> place_mice_2d(g, 2, set())
    >>> dump(g)
    board:
         [2, 'm']
         [2, 'm']
    dimensions: (2, 2)
    state: ongoing
    visible:
         [False, False]
         [False, False]

    >>> g = new_game_2d(2, 2, 2)
    >>> place_mice_2d(g, 2, {(0, 1), (1, 0)})
    >>> dump(g)
    board:
         ['m', 2]
         [2, 'm']
    dimensions: (2, 2)
    state: ongoing
    visible:
         [False, False]
         [False, False]
    """
    return place_mice_nd(game, num_mice, disallowed)  # Delegate to N-D version


def reveal_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mice (including diagonally), then recursively reveal its eight
    neighbors.  Return an integer indicating how many new squares were revealed
    in total, including neighbors, and neighbors of neighbors, and so on.

    If this is the first reveal performed in a game, then before performing
    the reveal operation, we add the appropriate number of mice to the game
    (the number given at initialization time).  No mice should be placed in
    the location to be revealed, nor in any of its neighbors.

    The state of the game should be changed to 'lost' when at least one mouse
    is visible on the board, 'won' when all safe squares (squares that do not
    contain a mouse) and no mice are visible, and 'ongoing' otherwise.

    If the game is not ongoing, or if the given square has already been
    revealed, reveal_2d should not reveal any squares.

    Parameters:
        game (dict): Game state
        row (int): Where to start revealing cells (row)
        col (int): Where to start revealing cells (col)

    Returns:
        int: the number of new squares revealed

    >>> game = new_game_2d(2, 4, 3)
    >>> reveal_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
         [3, 'm', 2, 0]
         ['m', 'm', 2, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
         [False, False, True, True]
         [False, False, True, True]
    >>> reveal_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
         [3, 'm', 2, 0]
         ['m', 'm', 2, 0]
    dimensions: (2, 4)
    state: won
    visible:
         [True, False, True, True]
         [False, False, True, True]
    """
    return reveal_nd(game, (row, col))  # Delegate to N-D version


def render_2d(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    'm' (mice), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mice).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored and
    all cells are shown.

    Parameters:
        game (dict): Game state
        all_visible (bool): Whether to reveal all tiles or just the ones allowed
                         by game['visible']

    Returns:
        A 2D array (list of lists)


    >>> game = new_game_2d(2, 4, 3)
    >>> reveal_2d(game, 0, 0)
    4
    >>> render_2d(game, False)
    [[' ', '1', '_', '_'], [' ', '1', '_', '_']]
    >>> render_2d(game, True)
    [[' ', '1', 'm', 'm'], [' ', '1', '3', 'm']]
    >>> reveal_2d(game, 0, 3)
    1
    >>> render_2d(game, False)
    [[' ', '1', '_', 'm'], [' ', '1', '_', '_']]
    """
    return render_nd(game, all_visible)  # Delegate to N-D version


def toggle_bed_2d(game, row, col):
    """
    Toggle a bed marker at the given 2D coordinate.

    Args:
        game (dict): The game state dictionary.
        row (int): The row coordinate.
        col (int): The column coordinate.

    Returns:
        bool or None: True if a bed was placed, False if removed,
                      None if the action was invalid.
    """
    return toggle_bed_nd(game, (row, col))  # Delegate to N-D version


# N-D IMPLEMENTATION


# ------------------- Helper functions -------------------


def get_coordinates(game, coord, extra="board"):
    """
    Retrieve the value at a given N-dimensional coordinate in the game.

    Parameters:
        game (dict): The game state dictionary.
        coord (tuple): The N-dimensional coordinate to access.
        extra (str): Which field of the game to access (default 'board').

    Returns:
        The value at the specified coordinate in the chosen field.
    """

    result = game[extra]
    for index in coord:
        result = result[index]
    return result


def replace_value(game, coord, new_value, extra="board"):
    """
    Replace the value at a given N-dimensional coordinate in the game.

    Parameters:
        game (dict): The game state dictionary.
        coord (tuple): The N-dimensional coordinate to modify.
        new_value: The value to place at the specified coordinate.
        extra (str): Which field of the game to modify (default 'board').

    Returns:
        None
    """

    result = game[extra]
    for index in coord[:-1]:  # Traverse to the second-to-last list
        result = result[index]
    result[coord[-1]] = new_value  # Set the value at the final index


def new_array(dimension, value):
    """
    Create a new N-dimensional array filled with a specified value.

    Parameters:
        dimension (tuple/list): The size of each dimension.
        value: The value to fill each element with.

    Returns:
        list: An N-dimensional nested list filled with 'value'.
    """
    if len(dimension) == 0:  # Base case
        return value

    # Recursive step
    return [new_array(dimension[1:], value) for _ in range(dimension[0])]


def get_offset(game):
    """
    Calculates and caches the N-dimensional offsets for finding neighbors.

    Args:
        game (dict): The game state dictionary.

    Returns:
        list: A list of N-dimensional tuples representing relative offsets.
    """
    dimension = len(game["dimensions"])
    build_adjacent = [()]
    if "offset" in game:  # Return cached list if available
        return game["offset"]
    # Build Cartesian product of (-1, 0, 1) for all dimensions
    for _ in range(dimension):
        new_result = []
        for tuples in build_adjacent:
            new_result.extend([tuples + (num,) for num in (-1, 0, 1)])
        build_adjacent = new_result
    game["offset"] = build_adjacent  # Cache the result
    return build_adjacent


def get_neighbours(game, coordinate, offset):
    """
    Generate all valid neighboring coordinates for a given N-dimensional cell.

    Parameters:
        game (dict): The game state dictionary.
        coordinate (tuple): The N-dimensional coordinate to find neighbors for.
        offset (list): The list of relative offsets from get_offset().

    Returns:
        list of tuples: All valid neighboring coordinates including the original cell.
    """
    dimension = len(game["dimensions"])
    if offset is None:
        offset = get_offset(game)
    result = []
    for tuples in offset:
        # Compute absolute coordinates
        neighbour = tuple(
            x + y for ((index, x), y) in zip(enumerate(coordinate), tuples)
        )
        # Check if the new coordinate is within the game bounds
        if all(
            0 <= neighbour[index] < game["dimensions"][index]
            for index in range(dimension)
        ):
            result.append(neighbour)

    return result


def build_coords(game):
    """
    Build a list of all valid coordinates for the N-dimensional game board.

    Parameters:
        game (dict): The game state dictionary.

    Returns:
        list of tuples: All coordinates for the N-dimensional board.
    """
    old_result = [()]
    for index in range(len(game["dimensions"])):
        new_result = []
        for tuples in old_result:
            new_result.extend(
                [tuples + (num,) for num in range(game["dimensions"][index])]
            )
        old_result = new_result
    return old_result


def total_squares(dimensions):
    """
    Calculate the total number of cells in a grid of given dimensions.

    Args:
        dimensions (tuple): A tuple representing the size of each dimension.

    Returns:
        int: The total number of cells (product of all dimension sizes).
    """
    total = 1
    for d in dimensions:
        total *= d
    return total


# main functions
def new_game_nd(dimensions, num_mice, num_power_cells):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
        dimensions (sequence): Dimensions of the board
        num_mice (int): The number of mice to be added to the board

    Returns:
        A game state dictionary

    >>> g = new_game_nd((2, 4, 2), 3)
    >>> dump(g)
    board:
         [[0, 0], [0, 0], [0, 0], [0, 0]]
         [[0, 0], [0, 0], [0, 0], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
         [[False, False], [False, False], [False, False], [False, False]]
         [[False, False], [False, False], [False, False], [False, False]]
    """
    return {
        "board": new_array(dimensions, 0),
        "dimensions": dimensions,
        "state": "ongoing",
        "visible": new_array(dimensions, False),
        "run_check": False,  # Flag to track if mice have been placed
        "num_mice": num_mice,
        "revealed_safe": 0,  # Counter for non-mouse cells revealed
        "beds": new_array(dimensions, False),
        'num_power_cells': num_power_cells
    }


def place_mice_nd(game, num_mice, disallowed):
    """
    Add mice to the given game, subject to limitations on where they may be
    placed.  The first num_mice valid locations from an appropriate
    random_coordinates generator should be used.

    Parameters:
        game (dict): game state
        num_mice (int): the number of mice to be added
        disallowed (set): a set of tuples, each representing a location where
                          mice cannot be placed

    This function works by mutating the given game, and it always returns None

    >>> g = new_game_nd((2, 2, 2), 2)
    >>> place_mice_nd(g, 2, set())
    >>> dump(g)
    board:
         [[2, 2], [2, 2]]
         [['m', 'm'], [2, 2]]
    dimensions: (2, 2, 2)
    state: ongoing
    visible:
         [[False, False], [False, False]]
         [[False, False], [False, False]]


    >>> g = new_game_nd((2, 2, 2), 2)
    >>> place_mice_nd(g, 2, {(1, 0, 0), (0, 1, 1)})
    >>> dump(g)
    board:
         [[2, 2], [2, 2]]
         [[2, 'm'], ['m', 2]]
    dimensions: (2, 2, 2)
    state: ongoing
    visible:
         [[False, False], [False, False]]
         [[False, False], [False, False]]
    """
    game["num_mice"] = num_mice
    count = 0
    random_coords = random_coordinates(game["dimensions"])
    disallowed = set(disallowed)
    offset = get_offset(game)
    result = set()
    # Iterate through the random coordinate generator
    for random_coord in random_coords:
        if count == num_mice:  # Stop when all mice are placed
            break

        if random_coord in disallowed:
            continue
        disallowed.add(random_coord)  # Add new mouse location to disallowed set

        replace_value(game, random_coord, "m")
        result.add(random_coord)
        count += 1

        neighbours = get_neighbours(game, random_coord, offset)
        neighbours.remove(random_coord)

        # Update neighbor counts
        for neighbour in neighbours:
            get_neighbour = get_coordinates(game, neighbour)
            if get_neighbour != "m":
                replace_value(game, neighbour, get_neighbour + 1)

    game["run_check"] = True  # Mark that mice have been placed
    return result
    
def place_power_cells_nd(game, disallowed):
    """
    Places 'num_power_cells' power cells ('p') on the board.
    
    Mutates the game dictionary.
    
    Parameters:
        game (dict): The game state dictionary.
        disallowed (set): A set of N-D coordinates where power cells
                          cannot be placed (includes first-click area
                          and all mouse locations).
    """
    # Your code here
    count = 0
    num_cell = game['num_power_cells']
    for coord in random_coordinates(game['dimensions']):
        if count == num_cell:
            break
        if (coord not in disallowed) :
            replace_value(game, coord, 'p')
            count +=1            
        
        


def reveal_nd(game, coordinates, visited=None, all_coords=None, offset=None, check = True):
    """
    Recursively reveal square at coords and neighboring squares.

    Update the visible to reveal square at the given coordinates; then
    recursively reveal its neighbors, as long as coords does not contain and is
    not adjacent to a mouse.  Return a number indicating how many squares were
    revealed.  No action should be taken (and 0 should be returned) if the
    incoming state of the game is not 'ongoing', or if the given square has
    already been revealed.

    If this is the first reveal performed in a game, then before performing
    the reveal operation, we add the appropriate number of mice to the game
    (the number given at initialization time).  No mice should be placed in
    the location to be revealed, nor in any of its neighbors.


    The updated state is 'lost' when at least one mouse is visible on the
    board, 'won' when all safe squares (squares that do not contain a mouse)
    and no mice are visible, and 'ongoing' otherwise.

    Parameters:
        coordinates (tuple): Where to start revealing squares

    Returns:
        int: number of squares revealed

    >>> g = new_game_nd((2, 4, 2), 3)
    >>> reveal_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
         [['m', 3], ['m', 3], [1, 1], [0, 0]]
         [['m', 3], [3, 3], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
         [[False, False], [False, False], [True, True], [True, True]]
         [[False, False], [False, False], [True, True], [True, True]]
    >>> reveal_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
         [['m', 3], ['m', 3], [1, 1], [0, 0]]
         [['m', 3], [3, 3], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
         [[False, True], [False, False], [True, True], [True, True]]
         [[False, False], [False, False], [True, True], [True, True]]
    >>> reveal_nd(g, (0, 0, 0))
    1
    >>> dump(g)
    board:
         [['m', 3], ['m', 3], [1, 1], [0, 0]]
         [['m', 3], [3, 3], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: lost
    visible:
         [[True, True], [False, False], [True, True], [True, True]]
         [[False, False], [False, False], [True, True], [True, True]]
    """

    # Initialize helpers on the first call of a reveal chain
    if any(i is None for i in (all_coords, visited, offset)):
        all_coords = build_coords(game)
        visited = set()
        offset = get_offset(game)
    game["total_safe"] = total_squares(game["dimensions"]) - game["num_mice"]

    # Beds cannot be revealed
    if get_coordinates(game, coordinates, "beds"):
        visited.add(coordinates)
    if coordinates in visited:
        return 0
    visited.add(coordinates)
    if game["state"] != "ongoing":
        return 0

    neighbours = get_neighbours(game, coordinates, offset)
    # If this is the first reveal, place mice
    if not game["run_check"]:
        power_disallowed = place_mice_nd(game, game["num_mice"], neighbours) + set(neighbours) 
        place_power_cells_nd(game, power_disallowed)
    count = 0
    if not get_coordinates(game, coordinates, "visible"):  # If cell is not visible
        replace_value(game, coordinates, True, "visible")
        count += 1
        game["revealed_safe"] += 1

        # Check for loss
        if get_coordinates(game, coordinates) == "m":
            game["state"] = "lost"
            game["revealed_safe"] -= 1  # Correct safe count
            return count
        
                
        # Check for win
        if game["revealed_safe"] == game["total_safe"]:
            game["state"] = "won"
            return count
        if get_coordinates(game, coordinates) == 'p':
            neighbours.remove(coordinates)
            for neighbour in neighbours:
                if get_coordinates(game, neighbour) == "m":
                    continue
                reveal_nd(game, neighbour, visited, all_coords, offset, check = False)
                count +=1
        # If cell is 0, recurse on neighbors
        if get_coordinates(game, coordinates) == 0 and check:
            neighbours.remove(coordinates)
            for neighbour in neighbours:
                extra_step = reveal_nd(game, neighbour, visited, all_coords, offset)
                count += extra_step

    # Check for win condition after recursive calls
    if game["revealed_safe"] >= game["total_safe"]:
        game["state"] = "won"
    return count


def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), 'm'
    (mice), ' ' (empty squares), or '1', '2', etc. (squares neighboring mice).
    The game['visible'] array indicates which squares should be visible.  If
    all_visible is True (the default is False), the game['visible'] array is
    ignored and all cells are shown.

    Parameters:
        all_visible (bool): Whether to reveal all tiles or just the ones allowed
                             by game['visible']

    Returns:
        An n-dimensional array of strings (nested lists)

    >>> g = new_game_nd((2, 4, 2), 3)
    >>> reveal_nd(g, (0, 3, 0))
    8
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]
    >>> render_nd(g, True)
    [[['m', '3'], ['m', '3'], ['1', '1'], [' ', ' ']],
     [['m', '3'], ['3', '3'], ['1', '1'], [' ', ' ']]]
    """
    # Create a new N-D array filled with '_'
    result = {
        "board": new_array(game["dimensions"], "_"),
        "dimensions": game["dimensions"],
    }

    for coord in build_coords(game):
        # Handle bed markers first if not all_visible
        if not all_visible and get_coordinates(game, coord, "beds"):
            replace_value(result, coord, "B")
            continue

        visible = all_visible or get_coordinates(game, coord, "visible")
        value = get_coordinates(game, coord)

        if visible:
            if value == 0:
                replace_value(result, coord, " ")
            else:
                replace_value(result, coord, str(value))

    return result["board"]


def toggle_bed_nd(game, coordinates):
    """
    Toggle a bed marker at the given N-dimensional coordinate.

    Args:
        game (dict): The game state dictionary.
        coordinates (tuple): The N-dimensional coordinate.

    Returns:
        bool or None: True if a bed was placed, False if removed,
                      None if the action was invalid.
    """
    # Cannot toggle beds on visible cells or after game ends
    if get_coordinates(game, coordinates, "visible") or game["state"] != "ongoing":
        return None
    else:
        if not get_coordinates(game, coordinates, "beds"):
            replace_value(game, coordinates, True, "beds")  # Place bed
            return True
        replace_value(game, coordinates, False, "beds")  # Remove bed
        return False
    


def random_coordinates(dimensions):
    """
    Given a tuple representing the dimensions of a game board, return an
    infinite generator that yields pseudo-random coordinates within the board.
    For a given tuple of dimensions and seed, the output sequence will always
    be the same.
    """

    def prng(state):
        # see https://en.wikipedia.org/wiki/Lehmer_random_number_generator
        while True:
            yield (state := state * 48271 % 0x7FFFFFFF) / 0x7FFFFFFF

    prng_gen = prng(
        seed
        if (seed := getattr(random_coordinates, "seed", None)) is not None
        else (sum(dimensions) + 61016101)
    )
    while True:
        yield tuple(int(dim * val) for val, dim in zip(prng_gen, dimensions))


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so,
    # comment out the above line, and uncomment the below line of code.  This
    # may be useful as you write/debug individual doctests or functions.  Also,
    # the verbose flag can be set to True to see all test results, including
    # those that pass.
    #
    # doctest.run_docstring_examples(
    #     render_2d,
    #     globals(),
    #     optionflags=_doctest_flags,
    #     verbose=False
    # )
    # g = new_game_2d(2, 2, 2)
    # place_mice_2d(g, 2, {(0, 1), (1, 0)})
    # dump(g)
    # g = new_game_nd((10, 20, 3), 2)
    # print(get_neighbours(g, (5, 13, 0)))
    g = new_game_nd((4,), 1)
    reveal_nd(g, (3,))
    dump(g)
