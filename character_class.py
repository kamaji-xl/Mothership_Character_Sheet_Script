class Character:
    def __init__(self):
        self.char_name = ""
        self.pronouns = ""
        self.char_class = ""
        self.high_score = 0
        self.stats = {"STR": 0, "SPD": 0, "INT": 0, "CBT": 0}
        self.saves = {"Sanity": 0, "Fear": 0, "Body": 0}
        self.health = {"Current": 0, "Max": 0}
        self.wounds = {"Current": 0, "Max": 0}
        self.stress = {"Current": 0, "Min": 0}
        self.conditions = []
        self.trained_skills = []
        self.expert_skills = []
        self.master_skills = []
        self.equipment = []
        self.armor_points = 0
        self.credits = 0
        self.weapons = []

    def __str__(self):
        # Build a list of strings to join together.
        character_as_str = [f"Name: {self.char_name}", f"Pronouns: {self.pronouns}", f"Class: {self.char_class}",
                            f"High Score: {self.high_score}",
                            f"Stats: \n\tSTR: {self.stats['STR']} \n\tSPD: {self.stats['SPD']} "
                            f"\n\tINT: {self.stats['INT']} \n\tCBT: {self.stats['CBT']}",
                            f"Saves: \n\tSanity: {self.saves['Sanity']} \n\tFear: {self.saves['Fear']}"
                            f"\n\tBody: {self.saves['Body']}",
                            f"Health: \n\t{self.health['Current']} out of {self.health['Max']}",
                            f"Wounds: \n\t{self.wounds['Current']} out of {self.wounds['Max']}",
                            f"Stress: \n\tCurrent: {self.stress['Current']}"
                            f"\n\tMinimum: {self.stress['Min']}", "Conditions:"]

        for condition in self.conditions:
            character_as_str.append(f"\t{condition}")

        character_as_str.append(f"Trained Skills:")
        for skill in self.trained_skills:
            character_as_str.append(f"\t{skill}")

        character_as_str.append(f"Expert Skills:")
        for skill in self.expert_skills:
            character_as_str.append(f"\t{skill}")

        character_as_str.append(f"Master Skills:")
        for skill in self.master_skills:
            character_as_str.append(f"\t{skill}")
        # character_as_str.append(f"Trained: {self.trained_skills}")
        # character_as_str.append(f"Expert: {self.expert_skills}")
        # character_as_str.append(f"Master: {self.master_skills}")
        character_as_str.append(f"Armor Points: {self.armor_points}")
        character_as_str.append(f"Credits: {self.credits}")
        character_as_str.append(f"Equipment: {self.equipment}")
        character_as_str.append(f"Weapons: {self.weapons}")

        return "\n".join(character_as_str)

    # Setters
    def set_details(self, new_name, new_pronouns, new_char_class, new_high_score):
        self.char_name = new_name
        self.pronouns = new_pronouns
        self.char_class = new_char_class
        self.high_score = new_high_score

    def set_stats(self, strength, speed, intellect, combat):
        self.stats["STR"] = strength
        self.stats["SPD"] = speed
        self.stats["INT"] = intellect
        self.stats["CBT"] = combat

    def set_saves(self, sanity, fear, body):
        self.saves["Sanity"] = sanity
        self.saves["Fear"] = fear
        self.saves["Body"] = body

    def set_health(self, curr, new_max):
        self.health["Current"] = curr
        self.health["Max"] = new_max

    def set_wounds(self, curr, new_max):
        self.wounds["Current"] = curr
        self.wounds["Max"] = new_max

    def set_stress(self, curr, new_min):
        self.stress["Current"] = curr
        self.stress["Min"] = new_min

    def set_conditions(self, new_condition):
        self.conditions.append(new_condition)

    def set_skills(self, train, exp, mast):
        self.trained_skills = train
        self.expert_skills = exp
        self.master_skills = mast

    def set_ap(self, new_ap):
        self.armor_points = new_ap

    def set_credits(self, new_credits):
        self.credits = new_credits

    def character_to_dict(self):
        return self.__dict__

    def print_character(self):
        print("\nName:", self.char_name)
        print("Pronouns:", self.pronouns)
        print("Class:", self.char_class)
        print("High Score:", self.high_score)
        print(f"Stats: \n\tSTR: {self.stats['STR']} \n\tSPD: {self.stats['SPD']} "
              f"\n\tINT: {self.stats['INT']} \n\tCBT: {self.stats['CBT']}")
        print(f"Saves: \n\tSanity: {self.saves['Sanity']} \n\tFear: {self.saves['Fear']}\n\tBody: {self.saves['Body']}")
        print(f"Health: \n\t{self.health['Current']} out of {self.health['Max']}")
        print(f"Wounds: \n\t{self.wounds['Current']} out of {self.wounds['Max']}")
        print(f"Stress: "
              f"\n\tCurrent: {self.stress['Current']}"
              f"\n\tMinimum: {self.stress['Min']}")
        print(f"Conditions:")
        for condition in self.conditions:
            print(f"\t{condition}")
        print(f"Trained: {self.trained_skills}")
        print(f"Expert: {self.expert_skills}")
        print(f"Master: {self.master_skills}")
        print(f"Armor Points: {self.armor_points}")
        print(f"Credits: {self.credits}")
        print(f"Equipment: {self.equipment}")
        print(f"Weapons: {self.weapons}")
