import os
import tkinter as tk
import json
from tkinter import filedialog
from character_class import Character
from load_character_frame import LoadCharacter


def main():
    gui = McssGui()
    gui.mainloop()


class McssGui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Mothership - Interactive Character Sheet')
        self.geometry('500x800')

        # style = ttk.Style()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)

        self.path = 'characters.json'

        # Initialize list of Characters and load data from characters.json
        self.characters = []
        self.load_from_json(self.path)

        # Load Frame
        self.load_frame = LoadCharacter(self)
        self.load_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Menu bar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.data_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)

        # Menubar - File Options
        self.menubar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Save', command=self.load_frame.export_to_json)
        self.file_menu.add_command(label='Save As', command=self.save_as)
        self.file_menu.add_command(label='Exit', command=self.destroy)

        # Menubar - Character Options
        self.menubar.add_cascade(label='Character', menu=self.data_menu)
        self.data_menu.add_command(label='Import PDF', command=self.load_frame.import_pdf)
        self.data_menu.add_command(label='Load Collection', command=self.choose_json)
        self.data_menu.add_command(label='Edit')
        self.data_menu.add_command(label='Clear Cache', command=self.load_frame.cache_warning)

        # Menubar - Help Options
        self.menubar.add_cascade(label='Help', menu=self.help_menu)
        self.help_menu.add_command(label='View Help')

    def choose_json(self):
        try:
            path = filedialog.askopenfilename(title='Choose a JSON file')
            self.load_from_json(path)
            self.load_frame.select_text.set(f"Active Collection: {os.path.basename(self.path)}")
            self.load_frame.select_box.current(0)
            self.load_frame.update_display()
        except FileNotFoundError:
            print('File not found')

    def load_from_json(self, new_path=''):
        if os.path.exists(new_path):
            self.path = new_path

        self.characters.clear()

        with open(self.path, 'r') as file:
            json_data = json.loads(file.read())
            file.close()

        print(json_data)
        print(len(json_data))

        for json_char in json_data:
            new_char = Character()
            for key, value in json_char.items():
                setattr(new_char, key, value)
            print(new_char)
            self.characters.append(new_char)

    def print_characters(self):
        for character in self.characters:
            character.print_character()

    def save_as(self):
        path = filedialog.asksaveasfilename(initialfile='character_list.json', defaultextension='*.json',
                                            filetypes=[('JSON', '*.json')])
        if path != '':
            self.path = path
            self.load_frame.export_to_json()


if __name__ == '__main__':
    main()
