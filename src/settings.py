# Contains definitions for the generation of content (e.g. biome-colors, relief)

# NOTES:
# - For the color definitions, only use integers with a range of 0-360 for the Hue
#   and 0-100 for Saturation and Value
# - For all definitions: use positive integers (with the exception of probabilities: here [0,1], and octave)


#======== BIOMES ========
P_BIOME = 0.001   # Prob. for a different biome
SIZE_X = 4        # Horizontal reach of biome = resolution_x/SIZE_X
SIZE_Y = 4        # Vertical reach of biome   = resolution_y/SIZE_Y

# COLOR DEF: (Hue, Saturation) | here, Value is based on the relief\
# IMPORTANT: The Hue value for each biome must be unique
GRASS = [133, 100]     # Also init value of map
WATER = [206, 100]
DESERT = [46, 34]        # For around the water and desert
SAVANNA = [32, 54]
JUNGLE = [160, 79]
MYCELLIUM = [267, 26]  # From Minecraft (purple ground with mushrooms)

N_BIOMES = 4           # Number of biomes, excluding GRASS and WATER

# List of all types of pixels, used for making smooth transitions..
# ..each time, take a deepcopy of this
# When adding more biomes, include it in this list
BIOME_LIST = [[GRASS, 0],
              [WATER, 0],
              [DESERT, 0],
              [SAVANNA, 0],
              [JUNGLE, 0],
              [MYCELLIUM, 0]]


#======== PLANTS ========
# COLOR DEF: (Hue, Saturation, Value)
PLANT = [100, 100, 40]
BROWN_MUSHROOM = [30, 34, 64]  # Exclusively to MYCELLIUM
RED_MUSHROOM = [359, 77, 100]

P_PLANT = 0.05   # Prob. to generate plant
P_CACTI = 0.3    # Cacti are less frequent in desert, so even lower prob..
                 # .. the prob for cacti is P_CACTI of P_PLANT


#======== VILLAGES ========
P_HOUSE = 0.05      # Prob. of house at a pixel
P_VILLAGE = 0.001   # Prob. of generating village (out of 2000)
P_ROAD = 0.1        # Prob. of road between two villages
SIZE_VILLAGE_X = 4  # Max possible width  (= SIZE_VILLAGE_X*2) of village
SIZE_VILLAGE_Y = 4  # Max possible height (= SIZE_VILLAGE_Y*2) of village

MAX_DIST = 32 # Max distance between two villages to create road between them
              # (Euclidian distance is used)

# COLOR DEF: (Hue, Saturation, Value)
HOUSE = [0, 100, 40]
ROAD = [0, 0, 35]


#======== MISC. ========
OCTAVE = 3.5 # Parameter for Perlin-noise

WATER_THRESHOLD = 37   # Water-level (max=100)
P_BEACH = [0.1, 0.2, 0.4, 0.2, 0.1] # Prob. of converting adding beach to water..
                                    # .. the middle prob. is the closest to the..
                                    # .. water; left is upwards, right is downwards
BEACH = DESERT # Color of the beach, only define Hue and Saturation