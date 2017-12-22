
# coding: utf-8

# In[1]:
import timeit
from math import ceil
from csv import reader
from random import randint, randrange, choice, seed
from tkinter import Toplevel, Canvas, NW, W, Button, mainloop, Frame, \
Scrollbar, HORIZONTAL, VERTICAL, BOTH, FLAT, E, Entry, RIGHT, BOTTOM, Y, \
X, Tk, YES
from PIL import ImageTk, Image
import pandas as pd
from .CharacterGenerator import Barbarian, Bard, Cleric, Druid, Fighter, \
                         Paladin, Rogue, Ranger, Wizard, Warlock, Sorcerer, \
                         Human, HillDwarf, MountainDwarf, HighElf, WoodElf, \
                         ForestGnome, RockGnome, LightfootHalfling, \
                         StoutHalfling, Dragonborn, HalfElf, HalfOrc, \
                         InfernalTiefling

# In[2]:

ALLITEMS = []
  
with open("Items/Adventuring Gear.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    ADVENTURING_GEAR = list(READ)
    ALLITEMS.append(ADVENTURING_GEAR) 

with open("Items/Armor.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    ARMOR = list(READ)
    ALLITEMS.append(ARMOR)        

with open("Items/Coins and Gems.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    COINS = list(READ)
    ALLITEMS.append(COINS)
 
with open("Items/Healing Potion.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    HEALING_POTIONS = list(READ)
    ALLITEMS.append(HEALING_POTIONS)
  
with open("Items/Magic Items.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    MAGIC_ITEMS = list(READ)
    ALLITEMS.append(MAGIC_ITEMS)

with open("Items/Mounts And Vehicles.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    MOUNTS = list(READ)
    ALLITEMS.append(MOUNTS)

with open("Items/Poisons.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    POISON = list(READ)
    ALLITEMS.append(POISON)

with open("Items/Tools.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    TOOLS = list(READ)
    ALLITEMS.append(TOOLS)

with open("Items/Weapons.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    WEAPONS = list(READ)
    ALLITEMS.append(WEAPONS)
    
with open("Encounters/Miscellaneous Creatures.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    MISCELL_CREATURES = list(READ)

with open("Encounters/CompleteMonsters.csv", 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    MONSTERS = list(READ)

with open('Encounters/NPC.csv', 'r', encoding='utf-8', errors='ignore') as file:
    READ = reader(file)
    NPC_BACKGROUND = list(READ)

# In[3]:
def Room_Generate(gridsize):
    """function to randomly populate the map with rooms

    The function returns two lists:
        roomloc:    Actuall coordinates for grid locations that are used in the image
                    creation.
        pathforroom:coordinates of room locations that the path must collide with
                    before the later path looping function will stop. This list
                    is slowly deleted until empty."""
             
    Randroom = randint(int(gridsize**2/9**2), int(gridsize**2/6**2))
    cter = 0
    RoomLoc = []
    pathforroom = []
    #randomly generate a room
    while cter < Randroom:
        buildroom = []
        #room size
        RandomY = randrange(3, 11, 2)
        RandomX = randrange(3, 11, 2)
        #room location
        RandRoomX = randrange(int((RandomX/2))+3, (gridsize - int(RandomX/2))-1, 2)
        RandRoomY = randrange(int((RandomY/2))+2, (gridsize - int(RandomY/2))-1, 2)
        Randomroom1 = (RandRoomX + gridsize * RandRoomY)
        Yval = 0 
        while Yval < RandomY:
            Xval = 0
            while Xval < RandomX:
                buildroom.append(Randomroom1 -(int(RandomY/2)*gridsize)-int(RandomX/2) + Xval + (gridsize*Yval))
                Xval = Xval + 1
            Yval = Yval + 1

        colroom = []
        for i in buildroom:        
            colroom.append(i)
            colroom.append(i - gridsize*2)
            colroom.append(i + gridsize*2)
            colroom.append(i - gridsize*2 + 3)
            colroom.append(i + gridsize*2 + 3)
            colroom.append(i - gridsize*2 - 3)
            colroom.append(i + gridsize*2 - 3)
            colroom.append(i + 1)
            colroom.append(i - 1)
        if not any(i in colroom for i in RoomLoc): #Destroy room if it collides with a currently existing room or is too close
            RoomLoc = RoomLoc + buildroom
            for space in buildroom:
                pathforroom.extend(["Room"+str(cter)])
                pathforroom.extend([space])
        cter = cter + 1
    RoomLoc = set(RoomLoc)
    pathforroom = pathforroom

    return(pathforroom, RoomLoc)


# In[4]:
def Create_Border(gridsize):
    """Define the perimeter of the mapspace"""

    North = list(range(1, gridsize+1))
    South = list(range(gridsize**2-gridsize, gridsize**2+1))
    East = list(range(gridsize, gridsize**2, gridsize))
    West = list(range(gridsize + 1, gridsize**2, gridsize))
    Startpath = North + South + East + West
    StartpathN = list(range(3, gridsize, 2))
    StartpathS = list(range(gridsize**2-gridsize+1, gridsize**2, 2))
    StartpathE = list(range(gridsize*3, gridsize**2+1, gridsize*2))
    StartpathW = list(range(gridsize*2+1, gridsize**2, gridsize*2))

    return Startpath, StartpathN, StartpathS, StartpathE, StartpathW


# In[5]:
def direction(varlook, gridsize):
    """returns a dictionary of directions from current location in the map.

    example:    if the program needs posible directions and its current location
                and its current location in the map is x = 5 y = 5, this function 
                will return coordinatates where north: x = 5 y = 6

                *note that the program sees the map as a single array"""

    coords = {}
    coords = {"North":varlook-gridsize, "South":varlook+gridsize, "East":varlook+1, "West":varlook-1, "NorthWest":varlook-gridsize-1, "NorthEast":varlook-gridsize+1, "SouthWest":varlook+gridsize-1, "SouthEast":varlook+gridsize+1}
    return coords

# In[6]:
def testdirection(var, gridsize, pathforroom, path, Startpath, RoomLoc):
    """This function is an attempt to build a "better" path.

    adjusting some of the parameters in this function may make paths more or less
    zigzaggy and may make paths more or less inclined to go near rooms and borders.
    """

    cter = 0
    cardinal = [direction(var, gridsize)["North"], direction(var, gridsize)["South"], direction(var, gridsize)["East"], direction(var, gridsize)["West"]]
    restdirec = [direction(var, gridsize)["NorthWest"], direction(var, gridsize)["NorthEast"], direction(var, gridsize)["SouthWest"], direction(var, gridsize)["SouthEast"]]
    for i in cardinal:
        if i in pathforroom:
            cter = cter - 2
        elif i in path:
            cter = cter + 2
        elif i in Startpath:
            cter = cter + 1
        elif i in RoomLoc:
            cter = cter + 1
    for i in restdirec:
        if i in path:
            cter = cter + 1
        elif i in Startpath:
            cter = cter + 0
        elif i in RoomLoc:
            cter = cter + 0
    return int(cter)

# In[7]:
def func_movements(gridsize, loc):
    """function to return valid movements within the map during path generation.

    This function ensures that the path does not generate outside of the
    specified grid locations."""

    cardN = [direction(direction(loc, gridsize)["North"], gridsize)["North"], direction(loc, gridsize)["North"]]
    cardS = [direction(direction(loc, gridsize)["South"], gridsize)["South"], direction(loc, gridsize)["South"]]
    cardE = [direction(direction(loc, gridsize)["East"], gridsize)["East"], direction(loc, gridsize)["East"]]
    cardW = [direction(direction(loc, gridsize)["West"], gridsize)["West"], direction(loc, gridsize)["West"]] 
    cards = []
    if cardN[0] > 0 and cardN[0] < gridsize**2:
        cards.append(cardN)
  
    if cardS[0] > 0 and cardS[0] < gridsize**2:
        cards.append(cardS)

    if cardE[0] > 0 and cardE[0] < gridsize**2:
        cards.append(cardE)

    if cardW[0] > 0 and cardW[0] < gridsize**2:
        cards.append(cardW)

    return cards
#%%
def startpathgen(gridsize, RoomLoc, valid_starts):
    """Function to initialize valid path starting locations"""

    Startpath, StartpathN, StartpathS, StartpathE, StartpathW = Create_Border(gridsize)

    loc = -1
    while 0 > loc:
        if valid_starts:
   
            loc = choice(choice([StartpathN, StartpathS, StartpathE, StartpathW])+[x for x in choice([valid_starts])]) #add path later

        else:
            loc = choice(choice([StartpathN, StartpathS, StartpathE, StartpathW]))

    #Starting the first path ---------------------------------------------------------------------
    locp = loc
    if loc in StartpathN:
        halfloc = direction(loc, gridsize)["South"]
        loc = direction(halfloc, gridsize)["South"]
    elif loc in StartpathS:
        halfloc = direction(loc, gridsize)["North"]
        loc = direction(halfloc, gridsize)["North"]
    elif loc in StartpathE:
        halfloc = direction(loc, gridsize)["West"]
        loc = direction(halfloc, gridsize)["West"]
    elif loc in StartpathW:
        halfloc = direction(loc, gridsize)["East"]
        loc = direction(halfloc, gridsize)["East"]
    else:
        cards = func_movements(gridsize, loc)
        pick = choice(cards)
        loc = pick[0]
        halfloc = pick[1]

    if loc in RoomLoc or loc in Startpath:
        return startpathgen(gridsize, RoomLoc, valid_starts)

    return loc, locp, halfloc, Startpath

# In[8]:
def trypick(DirectionMove, loc, locp, halfloc, RoomLoc, pathforroom, door, path, gridsize, valid_starts):
    """This function returns path movements during path creation and deletes pathforroom."""

    pick = choice(DirectionMove)
    pathforroom = pathforroom
    door = door
    path = path
    RoomLoc = RoomLoc

    if pick[0] in RoomLoc:
        """ This means the path is right next to a room that has not been visited before, 
            now that it has been visited remove the room from the list of rooms that still
            need to be visited."""
        if pick[0] in pathforroom:
            delvar = pathforroom[pathforroom.index(pick[0])-1]
            while delvar in pathforroom:
                pathforroom.pop(pathforroom.index(delvar)+1)
                pathforroom.pop(pathforroom.index(delvar))
            door.append(pick[0])
            path.append(pick[1])
            loc = loc
            locp = locp
            halfloc = halfloc
            return loc, locp, halfloc, door, pathforroom, path

        else:
            """This part of the code is not fully utalized in the program, but the 
                thought is that for each time the path visits a room create a door
                variable. Later this door variable could be used to create door
                images in the correct locations."""
            lowerdoor = choice([0, 1, 2, 3])
            if lowerdoor == 0:
                door.append(pick[0])
                if pick[1] not in RoomLoc:
                    path.append(pick[1])

                loc, locp, halfloc = loc, locp, halfloc 
            else:
                loc, locp, halfloc, Startpath = startpathgen(gridsize, RoomLoc, valid_starts)
            return loc, locp, halfloc, door, pathforroom, path
    else:
        locp = loc
        loc = pick[0]
        halfloc = pick[1]
    return loc, locp, halfloc, door, pathforroom, path

# In[9]:
def create_path(gridsize, pathforroom, RoomLoc):
    """The main path creation coordinator

    Main parts of this function:
        1:  initialize the starting location of the path
        2:  start the looping function of path creation until the path
            has visited every room in the map.
        3:  append path tiles where path is created
        4:  if there is a problem, reintialize the starting location"""

    path = []
    pathforroom = pathforroom

    valid_locals = [x + (y * gridsize) for x in range(3, (gridsize)-1, 2) for y in range(2, (gridsize)-1, 2)]
    loc, locp, halfloc, Startpath = startpathgen(gridsize, RoomLoc, valid_starts=[])
    if halfloc not in RoomLoc:
        path.append(halfloc)

    if loc not in RoomLoc:
        path.append(loc)

    path.append(locp)
    door = []
    DirectionMove = []
    while pathforroom: 
        #keep looping until there is a path by each room

        valid_starts = [x for x in valid_locals if x in path]
        """
        Initially the path starts on the edge of the map, but if the path gets stuck
        it can call from valid starts and start a creating a new path from previously
        generated path. This prevents the path generator getting stuck in an endless
        loop.
        """

        #creation of posible movements
        DirectionMove.clear()
        cardN = [direction(direction(loc, gridsize)["North"], gridsize)["North"], direction(loc, gridsize)["North"]]
        cardS = [direction(direction(loc, gridsize)["South"], gridsize)["South"], direction(loc, gridsize)["South"]]
        cardE = [direction(direction(loc, gridsize)["East"], gridsize)["East"], direction(loc, gridsize)["East"]]
        cardW = [direction(direction(loc, gridsize)["West"], gridsize)["West"], direction(loc, gridsize)["West"]] 
        if (loc - locp) == -2:
            locp = cardW[0]
            locF = cardE
        elif (loc - locp) == 2:
            locp = cardE[0]
            locF = cardW
        elif (loc - locp) == (-gridsize-gridsize):
            locp = cardN[0]
            locF = cardS
        elif (loc - locp) == (gridsize + gridsize):
            locp = cardS[0]
            locF = cardN
        else:
            locF = ""

        BadDirect = []
        BadDirect = Startpath + path #locations we do not want the path to overwrite
        if locF:
            roomcheck = [cardN, cardS, cardE, cardW, locF]
        else:
            roomcheck = [cardN, cardS, cardE, cardW]
       
        for i in roomcheck:
            if not i[0] in BadDirect and i[0] > 0 and i[0] < gridsize**2:
            #if the posible movement is not in an obviously problamatic position
                
                if testdirection(int(i[0]), gridsize, pathforroom, path, Startpath, RoomLoc) < 3:
                #and the path has a high score rating from test direction
                    DirectionMove.append(i) 
                    #append it to the movements being considered in this moment.

        if DirectionMove:
            """ If there is still a valid movement location(s), then randomly pick one
                of those valid movements."""
            loc, locp, halfloc, door, pathforroom, path = trypick(DirectionMove, loc, locp, halfloc, RoomLoc, pathforroom, door, path, gridsize, valid_starts)
            if loc not in RoomLoc:#double checking we are not overwriting rooms
                path.append(loc)
                
            if halfloc not in RoomLoc:
                path.append(halfloc)

        else:
            """ If our path got stuck reintialize the path generation at a new 
                valid location."""
            (loc, locp, halfloc, Startpath) = startpathgen(gridsize, RoomLoc, valid_starts)

        if halfloc not in RoomLoc:
            path.append(halfloc)

        if loc not in RoomLoc:
            path.append(loc)

    return path, Startpath, door

# In[10]:
def create_spellbook():
    """import spells from an excel sheet"""

    spellbook = pd.read_csv('Dungeon_Designer/spellcards1.4.csv', encoding="utf-8")
    return spellbook

#%%
def booty_tiles(gridsize):    
    """Create random booty coordinates on the map"""

    numbooty = randint(int(gridsize*gridsize/1000), int(gridsize*gridsize/60))
    booty = []
    cter = 0
    while cter < numbooty:
        RandbootyX = randint(2, gridsize-2)
        RandbootyY = randint(2, gridsize-2)
        Randbooty = RandbootyX + gridsize * RandbootyY
        booty.append(Randbooty)
        cter = cter + 1

    return booty

# In[11]:
def monster_tiles(gridsize):
    """Create random monster coordinates on the map"""

    numMonsters = randint(int(gridsize*gridsize/1000), int(gridsize*gridsize/60))
    monsters = []
    cter = 0
    while cter < numMonsters:
        RandmonX = randint(2, gridsize-2)
        RandmonY = randint(2, gridsize-2)
        Randmon = RandmonX + gridsize * RandmonY
        monsters.append(Randmon)
        cter = cter + 1

    return monsters

# In[15]:
def convert_to_tiles(gridsize, Startpath, booty, monsters, path, RoomLoc):
    """compile all coordinates into one list

    At this point the program has been creating a bunch of different lists of 
    coordinates. 
    For instance our path will look like [12, 13, 14, 24, 34, 35, 36]
    We need to combine all of these into one list that represents the entire
    board."""

    board = []
    var = 0
    room_tile = 'R'
    pTile = 'P'
    edgeTile = 'O'
    bootyTile = 'B'
    monsterTile = 'M'
    #doortile = 'D' this is currently not used
    grass = 'G' #if you're not a part of any list you're a grass

    for row in range(gridsize):
    # Appen a blank list to each row cell
        board.append([])
        for column in range(gridsize):
            var = (var + 1)
            if var in Startpath:
                board[row].append(edgeTile)
            elif var in booty:
                board[row].append(bootyTile)
            elif var in monsters:
                board[row].append(monsterTile)
            elif var in path:
                board[row].append(pTile)
            elif var in RoomLoc:
                board[row].append(room_tile)
            else:
                board[row].append(grass)

    return board #this is the representation of our map in text

# In[13]:
# Function will print board like an actual board
def save_board(board, file="Maps/newmap.txt"):
    """Save the text version of the board."""
    
    with open(file, 'w') as file:
        for row in board:
            file.write(' '.join(row))
            file.write('\n')
            print(" ".join([x.replace("G", " ") for x in row]))
    file.close()

#%%
def load_board(file="newmap.txt"):
    """function to pull the last created board"""

    with open(file, "r") as file:
        f = file.readlines()
        board = []
        for line in f:
            line = line.replace("\n", "")
            line = line.replace(" ", "")
            board.append(line)     
    file.close()
    return board

  # In[17]:
def load_image_tile(file, CellSize):
    """function to return a correctly sized image tile for use on the map GUI"""

    tile = Image.open('Maps/PathPictures/' + file + '.png')
    tile = tile.resize((CellSize, CellSize)) #The (250, 250) is (height, width)
    tile = ImageTk.PhotoImage(tile)  
    return tile

# In[18]:
def MakinMonsters(gridsize=100, EnemyLevel=1):
    """Creates a random creature, monster, or bandit in a GUI"""

    def new_window():
        """create a new GUI for the creature, monster or bandit"""

        MonsterType = randint(0, 2)#choose creature, monster, or bandit
        if MonsterType == 0:
            Monster1 = choice(MISCELL_CREATURES)

            master = Toplevel()      
            background = Image.open('Maps/PathPictures/Monster_Manual.jpg')
            background = background.resize((600, 300))
            background = ImageTk.PhotoImage(background)

            m = Canvas(master, width=640, height=340, background = "black")
            m.create_image(20, 20, image=background, anchor=NW)
            text1 = "Miscellaneous Creature\n"
            for i in Monster1:    
                text1 += str(i) + '\n'
            m.create_text(20, 20, text=(text1), anchor=NW, fill = "white", font=("Arial", 14, "bold", "underline"))
            m.pack() 

        elif MonsterType == 1:

            Monster1 = choice(MONSTERS)

            master = Toplevel()
            background = Image.open('Maps/PathPictures/Misc_Creature.png')
            background = background.resize((600, 300)) 
            background = ImageTk.PhotoImage(background)

            m = Canvas(master, width=640, height=340, background = "black")
            m.create_image(20, 20, image=background, anchor=NW)
            text1 = "Monster Creature\n"
            for i in Monster1:    
                text1 += str(i) + '\n'
            m.create_text(20, 20, text=(text1), anchor=NW, fill = "black", font=("Arial", 14, "bold", "underline"))
            m.pack()      

        else:           

            def rand_spell():
                """Function used to lookup D&D spell descriptions"""

                spells = []
                spellbook = create_spellbook()
                for spell_level in spell_levels:
                    spells.extend(spellbook[spellbook["Level"] == spell_level].values.tolist())
                spell = choice(spells)
                try:
                    spell = [str(x).replace("nan", "") for x in spell]
                except IndexError:
                    return
                spell_des = spell[0] + "\n" + spell[1] + "\n" + spell[2] + \
                            "\n" + spell[3] + "\n" + spell[4] + "\n" + spell[5] +\
                            "\n" + spell[6] + "\n\n" + spell[7] + "\n" + spell[8] \
                            + "\n" + spell[9] + "\n" + spell[10] + "\n" + spell[11]
                return spell[0], spell_des

            CharBackground = choice(NPC_BACKGROUND)
            cast_level = ceil(EnemyLevel/2)
            spell_levels = [str('Level: ' + str(x)) for x in range(1, cast_level)]

            spell1, sct1 = rand_spell()
            spell2, sct2 = rand_spell()
            spell3, sct3 = rand_spell()

            Weapon = [["Club", 4], ["Dagger", 4], ["Greatclub", 8], ["Handaxe", 6],
                      ["Javelin", 6], ["Light Hammer", 4], ["Mace", 6],
                      ["Quarterstaff", 6], ["Sickle", 4], ["Spear", 6],
                      ["Crossbow, light", 8], ["Dart", 4], ["Shortbow", 6],
                      ["Sling", 4], ["Battleaxe", 8], ["Flail", 8],["Glaive", 10],
                      ["Greataxe", 12], ["Greatsword", 6], ["Halberd", 10],
                      ["Lance", 12], ["Longsword", 8], ["Maul", 6],
                      ["Morningstar", 8], ["Pike", 10], ["Rapier", 8],
                      ["Scimitar", 6], ["Shortsword", 6], ["Trident", 6]]

            humanoids = [Barbarian, Bard, Cleric, Druid, Fighter, \
                         Paladin, Rogue, Ranger, Wizard, Warlock, \
                         Sorcerer] 

            races = [Human, HillDwarf, MountainDwarf, HighElf, \
                     WoodElf, ForestGnome, RockGnome, \
                     LightfootHalfling, StoutHalfling, \
                     Dragonborn, HalfElf, HalfOrc, \
                     InfernalTiefling]

            humanoid = choice(humanoids)
            race = choice(races)

            armorclass = choice(range(10, 25))
            char = humanoid(race=race, level=EnemyLevel)
            WeaponPick = choice(range(0, len(Weapon)))

            name = " ".join (['A', 'Random', CharBackground[0], race.__name__, humanoid.__name__])

            master = Toplevel()

            background = Image.open('Maps/PathPictures/bandits.jpg')
            background = background.resize((125, 125)) 
            background = ImageTk.PhotoImage(background)

            def close_windows():
                """Bandit kill button"""
                master.destroy()

            def remove_hit_points():
                """Built in hitpoint calculator"""

                damage = w.CurrentHits.get()
                if damage == "":
                    damage = 0
                ct = int(w.Hits.get()) - int(damage)
                w.Hits.delete(0,'end')
                w.Hits.insert(0, str(ct))

            def lookupspell():
                """Lookup the bandits spells"""

                master = Tk()
                Spellcanvas1 = Canvas(master, width=500, height=400)
                master.wm_title(spell1)
                Spellcanvas1.create_text(20, 20, text=sct1, width=400, anchor=NW)
                Spellcanvas1.pack(fill=BOTH, expand=YES)

                master = Tk()
                Spellcanvas2 = Canvas(master, width=500, height=400)
                master.wm_title(spell2)
                Spellcanvas2.create_text(20, 20, text=sct2, width=400, anchor=NW)
                Spellcanvas2.pack(fill=BOTH, expand=YES)

                master = Tk()
                Spellcanvas3 = Canvas(master, width=500, height=400)
                master.wm_title(spell3)
                Spellcanvas3.create_text(20, 20, text=sct3, width=400, anchor=NW)
                Spellcanvas3.pack(fill=BOTH, expand=YES)

            w = Canvas(master, width=500, height=250)
            master.wm_title(name)
            w.pack()
            w.create_image(250, 125, image=background)
            w.create_text(20, 20, text=str(Weapon[WeaponPick][0]) + "     Damage Die = d" + str(Weapon[WeaponPick][1]), anchor=W, font=(36), width=800)
            w.create_text(20, 40, text=str(armorclass) + ' = Armor Class', anchor=W, font=(36), width=800)
            w.create_text(20, 60, text=str(char.hit_points) + ' = Max Hit Points', anchor=W, font=(36), width=800)
            w.create_text(20, 80, text=str(char.strength) + ' = strength', anchor=W, font=(36), width=800)
            w.create_text(20, 100, text=str(char.dexterity) + ' = dexterity', anchor=W, font=(36), width=800)
            w.create_text(20, 120, text=str(char.constitution) + ' = constitution', anchor=W, font=(36), width=800)
            w.create_text(20, 140, text=str(char.intelligence) + ' = intelligence', anchor=W, font=(36), width=800)
            w.create_text(20, 160, text=str(char.wisdom) + ' = wisdom', anchor=W, font=(36), width=800)
            w.create_text(20, 180, text=str(char.charisma) + ' = charisma', anchor=W, font=(36), width=800)

            w.create_text(460, 20, text='Spells', anchor=E, font=(36), width=800)
            w.create_text(480, 40, text=spell1, anchor=E, font=(36), width=800)
            w.create_text(480, 60, text=spell2, anchor=E, font=(36), width=800)
            w.create_text(480, 80, text=spell3, anchor=E, font=(36), width=800)

            killbutton1 = Button(master, text="kill", command=close_windows)
            killbutton1.pack()

            removehitpointsbutton2 = Button(master, text="Remove Hit Points", command=remove_hit_points)
            removehitpointsbutton2.pack()

            spelllookupbutton = Button(master, text="Look up spells", command=lookupspell)
            spelllookupbutton.place(x=480, y=120, anchor=E)

            w.CurrentHits = Entry(master, width=25)
            w.CurrentHits.pack()
            w.Hits = Entry(master, width=25)
            w.Hits.insert(0, char.hit_points)
            w.Hits.pack()

        mainloop()
 
    new_window()

def MakinRain():
    """When a booty tile is pushed this function creates look in a GUI"""

    rain = Toplevel()
    background = Image.open('Maps/PathPictures/treasure_room.jpg')
    background = ImageTk.PhotoImage(background) 

    rain.title("Loot Found in the Booty Generator, you're welcome")
    ChanceLoot = randint(1, 1000)#How good is the loot
    if ChanceLoot >= 999:
        pick1 = choice(MAGIC_ITEMS)
    elif ChanceLoot >= 995:
        pick1 = choice(choice(ALLITEMS))
    elif ChanceLoot >= 935:
        pick1 = choice(WEAPONS)
    elif ChanceLoot >= 900:
        pick1 = choice(ARMOR)
    elif ChanceLoot >= 850:
        pick1 = choice(TOOLS)
    else:
        Money = randint(0, 2)#we are also going to create some loot money
        if Money == 0:
            pick1 = [str(randint(1, 18000)) + str(" Copper")]
        elif Money == 1:
            pick1 = [str(randint(1, 3500)) + str(" Silver")]
        else:
            pick1 = [str(randint(1, 200)) + str(" Gold")]

    loot2 = choice(ADVENTURING_GEAR)
    loot3 = choice(ADVENTURING_GEAR)

    m = Canvas(rain, width=640, height=376, background="black")
    m.create_image(20, 20, image=background, anchor=NW)
    m.create_text(20, 20, text=(" ".join([str(x) for x in pick1]) + '\n' + " ".join([str(x) for x in loot2])\
                  + '\n' + " ".join([str(x) for x in loot3]))\
    , anchor=NW, font=("Arial", 14, "bold", "underline"), fill="white", activefill="white")

    m.pack()
    mainloop()

def GenMap(gridsize, board, CellSize, EnemyLevel):
    """Create the map GUI

    gridsize: how big is the map
    board: a list of items on the map
    EnemyLeve: recommended 1-30, how tough are the bandits in this map"""

    def make_monster():
        """Subfunction to make monsters"""

        return MakinMonsters(EnemyLevel = EnemyLevel)

    def make_booty():
        """Subfunction to make loot"""

        return MakinRain()

    #create the GUI root
    master = Toplevel()
    frame = Frame(master, width=800, height=800)
    frame.grid(row=0, column=0)

    #create a canvas with scrollbars for the map to be built in
    w = Canvas(frame, width=gridsize*CellSize, height=gridsize*CellSize, background='#8c7f4e', scrollregion=(0, 0, gridsize*CellSize, gridsize*CellSize))
    hbar = Scrollbar(frame, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=w.xview)
    vbar = Scrollbar(frame, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=w.yview)
    w.config(width=600, height=600)
    w.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    #import tile images
    stonepath = load_image_tile('stone path', CellSize)    
    grass = load_image_tile('grass', CellSize)    
    floor = load_image_tile('stone brick', CellSize)
    red_grass = load_image_tile('red grass', CellSize)
    yellow_grass = load_image_tile('yellow grass', CellSize)
    treasure = load_image_tile('treasure', CellSize)
    monster = load_image_tile('monster', CellSize)
    grasses = [yellow_grass, red_grass, grass]

    w.pack(fill=BOTH, expand=1)
    frame.pack(fill=BOTH, expand=1)

    #create an image or button for every tile in the map
    TY = 0
    for row in board:
        TX = 0
        for letter in row:
            if letter == 'O':
                w.create_rectangle(TX*CellSize, TY*CellSize, TX*CellSize+CellSize*.95, TY*CellSize+CellSize*.95, fill="#000000")
            elif letter == 'B':
                button1 = Button(master, text = "T ", font=("Arial", int(CellSize/3), "bold"), command = make_booty)
                button1.configure(width = CellSize * 0.9, height = CellSize * 0.9, activebackground = "#33B5E5", relief=FLAT, image=treasure)
                w.create_window(TX*CellSize, TY*CellSize, anchor=NW, window=button1) #
            elif letter == 'P':
                w.create_image(TX*CellSize, TY*CellSize, image=stonepath, anchor=NW)                
            elif letter == 'R':
                w.create_image(TX*CellSize, TY*CellSize, image=floor, anchor=NW)
            elif letter == 'O':
                w.create_rectangle(TX*CellSize, TY*CellSize, TX*CellSize+CellSize*.95, TY*CellSize+CellSize*.95, fill="#000000")
            elif letter == 'M':
                button1 = Button(master, text = "M ", font=("Arial", int(CellSize/3), "bold"), command = make_monster)
                button1.configure(width = CellSize * 0.90, height = CellSize * 0.90, activebackground = "#33B5E5", relief = FLAT, image=monster)
                w.create_window(TX*CellSize, TY*CellSize, anchor=NW, window=button1)
            else:
                w.create_image(TX*CellSize, TY*CellSize, image=choice(grasses), anchor=NW) 
            TX = TX + 1
        TY = TY + 1

    master.mainloop()

# In[19]:
def create_map(gridsize=31, CellSize=50, EnemyLevel=1, map_seed="random"):
    """Initialize the creation of a new map

    gridsize:   how many tiles across and how many tiles tall
    CellSize:   how big are the tiles in the final map image in pixels
    EnemyLevel: how tough are the bandits in this dungeon
    seed:       random seed of the map"""

    Start_Timer = timeit.default_timer()#for benchmarking the map generation
    if gridsize % 2 == 0: #the map is required to be odd sized
        gridsize = gridsize + 1

    if map_seed == "random":
        map_seed = seed()
    seed(map_seed)

    path = []

    #Generate Room Locations
    pathforroom, RoomLoc = Room_Generate(gridsize)   

    #create path
    path, Startpath, door = create_path(gridsize, pathforroom, RoomLoc)

    #create booty and monster tiles
    booty = booty_tiles(gridsize)
    monsters = monster_tiles(gridsize)

    #convert to tiles
    board = convert_to_tiles(gridsize, Startpath, booty, monsters, path, RoomLoc)

    save_board(board)

    Stop_Timer = timeit.default_timer()

    print (Stop_Timer - Start_Timer, "seconds")
    GenMap(gridsize, board, CellSize, EnemyLevel)

#%%
def load_map(file, CellSize=50, EnemyLevel=1):
    """function in development for loading a previously built map"""

    board = load_board(file)
    for row in board:
        print(" ".join([x.replace("G", " ") for x in row]))
    gridsize = len(board[0])
    GenMap(gridsize, board, CellSize, EnemyLevel)
