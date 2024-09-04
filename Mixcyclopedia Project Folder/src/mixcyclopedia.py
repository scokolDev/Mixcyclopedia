from src.displays import mix_main_page, mix_add_recipe_page, mix_show_recipe_page
from src.database_io import db_out

import tkinter
from tkinter import ttk
from PIL import Image, ImageTk

class mixcyclopedia(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title('Mixcyclopedia')
        self.iconbitmap("img/small_logo.ico")
        self.geometry('1100x650')
        self.resizable(False, False)

        self.alert = None
        self.display_window = None
        
        self.canvas = tkinter.Canvas(self, width=1100, height=650)
        
        #background
        bg = ImageTk.PhotoImage(file="img/bg.png")
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tkinter.NW, image=bg)

        #large logo at top of window
        large_logo = ImageTk.PhotoImage(Image.open("img/large_logo.png"))
        self.canvas.create_image(350, 3, anchor=tkinter.NW, image=large_logo)

        self.transition_display("main page") #set display to main page
        
        self.mainloop()
    
    #displays a popup alert frame to alert the user
    def popup(self, message, border_color="black"):
        alert_text = str(message)
            
        self.alert = tkinter.Frame(self.canvas, width=400, height=100, highlightbackground=border_color, highlightthickness=3)
        self.alert.pack_propagate(False)
        
        tkinter.Label(self.alert, text=alert_text).pack(anchor=tkinter.CENTER)
        
        tkinter.Button(self.alert, text="dismiss", command=self.alert.destroy).pack(side=tkinter.BOTTOM)
        
        self.alert.place(x="350", y="275")

    #transitions the main display frame to a different view
    #-redirect: type of view to redirect to
    #-ingredients: list of user selected ingredients
    def transition_display(self, redirect, ingredients=None):
        
        #destroy current display and popup if they are in place
        if self.display_window != None: self.display_window.destroy()
        if self.alert != None: self.alert.destroy()

        #save selected ingredients as previously selected by user
        if ingredients != None:db_out.write_selected(ingredients)

        
        if redirect == "all recipes":
            self.display_window = mix_show_recipe_page.show_recipes_page(self.canvas, self.transition_display)
            
        elif redirect == "possible recipes":
            self.display_window = mix_show_recipe_page.show_recipes_page(self.canvas, self.transition_display, ingredients=ingredients, search_type="possible")

        elif redirect == "idea recipes":
            self.display_window = mix_show_recipe_page.show_recipes_page(self.canvas, self.transition_display, ingredients=ingredients, search_type="idea")

        elif redirect == "add recipe":
            self.display_window = mix_add_recipe_page.add_recipe_page(self.canvas, self.transition_display, self.popup)

        else: #main page
            self.display_window = mix_main_page.main_page(self.canvas, self.transition_display)
        
        #self.display_window.place(x="10", y="75")
        
if __name__ == "__main__":
    app = mixcyclopedia()
