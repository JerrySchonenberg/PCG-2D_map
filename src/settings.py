# Contains definitions for the generation of content (e.g. biome-colors, relief)

# NOTES:
# - For the color definitions, only use integers with a range of 0-360 for the Hue
#   and 0-100 for Saturation and Value
# - For all definitions: use positive integers (with the exception of probabilities: here [0,1], and octave)


#======== BIOMES ========
# COLOR DEF: (Hue, Saturation) | here, Value is based on the relief
# NOTE: each Hue must be unique in order to identify it
WATER = [206, 100]
BEACH = [62, 55]
GRASS = [133, 100]
FOREST = [135, 50]
DIRT = [26, 77]
MOUNTAIN = [10, 70]
SNOW = [16, 20]

N_BIOMES = 7
WATER_THRESHOLD = 37     # Water-level
BEACH_THRESHOLD = 42     # Beach surrounding the water
GRASS_THRESHOLD = 50     # Grass level
FOREST_THRESHOLD = 75    # Forest level
DIRT_THRESHOLD = 80      # Dirt level
MOUNTAIN_THRESHOLD = 96  # Mountain level
SNOW_THRESHOLD = 100     # Snow/vulcano level


#======== PLANTS ========
# COLOR DEF: (Hue, Saturation, Value)
PLANT = [100, 100, 40]
TRUNK = [12, 50, 36]
P_VEGETATION = 0.05        # Prob. to generate vegetation
P_VEGETATION_DIRT = 0.005  # Prob. on dirt


#======== VILLAGES ========
P_HOUSE = 0.05       # Prob. of house at a pixel
P_VILLAGE = 0.0003   # Prob. of generating village
P_ROAD = 0.04        # Prob. of road between two villages
SIZE_VILLAGE_X = 7   # Max possible width  (= SIZE_VILLAGE_X*2) of village
SIZE_VILLAGE_Y = 7   # Max possible height (= SIZE_VILLAGE_Y*2) of village
SIZE_HOUSE = 2

MAX_DIST = 128 # Max distance between two villages to create road between them
               # (Euclidian distance)

# COLOR DEF: (Hue, Saturation, Value)
HOUSE = [0, 100, 40]
ROAD = [1, 0, 0]
BRIDGE = [17, 64, WATER_THRESHOLD]


#======== PERLIN/FRACTAL NOISE ========
OCTAVE = 5
RES = (3,4)


#======== FLAG ON MOUNTAIN ========
P_FLAG = 0.001            # Prob. of generating a flag
FLAG_RED = [3, 100, 100]
FLAG_BLACK = [2, 100, 0]


#======== VULCANO ========
P_VULCANO = 0.3           # Prob. of generating a vulcano
P_VULCANO_STOP = 0.001    # Prob. to stop the stream of lava
VULCANO_COLOR = [[5, 89], [7, 89], [11, 89]]
VULCANO_STONE = [4, 0, 50]


#======== BOATS ========
P_BOAT = 0.00005          # Prob. of generating a boat
LEN_BOAT = 10
LEN_SIDES = 5
BOAT_BROWN = [27, 77, 28]