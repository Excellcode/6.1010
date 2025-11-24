# import typing  # optional import
# import pprint  # optional import
import doctest
import sys

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS


# helpers
def update_formula_main(formula, assignment_main):
    """Applies a list of variable assignments to a CNF formula.

    Args:
        formula (list): The CNF formula (a list of clauses).
        assignment_main (list): A list of (variable, value) tuples to apply.

    Returns:
        list: The simplified CNF formula after all assignments are applied.
    """
    if formula is None:
        return None
    result = formula
    # Helper to apply a list of assignments.
    for assignment in assignment_main:
        result = update_formula(result, assignment)
    return result


def update_formula(formula, assignment):
    """Applies a single assignment to a formula.

    Args:
        formula (list): A CNF formula (list of clauses).
        assignment (tuple): A single (var, value) tuple.
    """
    result = []
    var = assignment[0]
    value = assignment[1]
    for clause in formula:
        val = True
        for pair in clause:
            if var == pair[0]:
                # If assignment satisfies the clause, drop it.
                if (value == pair[1]) or ((var, value) in clause):
                    val = False
                    break

                # If assignment contradicts a literal, remove that literal.
                sub = [pair for pair in clause if pair[0] != var]

                result.append(sub)
                val = False
                break
        if val:
            # If var was not in the clause, keep it.
            result.append(clause)

    return result


# main
def satisfying_assignment(formula):
    """Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise. Does not
    mutate input formula.

    >>> satisfying_assignment([])
    {}
    >>> T, F = True, False
    >>> x = satisfying_assignment([[('a', T), ('b', F), ('c', T)]])
    >>> x.get('a', None) is T or x.get('b', None) is F or x.get('c', None) is T
    True
    >>> satisfying_assignment([[('a', T)], [('a', F)]])"""

    def helper(formula, so_far):
        if formula == []:
            return so_far
        # Base case: formula is empty, solution found.
        pair_build = [clause[0] for clause in formula if len(clause) == 1]

        if pair_build:
            # Found unit clauses, perform unit propagation.
            assigned_in_this_step = []
            for var, val in pair_build:
                if var in so_far and so_far[var] != val:
                    # Check for contradictions.
                    # Contradiction with a previous assignment
                    for mem in assigned_in_this_step:
                        so_far.pop(mem)  # Backtrack
                    return None
                if var not in so_far:
                    # Add new unit assignment.
                    so_far[var] = val
                    assigned_in_this_step.append(var)

            new_formula = update_formula_main(formula, pair_build)
            # Simplify formula with new assignments.

            if new_formula is not None and [] not in new_formula:
                if new_formula == []:
                    return so_far
                # Recurse with simplified formula.
                result = helper(new_formula, so_far)
                if result is not None:
                    return result
            for var in assigned_in_this_step:
                # If recursion failed, backtrack.
                so_far.pop(var)

            return None

        clause = formula[0]

        # No unit clauses, must branch.
        clause = formula[0]
        prev_pair = ()

        for pair in clause:
            # Try assigning each literal in the clause.
            pair_main = [pair]
            if prev_pair:
                pair_main.append(prev_pair)

            # Add ALL assumptions from pair_main to so_far
            vars_added_in_this_branch = []
            valid_branch = True
            # Check if assumptions conflict with `so_far`.
            for var, val in pair_main:
                if var in so_far and so_far[var] != val:
                    valid_branch = False  # Contradiction with existing assignment
                    break
                if var not in so_far:
                    # Add new assumption.
                    so_far[var] = val
                    vars_added_in_this_branch.append(var)

            if not valid_branch:
                for mem in vars_added_in_this_branch:
                    # If branch conflicts, backtrack and try next literal.
                    so_far.pop(mem)
                prev_pair = (pair[0], not pair[1])  # Prepare for next loop
                continue

            # Simplify formula with ALL assumptions
            new_formula = update_formula_main(formula, pair_main)

            if new_formula is None or [] in new_formula:
                # This path is a contradiction, so backtrack and continue
                for mem in vars_added_in_this_branch:
                    so_far.pop(mem)
                prev_pair = (pair[0], not pair[1])  # Prepare for next loop
                continue

            if new_formula == []:
                # If formula is empty, solution found.
                return so_far  # Success!

            result = helper(new_formula, so_far)
            if result is not None:
                return result

            for mem in vars_added_in_this_branch:
                # This branch failed, backtrack.
                so_far.pop(mem)

            # 5. Prepare for next iteration
            prev_pair = (pair[0], not pair[1])

        return None

    # All literals in clause tried and failed.

    return helper(formula, {})


