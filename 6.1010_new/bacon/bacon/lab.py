"""
6.101 Lab:
Bacon Number
"""

#!/usr/bin/env python3

import pickle
# import typing # optional import
# import pprint # optional import

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    """
    Transform raw actor-film tuples into a bidirectional adjacency dictionary.

    Parameters:
        raw_data (list of tuples): Each tuple is (actor1_id, actor2_id, film_id)

    Returns:
        dict: Mapping from actor_id - dict of {neighbor_actor_id: film_id}
    """
    transformed = {}
    for tuples in raw_data:
        if tuples[0] not in transformed:
            transformed[tuples[0]] = {}
        transformed[tuples[0]][tuples[1]] = tuples[2]
        if tuples[1] not in transformed:
            transformed[tuples[1]] = {}
        transformed[tuples[1]][tuples[0]] = tuples[2]
    return transformed


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """Check if two actors acted together in any film.

    Parameters:
        transformed_data (dict): actor_id - dict(actor_id: film_id)
        actor_id_1 (int)
        actor_id_2 (int)

    Returns:
        bool: True if actors acted together, else False
    """
    if actor_id_1 not in transformed_data:
        return False
    if actor_id_2 in transformed_data.get(actor_id_1, {}):
        return True
    return False


def actors_with_bacon_number(transformed_data, num):
    """Find all actors at a specific Bacon number (distance from Kevin Bacon).

    Parameters:
        transformed_data (dict)
        num (int): Desired Bacon number

    Returns:
        set[int]: Actor IDs with the given Bacon number
    """
    # Initialize BFS
    old_layer = {4724}
    entried = {4724}  # entried keeps track of actor_ids we have looked up

    # Perform BFS for `num` layers
    for _ in range(1, num + 1):
        new_layer = set()
        for actor in old_layer:
            for neighbor in transformed_data.get(actor, {}):
                if neighbor not in entried:
                    new_layer.add(neighbor)
        # early exit
        if not new_layer:
            return set()
        entried.update(new_layer)
        old_layer = new_layer

    return old_layer


# helper funtions


def generic_path(transformed_data, actor_id_1, goal_test_function, key_index):
    """
    Generic BFS path-finding function.

    Parameters:
        transformed_data (dict)
        actor_id_1 (int): Start node
        goal_test_function (callable): Returns True if node satisfies goal
        key_index (int): 0 = traverse actor neighbors, 1 = traverse film neighbors

    Returns:
        list[int] or None: Shortest path satisfying goal or None if not found
    """
    if actor_id_1 not in transformed_data:
        return None
    # BFS queue: list of paths
    paths = [[actor_id_1]]
    if goal_test_function(actor_id_1):  # check start node
        return [actor_id_1]
    visited = {actor_id_1}

    while paths:
        path_track = paths.pop(0)
        path_last = path_track[-1]
        if path_last not in transformed_data:
            return None

        # Select neighbors: actors or films
        neighbors = (
            transformed_data[path_last].keys()
            if key_index == 0
            else transformed_data[path_last].values()
        )
        for actor in neighbors:
            if actor not in visited:
                visited.add(actor)
                path_small = path_track + [actor]

                if goal_test_function(actor):
                    return path_small

                paths.append(path_small)

    return None


def actors_for_film(transformed_data):
    """
    Construct a mapping from film ID to the set of actors in that film.

    Parameters:
        transformed_data (dict)

    Returns:
        dict[int, set[int]]: film_id - set of actor IDs
    """
    result = {}
    for actor, dictionary in transformed_data.items():
        for movie in dictionary.values():
            if movie not in result:
                result[movie] = set()
            result[movie].add(actor)
    return result


# main functions


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Find the shortest path connecting two actors.

    Parameters:
        transformed_data (dict)
        actor_id_1 (int)
        actor_id_2 (int)

    Returns:
        list[int] or None: Ordered list of actor IDs connecting the two actors
    """

    def func(test_actor):
        """Returns  True if test actor is actor_id_2"""
        if test_actor == actor_id_2:
            return True
        return False

    return generic_path(transformed_data, actor_id_1, func, 0)


def bacon_path(transformed_data, actor_id):
    """
    Compute the Bacon path (shortest path to Kevin Bacon, ID=4724).

    Parameters:
        transformed_data (dict)
        actor_id (int)

    Returns:
        list[int]: ordered list of actor IDs from Kevin Bacon to actor_id
    """

    def func(test_actor):
        """Returns  True if test actor is bacon"""
        return test_actor == 4724

    result = generic_path(transformed_data, actor_id, func, 0)
    if result is None:
        return result
    result.reverse()
    return result


def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    Generic BFS to find path from actor_id_1 to any actor satisfying goal_test_function.

    Parameters:
        transformed_data (dict)
        actor_id_1 (int)
        goal_test_function (callable): function(actor_id) -> bool

    Returns:
        list[int]: ordered path of actor IDs
    """
    return generic_path(transformed_data, actor_id_1, goal_test_function, 0)


