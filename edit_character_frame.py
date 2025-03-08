import tkinter as tk
from tkinter import ttk
from constants import *


class EditCharacter(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Edit Character')
        self.geometry('1300x800')
        self.stat_spinboxes = {}
        self.save_spinboxes = {}
        self.status_spinboxes = {}
        self.details = {}
        self.parent = parent

        for col in range(7):
            self.columnconfigure(col, weight=1)

        for row in range(5):
            self.rowconfigure(row, weight=1)

        self.check_val = (self.register(self.is_valid), '%P')

        # Details Frame
        self.selection = self.select_character()
        self.details_frame = EditDetailsFrame(self, 'Details')
        self.details_frame.grid(row=0, column=0, columnspan=4, padx=10, sticky='nsew')

        # Stats/Saves Frame
        self.s_and_s_frame = EditStatsAndSaves(self, 'Stats/Saves')
        self.s_and_s_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Status Frame
        self.status_frame = EditStatus(self, 'Status')
        self.status_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Skills Frame
        self.skill_frame = EditSkills(self, 'Skills')
        self.skill_frame.grid(row=0, rowspan=4, column=4, columnspan=4, padx=10, pady=(0, 10), sticky='nsew')

        # Weapons Frame
        self.weapons_frame = EditWeapons(self, 'Weapons')
        self.weapons_frame.grid(row=2, column=0, rowspan=2, columnspan=4, padx=10, pady=(0, 10), sticky='nsew')

        # Buttons
        self.confirm_btn = ttk.Button(self, text='Apply', command=self.apply_changes)
        self.confirm_btn.grid(row=4, column=6, padx=2, pady=2, sticky='nsew')
        self.cancel_btn = ttk.Button(self, text='Cancel', command=self.destroy)
        self.cancel_btn.grid(row=4, column=5, padx=2, pady=2, sticky='nsew')

    def apply_changes(self):
        sel = self.selection

        if sel == 'Select Character...' or not sel:
            return

        # Details
        sel.char_name = self.details[NAME].get()
        sel.pronouns = self.details[PROS].get()
        sel.char_class = self.details[CLASS].get()
        sel.score = int(self.details[SCORE].get())

        # Stats
        for stat_key, spinbox in self.stat_spinboxes.items():
            sel.stats[stat_key] = int(spinbox.get())

        # Saves
        for save_key, spinbox in self.save_spinboxes.items():
            sel.saves[save_key] = int(spinbox.get())

        # 4. Status
        sel.health[CURRENT] = int(self.status_spinboxes[("health", CURRENT)].get())
        sel.health[MAX] = int(self.status_spinboxes[("health", MAX)].get())

        sel.wounds[CURRENT] = int(self.status_spinboxes[("wounds", CURRENT)].get())
        sel.wounds[MAX] = int(self.status_spinboxes[("wounds", MAX)].get())

        sel.stress[CURRENT] = int(self.status_spinboxes[("stress", CURRENT)].get())
        sel.stress[MIN] = int(self.status_spinboxes[("stress", MIN)].get())

        sel.armor_points = int(self.status_spinboxes[AP].get())
        sel.credits = int(self.status_spinboxes[CRED].get())

        # Skills
        sel.trained_skills.clear()
        sel.expert_skills.clear()
        sel.master_skills.clear()

        for skill, var in self.skill_frame.trained_vars.items():
            if var.get():
                sel.trained_skills.append(skill)
        for skill, var in self.skill_frame.expert_vars.items():
            if var.get():
                sel.expert_skills.append(skill)
        for skill, var in self.skill_frame.master_vars.items():
            if var.get():
                sel.master_skills.append(skill)

        self.destroy()
        self.parent.load_frame.update_box_list()
        self.parent.load_frame.select_box.current(0)
        self.parent.load_frame.update_display()
        print(f"Changes successfully applied to {sel.char_name}")

    @staticmethod
    def is_valid(val_to_check):
        if val_to_check == '':
            return True
        try:
            value = int(val_to_check)
            return 0 <= value <= 99
        except ValueError:
            return False

    def select_character(self):
        parent = self.parent
        selection = parent.load_frame.select_box.get()

        if selection != 'Select Character...':
            print(f"Now editing {selection}...")
            for i, x in enumerate(parent.characters):
                if x.char_name == selection:
                    selection = parent.characters[i]
                    break

        return selection


class Combo(ttk.Combobox):
    def __init__(self, parent, skill_list):
        super().__init__(parent, state='readonly', values=skill_list)


class EditDetailsFrame(ttk.LabelFrame):
    def __init__(self, parent, frame_text):
        super().__init__(parent, text=frame_text)
        self.parent = parent
        self.detail_vars = {}

        for col in range(9):
            self.columnconfigure(col, weight=1)

        self.check_val = (self.register(parent.is_valid), '%P')

        self.populate_details(parent.selection, parent.details)

    def populate_details(self, sel, entries):
        fields = [NAME, PROS, CLASS, SCORE]
        labels = ["Name:", "Pronouns:", "Class:", "Score:"]

        for i, field in enumerate(fields):

            # print(getattr(sel, field))
            detail_label = ttk.Label(self, text=f"{labels[i]}", font=FC_13B)
            detail_label.grid(row=0, column=i * 2, sticky='ew')

            if field != SCORE:
                # Create and save field_var
                field_var = tk.StringVar()
                field_var.set(getattr(sel, field))
                self.detail_vars[field] = field_var

                # Create Entry
                entry = ttk.Entry(self, textvariable=field_var)
                entry.grid(row=0, column=i * 2 + 1, padx=(0, 4), sticky='ew')
                entries[field] = entry

            else:
                spin_box = Spin(self)
                spin_box.set(getattr(sel, field))
                spin_box.grid(row=0, column=i * 2 + 1, sticky='ew')
                entries[field] = spin_box


class EditSkills(ttk.LabelFrame):
    def __init__(self, parent, frame_text):
        super().__init__(parent, text=frame_text)
        self.skill_vars = {}
        self.trained_vars = {}
        self.expert_vars = {}
        self.master_vars = {}

        for i in range(18):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)

        # skill_fields = [TRAINED, EXPERT, MASTER]
        labels = ["Trained:", "Expert:", "Master:"]
        field_strings = ['trained_skills', 'expert_skills', 'master_skills']

        # Trained Skills
        sorted_trained = list(TRAINED)
        sorted_trained.sort()
        sorted_trained = tuple(sorted_trained)
        has_trained_skills = getattr(parent.selection, field_strings[0])
        # self.trained_vars[TRAINED] = {}
        self.populate_skills(0, 0, sorted_trained, has_trained_skills, labels[0],
                             self.trained_vars)
        # Expert Skills
        sorted_expert = list(EXPERT)
        sorted_expert.sort()
        sorted_expert = tuple(sorted_expert)
        has_expert_skills = getattr(parent.selection, field_strings[1])
        self.populate_skills(6, 0, sorted_expert, has_expert_skills, labels[1],
                             self.expert_vars)

        # Master Skills
        sorted_master = list(MASTER)
        sorted_master.sort()
        sorted_master = tuple(sorted_master)
        has_master_skills = getattr(parent.selection, field_strings[2])
        self.populate_skills(12, 0, sorted_master, has_master_skills, labels[2],
                             self.master_vars)

    def populate_skills(self, row, col, all_skills, has_skills, skill_title, skill_vars):
        label = ttk.Label(self, text=skill_title, font=FC_13B)
        label.grid(row=row, column=col, sticky='ew')
        row = row + 1
        for i, skill in enumerate(all_skills):
            if i % 4 == 0:
                row = row + 1
                col = -1
            col = col + 1
            var = tk.BooleanVar(value=skill in has_skills)
            check_btn = ttk.Checkbutton(self, text=skill, variable=var)
            check_btn.grid(row=row, column=col, sticky='ew')
            skill_vars[skill] = var


