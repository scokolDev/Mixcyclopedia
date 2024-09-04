from src.database_io import db_in
from src.custom_widgets import custom_widgets

import tkinter
from tkinter import ttk
from PIL import Image, ImageTk

class show_recipes_page(ttk.Frame):
    def __init__(self, parent, transition_func, ingredients=None, search_type="all"):
        super().__init__(parent, width=1080, height=565)
        self.place(x="10", y="75")
        
        self.search_type = search_type
        self.ingredients = ingredients
        self.transition_func = transition_func #transition function from the main window

        #button to return to main page
        return_to_main = lambda: self.transition_func("main_page")
        tkinter.Button(self, text= "return", width=20, height=5, command=return_to_main).place(x=0,y=0)

        #scrollable frame which will hold all display recipes
        self.recipe_display = custom_widgets.scrollable_frame(self, width=800, height=525, label="Cocktail Recipes:")
        self.recipe_display.place(x=(1080-800)/2, y=0)

        #filling display with recipes
        self._show_recipes()
        
    #fills recipe display with all recipes to be display according to the search type
    def _show_recipes(self):
        
        #getting generator object according to search type
        if self.search_type == "possible": recipes = db_in.get_possible_recipes(self.ingredients)
        elif self.search_type == "idea": recipes = db_in.get_idea_recipes(self.ingredients)
        else: recipes = db_in.get_all_recipes()
        
        for recipe in recipes:
            custom_widgets.recipe_widget(self.recipe_display.display_frame, recipe, self.recipe_display.update_canvas_view, width=800, height=200).pack(pady=10, fill=tkinter.X)
            self.recipe_display.update_canvas_view()
            
        if len(self.recipe_display.display_frame.winfo_children()) == 0: self._show_no_recipes()

    #shows spilled cocktail and message that no recipes were found
    def _show_no_recipes(self):
        no_recipes_frame = tkinter.Frame(self.recipe_display.display_frame, width=800, height=450, bg="grey")
        no_recipes_frame.pack()

        tkinter.Label(no_recipes_frame, text="No Recipes Found, Try Selecting More Ingredients", bg="grey").place(x=280, y=50)
        
        spilled_img = ImageTk.PhotoImage(Image.open("img/spilled_logo.png"))
        spilled_img_label = tkinter.Label(no_recipes_frame, bg="grey")
        spilled_img_label.image = spilled_img
        spilled_img_label.configure(image=spilled_img)
        spilled_img_label.place(x=250, y=90)