def actors_connecting_films(transformed_data, film1, film2):
    """
    Find the shortest sequence of actors connecting two films.

    Returns:
        list[int]: ordered list of actor IDs
    """
    actor_films = actors_for_film(transformed_data)

    if (film2 not in actor_films) or (film1 not in actor_films):
        return None

    # special case: same film
    if film1 == film2:
        if actor_films[film1]:
            actor_list = list(actor_films[film1])
            return [actor_list[0]]
        # return any single actor from that film
        
    # BFS initialization
    paths = [[actor_id] for actor_id in actor_films[film1]]
    visited = set()
    visited.update(actor_films[film1])
    while paths:
        path_track = paths.pop(0)
        path_last = path_track[-1]

        if path_last in actor_films[film2]:
            return path_track
        # Explore neighbors
        for actor in transformed_data.get(path_last, {}):
                if actor not in visited:
                    path_small = path_track + [actor]
                    if actor in actor_films[film2]:
                        return path_small
                    paths.append(path_small)
                    visited.add(actor)

    return None


def films_connecting_actors(transformed_data, actor_id1, actor_id2):
    """
    Find the shortest sequence of films connecting two actors.

    Returns:
        list[int]: ordered list of film IDs

    """

    def func(test_movie):
        if test_movie in transformed_data[actor_id2].values():
            return True
        return False

    return generic_path(transformed_data, actor_id1, func, 1)


if __name__ == "__main__":
# with open("resources/names.pickle", "rb") as f:
# smalldb = pickle.load(f)
# print(smalldb['David Brass'])
# with open("resources/small.pickle", "rb") as f:
#    smalldb = pickle.load(f)
# print(smalldb)
# for name, id in smalldb.items():
#    if id == 35075:
#        print(name)
# additional code here will be run only when lab.py is invoked directly
# (not when imported from test.py), so this is a good place to put code
# used, for example, to generate the results for the online questions.
# with open("resources/names.pickle", "rb") as f:
#    smalldb1 = pickle.load(f)

#    with open("resources/tiny.pickle", "rb") as f:
#        smalldb2 = pickle.load(f)
#    print(transform_data(smalldb2))
# Bill, Charles = smalldb1["Bill Murray"] , smalldb1["Charles Berling"]

# Transformed = transform_data(smalldb2)
# print(acted_together(Transformed, Bill, Charles))
# toi, Denise = smalldb1["Toi Svane Stepp"],  smalldb1["Denise Richards"]
# print(acted_together(Transformed, toi, Denise))
    with open("resources/tiny.pickle", "rb") as f:
       smalldb = pickle.load(f)
# print(smalldb)
# with open("resources/large.pickle", "rb") as f:
#    largedb = pickle.load(f)
# ids = actors_with_bacon_number(transform_data(largedb), 6)


# db_small = {value: key for key, value in smalldb1.items()}
# print([db_small[id] for id in ids])

# ids = bacon_path(transform_data(largedb), smalldb1['Helen Carruthers'])
# print([db_small[id] for id in ids])
# print(actor_to_actor_path(
#   transform_data(largedb),
#   smalldb1["Kyoko Aoi"],
#   smalldb1["Kelle Kipp"]))
# ids = [228546, 10071, 69636, 26760, 2295, 75197]
# print([db_small[id] for id in ids])
# film = films_connecting_actors(transform_data(largedb),
#   smalldb1["Gerardo Davila"],
#   smalldb1["Iva Ilakovac"])
# print(film)
# with open("resources/movies.pickle", "rb") as f:
#    smalldb2 = pickle.load(f)
# db_small3 = {value: key for key, value in smalldb2.items()}
# print([db_small3[item] for item in film])
    print(actor_to_actor_path(transform_data(smalldb), 1640, 1532))