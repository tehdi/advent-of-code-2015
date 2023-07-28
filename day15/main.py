import logging
import argparse
import re
from collections import deque, defaultdict

def configure_logging(verbose, output_file):
    log_level = logging.DEBUG if verbose else logging.INFO
    if output_file is None:
        logging.basicConfig(
            format='%(message)s',
            level=log_level
        )
    else:
        logging.basicConfig(
            format='%(message)s',
            level=log_level,
            filename=output_file,
            filemode='w'
        )

stats = ['capacity', 'durability', 'flavour', 'texture', 'calories']

def parse_ingredients(data):
    ingredients = {}
    line_pattern = re.compile(r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)')
    for line in input_data:
        m = line_pattern.match(line)
        name = m.group(1)
        capacity = int(m.group(2))
        durability = int(m.group(3))
        flavour = int(m.group(4))
        texture = int(m.group(5))
        calories = int(m.group(6))
        ingredient = { 'capacity': capacity, 'durability': durability, 'flavour': flavour, 'texture': texture, 'calories': calories }
        ingredients[name] = ingredient
    return ingredients

def check_tsps(recipe):
    return recipe['tsps_used'] >= 100

def check_score(recipe, best_score, best_scoring_recipe):
    if recipe['tsps_used'] != 100: return (best_score, best_scoring_recipe)
    score = recipe['capacity'] * recipe['durability'] * recipe['flavour'] * recipe['texture']
    if score > best_score:
        logging.debug(f"new high score! {score} for {recipe}")
        return (score, recipe)
    return (best_score, best_scoring_recipe)

def wants_this_ingredient(ingredient, recipe):
    for stat in stats:
        if recipe[stat] < 1 and ingredient[stat] > 0: return True
    return False

def check_tsps_and_calories(recipe):
    return recipe['tsps_used'] >= 100 or recipe['calories'] >= 500

def check_score_and_calories(recipe, best_score, best_scoring_recipe):
    if recipe['tsps_used'] != 100 or recipe['calories'] != 500: return (best_score, best_scoring_recipe)
    score = recipe['capacity'] * recipe['durability'] * recipe['flavour'] * recipe['texture']
    if score > best_score:
        logging.debug(f"new high score! {score} for {recipe}")
        return (score, recipe)
    return (best_score, best_scoring_recipe)

def wants_these_calories(ingredient, recipe):
    needed_calories = 500 - recipe['calories']
    return ingredient['calories'] <= needed_calories

def find_best(ingredients, check_done_func, compare_best_func, wants_this_func):
    best_score = 0
    best_scoring_recipe = None
    recipe = defaultdict(int)
    recipes = deque([recipe])
    attempted_recipes = set()
    ingredient_names = tuple([name for name in ingredients])
    while len(recipes) > 0:
        recipe = recipes.pop()
        recipe_id = tuple([recipe[name] for name in ingredient_names])
        if recipe_id in attempted_recipes: continue
        attempted_recipes.add(recipe_id)

        if check_done_func(recipe):
            (best_score, best_scoring_recipe) = compare_best_func(recipe, best_score, best_scoring_recipe)
            continue

        queued_ingredients = set()
        for name,ingredient in ingredients.items():
            if wants_this_func(ingredient, recipe): queued_ingredients.add(name)
        if len(queued_ingredients) == 0: queued_ingredients.update([ingredient for ingredient in ingredients])
        for name in queued_ingredients:
            new_recipe = defaultdict(int)
            for key,value in recipe.items(): new_recipe[key] = value
            new_recipe[name] += 1
            new_recipe['tsps_used'] += 1
            for stat in stats:
                new_recipe[stat] += ingredients[name][stat]
            recipes.append(new_recipe)
    return (best_score, best_scoring_recipe)

def part_one(input_data: list[str], args) -> None:
    ingredients = parse_ingredients(input_data)
    (best_score, best_scoring_recipe) = find_best(ingredients, check_tsps, check_score, wants_this_ingredient)
    # test expected: 44 butterscotch + 56 cinnamon = score 62,842,880
        # A capacity of 44*-1 + 56*2 = 68
        # A durability of 44*-2 + 56*3 = 80
        # A flavor of 44*6 + 56*-2 = 152
        # A texture of 44*3 + 56*-1 = 76
    # actual: Part One: 62,842,880 = {'Butterscotch': 44, 'Cinnamon': 56, 'tsps_used': 100, 'capacity': 68, 'durability': 80, 'flavour': 152, 'texture': 76}
    logging.info(f"Part One: {best_score} = {best_scoring_recipe}")


# as above, but with exactly 500 calories
def part_two(input_data: list[str], args) -> None:
    ingredients = parse_ingredients(input_data)
    (best_score, best_scoring_recipe) = find_best(ingredients, check_tsps_and_calories, check_score_and_calories, wants_these_calories)
    # test expected: 40 butterscotch + 60 cinnamon = 40*8 + 60*3 = 500 calories, score = 57600000
    # actual: score 57600000 = 40 butterscotch + 60 cinnamon
    logging.info(f"Part Two: {best_score} = {best_scoring_recipe}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
