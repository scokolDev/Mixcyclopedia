from pysondb import db

#initializing database for recipes, ingredients and glasses
ingredients_DB = db.getDb("data/ingredients.json")
recipe_DB = db.getDb("data/recipies.json")
glass_DB = db.getDb("data/glasses.json")

#returns all glasses from db if no name is specified
#returns glass with given name if name is specified
def get_glasses(name = None):
    if name:
        return glass_DB.getByQuery({"name":name})[0]
    return glass_DB.getAll()

#returns all ingredients from db if no type is specified
#returns only ingredients of type(liquor, other alcohol, mixer) if specified
def get_ingredients(ingredient_type = None):
    if ingredient_type:
        return ingredients_DB.getByQuery({"type":ingredient_type})
    return ingredients_DB.getAll()

#returns all recipes from db
def get_all_recipes():
    return recipe_DB.getAll()

#get all priviously selected ingredients from file
def get_last_seclected_ingredients():
    return ingredients_DB.getByQuery({"prev_selected":True})

#generator which yields each recipe that can be made with given ingredients list 
def get_possible_recipes(ingredients):
    all_recipes = get_all_recipes()
        
    for recipe in all_recipes:
        is_compatible = True
        for i in recipe["ingredients"]:
            if not i[0].lower() in ingredients:
                is_compatible = False
                break
                
        if is_compatible:
            yield recipe

#generator which yields recipes which contain at least one ingredient
#from given ingredients list
def get_idea_recipes(ingredients):
    all_recipes = get_all_recipes()
    
    for recipe in all_recipes:
        for i in recipe["ingredients"]: 
            if i[0].lower() in ingredients:
                yield recipe
                break
