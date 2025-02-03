import tkinter as tk
import json
from tkinter import ttk
from tkinter import filedialog
import handle_file_data as pdf
from character_class import Character


def main():
    gui = McssGui()
    gui.mainloop()


class McssGui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Mothership - Interactive Character Sheet')
        self.geometry('500x800')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)

        self.characters = []
        frame = LoadCharacter(self)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # test_frame = ttk.Frame(self)
        # test_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        # test_frame.test_button = ttk.Button(self, text='Test', command=self.print_characters)
        # test_frame.test_button.grid(row=0, column=2, padx=0, pady=0)

    def print_characters(self):
        for character in self.characters:
            character.print_character()


class LoadCharacter(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Character select
        self.c_names = ['Select Character...']
        self.select_box = ttk.Combobox(self, state="readonly", values=self.c_names, postcommand=self.update_box_list)
        self.select_box.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.select_box.current(0)

        self.select_box.bind("<<ComboboxSelected>>", self.update_display)

        # Load Button
        # self.load_button = ttk.Button(self, text='Load')
        # self.load_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Import Button
        self.import_button = ttk.Button(self, text='Import PDF', command=self.import_pdf)
        self.import_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Character Info
        self.display = tk.Text(self, width=40, height=40)
        self.display.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
        self.display.config(state='disabled')

    def export_to_json(self):
        dict_list = []
        characters = self.parent.characters

        for character in characters:
            dict_list.append(character.character_to_dict())

        data = json.dumps(dict_list, indent=4)
        print(data)

        path = 'characters.json'
        with open(path, 'w') as file:
            file.write(data)

    def import_pdf(self):
        filename = filedialog.askopenfilename()
        character_data = pdf.extract_form_values(filename)
        self.parent.characters.append(pdf.parse_character_data(character_data))

        for character in self.parent.characters:
            print(character)

        print("JSON:")
        self.export_to_json()

    def update_box_list(self):
        updated_clist = ['Select Character...']
        for character in self.parent.characters:
            updated_clist.append(character.char_name)

        self.select_box['values'] = updated_clist

    def update_display(self, event=None):
        selection = self.select_box.get()
        self.display.config(state='normal')
        if selection != 'Select Character...':
            for i, x in enumerate(self.parent.characters):
                if x.char_name == selection:
                    selection = self.parent.characters[i]
                    break

            self.display.delete('1.0', tk.END)
            self.display.insert(tk.END, selection)

        else:
            self.display.delete('1.0', tk.END)

        self.display.config(state='disabled')


if __name__ == '__main__':
    main()
