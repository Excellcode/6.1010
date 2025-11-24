#def bacon_path(transformed_data, actor_id):
    bacon = {}
    bacon["bacon_0"] = {4724}
    bacon["entried"] = {4724}
    bacon["bacon_1"] = set()

    if actor_id != 4724:
        for movie_actors in transformed_data.values():
            if 4724 in movie_actors:
                bacon["bacon_1"].update(movie_actors)
                bacon["entried"].update(movie_actors)

                bacon["bacon_1"].remove(4724)
    count = 1
    bool_value = True if actor_id != 4724 else False
    while bool_value:
        count += 1
        bacon["bacon_" + str(count)] = set()
        for movie_actors in transformed_data.values():
            if movie_actors.intersection(bacon["bacon_" + str(count - 1)]):
                new_actors = (
                    movie_actors - bacon["bacon_" + str(count - 1)] - bacon["entried"]
                )
                bacon["bacon_" + str(count)].update(new_actors)
                bacon["entried"].update(bacon["bacon_" + str(count)])
        if actor_id in bacon["bacon_" + str(count)]:
            bool_value = False
    track = [actor_id]
    for num in range(count - 1, 0, -1):
        for actor in bacon["bacon_" + str(num)]:
            if acted_together(transformed_data, actor, track[-1]):
                track.append(actor)
                break
    if track != [actor_id]:
        track.append(4724)
    return track[::-1]

    # def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    bacon = {}
    bacon["bacon_0"] = {actor_id_1}
    bacon["entried"] = {actor_id_1}
    bacon["bacon_1"] = set()

    if actor_id_2 != actor_id_1:
        for movie_actors in transformed_data.values():
            if actor_id_1 in movie_actors:
                bacon["bacon_1"].update(movie_actors)
                bacon["entried"].update(movie_actors)

                bacon["bacon_1"].remove(actor_id_1)
    count = 1
    bool_value = True if actor_id_2 != actor_id_1 else False
    while bool_value:
        count += 1
        bacon["bacon_" + str(count)] = set()
        for movie_actors in transformed_data.values():
            if movie_actors.intersection(bacon["bacon_" + str(count - 1)]):
                new_actors = (
                    movie_actors - bacon["bacon_" + str(count - 1)] - bacon["entried"]
                )
                bacon["bacon_" + str(count)].update(new_actors)
                bacon["entried"].update(bacon["bacon_" + str(count)])
        if actor_id_2 in bacon["bacon_" + str(count)]:
            bool_value = False
    track = [actor_id_2]
    for num in range(count - 1, 0, -1):
        print(track)
        for actor in bacon["bacon_" + str(num)]:
            if acted_together(transformed_data, actor, track[-1]):
                track.append(actor)

                break
    if track != [actor_id_2]:
        track.append(actor_id_1)
    return track[::-1]