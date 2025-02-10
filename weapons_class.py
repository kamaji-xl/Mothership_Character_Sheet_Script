class Weapon:
    def __init__(self):
        self.name = ""
        self.cost = ""
        self.range = ""
        self.shots = ""
        self.wound = ""
        self.special = ""

    def __str__(self):
        weapon_as_string = [f"\tName: {self.name}",
                            f"\tCost: {self.cost}",
                            f"\tRange: {self.range}",
                            f"\tShots: {self.shots}",
                            f"\tWound: {self.wound}",
                            f"\tSpecial: {self.special}"]
        return "\n".join(weapon_as_string)