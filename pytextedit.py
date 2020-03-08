import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Menubar:

    def __init__(self, parent):
        font_spaces = ("windows", 14)
        menubar = tk.Menu(parent.master)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_spaces, tearoff=0)
        file_dropdown.add_command(label="New File", accelerator="Ctrl+N",command=parent.new_file)
        file_dropdown.add_command(label="Open File", accelerator="Ctrl+O", command=parent.open_file)
        file_dropdown.add_command(label="Save", accelerator="Ctrl+S", command=parent.save)
        file_dropdown.add_command(label="Save as", accelerator="Ctrl+Shift+S", command=parent.saveas)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit", command=parent.master.destroy)

        about_dropdown = tk.Menu(menubar, font=font_spaces, tearoff=0)
        about_dropdown.add_command(label="Release Notes", command=self.show_release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="About", command=self.show_about_message)
        menubar.add_cascade(label="File", menu=file_dropdown)
        menubar.add_cascade(label="About", menu=about_dropdown)       
    def show_about_message(self):
        box_title = "About NickyNotes"
        box_message = "A simple python text editor"
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = "Release Notes"
        box_message = "Version 1.0"
        messagebox.showinfo(box_title, box_message)

class Statusbar:
    
    def __init__(self, parent):

        font_spaces = ("windows", 12)
        
        self.status = tk.StringVar()
        self.status.set("NickyNotes - 0.1")

        label = tk.Label(parent.textarea, textvariable=self.status, fg="black",
                          bg="lightgrey", anchor='sw', font=font_spaces)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)                  

    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set("Your file has been saved")
        else:
            self.status.set("NickyNotes - 0.1")  

class PyText:

    def __init__(self,master):
        master.title("NickyNotes")
        master.geometry("1200x700")

        font_spaces = ("windows", 18)

        self.master = master
        self.filename = None

        self.textarea = tk.Text(master, font=font_spaces)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)
        self.bind_shortcuts()

    def set_window_title(self, name=None):
        if name:
            self.master.title(name + " - NickyNotes")
        else:
            self.master.title("NickyNotes")    
    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"),
                       ("Text Files", "*.txt"),
                       ("Python Scripts", "*.py"),
                       ("Marksown Documents", "*.md"),
                       ("Javascript Files", "*.js"),
                       ("HTML Documents", "*.html"),
                       ("CSS Documents", "*.css")])
        if self.filename:
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.textarea.insert(1.0, f.read())
            self.set_window_title(self.filename)    
    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textarea_content)
                self.statusbar.update_status(True)    
            except Exception as e:
                print(e)
        else:
            self.saveas()
    def saveas(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"),
                        ("Text Files", "*.txt"),
                        ("Python Scripts", "*.py"),
                        ("Marksown Documents", "*.md"),
                        ("Javascript Files", "*.js"),
                        ("HTML Documents", "*.html"),
                        ("CSS Documents", "*.css")])
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.statusbar.update_status(True)               
        except Exception as e:
                print(e)

    def bind_shortcuts(self):
           self.textarea.bind('<Control-n>', self.new_file)
           self.textarea.bind('<Control-o>', self.open_file)
           self.textarea.bind('<Control-s>', self.save)
           self.textarea.bind('<Control-S>', self.saveas)
           self.textarea.bind('<Key>', self.statusbar.update_status)         

if __name__ == "__main__":
    master = tk.Tk()
    pt = PyText(master)
    master.mainloop()
