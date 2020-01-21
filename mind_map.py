from tkinter import * # I am aware that it is bad practice and shall not repeat it in the future
from tkinter import messagebox, colorchooser
import  tkinter.font


#------------------------------------ CANVAS CLASS ---------------------------------------------------
class Mind_map(Canvas):
    
    #---- VARIABLES-------
    # Coordinates for creating shapes
    x_start = None
    x_end = None
    y_start = None
    y_end = None

    # Chosen shape to insert
    shape = None
   
    # Coordinates for moving shapes
    x_motion = None
    y_motion = None

    # Information about copied item
    copied = None
    item_type = None
    copied_coords = None

    # Set up position for left button
    left_button_position = "clicked"
    # Set up color for inserting shapes
    chosen_color_hex = "Blue"
      
    # ------ FUCTIONS -----
    def left_button_clicked(self, event=None):
        """Sets left button as clicked or not and sets current coordinates"""
        
        self.left_button_position = "clicked"

        self.x_start = event.x
        self.y_start = event.y
                
    def left_button_released(self, event=None):
        """"After left button is released inserts shape to canvas"""
        self.left_button_position = "released"

        x_motion = None
        y_motion = None

        self.x_end = event.x
        self.y_end = event.y
        
        if self.shape == "rectangle":
            self.insert_rectangle(event)
        elif self.shape == "line":
            self.insert_line(event)
        elif self.shape == "text":
            self.insert_text(event)

    def motion(self, event=None):
        """Follows mouse coordinates and moves chosen object"""
        if self.x_motion is not None and self.y_motion is not None and self.shape == None and self.left_button_position == "clicked":
            self.move(CURRENT, event.x - self.x_motion, event.y - self.y_motion)
        self.x_motion = event.x
        self.y_motion = event.y

    def create_shape(self, type):
        """User sets shape to insert on canvas"""  
        self.shape = type
        
    def insert_rectangle(self, event=None):
        """Will insert rectangle on canvas"""  
        if None not in (self.x_start, self.y_start, self.x_end, self.y_end):
            self.create_rectangle(self.x_start, self.y_start, self.x_end, self.y_end, fill=self.chosen_color_hex, tags="rectangle")
            self.shape = None

    def insert_line(self, event=None):
        """Will insert line on canvas"""  
        if None not in (self.x_start, self.y_start, self.x_end, self.y_end):
            self.create_line(self.x_start, self.y_start, self.x_end, self.y_end, smooth=True, fill=self.chosen_color_hex, width = 4, tags="line")
            self.shape = None
       
    def delete(self, event=None):
        """Will show message box and if user declines to save, will delete all items on canvas"""  
        message = messagebox.askyesnocancel('Info', 'Do you want to save?')
        if message == 0:
            super().delete("all")
    
    def choose_color(self, event=None):
        """Shows colorchooser and sets color for inserted shapes"""
        chosen_color = colorchooser.askcolor(title="Select Color")
        self.chosen_color_hex = chosen_color[1]
    
    def choose_background(self, event=None):
        """Will change background color"""
        bg_color = colorchooser.askcolor(title="Select Color")
        self.config(bg= bg_color[1])

    def change_color(self, current):
        """Will change color of currently chosen object"""  
        color = colorchooser.askcolor(title="Select Color")
        self.itemconfig(current, fill=color[1]) 

    def help(self, event=None):
        """Will show message box with information""" 
        messagebox.showinfo("Help Haiku", "In this useless thing\nyou should be able to place shapes and move them around\nEmphasis on should")        

    def right_button_clicked(self, event):
        """Will create context menu on canvas according to current situation"""  
        tags = self.itemcget(self.find_withtag(CURRENT), "tags")
        current = self.find_withtag(CURRENT)
        coords = event.x, event.y
                       
        # pop up menu on canvas
        popup_menu = Menu(self, tearoff=0)
        if "rectangle" in tags or "line" in tags or "text" in tags:
            popup_menu.add_command(label="Delete", command= lambda: self.delete_item(current)) 
        if "rectangle" in tags or "line" in tags or "text" in tags:
            popup_menu.add_command(label="Copy", command= lambda: self.copy_item(current))
        # if  "text" in tags:
        #     popup_menu.add_command(label="Edit Text")
        if "rectangle" in tags or "line" in tags or "text" in tags:
            popup_menu.add_command(label="Change Color", command= lambda: self.change_color(current))
        if  tags == "":
            popup_menu.add_command(label="Change Background Color", command=self.choose_background)
        if  self.copied is not None:
            popup_menu.add_command(label="Insert", command= lambda: self.insert_item(coords))
        if "rectangle" in tags or "line" in tags or "text" in tags:
            popup_menu.add_command(label="Move Forward", command=lambda:self.tag_raise(current))
        if "rectangle" in tags or "line" in tags or "text" in tags:
            popup_menu.add_command(label="Move Backwards", command=lambda:self.tag_lower(current))

        popup_menu.post(event.x_root+5, event.y_root+5)               
    
    def delete_item(self, current):
        """Will delete currently chosen object"""      
        super().delete(current)

    def copy_item(self, current):
        """Will copy currently chosen object into memory"""
        self.item_type = self.type(current)
        item_config = self.itemconfig(current)
        self.copied = {key: item_config[key][-1] for key in item_config.keys()}
        self.copied_coords = self.coords(current)
                
    def insert_item(self, coords):
        """Will insert currently copied object from memory"""
        try:
            new_coords = coords + (coords[0] + self.copied_coords[2] - self.copied_coords[0], coords[1] + self.copied_coords[3] - self.copied_coords[1])
        except IndexError:
            pass

        if self.item_type == "rectangle":
            self.create_rectangle(new_coords, **self.copied)           
                       
        elif self.item_type == "line":
            self.create_line(new_coords, **self.copied)            
           
        elif self.item_type == "text":
            self.create_text(coords, **self.copied)                       

        self.copied = None
        self.item_type = None
        self.copied_coord = None        
        

    def insert_text(self, event):
        text_font = tkinter.font.Font(family="Helvetica", weight = "bold", size=20)    
        self.create_text(self.x_start, self.y_start, fill=self.chosen_color_hex, font=text_font,text=" ", tags="text")
        self.shape= None
        self.update_idletasks()
        self.focus_on_text(event)
        self.dchars(CURRENT, 0)
        self.select_clear()

    # functions for text editing
    def focus_on_text(self, event):
        """After double click - we need to focus on this item in order to receive keyboard inputs"""
        self.focus_set() #first to canvas itself
        self.focus(CURRENT) # then on currrent item
        self.select_from(CURRENT, 0) # selects from start
        self.select_to(CURRENT, END) # to end


    def key_pressed(self, event):
        """ Will insert letters according to keys pressed"""
        focused_item = self.focus() # selection of focused item - even though mouse is in different place
        # If the item specifier is omitted,
        # this method returns the item that currently has focus, or None if no item has focus.
        
        if focused_item and event.char >= " ": # will only insert printable chracters (ASCII)
            self.insert(focused_item, INSERT, event.char)            

    def set_cursor_on_text(self, event):
        """Moves the insertion cursor to text"""       
        focused_item = self.focus()  
        x = self.canvasx(event.x) # converts to canvas coordinates, accroding to mouse click - left button click
        y = self.canvasy(event.y)

        self.icursor(focused_item, "@%d,%d" % (x, y)) # Moves the insertion cursor to the given position. This method can only be used with editable items.
        self.select_clear() # Removes the selection, if it is in this canvas widget. - removes blue highlight

    def return_pressed(self, event=None):
        """Cancels focus on text"""
        self.focus("") # To remove focus from the item, call this method with an empty string.
        self.select_clear()

    def backspace_pressed(self, event):
        """ Backspace button works on text"""
        focused_item = self.focus()
        # Gets the numerical cursor index corresponding to the given index.
        insert_index = self.index(focused_item, INSERT) # index number of current position of cursor
    
        if focused_item and insert_index > 0:        
            self.dchars(focused_item, insert_index - 1)
            # dchars(item, index) deletes the character at the given index
            # dchars(item, from, to) removes the characters in the given range.

    def left_key_pressed(self, event):
        """Left kex works - by moving cursor 1 place to the left """
        focused_item = self.focus()
        if focused_item:
            new_index = self.index(focused_item, INSERT) - 1
            self.icursor(focused_item, new_index)
            self.select_clear()

    def right_key_pressed(self, event):
        """Right kex works - by moving cursor 1 place to the right """
        focused_item = self.focus()
        if focused_item:
            new_index = self.index(focused_item, INSERT) + 1
            self.icursor(focused_item, new_index)
            self.select_clear()

    def __init__(self, root):
        super().__init__(root) 
        self.configure(width=400, height=400, bg="white")       
        self.bind("<ButtonPress-1>", self.left_button_clicked)
        self.bind("<ButtonRelease-1>", self.left_button_released)
        self.bind("<Motion>", self.motion)        
        self.bind("<ButtonPress-3>", self.right_button_clicked)
        
        # self.config(cursor = "fleur")
           
        # init for text editing - tag "text"
        self.tag_bind("text","<Double-Button-1>", self.focus_on_text)
        self.tag_bind("text","<Button-1>", self.set_cursor_on_text)
        self.tag_bind("text","<Key>", self.key_pressed)        
        self.tag_bind("text","<Left>", self.left_key_pressed)
        self.tag_bind("text","<Right>", self.right_key_pressed)
        self.tag_bind("text","<BackSpace>", self.backspace_pressed)
        self.tag_bind("text","<Return>", self.return_pressed)
           
