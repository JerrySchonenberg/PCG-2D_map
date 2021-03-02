#contains definitions for the generation of content (e.g. biome-colors, relief)

#BIOMES COLORS + CHANCE
CHANCE_BIOME = 1       #chance for a different biome
GRASS = 133            #also init value of map
WATER = 206

N_BIOMES = 4           #number of biomes, excluding GRASS and WATER
SAND = (46, 34)        #for around the water and desert
ICE = (216, 28)
JUNGLE = (160, 79)
MUSHROOM = (267, 26)   #from Minecraft

#RELIEF
RELIEF_FACTOR = 20.0   #how much relief between neighbouring pixels

#WATER RELATED
WATER_THRESHOLD = 40.0 #what is the water-level (max 100)