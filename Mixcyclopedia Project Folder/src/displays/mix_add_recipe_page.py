import tkinter
from tkinter import ttk
from PIL import Image, ImageTk

from src.database_io import db_in, db_out
from src.input_verification import input_verification
from src.custom_widgets import custom_widgets

#__glass_img_path__ = "img/glasses/"        
class add_recipe_page(ttk.Frame):
    def __init__(self, parent, transition_func, popup_func):
        super().__init__(parent, width=1080, height=565)
        self.place(x=10, y=75)
        
        self.ingredients_dictionary = {} #dictionary of active ingredient input widgets key:widget value:True
        
        self.transition_func = transition_func #parent transition function
        self.popup_func = popup_func #function to display a popup alert
        self.pack_propagate(False)

        #recipe name input
        self.name_frame = tkinter.Frame(self)
        tkinter.Label(self.name_frame, text = "*Recipe Name:").pack(side=tkinter.LEFT)
        self.name_entry = tkinter.Entry(self.name_frame)
        self.name_entry.pack(side=tkinter.LEFT)
        self.name_frame.pack(side=tkinter.TOP, anchor="nw")

        #recipe ingredient input section
        self.ingredients_section = custom_widgets.scrollable_frame(self, width=800, height=250, label="*Recipe Ingredients:")
        self.ingredients_section.pack(side=tkinter.TOP, anchor="nw")

        #add ingredient button
        self.add_ingredient_frame = tkinter.Frame(self, width=1000, height=30)
        self.add_ingredient_frame.pack_propagate(False)
        self.add_ingredient_frame.pack(side=tkinter.TOP, anchor="nw")
        tkinter.Button(self.add_ingredient_frame, text="add ingredient", command=self._add_ingredient_input).pack(side=tkinter.TOP)
        self._add_ingredient_input()#add starting ingredient
        
        #recipe garnish input
        self.garnish_frame = tkinter.Frame(self)
        tkinter.Label(self.garnish_frame, text = "Garnishes (separate by comma):").pack(side=tkinter.LEFT)
        self.garnish_entry = tkinter.Entry(self.garnish_frame)
        self.garnish_entry.pack(side=tkinter.LEFT)
        self.garnish_frame.pack(side=tkinter.TOP, anchor="nw")

        #recipe recommended glass input
        self.glass_section = custom_widgets.scrollable_frame(self, width=1055, height=100, is_vertical=False, label="Recommended Glass:")
        self.glass_section.pack(side=tkinter.TOP, anchor="nw")
        self.glasses = db_in.get_glasses() #getting glasses from db
        self.glass_input = tkinter.StringVar()
        self.glass_input.set("Collins")
        for glass in self.glasses:
            custom_widgets.glass_option(self.glass_section.display_frame, glass, self.glass_input).pack(side=tkinter.LEFT, padx=10)
            self.glass_section.update_canvas_view()
            
        #save recipe button
        tkinter.Button(self, text="Save Recipe", width=10, height=5, command=self.save_recipe).pack(side=tkinter.RIGHT, anchor="se")

        #return button
        return_to_main = lambda:self.transition_func("main_page")
        tkinter.Button(self, text="Return", width=10, height=5,command=return_to_main).pack(side=tkinter.RIGHT, anchor="se")

    #adds ingredient input widget to ingredients section
    def _add_ingredient_input(self):
        new_ingredient = custom_widgets.ingredient_input(self.ingredients_section.display_frame, self.ingredients_section.update_canvas_view, self.ingredients_dictionary)
        new_ingredient.pack(side=tkinter.TOP, anchor="n", pady=5)
        self.ingredients_section.update_canvas_view()

    #converts all entered ingredients into tuples and returns them in a list
    def get_ingredients_list(self):
        all_ingredients = []
        for ingredient in self.ingredients_dictionary:
            all_ingredients.append(ingredient.get_data())
        return all_ingredients

    #converts entered garnishes from string to list
    def parse_garnishes(self):
        if len(self.garnish_entry.get()) == 0: return []
        
        garnish_list = self.garnish_entry.get().split(",")

        #removing white space
        for i in range(len(garnish_list)):
            garnish_list[i] = garnish_list[i].strip()
            
        return garnish_list

    #checks to see if all inputs are valid, then saves recipe data to db
    def save_recipe(self):
        name = self.name_entry.get().strip()
        ingredients = self.get_ingredients_list()
        garnishes = self.parse_garnishes()
        glass = self.glass_input.get()
        
        try:
            input_verification.verify_recipe(name, ingredients)
        except Exception as e: #input invalid, alert user with popup
            self.popup_func(e, "red")
        else: #input is valid
            db_out.write_recipe(name, ingredients, garnishes, glass) #save recipe to db
            self.transition_func("main_page") #redirect user to main
            self.popup_func("Recipe Successfully Added!", "green") #alert user of successful save with popup
