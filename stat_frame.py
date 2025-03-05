import tkinter as tk
from tkinter import ttk
from constants import *
from pyhedral_client import get_char_stats, socket_stuff
import zmq
from PIL import Image, ImageTk


class StatFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.af = parent.action_frame
        self.character = None
        self.photo = None

        self.stat_box = None
        self.stat_box_lbl = None

        self.choices = ['all']
        self.choices = self.choices + self.af.stats + self.af.saves

        self.af.grid_config(3, 0)
        self.make_stat_box()

        self.stat_box.bind("<<ComboboxSelected>>", self.get_rolls)

    def make_stat_box(self):
        self.stat_box_lbl = ttk.Label(self, text='Roll History:', font=('Fira Code', 15))
        self.stat_box_lbl.grid(row=0, column=0, padx=5, pady=(5, 0), sticky='nw')

        self.stat_box = ttk.Combobox(self, state="readonly", values=self.choices)
        self.stat_box.grid(row=1, column=0, padx=5, sticky='nw')
        self.stat_box.current(0)
        self.get_rolls()

    def get_rolls(self, event=None):
        choice = self.stat_box.get()
        if self.af.selection:
            cname = self.af.selection.char_name
        else:
            cname = "None"
        roll_history = get_char_stats(cname, choice.lower())
        no_mod_history = []
        for roll in roll_history:
            no_mod_history.append(roll[0])

        request_json = {
            "data": no_mod_history,
            "title": f"{choice} Roll History",
            "xlabel": "Roll Value",
            "ylabel": "Roll Count",
            "bins": 25
        }

        self.histogram_request(request_json)

    def histogram_request(self, request):
        socket = socket_stuff(HGM_PORT)
        socket.send_json(request)

        response = socket.recv()

        with open("hist.png", "wb") as f:
            f.write(response)

        img = Image.open("hist.png")
        img = img.resize((400, 400))
        self.photo = ImageTk.PhotoImage(img)

        img_label = ttk.Label(self, image=self.photo)
        img_label.grid(row=3, column=0, padx=5, pady=5, sticky='ew')





