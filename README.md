# Dungeon_Designer
Dungeon Designer is a tool kit for use by a dungeon master in the role-playing game, Dungeons and Dragons. The user-friendly GUI tackles quick random enemy generation, random loot, and an easy spell lookup function. But the real power of Dungeon Designer is in its ability to generate dungeons. Dungeons are randomly generated rooms with intertwining paths connecting them all together. Dungeons are then populated with monsters, miscellaneous creatures, bandits, and most importantly loot. Let the adventures begin.

Requirements:
python3.4 or higher
working version PIL
Pandas
Anaconda3

Windows Users
This program was initially developed on a windows system with up-to-date anaconda
Download anaconda and create a new environment with the requirements.txt file in this repository
conda env create -f=/path/to/requirements.txt -n

Mac Users
Follow the same instructions for creating a new conda environment but use MacRequirements.txt instead.
conda env create -f=/path/to/MacRequirements.txt -n

If there is an error it is most likely due to the python imaging library or PIL. An option may be to remove and reinstall your version of PIL.

  Remove pil and reinstall working version
  sudo apt-get purge python3-pil;
  sudo apt-get install python3-pil python3-pil.imagetk

Instructions for raspberry pi 3
Miniconda is not required to run on the raspberry pi 3

Remove pil and reinstall working version
sudo apt-get purge python3-pil
sudo apt-get install python3-pil python3-pil.imagetk
sudo apt-get install python3-pandas

Sudo python3 dungeon_designer.py

Getting started:

Open the dungeon_designer.py file with python3. It should open a GUI with the option to create a random map. Start by clicking that button. A random map should have been generated, focus in on it and widen it. You should see rooms and a pathway connecting all the rooms together. Scattered throughout the map are monsters and most importantly loot tiles. Click on the monster tiles to randomly generate a monster or bandit, and click on the loot to see what awesome items your player characters found.

Back on the main GUI screen there is the option to just create a monster or bandit. Within the bandit screen there will be randomly generated spells that the bantit knows. Click on the spell lookup button to see a more in depth description of the spell.

The load map button will load the previously generated map. The spell look up entry is to help you lookup the spell rules quickly. Begin typing the spell and press enter when the spell is typed out. Try typing "Fireball" and pressing enter. A new GUI should appear with all of the rules of casting the fireball spell.

Within the Dungeon_Designer folder there are two more programs that the main dungeon_designer.py is pulling from. GenerateMap.py, and Character_Generator.py. The GenerateMap.py will probably not run by itself without a little modification to the file locations. The Character_Generator.py file on the other hand should run by itself.

The Character_Generator.py is program for creating D&D characters. The main class is a Creature class that keeps the mains stats of strength, dexterity, constitution... and there are additional classes that inherit from the Creature class. Barbarian, Wizards, Clerics.. and then race classes Human, WoodElf, MountainDwarf...

Examples for using the character class: 

Bob = Character()

print(Bob)

Should create stats for bob including hit points and size

Bob = Barbarian(race=Human)

print(Bob)

should create stats for bob that are representative of a human barbarian (There should be a high strength stat)

Inspiration from:
https://donjon.bin.sh/

Thanks to:
https://gist.github.com/uroshekic/11078820

This is code for a class that inherits from tkiner's entry class. It autocompletes text fields, and is used in the spell lookup function.

