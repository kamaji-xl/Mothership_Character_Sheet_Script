import PyPDF2
from character_class import Character
from constants import *


def extract_form_values(path):
    reader = PyPDF2.PdfReader(path)
    with open(path, 'rb') as file:
        if not reader.get_fields():
            return

        form_fields = reader.get_fields()
        field_values = {}

        for field_name, field_data in form_fields.items():
            value = field_data.get('/V', None)
            if value is not None and value != '/Off':
                field_values[field_name] = value

        # print(field_values)
        return field_values


def parse_character_data(data):
    train = []
    exp = []
    mast = []
    new_class = "None"
    new_char = Character()

    if data.get("Class") == '/0':
        new_class = "Teamster"
    elif data.get("Class") == '/1':
        new_class = "Scientist"
    elif data.get("Class") == '/2':
        new_class = "Android"
    elif data.get("Class") == '/3':
        new_class = "Marine"

    new_char.set_details(data.get("Character Name", "None"), data.get("Pronouns", "None"), new_class,
                         data.get("High Score", "None"))

    new_char.set_stats(data.get("Strength", "None"), data.get("Speed", "None"), data.get("Intellect", "None"),
                       data.get("Combat", "None"))

    new_char.set_saves(data.get("Sanity", 0), data.get("Fear", 0), data.get("Body", 0))

    new_char.set_health(data.get("Health Current", 0), data.get("Health Maximum", 0))

    new_char.set_wounds(data.get("Wounds Current", 0), data.get("Wounds Maximum", 0))

    new_char.set_stress(data.get("Stress Current", 0), data.get("Stress Minimum", 0))

    new_char.set_conditions(data.get("Conditions", "None"))

    for skill in TRAINED:
        if data.get(skill):
            train.append(skill)

    for skill in EXPERT:
        if data.get(skill):
            exp.append(skill)

    for skill in MASTER:
        if data.get(skill):
            mast.append(skill)

    new_char.set_skills(train, exp, mast)

    new_char.set_ap(data.get("Armor Points", 0))

    new_char.set_credits(data.get("Credits", 0))

    return new_char
