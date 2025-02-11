import os
import tkinter as tk
from tkinter import ttk
import json
from tkinter import filedialog
from character_class import Character
from weapons_class import Weapon
from load_character_frame import LoadCharacter
from edit_character_frame import EditCharacter
from constants import *


def main():
    gui = McssGui()
    gui.mainloop()


class McssGui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Mothership - Interactive Character Sheet')
        self.geometry('500x800')
        self.edit_window = None
        self.no_selection = None
        self.help_text = None

        # Initialize and Load Weapon Library
        self.weapon_library = []
        self.load_weapon_library('weapons.json')

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.path = 'characters.json'

        # Load Frame
        self.load_frame = LoadCharacter(self)
        self.load_frame.grid(row=0, column=0)

        # Initialize list of Characters and load data from characters.json
        self.characters = []
        self.load_frame.load_from_json(self.path)

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
        self.data_menu.add_command(label='Load Collection', command=self.choose_json)
        self.data_menu.add_command(label='Import Character from PDF', command=self.load_frame.import_pdf)
        self.data_menu.add_command(label='Edit Character', command=self.edit_character)
        self.data_menu.add_command(label='Clear Cache', command=self.load_frame.cache_warning)

        # Menubar - Help Options
        self.menubar.add_cascade(label='Help', menu=self.help_menu)
        self.help_menu.add_command(label='View Help', command=self.help)

    def choose_json(self):
        try:
            path = filedialog.askopenfilename(title='Choose a JSON file',
                                              filetypes=[('JSON', '*.json')])
            self.load_frame.load_from_json(path)
            self.load_frame.select_text.set(f"Active Collection: {os.path.basename(self.path)}")
            self.load_frame.select_box.current(0)
            self.load_frame.update_display()

        except FileNotFoundError:
            print('File not found')

    def edit_character(self):
        if self.load_frame.select_box.get() == 'Select Character...':
            self.no_selection = tk.Toplevel(self)
            self.no_selection.geometry('450x100')
            self.no_selection.title('Oops, No character selected!')
            self.no_selection.grab_set()
            self.no_selection.focus_force()
            self.no_selection.resizable(False, False)

            no_selection_label = ttk.Label(self.no_selection,
                                           text='No character selected!\n\n'
                                                'Select a character from the drop menu to edit.',
                                           font=FC_13B)
            no_selection_label.place(relx=0.5, rely=0.5, anchor='center')

            return 0
        else:
            self.edit_window = EditCharacter(self)

    def help(self):
        if self.help_text and tk.Toplevel.winfo_exists(self.help_text):
            if self.help_text:
                self.help_text.lift()
                self.help_text.focus_force()
                self.help_text.destroy()
                self.help_text = None
        self.help_text = tk.Toplevel(self)
        self.help_text.title('Help')
        self.help_text.geometry('850x400')
        self.help_text.resizable(False, False)
        help_label = ttk.Label(self.help_text, text="Welcome to the Mothership interactive character sheet!\n\n"
                                                    "This program imports character sheet data from official "
                                                    "Mothership PDFs. \n\nImported characters are then saved as JSON"
                                                    "and are loaded automatically the next time you boot the "
                                                    "program.\n\n"
                                                    "File Menu:\n\t"
                                                    "Save -> Save current character edit to active character "
                                                    "collection.\n\t"
                                                    "Save As -> Save current current character collection "
                                                    "as a new JSON file.\n\t"
                                                    "Exit -> Close program.\n\n"
                                                    "Character Menu:\n\t"
                                                    "Load Collection -> Load character collection from JSON file.\n\t"
                                                    "Import Character from PDF -> Import character from PDF file.\n\t"
                                                    "Edit Character -> Edit currently loaded character.\n\t"
                                                    "Clear Cache -> Erased active character collection.\n\n"
                                                    "Help Menu:\n\t"
                                                    "View help -> View the help guide.",
                               font=('Fira Code', 13))
        help_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    def load_weapon_library(self, wpn_path):
        with open(wpn_path, 'r') as file:
            json_data = json.loads(file.read())
            file.close()

        for json_wpn in json_data:
            # print(json_wpn)
            new_wpn = Weapon()
            for (key, value) in json_wpn.items():
                # print(key, value)
                setattr(new_wpn, key, value)

            self.weapon_library.append(new_wpn)

        # for wpn in self.weapon_library:
        #     print(wpn, '\n')
        print(f'Loaded {len(self.weapon_library)} weapons from {os.path.basename(wpn_path)}')

    # def load_from_json(self, new_path=''):
    #     if os.path.exists(new_path):
    #         self.path = new_path
    #
    #     self.characters.clear()
    #
    #     with open(self.path, 'r') as file:
    #         json_data = json.loads(file.read())
    #         file.close()
    #
    #     # print(json_data)
    #     # print(len(json_data))
    #
    #     for json_char in json_data:
    #         new_char = Character()
    #         for key, value in json_char.items():
    #             setattr(new_char, key, value)
    #         # print(new_char)
    #         self.characters.append(new_char)
    #
    #     print(f'Loaded {len(self.characters)} characters from {os.path.basename(self.path)}')

    def save_as(self):
        path = filedialog.asksaveasfilename(initialfile='character_list.json', defaultextension='*.json',
                                            filetypes=[('JSON', '*.json')])
        if path != '':
            self.path = path
            self.load_frame.export_to_json()


if __name__ == '__main__':
    main()
