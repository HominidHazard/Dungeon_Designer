"""
This character generator module is meant designed to create character from the
D&D realm. It creates python class objects to be used in Dungeon Designer or as
a standalone program.

example:
    lets say we are recreating a lord of the rings D&D scenario and we really
    want a tree ent character.
        Treebeard = Creature()
        print(Treebeard)
            Modifiers
                strength:     -3 (3)
                dexterity:    1 (12)
                constitution:  -1 (7)
                wisdom:       0 (11)
                intelligence: -3 (4)
                charisma:     -1 (7)

            Size: Medium
            Hit Die: 8

        Now this is awesome, but some things don't make much sense. Treebeard
        is not going to be a medium character, he is "Huge!" if not Gargantuan,
        and his strength should be off the charts, not a -3 modifier.

    lets try this again.
        Treebeard = Creature(size="Gargantuan", strength=20)
        print(Treebeard)
            Modifiers
                strength:     5 (20)
                dexterity:    -2 (5)
                constitution:  1 (13)
                wisdom:       0 (11)
                intelligence: 0 (10)
                charisma:     1 (12)

            Size: Gargantuan
            Hit Die: 20

        Now that's more like it. Our Treebeard character is going to be pooning
        some orc scum in no time at all.

    lets say we need to create some man-orc fodder to protect Saruman's tower.
    The HalfOrc class will inherit from creature, and therefor we can add
    some specific strength attributes similar to what we did with Treebeard.

        Grog_the_HalfOrc = HalfOrc(strength=16, dexterity=15)
        print(Grog_the_HalfOrc)
            Modifiers
            strength:     4 (18)
            dexterity:    2 (15)
            constitution:  2 (15)
            wisdom:       2 (14)
            intelligence: 0 (11)
            charisma:     0 (11)

            Size: Medium
            Hit Die: 8

        In this case the program already knows that half-orcs are medium in
        size.
"""

# In[1]:

import random
import numpy as np

def define_stat(result, mean, std_dev=3):
    """function to randomly generate general stats of a creature"""

    if result == "random":
        return int(random.gauss(mean, std_dev))
    else:
        return result

def define_size_hit_die(size, hit_die):
    """function to define to set the size and hit die of a creature"""

    sizes = {"Tiny":4, "Small":6, "Medium":8, "Large":10, "Huge":12, "Gargantuan":20}
    if size == "random":
        size = random.choice(list(sizes.keys()))
    if hit_die == "random" and size in sizes.keys():
        return size, sizes[size]
    elif type(hit_die) == int and hit_die > 0 and size in sizes:
        return size, hit_die
    raise TypeError

def define_hit_points(constitution, hit_die, level):
    """function to set hit points of a creature"""

    return hit_die + int(np.sum([random.randint(1, hit_die) + ((constitution - 10)/2)\
                                 for _ in range(level - 1)]))

#%%
class Creature(object):
    """Create a base creature for use in a D&D game"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1, \
                 hit_points="random", size="random", hit_die="random"):
        """Initialize the creature"""

        level_mod = 10 + level/4
        self.level = level

        self.strength = define_stat(strength, level_mod)
        self.dexterity = define_stat(dexterity, level_mod)
        self.constitution = define_stat(constitution, level_mod)
        self.wisdom = define_stat(wisdom, level_mod)
        self.intelligence = define_stat(intelligence, level_mod)
        self.charisma = define_stat(charisma, level_mod)

        self.size, self.hit_die = define_size_hit_die(size, hit_die)
        if hit_points == "random":
            self.hit_points = define_hit_points(self.constitution, self.hit_die, self.level)
        else:
            self.hit_points = hit_points

    @property
    def modifiers(self):
        """method to return roll modifiers built base stats"""

        strength_mod = int((self.strength - 10) / 2)
        dexterity_mod = int((self.dexterity - 10) / 2)
        constitution_mod = int((self.constitution - 10) / 2)
        wisdom_mod = int((self.wisdom - 10) / 2)
        intelligence_mod = int((self.intelligence - 10) / 2)
        charisma_mod = int((self.charisma - 10) / 2)
        return """Modifiers
        strength:     %s (%s) 
        dexterity:    %s (%s) 
        constitution:  %s (%s) 
        wisdom:       %s (%s) 
        intelligence: %s (%s) 
        charisma:     %s (%s)"""%(strength_mod, self.strength, dexterity_mod,\
        self.dexterity, constitution_mod, self.constitution, wisdom_mod, self.wisdom\
        , intelligence_mod, self.intelligence, charisma_mod, self.charisma)


    @property
    def strength(self):
        """Return creature's base strength"""

        return self.__strength

    @strength.setter
    def strength(self, strength):
        self.__strength = strength

    @property
    def dexterity(self):
        """Return creature's base dexterity"""

        return self.__dexterity

    @dexterity.setter
    def dexterity(self, dexterity):
        self.__dexterity = dexterity

    @property
    def constitution(self):
        """Return creature's base constitutionstitution"""

        return self.__constitution

    @constitution.setter
    def constitution(self, constitution):
        self.__constitution = constitution

    @property
    def wisdom(self):
        """Return creature's base wisdom"""

        return self.__wisdom
    @wisdom.setter
    def wisdom(self, wisdom):
        self.__wisdom = wisdom

    @property
    def intelligence(self):
        """Return creature's base intelligence"""

        return self.__intelligence

    @intelligence.setter
    def intelligence(self, intelligence):
        self.__intelligence = intelligence

    @property
    def charisma(self):
        """Return creature's base charisma"""

        return self.__charisma

    @charisma.setter
    def charisma(self, charisma):
        self.__charisma = charisma

    def __str__(self):
        return self.modifiers + "\n\nSize: " + self.size + "\nHit Die: " + \
    str(self.hit_die)

