class Weapon:
    def __init__(self, name="", cost="", w_range="", shots="", wounds="", special="", qty=0):

        self.name = name
        self.cost = cost
        self.range = w_range
        self.shots = shots
        self.wound = wounds
        self.special = special
        self.qty = qty

    def __str__(self):
        weapon_as_string = [f"\tName: {self.name}",
                            f"\tCost: {self.cost}",
                            f"\tRange: {self.range}",
                            f"\tShots: {self.shots}",
                            f"\tWound: {self.wound}",
                            f"\tSpecial: {self.special}"]
        return "\n".join(weapon_as_string)

    def weapon_to_dict(self):
        return self.__dict__