class EditStatsAndSaves(ttk.LabelFrame):
    def __init__(self, parent, frame_text):
        super().__init__(parent, text=frame_text)

        # Column Config
        for col in range(10):
            self.columnconfigure(col, weight=1)

        # Row Config
        for row in range(4):
            self.rowconfigure(row, weight=1)

        self.check_val = (self.register(parent.is_valid), '%P')

        # Stats
        self.stats_label = ttk.Label(self, text='Stats:', font=FC_13B)
        self.stats_label.grid(row=0, column=0, padx=2, sticky='ew')
        self.populate_spinners(parent.stat_spinboxes, parent.selection.stats, 1)

        # Saves
        self.saves_label = ttk.Label(self, text='Saves:', font=FC_13B)
        self.saves_label.grid(row=2, column=0, padx=2, sticky='ew')
        self.populate_spinners(parent.save_spinboxes, parent.selection.saves, 3)

    def populate_spinners(self, boxes, data, enter_row):
        for i, (key, value) in enumerate(data.items()):
            label = ttk.Label(self, text=f"{key}:", font=FC_13B)
            label.grid(row=enter_row, column=i * 2 + 1)

            spin_box = Spin(self)
            spin_box.set(value)
            spin_box.grid(row=enter_row, column=i * 2 + 2, padx=2)

            boxes[key] = spin_box