# In[4]:
class Barbarian(Creature):
    """Create a barbarian character"""

    def __init__(self, strength="random", dexterity="random", constitution="random", \
                 wisdom="random", intelligence="random", charisma="random", level=1, \
                 race="random", size="random"):
        """Barb initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                              intelligence, charisma, level, size)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level)
        if strength == "random":
            self.strength = self.strength + 6
        elif race == "random":
            self.strength = self.strength + 6
        else:
            self.strength = strength

# In[5]:
class Bard(Creature):
    """Create a bard character"""

    def __init__(self, strength="random", dexterity="random", constitution="random", \
                 wisdom="random", intelligence="random", charisma="random", level=1, \
                 race="random"):
        """Bard Initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                              intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level)

        if charisma == "random":
            self.charisma = self.charisma + 6
        else:
            self.charisma = charisma

# In[6]:
class Cleric(Creature):
    """Create a cleric character"""

    def __init__(self, strength="random", dexterity="random", constitution="random", \
                 wisdom="random", intelligence="random", charisma="random", level=1, \
                 race="random"):
        """Cheric Initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                              intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level)
        if wisdom == "random":
            self.wisdom = self.wisdom + 6
        else:
            self.wisdom = wisdom

# In[7]:
class Druid(Creature):
    """Create a druid character"""

    def __init__(self, strength="random", dexterity="random", constitution="random", \
                 wisdom="random", intelligence="random", charisma="random", level=1, \
                 race="random"):
        """Druid Initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                              intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, intelligence,\
                          charisma, level)
        if wisdom == "random":
            self.wisdom = self.wisdom + 6
        else:
            self.wisdom = wisdom

# In[8]:
class Fighter(Creature):
    """Create a fighter character"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1,\
                 race="random"):
        """Fighter initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                              intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level)
        if strength == "random":
            self.strength = self.strength + 4
        else:
            self.strength = strength
        if dexterity == "random":
            self.dexterity = self.dexterity + 4
        else:
            self.dexterity = dexterity

# In[9]:
class Monk(Creature):
    """Create a monk character"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1,\
                 race="random"):
        """Monk Initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom,\
                              intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level)
        if strength == "random":
            self.wisdom = self.wisdom + 4
        else:
            self.wisdom = wisdom
        if dexterity == "random":
            self.dexterity = self.dexterity + 4
        else:
            self.dexterity = dexterity

# In[10]:
class Paladin(Creature):
    """Create a paladin character"""

    def __init__(self, strength="random", dexterity="random", constitution="random", \
                 wisdom="random", intelligence="random", charisma="random", level=1, \
                 race="random"):
        """Initialize paladin character"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                              intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level)
        if strength == "random":
            self.strength = self.strength + 4
        else:
            self.strength = strength
        if charisma == "random":
            self.charisma = self.charisma + 4
        else:
            self.charisma = charisma

# In[11]:
class Ranger(Creature):
    """Create a ranger class"""

    def __init__(self, strength="random", dexterity="random", constitution="random", \
                 wisdom="random", intelligence="random", charisma="random", level=1, \
                 race="random"):
        """Ranger initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                              intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, intelligence, \
                          charisma, level)
        if strength == "random":
            self.wisdom = self.wisdom + 4
        else:
            self.wisdom = wisdom
        if dexterity == "random":
            self.dexterity = self.dexterity + 4
        else:
            self.dexterity = dexterity

