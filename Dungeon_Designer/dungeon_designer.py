# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 12:28:02 2017
Author HominidHazard
"""
from tkinter import Tk, Canvas, Button, StringVar, END, NW, BOTH, YES
from PIL import ImageTk, Image
from Dungeon_Designer import MapGenerator, AutocompleteEntry

def load_background(file):
    """Load the front GUI background"""

    background = Image.open('Maps/PathPictures/' + file)
    background = background.resize((800, 500)) #(height, width)
    background = ImageTk.PhotoImage(background)
    return background

def gen_map():
    """Create a randomly generated map in a Tkinter canvas for use in D&D

    The map will generate loot buttons and monster buttons within the
    canvas."""

    MapGenerator.create_map(gridsize=45, EnemyLevel=10)

def gen_booty():
    """Create random booty (D&D in-game loot)"""

    MapGenerator.MakinRain()

def gen_monster():
    """Create a monster from the D&D realm, or a random bandit"""

    MapGenerator.MakinMonsters(EnemyLevel=20)

def load_map():
    """Load the last generated map"""

    MapGenerator.load_map(file="Maps/newmap.txt")

#%% execute when loaded
def dungeon_designer_gui():
    """Build the GUI for Dungeon Designer"""

    def format_on_focus(event):
        """When spell lookup box takes focus reconfigure the text format"""

        event = event
        generate_spell.delete(0, END)
        generate_spell.config(foreground='black')

    def find_spell(event):
        """Function used to lookup D&D spell descriptions"""

        spell = spellbook[spellbook["Spell"] == generate_spell.get()].values.tolist()
        try:
            spell = [str(x).replace("nan", "") for x in spell[0]]
        except IndexError:
            return

        spell1 = spell[0] + "\n" + spell[1] + "\n" + spell[2] + \
        "\n" + spell[3] + "\n" + spell[4] + "\n" + spell[5] + "\n" + spell[6] + \
        "\n\n" + spell[7] + "\n" + spell[8] + "\n" + spell[9] + "\n" + spell[10] + \
        "\n" + spell[11]
        master = Tk()
        spellcanvas1 = Canvas(master, width=500, height=400)
        master.wm_title(spell[0])
        spellcanvas1.create_text(20, 20, text=spell1, width=400, anchor=NW)
        spellcanvas1.pack(fill=BOTH, expand=YES)

    home = Tk()
    background = load_background("DungeonDoor.jpg")
    spellbook = MapGenerator.create_spellbook()

    front = Canvas(home, width=840, height=540, background="black")
    front.master.title("Dungeon Designer")
    front.create_image(20, 20, image=background, anchor=NW)

    generate_map = Button(front, text="Generate Random Map", font=("Arial", 14, "bold"),\
                          command=gen_map)
    generate_map.place(x=550, y=250)

    generate_booty = Button(front, text="Booty Generator", font=("Arial", 14, "bold"),\
                            command=gen_booty)
    generate_booty.place(x=550, y=300)

    generate_monster = Button(front, text="Monster Generator", font=("Arial", 14, "bold"),\
                              command=gen_monster)
    generate_monster.place(x=550, y=350)

    generate_load = Button(front, text="Load Map", font=("Arial", 14, "bold"),\
                           command=load_map)
    generate_load.place(x=550, y=400)

    spells = spellbook["Spell"].values.tolist()
    init_spell = StringVar()
    init_spell.set("Spell")

    generate_spell = AutocompleteEntry.AutocompleteEntry(spells)
    generate_spell.bind('<FocusIn>', format_on_focus)
    generate_spell.place(x=550, y=450)
    generate_spell.config(foreground='grey', font=("Arial", 14, "bold"))
    generate_spell.insert(END, "-spell lookup")

    generate_spell.bind('<Return>', find_spell)

    front.pack()
    home.mainloop()

if __name__ == "__main__":
    dungeon_designer_gui()
