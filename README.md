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
sudo apt-get purge python3-pil;
sudo apt-get install python3-pil python3-pil.imagetk
sudo apt-get install python3-pandas

Sudo python3 dungeon_designer.py

Getting started:


Inspiration from:
https://donjon.bin.sh/