# In[12]:
class Rogue(Creature):
    """Create a rogue character"""

    def __init__(self, strength="random", dexterity="random", constitution="random", \
                 wisdom="random", intelligence="random", charisma="random", level=1, \
                 race="random"):
        """Rogue initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                              intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level)
        if dexterity == "random":
            self.dexterity = self.dexterity + 6
        else:
            self.dexterity = dexterity

# In[13]:
class Sorcerer(Creature):
    """Create a sorcerer character"""

    def __init__(self, strength="random", dexterity="random", constitution="random", \
                 wisdom="random", intelligence="random", charisma="random", level=1,\
                 race="random"):
        """Sorcerer initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                              intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level)
        if charisma == "random":
            self.charisma = self.charisma + 6
        else:
            self.charisma = charisma

# In[14]:
class Warlock(Creature):
    """Create a warlock character"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", \
                 intelligence="random", charisma="random", level=1, race="random"):
        """Warlock initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                             intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, intelligence,\
                         charisma, level)
        if charisma == "random":
            self.charisma = self.charisma + 6
        else:
            self.charisma = charisma

# In[15]:
class Wizard(Creature):
    """Create a wizard character"""
    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1,\
                 race="random"):
        """Wizard initialization"""

        if race == "random":
            Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                              intelligence, charisma, level)
        else:
            race.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level)
        if charisma == "random":
            self.intelligence = self.intelligence + 6
        else:
            self.intelligence = intelligence

# In[16]:
class Human(Creature):
    """Create a human character"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level, size="Medium")
        self.strength = self.strength + 1
        self.dexterity = self.dexterity + 1
        self.constitution = self.constitution + 1
        self.wisdom = self.wisdom + 1
        self.intelligence = self.intelligence + 1
        self.charisma = self.charisma + 1


# In[17]:
class HillDwarf(Creature):
    """Create a hill dwarf chracter"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Hill Dwarf Initialize"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom, intelligence,\
                          charisma, level, size="Medium")
        self.constitution = self.constitution + 2
        self.wisdom = self.wisdom + 1

# In[18]:
class MountainDwarf(Creature):
    """Create a mountain dwarf chracter"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Mountain dwarf initialization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom, intelligence,\
                          charisma, level, size="Medium")
        self.constitution = self.constitution + 2
        self.strength = self.strength + 1

# In[19]:
class HighElf(Creature):
    """Create a high elf chracter"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """High Elf initialization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom, intelligence,\
                          charisma, level, size="Medium")
        self.dexterity = self.dexterity + 2
        self.intelligence = self.intelligence + 1

# In[20]:
class WoodElf(Creature):
    """Create a wood elf character"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Wood Elf Initialization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom, intelligence,\
                          charisma, level, size="Medium")
        self.dexterity = self.dexterity + 2
        self.wisdom = self.wisdom + 1

# In[21]:
class ForestGnome(Creature):
    """Create a forest gnome chracter"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Forest Gnome initilization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom, intelligence,\
                          charisma, level, size="Small")
        self.dexterity = self.dexterity + 1
        self.intelligence = self.intelligence + 2

# In[22]:
class RockGnome(Creature):
    """Create a rock gnome chracter"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Rock Gnome initilization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom,\
                          intelligence, charisma, level, size="Small")
        self.dexterity = self.dexterity + 1
        self.intelligence = self.intelligence + 2

# In[23]:
class LightfootHalfling(Creature):
    """Create a lightfoot halfling"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Lightfoot Halfling initialization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom, intelligence,\
                          charisma, level, size="Small")
        self.charisma = self.charisma + 1
        self.dexterity = self.dexterity + 2

# In[24]:
class StoutHalfling(Creature):
    """Create a stout halfling"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Stout Halfling initilization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom, \
                          intelligence, charisma, level, size="Small")
        self.constitution = self.constitution + 1
        self.dexterity = self.dexterity + 2

# In[25]:
class Dragonborn(Creature):
    """Create a dragonborn character"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Dragonborn initilization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom,\
                          intelligence, charisma, level, size="Medium")
        self.charisma = self.charisma + 1
        self.strength = self.strength + 2

# In[26]:
class HalfElf(Creature):
    """Create a half elf character"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Half Elf initialization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom,\
                          intelligence, charisma, level, size="Medium")
        self.charisma = self.charisma + 2

# In[27]:
class HalfOrc(Creature):
    """Create a half orc character"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Half Orc initilization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom,\
                          intelligence, charisma, level, size="Medium")
        self.strength = self.strength + 2
        self.constitution = self.constitution + 1

# In[28]:
class InfernalTiefling(Creature):
    """Create an Infernal Tiefling character"""

    def __init__(self, strength="random", dexterity="random", constitution="random",\
                 wisdom="random", intelligence="random", charisma="random", level=1):
        """Infernal Tiefling initialization"""

        Creature.__init__(self, strength, dexterity, constitution, wisdom,\
                          intelligence, charisma, level, size="Medium")
        self.charisma = self.charisma + 2
        self.intelligence = self.intelligence + 1