def build_comb(maxim, room_cap):
    """Generates combinations recursively.

    Args:
        maxim (int): Number of items to choose from.
        room_cap (int): Number of items to choose - 1.
    """
    # We need to choose k items, where k is 1 more than the capacity

    indices = list(range(maxim))

    def find_comb_recursive(start_index, current_combination):
        # Base case: we've picked k items, yield a copy
        if len(current_combination) == room_cap + 1:
            yield tuple(current_combination)
            # Yield a found combination.
            return

        # Recursive step:
        # Iterate from the current start index to the end
        # This prevents duplicate combinations (e.g., (0, 1) and (1, 0))
        for i in range(start_index, len(indices)):
            # Choose: Add the item to our current path
            current_combination.append(indices[i])

            # Explore: Recurse, starting from the *next* index (i + 1)
            # Explore deeper.
            yield from find_comb_recursive(i + 1, current_combination)

            # Unchoose: Backtrack by removing the item
            current_combination.pop()

    # Start the generator
    return find_comb_recursive(0, [])


# Start the combination generator.


def boolify_scheduling_problem(student_preferences, room_capacities):
    """Converts scheduling problem to a Boolean formula.

    Args:
        student_preferences (dict): Map of student to preferred room set.
        room_capacities (dict): Map of room name to integer capacity.
    """
    result = []
    for student, rooms in student_preferences.items():
        main_rule = []
        for room in room_capacities:
            var = student + "_" + room
            if room in rooms:
                main_rule.append((var, True))
            else:
                # Student not in non-preferred rooms.
                result.append([(var, False)])
        result.append(main_rule)
        result.extend(
            [
                [(main_rule[i][0], False), (main_rule[j][0], False)]
                # Student in at most one room.
                for i in range(len(main_rule))
                for j in range(len(main_rule))
                if i != j
            ]
        )
    stud_names = list(student_preferences.keys())
    maxim = len(stud_names)
    result_2 = []
    # Room capacity not exceeded.
    for room, num in room_capacities.items():
        if num >= maxim:
            continue
        all_comb = build_comb(maxim, num)
        # For each combo of (cap+1) students, add clause:
        # "at least one is NOT in the room".
        for tuples in all_comb:
            result_2.append(
                [(stud_names[index] + "_" + room, False) for index in tuples]
            )

    return result_2 + result


if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
    # (This block is commented out in your original)
    print(
        update_formula(
            update_formula(
                [
                    [("a", True), ("b", True), ("c", True)],
                    [("a", False), ("f", True)],
                    [("a", False), ("f", False)],
                    # Test print 1.
                    [("d", False), ("e", True), ("a", True), ("g", True)],
                    [("h", False), ("c", True), ("a", False)],
                ],
                ("a", True),
            ),
            ("f", True),
        )
    )
    print(
        update_formula(
            [
                # Test print 2.
                [("a", True), ("b", True), ("c", True)],
                [("a", False), ("f", True)],
                [("a", False), ("f", False)],
                [("d", False), ("e", True), ("a", True), ("g", True)],
                [("h", False), ("c", True), ("a", False)],
            ],
            ("b", True),
        )
    )
    print(
        update_formula(
            update_formula(
                update_formula(
                    [
                        # Test print 3.
                        [("a", True), ("b", True), ("c", True)],
                        [("a", False), ("f", True)],
                        [("a", False), ("f", False)],
                        [("d", False), ("e", True), ("a", True), ("g", True)],
                        [("h", False), ("c", True), ("a", False)],
                    ],
                    ("b", True),
                ),
                ("a", False),
            ),
            ("d", False),
        )
    )

    cnf = [
        [("a", True), ("b", True)],
        # Test print 4 (SAT solver).
        [("a", False), ("b", False), ("c", True)],
        [("b", True), ("c", True)],
        [("b", True), ("c", False)],
    ]
    print(satisfying_assignment(cnf))
    print(
        satisfying_assignment(
            [
                # Test print 5 (SAT solver).
                [("a", False), ("b", False)],
                [("a", True), ("d", False)],
                [("a", True)],
                [("a", False), ("e", True), ("f", False), ("g", True)],
                [("b", True), ("c", True), ("f", True)],
                [("b", False), ("f", True), ("g", False)],
            ]
        )
    )

    print(
        boolify_scheduling_problem(
            {
                "Alex": {"basement", "penthouse"},
                # Main execution block.
                "Blake": {"kitchen"},
                "Chris": {"basement", "kitchen"},
                "Dana": {"kitchen", "penthouse", "basement"},
            },
            {
                "basement": 1,
                # Test print for scheduling problem.
                "kitchen": 2,
                "penthouse": 4,
            },
        )
    )
