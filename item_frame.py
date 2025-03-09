import tkinter as tk
from tkinter import ttk
from constants import *
from weapons_class import Weapon
from pyhedral_client import socket_stuff


class ItemFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.af = parent.action_frame
        self.wpn_info_headers = ['Name', 'Cost', 'Range', 'Shots', 'Wound', 'Special', 'Qty']
        self.wpn_keys = ['name', 'cost', 'range', 'shots', 'wound', 'special', 'qty']

        self.wpn_info_labels = {}
        self.character = None
        self.row = 0

        self.inv_box = None
        self.inv_box_lbl = None
        self.transaction_box = None
        self.transaction_box_lbl = None
        self.transaction_labels = {}

        self.weapons_dict = {}
        self.weapon_names = ['Choose item...']
        wpn_lib = self.parent.weapon_library
        for weapon in wpn_lib:
            self.weapons_dict[weapon.name] = weapon
            self.weapon_names.append(weapon.name)

        self.inv_list = ['View Item...']

        # Inventory
        for i in range(15):
            self.rowconfigure(i, weight=1)
        for j in range(20):
            self.columnconfigure(j, weight=1)
        self.row = self.make_inv_box()
        print(self.row)
        self.sep1 = ttk.Separator(self, orient="horizontal")
        self.sep1.grid(column=0, row=self.row, padx=5, columnspan=10, pady=5, sticky="nsew")
        self.row += 1

        # Transaction Radio Buttons
        self.transaction_var = tk.StringVar(value="none")
        self.buy_radio = ttk.Radiobutton(self, text="Buy", value="buy", variable=self.transaction_var)
        self.sell_radio = ttk.Radiobutton(self, text="Sell", value="sell", variable=self.transaction_var)

        # Transaction Qty Spinbox
        self.qty_var = tk.IntVar(value=0)
        self.qty_label = ttk.Label(self, text="Qty:", font=FC_13B)
        self.qty_spinbox = ttk.Spinbox(self, from_=0, to=100, textvariable=self.qty_var)

        # Complete Transaction Button
        self.complete_transaction_button = ttk.Button(self, text="Complete Transaction",
                                                      command=self.complete_transaction)

        # Transactions
        self.row = self.make_transaction_box(self.row)

        self.sep2 = ttk.Separator(self, orient="horizontal")
        self.sep2.grid(column=0, row=self.row, padx=5, columnspan=10, pady=5, sticky="nsew")
        self.row += 1

        # Transaction History
        self.t_hist_lbl = ttk.Label(self, text="Transaction History:", font=FC_13B)
        self.t_hist_lbl.grid(column=0, row=self.row, padx=5, pady=5, sticky="nsew")
        self.row += 1

        self.t_frame = TransactionFrame(self)
        self.t_frame.grid(column=0, row=self.row, columnspan=15, padx=5, pady=5, sticky="nsew")
        print(self.row)

    # def complete_purchase(self):
    #     if self.transaction_var.get() == "buy":
    #         self.purchase()
    #     elif self.transaction_var.get() == "sell":
    #         pass
    #     else:
    #         print("Error: Must select buy or sell.")

    def make_inv_box(self):
        row = 0
        self.inv_box_lbl = ttk.Label(self, text='Inventory:', font=FC_13B)
        self.inv_box_lbl.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='nw')
        row += 1

        self.inv_box = ttk.Combobox(self, state="readonly", values=self.inv_list)
        self.inv_box.grid(row=row, column=0, columnspan=4, padx=5, sticky='nw')
        row += 1

        for header, key in zip(self.wpn_info_headers, self.wpn_keys):
            header_label = ttk.Label(self, text=f"{header}:", font=FC_13B)
            value_label = ttk.Label(self, text=f"None")
            header_label.grid(row=row, column=0, padx=(5, 0), pady=(5, 0), sticky='nw')
            value_label.grid(row=row, column=1, padx=0, pady=(5, 0), sticky='new')
            row += 1
            self.wpn_info_labels[key] = [header_label, value_label]

        self.inv_box.current(0)
        return row

    def make_transaction_box(self, row):
        self.transaction_box_lbl = ttk.Label(self, text='Transactions:', font=FC_13B)
        self.transaction_box_lbl.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='nw')
        row += 1

        self.transaction_box = ttk.Combobox(self, state="readonly", values=self.weapon_names)
        self.transaction_box.grid(row=row, column=0, columnspan=2, padx=5, pady=(5, 0), sticky='nw')
        self.inv_box.bind("<<ComboboxSelected>>", self.populate_inv_labels)
        row += 1

        self.buy_radio.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='nw')
        self.sell_radio.grid(row=row, column=1, padx=5, pady=(5, 0), sticky='nw')
        row += 1

        self.qty_label.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='nw')
        self.qty_spinbox.grid(row=row, column=1, padx=0, pady=(5, 0), sticky='nw')
        row += 1

        self.complete_transaction_button.grid(row=row, column=0, padx=5, pady=(5, 0), sticky='nw')
        row += 1

        self.transaction_box.current(0)
        return row

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
            sel_weapon = None
            for weapon in sel.weapons:
                if weapon.name == item_name:
                    sel_weapon = weapon
                    break

            for header, key in zip(self.wpn_info_headers, self.wpn_keys):
                label = self.wpn_info_labels[key]
                if sel_weapon:
                    label[1].configure(text=f"{getattr(sel_weapon, key)}")
                else:
                    label[1].configure(text=f"None")

    def complete_transaction(self):
        request_json = self.build_request()
        if request_json:
            sel = self.af.selection
            print("Sending Request:")
            for key, value in request_json.items():
                print(f"\t{key}: {value}")

            socket = socket_stuff(MERC_PORT)
            socket.send_json(request_json)
            response = socket.recv_json()

            print("\nReceived Response:")
            for key, value in response.items():
                print(f"\t{key}: {value}")
            self.handle_transaction_response(sel, response)
        self.t_frame.get_history()

    def build_request(self):
        sel = self.af.selection
        command = self.transaction_var.get()
        qty = int(self.qty_spinbox.get())
        choice_name = self.transaction_box.get()

        if not sel:
            print("Error: Must select a character.")
            req = None
        elif qty == 0:
            print("Error: Must set a quantity greater than zero.")
            req = None
        elif choice_name == 'Choose item...':
            print("Error: Must select an item.")
            req = None
        else:
            item = self.weapons_dict[choice_name]

            req = {"command": command,
                   "item_name": choice_name,
                   "qty": qty,
                   "cost": item.cost,
                   "char_name": sel.char_name,
                   "balance": sel.credits
                   }
        return req

    def handle_transaction_response(self, sel, response):
        choice_name = self.transaction_box.get()
        qty = int(self.qty_spinbox.get())
        item = self.weapons_dict[choice_name]

        if response.get("status") == "success":
            sel.credits = response.get("post_balance")
            sel_wpn_dict = {}
            for weapon in sel.weapons:
                sel_wpn_dict.update({weapon.name: weapon})

            weapon = sel_wpn_dict.get(choice_name, None)
            # print(response)
            if weapon and response.get("action") == "buy":
                weapon.qty += qty

            elif weapon and response.get("action") == "sell":
                weapon.qty -= qty
                for i, weapon in enumerate(sel.weapons):
                    if weapon.name == choice_name:
                        sel.weapons.pop(i)
            else:
                new_weapon = Weapon(item.name, item.cost, item.range, item.shots, item.wound, item.special, qty)
                sel.weapons.append(new_weapon)

            self.update_item_info()
            self.populate_inv_labels()
            self.inv_box.current(0)
            self.parent.action_frame.update_options(sel)


class TransactionFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.t_headers = ['Number', 'Item', 'Action', 'Qty', 'Cost', 'Total', 'Credits Before',
                          'Credits After', 'Date']
        self.t_header_labels = {}
        self.t_type = self.parent.weapon_names
        self.t_type.pop(0)
        self.t_type.insert(0, "all")

        for i in range(0):
            self.rowconfigure(i, weight=1)
        for j in range(10):
            self.columnconfigure(j, weight=1)

        self.t_box = ttk.Combobox(self, state="readonly", values=self.t_type)
        self.t_box.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky='nw')
        self.t_box.bind("<<ComboboxSelected>>", self.get_history)
        self.t_box.current(0)

        self.tree = ttk.Treeview(self, columns=self.t_headers, show='headings')
        self.make_tree()

    def build_t_req(self):
        sel = self.parent.af.selection
        t_type = self.t_box.get()

        req = {"command": "pull_hist",
               "char_name": sel.char_name,
               "type": t_type
               }

        return req

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def get_history(self, event=None):
        req = self.build_t_req()

        socket = socket_stuff(MERC_PORT)
        print("\nSending Request:")
        for key, value in req.items():
            print(f"\t{key}: {value}")

        socket.send_json(req)
        response = socket.recv_json()

        print("\nReceived Response:")
        print(f"\tstatus: {response['status']}\n\ttransactions:\n")
        self.clear_tree()
        if response.get('transactions', None):
            for transaction in response['transactions']:
                print(f"\t{transaction}")
                self.tree.insert('', 'end', values=transaction)

    def make_tree(self):
        for header in self.t_headers:
            self.tree.heading(header, text=header)
            if header == "Item":
                self.tree.column(header, anchor="w", width=200)
            else:
                self.tree.column(header, anchor="center", width=100)

        self.tree.grid(row=1, column=0, sticky='nsew')

    def make_t_headers(self, row, col):
        for header in self.t_headers:
            header_lbl = ttk.Label(self, text=header, font=FC_10B)
            header_lbl.grid(column=col, row=row, sticky="nsew", padx=2)
            self.t_header_labels[header] = header_lbl
            col += 1
