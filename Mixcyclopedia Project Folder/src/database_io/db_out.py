from src.database_io import db_in

from pysondb import db

#initializing database for recipes, ingredients and glasses
ingredients_DB = db.getDb("data/ingredients.json")
recipe_DB = db.getDb("data/recipies.json")
glass_DB = db.getDb("data/glasses.json")

#returns a database entry with the given name
def get_by_name_case_insensitive(db, name):
    
    matching = db.reSearch("name", r"(?i)" + name) #case insensitive search

    #only return match if name is same as given name
    for match in matching:
        if match["name"].lower() == name.lower():
            return match
        
    return None
        
        
#write an ingredient to file
def write_ingredient(ingredient, ingredient_type):
    ingredients_DB.add({"name":ingredient, "type":ingredient_type, "prev_selected": False})

#calls write_ingredient to write all ingredients in given list,
#checks to see if ingredient exists in file before writing it to file
def check_and_add_ingredients(ingredients):
    for i in ingredients:
        if not get_by_name_case_insensitive(ingredients_DB, i[0]):
            write_ingredient(i[0], i[3])

#write a recipe to file
def write_recipe(name, ingredients, garnishes, glass):
    recipe_data = {"name":name, "ingredients":ingredients, "garnishes":garnishes, "glass":glass}

    check_and_add_ingredients(ingredients) #add all recipe ingredients

    existing_recipe = recipe_DB.getByQuery({"name": name})
    if len(existing_recipe) == 0: #write new recipe
        recipe_DB.add(recipe_data)
        
    else: #update recipe if already exists in db
        old_ingredients = existing_recipe[0]["ingredients"]
        recipe_DB.updateByQuery({"name": name}, recipe_data)
        clean_up_ingredients(old_ingredients) #remove unused ingredients

#sets prev_selects attribute of ingredients given list to true
#and all other to false
def write_selected(ingredients):
    #set prev_selected to false for all ingredients in db 
    try:
        ingredients_DB.updateByQuery({"prev_selected":True},{"prev_selected":False})
    except:
        pass

    #sets prev_selected to true for all ingredients in given list
    for i in ingredients:
        i_id = get_by_name_case_insensitive(ingredients_DB, i)["id"]
        ingredients_DB.updateById(i_id,{"prev_selected":True})

#writes a new glass type to db
def write_glass(name, file_name):
    glass_DB.add({"name":name, "file_name":file_name})

#deletes a recipe from the database by recipe id
def delete_recipe(recipe_id):
    used_ingredients = recipe_DB.getById(recipe_id)["ingredients"]
    recipe_DB.deleteById(recipe_id)
    clean_up_ingredients(used_ingredients) #remove unused ingredients from db
    
#deletes an ingredient from db by id
def delete_ingredient(ingredient_id):
    ingredients_DB.deleteById(ingredient_id)

#removes each ingredient in given list from db if unused by any active recipes
def clean_up_ingredients(ingredients):

    for ingredient in ingredients:

        #checking if generator object returned from get_idea_recipes is empty
        _empty = object()
        if next(db_in.get_idea_recipes([ingredient[0].lower()]), _empty) is _empty:
            try: #delete ingredient by id if ingredient exists 
                delete_ingredient(get_by_name_case_insensitive(ingredients_DB, ingredient[0])["id"])
            except:
                pass


