from src.database_io import db_in, db_out

import tkinter
from PIL import Image, ImageTk

GLASS_IMG_PATH = "img/glasses/"

#frame with a scroll bar
#self is a panel which holds a scrollable canvas with a display frame
#widgets are added to display frame
#can be vertical scrolling frame or horizontal
class scrollable_frame(tkinter.Frame):
    def __init__(self, parent, width=0, height=0, is_vertical=True, label=None):
        super().__init__(parent, width=width, height=height)
        
        if label: tkinter.Label(self, text=label).pack(side=tkinter.TOP)#label that goes at top of widget

        self.canvas = tkinter.Canvas(self, width=width, height=height)
        self.canvas.pack_propagate(False)
        
        if is_vertical: #vertical scroll bar
            self.scrollbar = tkinter.Scrollbar(self, orient=tkinter.VERTICAL,command=self.canvas.yview)
            self.scrollbar.pack(side=tkinter.RIGHT, fill="y")

            self.canvas.configure(yscrollcommand=self.scrollbar.set)
        else: #horizontal scroll bar
            self.scrollbar = tkinter.Scrollbar(self, orient=tkinter.HORIZONTAL, command=self.canvas.xview)
            self.scrollbar.pack(side=tkinter.BOTTOM, fill="x")

            self.canvas.configure(xscrollcommand=self.scrollbar.set)
            
        self.canvas.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH, pady=10)

        self.display_frame = tkinter.Frame(self.canvas, width=width, height=height)

        self.canvas.create_window((0,0), window=self.display_frame, anchor="nw")

    #updates the scrollbar when a widget is added or removed from display frame
    def update_canvas_view(self):
        self.display_frame.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

#glass option for add recipe page
#contains glass name, image, and radio button for selection
class glass_option(tkinter.Frame):
    def __init__(self, parent, glass, variable):
        super().__init__(parent, width=100, height=100)
        
        self.bind('<Button>', lambda e:variable.set(glass["name"]))
        self.pack_propagate(False)

        #glass name
        name_label = tkinter.Label(self, text=glass["name"])
        name_label.bind('<Button>', lambda e:variable.set(glass["name"]))
        name_label.pack(side=tkinter.BOTTOM)

        #glass radio button
        tkinter.Radiobutton(self, value=glass["name"], variable=variable).pack(side=tkinter.LEFT)

        #glass image
        self.image = ImageTk.PhotoImage(Image.open(GLASS_IMG_PATH + glass["file_name"]))
        image_label = tkinter.Label(self)
        image_label.bind('<Button>', lambda e:variable.set(glass["name"]))
        image_label.image = self.image
        image_label.configure(image=self.image)
        image_label.pack(side=tkinter.RIGHT)

#widget for inputting an ingredient on add recipe page
#has a name, type, amount, and unit input field
#has a delete button which removes widget
class ingredient_input(tkinter.Frame):
    def __init__(self, parent, update_func, ingredients_dictionary):
        super().__init__(parent, width=800, height=30)
        self.update_func = update_func #updates scrollbar on parent frame when self is added or removed
        self.ingredients_dictionary = ingredients_dictionary #dictionary of all active ingredients on add ingredients page
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_propagate(False)

        #ingredient name input
        name_frame = tkinter.Frame(self)
        name_frame.grid(column=0, row=0, sticky="w")
        tkinter.Label(name_frame, text= "*Name: ").pack(side=tkinter.LEFT)
        self.name_input = tkinter.Entry(name_frame)
        self.name_input.pack(side=tkinter.LEFT)

        #ingredient type drop down menu
        type_frame = tkinter.Frame(self, width=200, height=30)
        type_frame.pack_propagate(False)
        type_frame.grid(column=1, row=0)
        tkinter.Label(type_frame, text= "*Type: ").pack(side=tkinter.LEFT)
        self.type_input = tkinter.StringVar() 
        self.type_input.set("Select a Type")
        options = ["liquor", "other alcohol", "mixer"]
        tkinter.OptionMenu(type_frame, self.type_input, *options).pack(side=tkinter.LEFT)

        #ingredient amount input
        amount_frame = tkinter.Frame(self)
        amount_frame.grid(column=2, row=0, sticky="e")
        tkinter.Label(amount_frame, text= "*amount: ").pack(side=tkinter.LEFT)
        self.amount_input = tkinter.Entry(amount_frame)
        self.amount_input.pack(side=tkinter.LEFT)

        #ingredient unit input
        unit_frame = tkinter.Frame(self)
        unit_frame.grid(column=3, row=0, sticky="e")
        tkinter.Label(unit_frame, text= "unit: ").pack(side=tkinter.LEFT)
        self.unit_input = tkinter.Entry(unit_frame)
        self.unit_input.pack(side=tkinter.LEFT)

        #delete button
        tkinter.Button(self, text= "delete", command=self.delete).grid(column=4, row=0, sticky="e")

        #adding self to dictionary of ingredients
        ingredients_dictionary[self] = True

    def delete(self):
        self.destroy() 
        self.update_func() #update ingredients section scrollbar
        del self.ingredients_dictionary[self] #remove self from dictionary

    #returns inputed data as a tuple
    def get_data(self):
        return (self.name_input.get().strip(), self.amount_input.get().strip(), self.unit_input.get().strip(), self.type_input.get())
    
#widget that displays all information about an individual recipe for the show recipe page
#shows recipe name, ingredients, garnishes, and recommended glass type
#has a delete button which removes widget and recipe from db
class recipe_widget(tkinter.Frame):
    def __init__(self, parent, recipe, update_func, width=0, height=0):
        color = "grey" #background color
        super().__init__(parent, width=width, height=height, bg=color)

        self.update_func = update_func
        self.r_id = recipe["id"]

        #recipe glass
        self.glass_image = ImageTk.PhotoImage(Image.open(GLASS_IMG_PATH + db_in.get_glasses(recipe["glass"])["file_name"]))
        self.image_label = tkinter.Label(self, highlightbackground="black", highlightthickness=3)
        self.image_label.image = self.glass_image
        self.image_label.configure(image=self.glass_image)
        self.image_label.pack(side=tkinter.LEFT, padx=50)

        #delete button
        tkinter.Button(self, text="Delete Recipe", command=self.delete).pack(side=tkinter.RIGHT, padx=50)
        
        #recipe name
        self.name = tkinter.Label(self, bg=color, text=recipe["name"])
        self.name.pack(side=tkinter.TOP)

        #recipe ingredients
        self.ingredients = tkinter.Frame(self, bg=color, width=150, height = 200)
        tkinter.Label(self.ingredients, bg=color, text="Ingredients:").pack(anchor="nw")
        for ingredient in recipe["ingredients"]:
            tkinter.Label(self.ingredients, bg=color, text=f"   - {ingredient[1]} {ingredient[2]} {ingredient[0]}").pack(anchor="nw")
        self.ingredients.pack(side=tkinter.LEFT, padx=50, pady=20, anchor="n")

        #recipe garnishes
        self.garnishes = tkinter.Frame(self, bg=color, width=150, height = 200)
        tkinter.Label(self.garnishes, bg=color, text="Optional Garnishes:").pack(anchor="nw")
        for garnish in recipe["garnishes"]:
            tkinter.Label(self.garnishes, bg=color, text=f"   - {garnish}").pack(anchor="nw")
        self.garnishes.pack(side=tkinter.RIGHT, padx=50, pady=20, anchor="n")

        self.config(width=width)
        

    def delete(self):
        db_out.delete_recipe(self.r_id)
        self.destroy()
        self.update_func()
   
