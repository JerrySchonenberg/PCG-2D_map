#contains definitions for the generation of content (e.g. biome-colors, relief)

# BIOMES =====================================================================
CHANCE_BIOME = 1       #chance for a different biome (in 2000)
SIZE_X = 4             #horizontal reach of biome = resolution_x/SIZE_X
SIZE_Y = 4             #vertical reach of biome = resolution_y/SIZE_Y

N_BIOMES = 4           #number of biomes, excluding GRASS and WATER
#COLOR DEF: (Hue, Saturation)
GRASS = (133, 100)     #also init value of map
WATER = (206, 100)
SAND = (46, 34)        #for around the water and desert
DIRT = (32, 54)
JUNGLE = (160, 79)
MUSHROOM = (267, 26)   #from Minecraft (mycellium)

#list of all types of pixels, used for making smooth transitions
#each time, take a deepcopy of this
BIOME_LIST = [[GRASS, 0],
              [WATER, 0],
              [SAND, 0],
              [DIRT, 0],
              [JUNGLE, 0],
              [MUSHROOM, 0]]
#=============================================================================

# RELIEF =====================================================================
RELIEF_FACTOR = 18     #how much relief between neighbouring pixels
#=============================================================================

# WATER RELATED ==============================================================
WATER_THRESHOLD = 35   #what is the water-level (max 100)
CHANCE_BEACH = [10, 20, 40, 20, 10] #chance of converting pixel next to water to beach
#=============================================================================