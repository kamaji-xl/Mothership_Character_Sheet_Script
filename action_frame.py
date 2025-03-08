import tkinter as tk
from tkinter import ttk
from constants import *
import ast
from pyhedral_client import make_roll


class ActionFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.stats = [STR, SPD, INT, CBT]
        self.saves = [SANITY, FEAR, BODY]
        self.details = [NAME_LBL, PROS_LBL, CLASS_LBL, SCORE_LBL]
        self.extra_details = [HEALTH, WOUND, STRESS]
        self.ap_cred = ["AP", "Credits"]
        self.ap_cred_labels = {}
        self.detail_keys = [NAME, PROS, CLASS, SCORE]
        self.stat_buttons = {}
        self.save_buttons = {}
        self.trained_buttons = {}
        self.expert_buttons = {}
        self.master_buttons = {}
        self.detail_labels = {}
        self.extra_labels = {}
        self.details_row = 0
        self.selection = None
        self.roll_type = None
        self.roll_mod = 0
        self.target = 0

        self.grid_config(20, 6)

        # Details
        self.sep_row = self.details_block(self.details_row, 0)
        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.grid(column=0, row=self.sep_row, columnspan=6, pady=5, sticky="nsew")
        self.stat_row = self.sep_row + 1

        # Stats & Saves
        self.base_option = tk.StringVar(value='0')
        self.sep2_row = self.option_block("[Stats]", self.stats, self.stat_row, 0, self.stat_buttons)
        self.sep2_row = max(
            self.sep2_row,
            self.option_block("[Saves]", self.saves, self.stat_row, 1, self.save_buttons)
        )

        self.sep2 = ttk.Separator(self, orient="horizontal")
        self.sep2.grid(column=0, row=self.sep2_row, columnspan=6, pady=5, sticky="nsew")

        # Skills
        self.skill_row = self.sep2_row + 1
        self.skill_option = tk.StringVar(value=str({'None': 0}))
        self.sep3_row = self.skill_block("[Trained Skills]", TRAINED,
                                         self.skill_row, 0, self.trained_buttons, 10)
        self.sep3_row = max(self.sep3_row,
                            self.skill_block("[Expert Skills]", EXPERT,
                                             self.skill_row, 1, self.expert_buttons, 15))
        self.sep3_row = max(self.sep3_row,
                            self.skill_block("[Master Skills]", MASTER,
                                             self.skill_row, 2, self.master_buttons, 20))

        self.sep3 = ttk.Separator(self, orient="horizontal")
        self.sep3.grid(column=0, row=self.sep3_row, columnspan=6, pady=5, sticky="nsew")

        # Roll Block
        self.roll_label = ttk.Label(self, text=f"Roll Calculation:", font=FC_15B)
        self.roll_label.grid(column=0, row=self.sep3_row+1, columnspan=3, padx=5, pady=5, sticky="ew")

        self.results_label = ttk.Label(self, text=f"Results:", font=FC_15B)
        self.results_label.grid(column=0, row=self.sep3_row+2, columnspan=3, padx=5, pady=5, sticky="ew")

        self.roll_btn = ttk.Button(self, text='Roll', command=self.request_roll)
        self.roll_btn.grid(row=self.sep3_row+3, column=0, padx=10, pady=10, sticky='ew')

    def details_block(self, row, col):
        extra_row = 0

        for i in self.details:
            detail_label = ttk.Label(self, text=f"{i}:", font=FC_13B)
            detail_label.grid(row=row, column=col, padx=5, pady=0, sticky='ew')
            detail_val_label = ttk.Label(self, text=f"None")
            detail_val_label.grid(row=row, column=col+1, sticky='ew')
            self.detail_labels.update({i: [detail_label, detail_val_label]})
            row += 1

        for extra in self.extra_details:
            extra_label = ttk.Label(self, text=f"{extra}:", font=FC_13B)
            extra_label.grid(row=extra_row, column=col+2, padx=5, sticky='ew')
            extra_val_label = ttk.Label(self, text=f"None")
            extra_val_label.grid(row=extra_row, column=col+3, sticky='ew')
            self.extra_labels.update({extra: [extra_label, extra_val_label]})
            extra_row += 1

        extra_row = 0
        for header in self.ap_cred:
            ap_cred_label = ttk.Label(self, text=f"{header}:", font=FC_13B)
            ap_cred_label.grid(row=extra_row, column=col+4, padx=5, sticky='ew')
            ap_cred_val_label = ttk.Label(self, text=f"None")
            ap_cred_val_label.grid(row=extra_row, column=col+5, sticky='ew')
            self.ap_cred_labels.update({header: [ap_cred_label, ap_cred_val_label]})
            extra_row += 1

        return row

    def display_roll(self):
        base_roll = ast.literal_eval(self.base_option.get())
        skill_roll = ast.literal_eval(self.skill_option.get())

        key1 = list(base_roll.keys())
        roll_type = key1[0]
        self.roll_type = roll_type
        base_value = int(base_roll[roll_type])

        key2 = list(skill_roll.keys())
        skill = key2[0]
        skill_mod = int(skill_roll[skill])
        self.roll_mod = skill_mod

        total = base_value + skill_mod
        self.target = total
        self.roll_label.config(text=f"Roll Calculation:\n"
                                    f"\t     ({base_value}) {roll_type}\n"
                                    f"\t+   ({skill_mod}) {skill}\n"
                                    f"\t<= ({total}) Needed",
                               font=FC_15B)

    def grid_config(self, rows, columns):
        for i in range(columns):
            self.columnconfigure(i, weight=1, uniform="col")

        for j in range(rows):
            self.rowconfigure(j, weight=1, uniform="row")

    def option_block(self, header, opts, row, col, group):
        opt = self.base_option
        option_label = ttk.Label(self, text=header, font=FC_13B)
        option_label.grid(row=row, column=col, padx=5, sticky='nw')
        row += 1
        for i, stat in enumerate(opts):
            option_btn = ttk.Radiobutton(self, text=f"{stat}: {ZERO}", value={stat: ZERO},
                                         variable=opt, command=self.display_roll)
            option_btn.grid(row=row, column=col, padx=5, sticky='nw')
            group.update({stat: option_btn})
            row += 1

        return row

    def request_roll(self):
        for i in range(1):
            status = "Fail"
            color = "red"

            roll = make_roll(1, 100, self.selection.char_name, self.roll_type.lower(), self.roll_mod)

            if roll[0] <= self.target:
                status = "Pass"
                color = "green"

            self.results_label.config(text=f"Results: {roll} ({status})", foreground=color)
            self.parent.stat_frame.get_rolls()

    def skill_block(self, header, opts, row, col, group, mod):
        opt = self.skill_option
        skill_label = ttk.Label(self, text=header, font=FC_13B)
        skill_label.grid(row=row, column=col, padx=5, sticky='ew')
        row += 1
        for i, skill in enumerate(opts):
            skill_button = ttk.Radiobutton(self, text=skill, value={skill: mod},
                                           variable=opt, command=self.display_roll)
            group.update({skill: skill_button})
            row += 1

        return row

    def update_labels(self, sel):
        if sel:
            bio = [sel.char_name, sel.pronouns, sel.char_class, sel.high_score]
            bio2 = [sel.health, sel.wounds, sel.stress]
            bio3 = [sel.armor_points, sel.credits]

            for label, attr in zip(self.details, bio):
                lbl = self.detail_labels.get(label)
                lbl = lbl[1]
                lbl.config(text=f"{attr}")

            for label, attr in zip(self.extra_details, bio2):
                lbl = self.extra_labels.get(label)
                lbl = lbl[1]
                if attr.get('Min', None) is not None:
                    lbl.config(text=f"{attr[CURRENT]}/{attr['Min']}")
                else:
                    lbl.config(text=f"{attr[CURRENT]} / {attr['Max']}")

            for label, attr in zip(self.ap_cred, bio3):
                lbl = self.ap_cred_labels.get(label)
                lbl = lbl[1]
                lbl.config(text=f"{attr}")

        else:
            for label in self.details:
                lbl = self.detail_labels.get(label)
                lbl = lbl[1]
                lbl.config(text=f"None")

            for label in self.extra_details:
                lbl = self.extra_labels.get(label)
                lbl = lbl[1]
                lbl.config(text=f"None")

            for label in self.ap_cred:
                lbl = self.ap_cred_labels.get(label)
                lbl = lbl[1]
                lbl.config(text=f"None")

    def update_saves(self, sel):
        if sel:
            for key, value in sel.saves.items():
                button = self.save_buttons[key]
                button.config(text=f"{key}: {value}", value={key: value})
        else:
            for key, value in self.save_buttons.items():
                button = value
                button.config(text=f"{key}: 0", value={key: 0})

    def update_skills(self, sel, row, col):
        # print(sel)
        new_row = row
        skill_buttons = [self.trained_buttons, self.expert_buttons, self.master_buttons]
        if sel:
            char_skills = [sel.trained_skills, sel.expert_skills, sel.master_skills]

            for skills, buttons in zip(char_skills, skill_buttons):
                new_row = max(new_row, self.update_skills_helper(skills, buttons, row, col))
                col += 1
        else:
            for buttons in skill_buttons:
                for key, value in buttons.items():
                    value.grid_forget()

        return new_row

    def update_skills_helper(self, skills, group, row, col):
        for key, value in group.items():
            if key in skills:
                value.grid(column=col, row=row, padx=5, sticky='ew')
                row += 1
            else:
                value.grid_forget()
        return row

    def update_stats(self, sel):
        if sel:
            for key, value in sel.stats.items():
                button = self.stat_buttons[key]
                button.config(text=f"{key}: {value}", value={key: value})
        else:
            for key, value in self.stat_buttons.items():
                button = value
                button.config(text=f"{key}: 0", value={key: 0})

    def update_options(self, sel):
        self.selection = sel
        self.update_labels(sel)
        self.update_stats(sel)
        self.update_saves(sel)
        self.sep3_row = self.update_skills(sel, self.skill_row+1, 0)
