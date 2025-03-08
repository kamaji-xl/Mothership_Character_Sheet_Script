import tkinter as tk
from tkinter import ttk
from constants import *
from weapons_class import Weapon


class ItemFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.af = parent.action_frame
        self.wpn_info_headers = ['Name', 'Cost', 'Range', 'Shots', 'Wound', 'Special', 'Qty']
        self.wpn_keys = ['name', 'cost', 'range', 'shots', 'wound', 'special', 'qty']
        self.wpn_info_labels = {}
        self.character = None

        self.inv_box = None
        self.inv_box_lbl = None

        self.inv_list = ['View Item...']

        self.af.grid_config(8,3)
        self.make_inv_box()
        self.inv_box.bind("<<ComboboxSelected>>", self.populate_inv_labels)

    def make_inv_box(self):
        row = 0
        self.inv_box_lbl = ttk.Label(self, text='Inventory:', font=('Fira Code', 15))
        self.inv_box_lbl.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='nw')
        row += 1

        self.inv_box = ttk.Combobox(self, state="readonly", values=self.inv_list)
        self.inv_box.grid(row=row, column=0, columnspan=3, padx=5, sticky='nw')
        row += 1

        for header, key in zip(self.wpn_info_headers, self.wpn_keys):
            header_label = ttk.Label(self, text=f"{header}:", font=FC_13B)
            value_label = ttk.Label(self, text=f"None")
            header_label.grid(row=row, column=0, padx=(5, 0), pady=(5, 0), sticky='nw')
            value_label.grid(row=row, column=1, padx=0, pady=(8,0), sticky='nsw')
            row += 1
            self.wpn_info_labels[key] = [header_label, value_label]

        self.inv_box.current(0)

    def update_item_info(self):
        sel = self.af.selection
        self.inv_list = ['View Item...']
        if sel is not None:
            for item in sel.weapons:
                self.inv_list.append(f"{item.name}")

        self.inv_box['values'] = self.inv_list

    def populate_inv_labels(self, event=None):
        sel = self.af.selection
        item_name = self.inv_box.get()

        if item_name == 'View Item...':
            for header, key in zip(self.wpn_info_headers, self.wpn_keys):
                label = self.wpn_info_labels[key]
                label[1].configure(text=f"None")
        else:
            sel_wpn = Weapon()
            for weapon in sel.weapons:
                if weapon.name == item_name:
                    sel_weapon = weapon
                    break

            for header, key in zip(self.wpn_info_headers, self.wpn_keys):
                label = self.wpn_info_labels[key]
                label[1].configure(text=f"{getattr(sel_weapon, key)}")
