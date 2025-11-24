import time
def free_food_bonanza(board):
    """
    You belong to a student group that is investing in writing a Python program
    to plot out the shortest path through space to collect all the free food
    that is available at some moment in time.  Write a function that takes in a
    two-dimensional grid with positions of free food and a hungry student.  The
    function should return the minimum number of steps needed for the student to
    enter all of the squares with food.  The student can move up, down, left, or
    right on any given step.  If the student has no way to collect all the food,
    return None.

    The grid comes in as a nested list, where each cell holds one of:
    - 'S' for student (exactly one on the board)
    - 'F' for food (arbitrarily many on the board)
    - 'W' for wall (arbitrarily many on the board, student may not walk thru them)
    - ' ' for an empty square
    """
    def make_state_from_board(board):
        result = {'F': set(), 'W': set()}
        for row in range(len(board)):
            for col in range(len(board[0])):
                a_state = board[row][col]

                if a_state in result:
                    result[a_state].add((row, col))
                if a_state == 'S':
                    result[a_state] = (row, col)

        return result


    def neighbors(state):
        result = []
        student = state['S']
        (row, col) = student
        for i in (-1, 1):
            if ((row + i, col) not in state['W']) and :
                result.append((row + i, col))
        for j in (-1, 1):
            if (row , col + j) not in state['W']:
                result.append((row, col + j))
        return result



    def goal(state):
        if not state['F']:
            return True
        return False

    def find_path(neighbors, start, goal):
        paths = [(0, start)]
        visited = {start['S']}

        if goal(start):
            return 0
        while paths:
                path = paths.pop(0)
                neighbor_state = neighbors(path[1])
                for neighbour in neighbor_state:
                    if neighbour not in visited:
                        new_state = {'F': path[1]['W'] , 'W': path[1]['W'], 'S': neighbour}
                        if goal(new_state):
                            return path[0] + 1
                        visited.add(neighbour)
                        paths.append((path[0] + 1, new_state))

        return None

    start = make_state_from_board(board)
    path = find_path(neighbors, start, goal)
    return path





def test_small():
    ## Small boards

    board1 = [['S', ' ', ' ', ' ', 'F']]

    board2 = [['F', ' ', ' ', ' ', ' '],
              ['W', 'W', 'S', 'W', 'F'],
              [' ', ' ', ' ', 'W', ' ']]

    board3 = [['W', ' ', ' ', 'W', 'F'],
              ['W', 'W', ' ', ' ', 'F'],
              ['W', ' ', ' ', ' ', ' '],
              [' ', 'S', 'F', ' ', ' '],
              ['F', 'F', 'F', ' ', ' ']]

    expected_results = [4, 8, 10]

    for b, r in zip([board1, board2, board3], expected_results):
        print(free_food_bonanza(b))
        assert free_food_bonanza(b) == r


def test_large():
    board_sizes = [10, 20, 40, 80]
    for N in board_sizes:
        board = [[' ' for _ in range(N)] for _ in range(N)]
        board[0][0] = 'S'
        board[N-1][N-1] = 'F'
        board[N//2][N//2] = 'W'
        print(f'\nTesting Board Size: {N}')
        start = time.time()
        out = free_food_bonanza(board)
        print(f'Run Took: {time.time() - start} sec')
        assert out == 2*(N-1)
  

if __name__ == '__main__':
    test_small()
    test_large()