class EditStatus(ttk.LabelFrame):
    def __init__(self, parent, frame_text):
        super().__init__(parent, text=frame_text)
        self.parent = parent
        self.check_val = (self.register(parent.is_valid), '%P')

        sel = parent.selection

        for col in range(8):
            self.columnconfigure(col, weight=1)
        for row in range(3):
            self.rowconfigure(row, weight=1)

        field_strs = [HEALTH, WOUND, STRESS]
        data = [sel.health, sel.wounds, sel.stress]
        field_strings = ['health', 'wounds', 'stress']

        max_min = 'Max'
        for i, status_dict in enumerate(data):
            label = ttk.Label(self, text=f'{field_strs[i]}:', font=FC_13B)
            label.grid(row=i, column=0, sticky='w')

            # Current
            label = ttk.Label(self, text=f'{CURRENT}:', font=FC_13B)
            label.grid(row=i, column=1, sticky='w')

            spin_box = Spin(self)
            spin_box.set(status_dict[CURRENT])
            spin_box.grid(row=i, column=2, padx=2, sticky='w')

            parent.status_spinboxes[(field_strings[i], CURRENT)] = spin_box

            if i == 2:
                max_min = 'Min'

            # Max or Min
            label = ttk.Label(self, text=f'{max_min}:', font=FC_13B)
            label.grid(row=i, column=3, sticky='w')

            spin_box = Spin(self)
            spin_box.set(status_dict[max_min])
            spin_box.grid(row=i, column=4, padx=2, sticky='w')

            parent.status_spinboxes[(field_strings[i], max_min)] = spin_box

        # AP
        label = ttk.Label(self, text=f'AP:', font=FC_13B)
        label.grid(row=3, column=0, sticky='w')

        spin_box = Spin(self)
        spin_box.set(getattr(sel, AP))
        spin_box.grid(row=3, column=1, padx=2, sticky='w')
        parent.status_spinboxes[AP] = spin_box

        # Credits
        label = ttk.Label(self, text=f'Credits:', font=FC_13B)
        label.grid(row=4, column=0, sticky='w')

        spin_box = Spin(self)
        spin_box.set(getattr(sel, CRED))
        spin_box.grid(row=4, column=1, padx=2, sticky='w')
        parent.status_spinboxes[CRED] = spin_box


class EditWeapons(ttk.LabelFrame):
    def __init__(self, parent, frame_text):
        super().__init__(parent, text=frame_text)
        self.grandparent = parent.parent
        self.parent = parent

        for col in range(5):
            self.columnconfigure(col, weight=1)
        for row in range(4):
            self.rowconfigure(row, weight=1)

        # Inventory Combobox
        self.inv_label = ttk.Label(self, text='Character Inventory:', font=FC_13B)
        self.inv_label.grid(row=0, column=0, sticky='w')
        self.wpn_inv_names = ['Select Weapon...']
        for weapon in self.parent.selection.weapons:
            print(f"{weapon}\n")
        for weapon in self.parent.selection.weapons:
            self.wpn_inv_names.append(weapon.name)

        self.wpn_inv_box = ttk.Combobox(self, state='readonly', values=self.wpn_inv_names)
        self.wpn_inv_box.grid(row=1, column=0, padx=2, pady=2, sticky='w')
        self.wpn_inv_box.current(0)

        self.wpn_inv_box_btn = ttk.Button(self, text='Remove', command=self.pop_wpn)
        self.wpn_inv_box_btn.grid(row=1, column=1, padx=2, pady=2, sticky='w')

        # Add Weapons from Weapon Library
        self.weapon_names = ['Select Weapon...']
        for weapon in self.grandparent.weapon_library:
            self.weapon_names.append(weapon.name)

        self.weapon_box = ttk.Combobox(self, state='readonly', values=self.weapon_names)
        self.weapon_box.grid(row=2, column=0, padx=2, pady=2, sticky='w')
        self.weapon_box.current(0)

        self.weapon_box_btn = ttk.Button(self, text='Add', command=self.add_wpn)
        self.weapon_box_btn.grid(row=2, column=1, padx=2, pady=2, sticky='w')

        self.wpn_info = ttk.Label(self, text='Weapon Info...', font=FC_13B, wraplength=400)
        self.wpn_info.grid(row=1, column=3, rowspan=2, padx=2, pady=2, sticky='w')

        self.weapon_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.show_weapon(self.grandparent.weapon_library)
        )

    def add_wpn(self):
        wpn_to_add_name = self.weapon_box.get()
        # Add Weapon to Inventory
        for wpn in self.grandparent.weapon_library:
            if wpn.name == wpn_to_add_name:
                self.parent.selection.weapons.append(wpn)

                if wpn_to_add_name not in self.wpn_inv_names:
                    self.wpn_inv_names.append(wpn_to_add_name)
                break

        # Update Combobox
        self.wpn_inv_box['values'] = self.wpn_inv_names
        self.wpn_inv_box.current(len(self.wpn_inv_names) - 1)

    def pop_wpn(self):
        wpn_to_remove_name = self.wpn_inv_box.get()
        # Remove from the name list
        if wpn_to_remove_name in self.wpn_inv_names:
            self.wpn_inv_names.remove(wpn_to_remove_name)

        # Remove from Character Inventory
        for wpn in self.parent.selection.weapons:
            if wpn.name == wpn_to_remove_name:
                self.parent.selection.weapons.remove(wpn)
                break

        # Update the combobox with the new list
        self.wpn_inv_box['values'] = self.wpn_inv_names

        if self.wpn_inv_names:
            self.wpn_inv_box.current(0)

    def show_weapon(self, wpn_library):
        selection = self.weapon_box.get()
        for wpn in wpn_library:
            if wpn.name == selection:
                selection = str(wpn)
                break
        self.wpn_info.config(text=f'{selection}')


class Spin(ttk.Spinbox):
    def __init__(self, parent):
        super().__init__(
            parent,
            from_=0,
            to=99,
            width=3,
            font=(FC_13B, 11),
            validate='key',
            validatecommand=parent.check_val
        )
