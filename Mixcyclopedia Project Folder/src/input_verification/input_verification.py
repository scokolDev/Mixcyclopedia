#raised when an input field of a recipe is invalid
class InvalidFieldException(Exception):
    def __init__(self, message=None):
        Exception.__init__(self, message)

#verifies all user inputted recipe information
#raises an error if recipe data is invalid
def verify_recipe(name, ingredients):

    #check if recipe name is empty
    if name.replace(" ", "") == "":
        raise InvalidFieldException("recipe name is empty!")

    #check if no ingredients
    if len(ingredients) < 1:
        raise InvalidFieldException("no ingredients added")

    #check if each ingredient has a name, amount, and type; unit not required
    for i in range(len(ingredients)):
        if ingredients[i][0].replace(" ", "") == "":
            raise InvalidFieldException(f"ingredient {i+1}'s name is empty!")
        
        if ingredients[i][1].replace(" ", "") == "":
            raise InvalidFieldException(f"ingredient {i+1}'s amount is empty!")

        if ingredients[i][3] not in ("liquor", "other alcohol", "mixer"):
            raise InvalidFieldException(f"ingredient {i+1}'s type is not selected!")
