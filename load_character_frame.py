import os
import tkinter as tk
import json
from tkinter import ttk
from tkinter import filedialog
import handle_file_data as pdf
from character_class import Character
from weapons_class import Weapon


class LoadCharacter(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.warning_label = None
        self.warn = None
        self.confirmation_btn = None
        self.decline_btn = None
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.rowconfigure(1, weight=0)
        # self.rowconfigure(2, weight=1)

        # Character select
        self.select_text = tk.StringVar()
        self.select_text.set(f"Active Collection: {parent.path}")
        self.select_label = ttk.Label(self, textvariable=self.select_text, font=('Fira Code', 15))
        self.select_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky='ew')

        self.c_names = ['Select Character...']
        self.select_box = ttk.Combobox(self, state="readonly", values=self.c_names, postcommand=self.update_box_list)
        self.select_box.grid(row=1, column=0, padx=5, sticky='ew')
        self.select_box.current(0)

        self.select_box.bind("<<ComboboxSelected>>", self.update_display)

        # Character Info
        self.display = tk.Text(self, width=60, height=40, font=('Fira Code', 10))
        # self.display.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        self.display.config(state='disabled')

    def cache_warning(self):
        self.warn = tk.Toplevel(self)
        self.warn.grab_set()
        self.warn.focus()
        self.warn.geometry('400x100')
        self.warn.resizable(False, False)
        self.warn.title('Warning!!!')
        self.warn.columnconfigure(0, weight=1)
        self.warn.columnconfigure(1, weight=1)
        self.warn.rowconfigure(0, weight=1)
        self.warn.rowconfigure(1, weight=1)

        self.warning_label = ttk.Label(self.warn,
                                       text='Warning, clearing the cache will erase all saved character data!\
                                                  \n\nDo you still wish to proceed?')
        self.warning_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.confirmation_btn = ttk.Button(self.warn, text='Yes', command=self.clear_cache)
        self.confirmation_btn.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.decline_btn = ttk.Button(self.warn, text='No', command=self.warn.destroy)
        self.decline_btn.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    def clear_cache(self):
        self.parent.characters.clear()
        self.export_to_json()
        self.select_box.current(0)
        self.update_display()
        self.warn.destroy()

    def export_to_json(self):
        dict_list = []
        characters = self.parent.characters

        for character in characters:
            dict_list.append(character.character_to_dict())

        data = json.dumps(dict_list, indent=4)
        # print(data)

        # path = 'characters.json'
        with open(self.parent.path, 'w') as file:
            file.write(data)
            file.close()

        print(f"Characters saved to {self.parent.path}")
        self.load_from_json(self.parent.path)

    def import_pdf(self):
        """
        Open file explorer to select a PDF file and import character data from PDF file,
        and save updated character data as JSON.
        :return: None
        """
        try:
            filename = filedialog.askopenfilename(title='Choose a PDF file to import',
                                                  filetypes=(('PDF files', '*.pdf'),))
            character_data = pdf.extract_form_values(filename)
            self.parent.characters.append(pdf.parse_character_data(character_data))
            self.update_box_list()
            self.select_box.current(len(self.select_box['values']) - 1)
            self.update_display()

            # for character in self.parent.characters:
            #     print(character)

            # print("JSON:")
            self.export_to_json()

        except FileNotFoundError:
            pass

    def load_from_json(self, new_path=''):
        if os.path.exists(new_path):
            self.parent.path = new_path

        self.parent.characters.clear()

        with open(self.parent.path, 'r') as file:
            json_data = json.loads(file.read())
            file.close()

        # print(json_data)
        # print(len(json_data))

        for json_char in json_data:
            new_char = Character()
            for key, value in json_char.items():
                if key == 'weapons':
                    for w in value:
                        new_wpn = Weapon(w['name'], w['cost'], w['range'], w['shots'],
                                         w['wound'], w['special'], w['qty'])
                        new_char.weapons.append(new_wpn)
                else:
                    setattr(new_char, key, value)
            self.parent.characters.append(new_char)

        print(f'Loaded {len(self.parent.characters)} characters from {os.path.basename(self.parent.path)}')

    def update_box_list(self):
        updated_clist = ['Select Character...']
        for character in self.parent.characters:
            updated_clist.append(character.char_name)

        self.select_box['values'] = updated_clist

    def update_display(self, event=None):
        parent = self.parent
        selection = self.select_box.get()

        self.display.config(state='normal')  # Unlock display

        if selection != 'Select Character...':

            print(f"{selection} selected...")
            for i, x in enumerate(parent.characters):
                if x.char_name == selection:
                    selection = self.parent.characters[i]
                    break

            self.display.delete('1.0', tk.END)
            self.display.insert(tk.END, selection)
            parent.action_frame.update_options(selection)
            parent.inv_frame.update_item_info()
            parent.stat_frame.get_rolls()
            parent.inv_frame.t_frame.get_history()

        else:
            self.display.delete('1.0', tk.END)
            parent.action_frame.update_options(None)
            parent.stat_frame.get_rolls()

        self.display.config(state='disabled')  # Lock display
