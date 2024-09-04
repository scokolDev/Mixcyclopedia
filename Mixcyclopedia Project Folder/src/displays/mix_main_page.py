from src.database_io import db_in
from src.custom_widgets import custom_widgets

import tkinter

INSTRUCTIONS = """Welcome to Mixcyclopedia! This application allows you to find the perfect cocktail recipe to make for any occasion.

Below are three ingredient panels which contain a wide variety of cocktail ingredients. The first panel lists all liquors with a high
abv, such as vodka, gin, and tequila.The second panel lists all ingredients which contain a lower alcohol percentage, such as liqueu-
rs, wines,and beers. The third panel lists all non-alcoholic mixers, such as fruits, juices, and sodas.

Clicking on an ingredient from any of these panels will select the checkbox next to the ingredient’s name. All selected ingredients
will then be used to find the perfect cocktail recipe for you.

On the bottom right,there are four buttons which allow you to add a new recipe, view possible recipes,view recipe ideas,and view all
recipes. Clicking on the “show possible” button will show you all recipes which you can make with the selected ingredients. All reci-
pes which contain a non-selected ingredient will not be shown. Clicking the “show ideas” button will show you all recipes which cont-
ain at least one of the selected ingredients. This will show recipes which contain non-selected ingredients, but is great when searc-
hing for a new idea before going to the store, or finding all recipes with a specific ingredient. Clicking the “show all” button will
show all recipes regardless of selected ingredients. Finally, Clicking on the “add recipe” will direct you to a page where you can
input a new recipe into the program. All newly added recipes will be saved for future uses of the program.

When on the viewing recipes page, all displayed recipes will have a “delete recipe” button which will delete the recipe from storage
if there is a recipe you do not like, or if a newly inputted recipe contains a mistake such as a spelling error.

Happy Mixing!"""

class main_page(tkinter.Frame):
    def __init__(self, parent, transition_func, width=0, height=0):
        
        super().__init__(parent, width=1080, height=565)
        self.place(x="10", y="75")
        
        self.transition_func = transition_func #transition function from the main window
        self.option_map = {} #key:ingredient name, value: boolean tkinter var attached to ingredient's checkbutton

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        #instructions section at top of frame
        self.instructions_section = tkinter.Frame(self, width=1075, height=300)
        self.instructions_section.pack_propagate(False)
        text = INSTRUCTIONS
        instructions = tkinter.Text(self.instructions_section, width=1075)

        instructions.insert(tkinter.END, text)
        instructions.config(state="disabled")
        instructions.pack()
        self.instructions_section.grid(row=0, column=0, columnspan=2)
        
        #ingredients selection panels on bottom left of frame
        self.ingredients_section = tkinter.Frame(self, width=550, height=350)
        self.ingredients_section.grid(column=0, row=1, sticky="w")
        
        self._add_ingredient_panel("liquor", "Liquors")
        self._add_ingredient_panel("other alcohol", "Other Alcohols")
        self._add_ingredient_panel("mixer", "Mixers")


        #buttons section on bottom right of frame
        self.button_section = tkinter.Frame(self, width=350, height=350)
        self.button_section.grid(column=1, row=1, sticky="e")
        self.button_section.grid_propagate(False)
        self.button_section.grid_columnconfigure(0, weight=1)
        self.button_section.grid_columnconfigure(1, weight=1)
        self.button_section.grid_rowconfigure(0, weight=1)
        self.button_section.grid_rowconfigure(1, weight=1)
        
        #directs to show recipe page: only possible recipes will be shown
        show_possible = lambda: self.transition_func("possible recipes", ingredients=self.get_selected())
        tkinter.Button(self.button_section, text="show possible", width=18, height=8,command=show_possible).grid(row=0, column=0)

        #directs to show recipe page: only recipes with at least 1 selected ingredient will be shown
        show_ideas = lambda: self.transition_func("idea recipes", ingredients=self.get_selected())
        tkinter.Button(self.button_section, text="show ideas", width=18, height=8,  command=show_ideas).grid(row=0, column=1)

        #directs to show recipe page: all recipes shown
        show_all = lambda: self.transition_func("all recipes", ingredients=self.get_selected())
        tkinter.Button(self.button_section, text="show all", width=18, height=8, command=show_all).grid(row=1, column=0)

        #directs to add recipe page
        add_recipe = lambda: self.transition_func("add recipe", ingredients=self.get_selected())
        tkinter.Button(self.button_section, text="add recipe", width=18, height=8, command=add_recipe).grid(row=1, column=1)

    #creates an ingredient panel and fills it with a specified ingredient type
    def _add_ingredient_panel(self, i_type, label):
        panel = custom_widgets.scrollable_frame(self.ingredients_section, width=200, height=300, label=label)
        panel.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
        ingredients = db_in.get_ingredients(i_type)
        
        for ingredient in ingredients:
            self.option_map[ingredient["name"]] = tkinter.BooleanVar()
            checkbox = tkinter.Checkbutton(panel.display_frame, text=ingredient["name"],variable=self.option_map[ingredient["name"]])
            checkbox.pack(side=tkinter.TOP, anchor="nw")
            if ingredient["prev_selected"]:
                checkbox.select()
            panel.update_canvas_view()
                
    #returns an list of all user selected ingredients
    def get_selected(self):
        selected = []
        for ingredient in self.option_map:
            if self.option_map[ingredient].get(): selected.append(ingredient.lower())

        return selected
