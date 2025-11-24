"""
6.101 Lab:
Recipes
"""

import pickle
import sys
# import typing # optional import
# import pprint # optional import

# Increase recursion limit for deep recipe trees
sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def atomic_ingredient_costs(recipes_db):
    """
    Given a recipes database, a list containing compound and atomic food tuples,
    make and return a dictionary mapping each atomic food name to its cost.
    """
    # Filter only 'atomic' tuples and map food name to cost
    return {recipe[1]: recipe[2] for recipe in recipes_db if recipe[0] == "atomic"}


def compound_ingredient_possibilities(recipes_db):
    """
    Given a recipes database, a list containing compound and atomic food tuples,
    make and return a dictionary that maps each compound food name to a
    list of all the ingredient lists associated with that name.
    """
    result = {}
    for recipe in recipes_db:
        if recipe[0] == "compound":
            # Initialize entry if not already present
            if recipe[1] not in result:
                result[recipe[1]] = []
            # Append ingredient list to compound name
            result[recipe[1]].append(recipe[2])
    return result


def scaled_recipe(recipe_dict, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    # Multiply each ingredient quantity by scaling factor n
    return {key: value * n for key, value in recipe_dict.items()}


def add_recipes(recipe_dicts):
    """
    Given a list of recipe dictionaries that map atomic food items to quantities,
    return a new dictionary that maps each ingredient name
    to the sum of its quantities across the given recipe dictionaries.

    Example:
        add_recipes([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
        - {'milk':3, 'chocolate':1, 'sugar':1}
    """
    result = {}
    # Merge all ingredient counts across dictionaries
    for recipe_dict in recipe_dicts:
        for recipe, recipe_num in recipe_dict.items():
            # Initialize missing entries with 0
            if recipe not in result:
                result[recipe] = 0
            result[recipe] += recipe_num
    return result


def generic_cost(recipes_db, food_name, determiner, ingredients_disallowed=[]):
    """
    Core recursive helper for cost and recipe computation.
    Given a recipes database and a food name, compute either:
       The lowest cost ('cost')
    depending on the 'determiner' argument.
    """
    atomic = atomic_ingredient_costs(recipes_db)
    compound = compound_ingredient_possibilities(recipes_db)

    # Remove disallowed ingredients from both atomic and compound maps
    for ingredient in ingredients_disallowed:
        atomic.pop(ingredient, None)
        compound.pop(ingredient, None)

    # Recursive helper function
    def recur_lowest_cost(food_name):
        # Base case: atomic ingredient
        if food_name in atomic:
            return atomic[food_name], {food_name: 1}

        # Recursive case: compound ingredient
        elif food_name in compound:
            food_list = []  # track total costs
            track_recipe = []  # track corresponding recipes

            for food_recipe in compound[food_name]:
                total = -1  # sentinel for invalid combinations
                recipe_main = []

                # Loop through sub-ingredients
                for food_sub in food_recipe:
                    if (food_sub[0] not in atomic) and (food_sub[0] not in compound):
                        total = -1
                        break

                    # Recursively compute cost for sub-ingredient
                    low_cost, recipe = recur_lowest_cost(food_sub[0])
                    if low_cost is None:
                        total = -1
                        break

                    # Update total cost with quantity * sub-cost
                    total += food_sub[1] * low_cost
                    recipe_main.append(scaled_recipe(recipe, food_sub[1]))

                # If valid recipe, store its total and structure
                if total != -1:
                    track_recipe.append(add_recipes(recipe_main))
                    food_list.append(total + 1)  # +1 for base cost or overhead

            # Return cheapest valid recipe
            if food_list:
                final_cost = min(food_list)
                final_recipe = track_recipe[food_list.index(final_cost)]
                return final_cost, final_recipe
            else:
                return None, None
        else:
            return None, None

    cost, recipe = recur_lowest_cost(food_name)
    if determiner == "cost":
        return cost
    if determiner == "recipe":
        return recipe


def lowest_cost(recipes_db, food_name, ingredients_disallowed=[]):
    """
    Wrapper function returning only the lowest possible cost for a food.
    """
    return generic_cost(recipes_db, food_name, "cost", ingredients_disallowed)


def cheapest_flat_recipe(recipes_db, food_name, ingredients_disallowed=[]):
    """
    Wrapper function returning only the cheapest full recipe dictionary
    (mapping atomic items to quantities).
    """
    return generic_cost(recipes_db, food_name, "recipe", ingredients_disallowed)


def combine_recipes(nested_recipes):
    """
    Given a list of lists of recipe dictionaries, where each inner list
    represents all the recipes for a certain ingredient, compute and return a
    list of recipe dictionaries that represent all the possible combinations of
    ingredient recipes.

    Essentially computes the Cartesian product of recipe options.
    """
    result = [[]]
    for flat_recipe in nested_recipes:
        # Combine current ingredient recipes with accumulated combinations
        new_result = [
            recipe_list[:] + [recipe]
            for recipe_list in result
            for recipe in flat_recipe
        ]
        result = new_result

    # Merge all ingredient quantities for each full combination
    return [add_recipes(recipes_list) for recipes_list in result]


def all_flat_recipes(recipes_db, food_name, ingredients_disallowed=[]):
    """
    Generate a list of all possible flat recipe dictionaries for a food.
    Each dictionary maps atomic items to their total quantities.

    Returns an empty list if no recipes are possible.
    """
    atomic = atomic_ingredient_costs(recipes_db)
    compound = compound_ingredient_possibilities(recipes_db)

    # Remove disallowed ingredients
    for ingredient in ingredients_disallowed:
        atomic.pop(ingredient, None)
        compound.pop(ingredient, None)

    # Recursive helper
    def recur_flat_recipes(food_name):
        if food_name in atomic:
            return [{food_name: 1}]

        elif food_name in compound:
            result = []
            for food_recipe in compound[food_name]:
                total = 0
                recipe_nested = []

                for food_sub in food_recipe:
                    # Skip if ingredient not defined
                    if (food_sub[0] not in atomic) and (food_sub[0] not in compound):
                        total = -1
                        break
                    recipe = recur_flat_recipes(food_sub[0])
                    if not recipe:
                        total = -1
                        break

                    # Scale subrecipes by quantity
                    recipe = [scaled_recipe(item, food_sub[1]) for item in recipe]
                    recipe_nested.append(recipe)

                # Combine ingredient subrecipes
                if total != -1:
                    result.extend(combine_recipes(recipe_nested))

            if result:
                return result
            return None
        else:
            return None

    result = recur_flat_recipes(food_name)
    return [] if result is None else result


if __name__ == "__main__":
    # Load example recipe databases from pickle files
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes_db = pickle.load(f)

    with open("test_recipes/dairy_recipes.pickle", "rb") as f:
        dairy_recipes_db = pickle.load(f)

    with open("test_recipes/cookie_recipes.pickle", "rb") as f:
        cookie_recipes_db = pickle.load(f)

    # print(lowest_cost(dairy_recipes_db, 'cheese'))
    # print(cheapest_flat_recipe(example_recipes_db, 'cake'))
#    print(sum([i for i in (atomic_ingredient_costs(example_recipes_db)).values()]))
#    compound = compound_ingredient_possibilities(example_recipes_db)
#    print(len([i for i,j in compound.items() if len(j) > 1]))
#    print(lowest_cost(dairy_recipes_db, 'cheese'))
#    dairy_recipes_db2 = [
#        ('compound', 'milk', [('cow', 1), ('milking stool', 1)]),
#        ('compound', 'cheese', [('milk', 1), ('time', 1)]),
#        ('compound', 'cheese', [('cutting-edge laboratory', 11)]),
#        ('atomic', 'milking stool', 5),
#        ('atomic', 'cutting-edge laboratory', 1000),
#        ('atomic', 'time', 10000),
#    ]
#    print(lowest_cost(dairy_recipes_db2, 'cheese'))
# oup = {"carrots": 5, "celery": 3, "broth": 2, "noodles": 1, "chicken": 3, "salt": 10}
#    print(scaled_recipe(soup, 3))
#    carrot_cake = {"carrots": 5, "flour": 8,
# "sugar": 10, "oil": 5, "eggs": 4, "salt": 3}
#    bread = {"flour": 10, "sugar": 3, "oil": 3, "yeast": 15, "salt": 5}
#    recipe_dicts = [soup, carrot_cake, bread]
# print(add_recipes(recipe_dicts))
#    print(compound_ingredient_possibilities(example_recipes_db),
# atomic_ingredient_costs(example_recipes_db))
# cake_recipes = [{"cake": 1}, {"gluten free cake": 1}]
# icing_recipes = [{"vanilla icing": 1}, {"cream cheese icing": 1}]
# print(combine_recipes([cake_recipes, icing_recipes]))
# topping_recipes = [{"sprinkles": 20}]
# print(combine_recipes([cake_recipes, icing_recipes, topping_recipes]))