#--------------------------------------------- MENU ----------------------------------------------------
# Main Navigation Bar - creation through Menu
class Main_menu(Menu):  
    def __init__(self, root):
        super().__init__(root) 
        # First part of the menu - File (cascade)
        file_menu = Menu(self, tearoff = 0)
        self.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New File", command=mind_map.delete) # will add command, where canvas will restart (or all items will be deleted)
        file_menu.add_command(label="Save File") # will add command to save file??
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        # Second Part of the menu
        self.add_command(label="Help", command =mind_map.help) # will add new messagebox with help information

        # Menu which provides shapes to add to canvas + includes options for their change
        insert_menu = Menu(self, tearoff = 0)
        self.add_cascade(label="Insert", menu=insert_menu)
        insert_menu.add_command(label="Rectangle", command = lambda: mind_map.create_shape("rectangle")) # will add command to insert rectangle + will add icon of rectangle
        insert_menu.add_command(label="Line", command = lambda: mind_map.create_shape("line")) # will add command to insert line + will add icon of line
        insert_menu.add_command(label="Text", command = lambda: mind_map.create_shape("text")) 

        # # Menu which provides colors -  colorchooser
        self.add_command(label="Choose Color", command=mind_map.choose_color)
        # add choices for fonts (maybe add some font chooser?)
#------------------------- START--------------------------------
if __name__ == '__main__':
    #----------------------------------------- MAIN WINDOW ------------------------------------------------
    # Creation of main window
    root = Tk()
    root.title("Mind Map")
    # root.iconbitmap('c:\python\Tkinter\mind_map.ico')
    root.geometry("400x400")
    root.resizable(False, False)
    # ------------------------------------------ CANVAS ACTIVATION --------------------------------------
    mind_map = Mind_map(root)
    mind_map.pack()
    # ------------------------------------------ MENU ACTIVATION --------------------------------------
    menu = Main_menu(root)
    # To make menu visible
    root.config(menu=menu)
    # -------------------------------------------------- LOOP ------------------------------------------
    root.mainloop()

    
    # just trying to invoke pullrequest for code review
    
