# Contains definitions for the generation of content (e.g. biome-colors, relief)

# NOTES:
# - For the color definitions, only use integers with a range of 0-360 for the Hue
#   and 0-100 for Saturation and Value
# - The chance for something is out of 100, unless specifically told otherwise
# - For all definitions: use positive integers


#======== BIOMES ========
CHANCE_BIOME = 1       # Chance for a different biome (out of 2000)
SIZE_X = 4             # Horizontal reach of biome = resolution_x/SIZE_X
SIZE_Y = 4             # Vertical reach of biome   = resolution_y/SIZE_Y

# COLOR DEF: (Hue, Saturation) | here, Value is based on the relief\
# IMPORTANT: The Hue value for each biome must be unique
GRASS = [133, 100]     # Also init value of map
WATER = [206, 100]
SAND = [46, 34]        # For around the water and desert
SAVANNAH = [32, 54]
JUNGLE = [160, 79]
MYCELLIUM = [267, 26]  # From Minecraft (purple ground with mushrooms)

N_BIOMES = 4           # Number of biomes, excluding GRASS and WATER

# List of all types of pixels, used for making smooth transitions..
# ..each time, take a deepcopy of this
# When adding more biomes, include it in this list
BIOME_LIST = [[GRASS, 0],
              [WATER, 0],
              [SAND, 0],
              [SAVANNAH, 0],
              [JUNGLE, 0],
              [MYCELLIUM, 0]]


#======== PLANTS ========
# COLOR DEF: (Hue, Saturation, Value)
PLANT = [100, 100, 40]
BROWN_MUSHROOM = [30, 34, 64]
RED_MUSHROOM = [359, 77, 100]

CHANCE_PLANT = 5   # Chance to generate plant
CHANCE_CACTI = 30  # Cacti are less frequent in desert, so even lower chance..
                   # .. the chance for cacti is 30% of CHANCE_PLANT


#======== VILLAGES ========
CHANCE_HOUSE = 8    # Chance of house at a pixel
CHANCE_VILLAGE = 2  # Chance of generating village (out of 2000)
CHANCE_ROAD = 50    # Chance of road between two villages
SIZE_VILLAGE_X = 4  # Max possible width  (= SIZE_VILLAGE_X*2) of village
SIZE_VILLAGE_Y = 4  # Max possible height (= SIZE_VILLAGE_Y*2) of village

MAX_DIST = 32 # Max distance between two villages to create road between them
              # (Euclidian distance is used)

# COLOR DEF: (Hue, Saturation, Value)
HOUSE = [0, 100, 40]
ROAD = [0, 0, 35]


#======== MISC. ========
RELIEF_FACTOR = 18 # How much relief between neighbouring pixels is possible

WATER_THRESHOLD = 37   # Water-level (max=100)
CHANCE_BEACH = [10, 20, 40, 20, 10] # Chance of converting adding beach to water..
                                    # .. the middle chance is the closest to the..
                                    # .. water; left is upwards, right is downwards
BEACH = SAND # Color of the beach