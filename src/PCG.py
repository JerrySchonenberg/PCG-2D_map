import numpy as np
import random
import copy
import typing

from perlin2d import generate_perlin_noise_2d
from settings import *
from utility import euclidian_dist

# Definition of the map; contains all procedure, ordered by when they are called
class Map:
  def __init__(self, res_X: int, res_Y: int, seed: int = None) -> None:
    self.res_X = res_X  # Resolution of map
    self.res_Y = res_Y
    self.map = np.full((res_Y, res_X, 3), GRASS[0], dtype=int) # Contains the HSV-values
    random.seed(seed)
   
    # Initialise the map full with GRASS
    # Value will be overwritten, when relief is generated
    for y in range(res_Y):
      for x in range(res_X):
        self.map[y][x][1] = GRASS[1] # Set Saturation to 100%
  
  # Return whether the given coordinates are on the map
  def on_map(self, x: int, y: int) -> bool:
    return 0 <= x < self.res_X and 0 <= y < self.res_Y
  
  # Start generating the map via the defined procedures
  def generate(self) -> None:
    print("Generating relief ...")
    self.__add_relief()
    print("Generating biomes ...")
    self.__add_biomes()
    print("Generating water ...")
    self.__add_water()
    print("Generating beaches ...")
    self.__add_beach()
    print("Generating vegetation ...")
    self.__add_plants()
    print("Generating villages ...")
    self.__add_villages()
  
  # Return the generated map
  def get_map(self) -> np.ndarray:
    return self.map


  # Private methods of class

  #======== RELIEF GENERATION PROCEDURES ========
  # Here, the Value-component is used to represent the height of one pixel
  # Perlin noise is used to generate the relief
  def __add_relief(self) -> None:
    # Generate Perlin Noise
    noise = generate_perlin_noise_2d((self.res_Y, self.res_X), (4, 4))

    # Normalize to [0, 1], then multiply with 100 for Value (of HSV)
    noise = (noise - noise.min()) / (noise.max()-noise.min()) * 100

    # Copy the noise to the map
    for y in range(self.res_Y):
      for x in range(self.res_X):
        self.map[y][x][2] = noise[y][x]
    

  #======== BIOME GENERATION PROCEDURES ========
  # Here, the Hue- and Saturation-components are altered to represent biomes
  def __add_biomes(self) -> None:
    for y in range(0, self.res_Y, 8):
      for x in range(0, self.res_X, 8):
        # Add biome to map
        if random.uniform(0,1) <= P_BIOME:
          self.__create_biome(self.__select_biome(), x, y)
    self.__cleanup_biomes() # Remove small patches of biomes
  
  # Increment counter of element in list corresponding to the pixel's biome
  def __update_counters(self, pixel: np.ndarray, lst: list) -> list:
    for item in lst:
      if item[0][0] == pixel[0]: # Every biome's Hue is unique
        item[1] += 1
        return lst

  # Return the most frequent biome around origin (x,y) within a radius of R
  def __count_highest_biome(self, x: int, y: int, R: int) -> typing.Tuple[typing.Tuple[int, int], int]:
    count_biomes = copy.deepcopy(BIOME_LIST)
    for j in range(-R, R+1):
      for i in range(-R, R+1):
        if i == 0 and j == 0: # Don't count the origin
          continue
        if self.on_map(x+i, y+j):
          count_biomes = self.__update_counters(self.map[y+j][x+i], count_biomes)
    return max(count_biomes, key=lambda x:x[1]) # Return biome with highest counter

  # Randomly selects a biome (excluding GRASS and WATER)
  def __select_biome(self) -> typing.Tuple[int, int]:
    R = random.randint(0, N_BIOMES-1)
    if R == 0   : return DESERT
    elif R == 1 : return SAVANNA
    elif R == 2 : return JUNGLE
    elif R == 3 : return MYCELLIUM
  
  # Create biome with (x,y) as origin
  def __create_biome(self, biome: typing.Tuple[int, int], x: int, y: int) -> None:
    # Initialize radius in which the biome is generated
    rad_X, rad_Y = int(self.res_X/SIZE_X), int(self.res_Y/SIZE_Y)

    step = int(50/rad_Y)*2 # Stepsize to in-/decrease the chance
    P = 0
    for j in range(-rad_Y, rad_Y+1):
      mult = 1 if j < 0 else -1 # Increase or decrease chance?
      P += step * mult          # Highest around origin
      for i in range(-rad_X, rad_X+1):
        if self.on_map(x+i, y+j) and random.uniform(0,1) <= P:
          self.map[y+j][x+i][:2] = biome
  
  # Remove the small patches of biomes; not realistic
  def __cleanup_biomes(self) -> None:
    for y in range(self.res_Y):
      for x in range(self.res_X):
        biome, count = self.__count_highest_biome(x, y, 2)
        if count >= 8: # Too many pixels of a different biome -> small patch found
          self.map[y][x][:2] = biome


  #======== WATER GENERATION PROCEDURES ========
  # Here, the biome of every pixel with VALUE <= WATER_THRESHOLD is changed to WATER
  def __add_water(self) -> None:
    for y in range(self.res_Y):
      for x in range(self.res_X):
        if self.map[y][x][2] <= WATER_THRESHOLD: # Below threshold, becomes WATER
          self.map[y][x][:2] = WATER
    self.__remove_small_patches()
  
  # Remove the small patches (e.g. 1 pixel) of water
  def __remove_small_patches(self) -> None:
    for y in range(self.res_Y):
      for x in range(self.res_X):
        # Count number of surrounding non-water pixels
        if self.map[y][x][0] == WATER[0] and self.__count_non_water(x, y) >= 5:
          biome, _ = self.__count_highest_biome(x, y, 1)
          self.map[y][x][:2] = biome            # Change biome
          self.map[y][x][2] = WATER_THRESHOLD+1 # Let pixel be just above threshold
  
  # Count number of non-water pixels around the origin
  def __count_non_water(self, x: int, y: int) -> int:
    count = 0
    for j in range(-1, 2):
      for i in range(-1, 2):
        if i == 0 and j == 0: # Skip the origin
          continue
        if self.on_map(x+i, y+j) and not self.map[y+j][x+i][0] == WATER[0]:
          count += 1
    return count         


  #======== BEACH GENERATION PROCEDURES ========
  # Add beaches surrounding the water
  # Probability of a pixel becoming a beach is dependent on the distance to the water..
  # .. the further away, the lower the probability
  def __add_beach(self) -> None:
    for y in range(self.res_Y):
      for x in range(self.res_X):
        if self.map[y][x][0] == WATER[0]: # Pixel with water found, add some beaches
          self.__create_beach(x, y)
  
  # Create beach around origin (x,y), but leave the water intact
  def __create_beach(self, x: int, y: int) -> None:
    for j in range(-2, 3):
      for i in range(-2, 3):
        if self.on_map(x+i, y+j) and not self.map[y+j][x+i][0] == WATER[0]:
          if random.uniform(0,1) <= P_BEACH[j+2]: # Change pixel to beach
            self.map[y+j][x+i][:2] = BEACH


  #======== PLANT GENERATION PROCEDURES ========
  # Add plants to all biomes (e.g. trees, bushes, cacti)
  def __add_plants(self) -> None:
    for y in range(self.res_Y):
      for x in range(self.res_X):
        if random.uniform(0,1) <= P_PLANT: # Generate a new plant?
          # Determine type of plant, based on the biome
          if self.map[y][x][0] == WATER[0]:  # Water? -> no plant
            continue
          elif self.map[y][x][0] == MYCELLIUM[0]: # Special biome -> plant brown/red mushrooms
            self.map[y][x] = BROWN_MUSHROOM if random.randint(0,1) == 0 else RED_MUSHROOM
          else: # Plant trees/bushes/cacti
            # Chance of cacti is lower than trees/bushes
            if self.map[y][x][0] == DESERT[0] and random.uniform(0,1) > P_CACTI:
              continue
            self.map[y][x] = PLANT
  

  #======== VILLAGE + ROAD GENERATION PROCEDURES ========
  # Add villages and roads to the map, but only if it is on GRASS
  def __add_villages(self) -> None:
    loc = []  # Origin of the villages, for creating the roads
    for y in range(0, self.res_Y, 8):
      for x in range(0, self.res_X, 8):
        # Only create villages in GRASS biome
        if self.map[y][x][0] == GRASS[0] and random.uniform(0,1) <= P_VILLAGE:
          self.__add_houses(x, y)
          loc.append([x,y])
    self.__add_roads(loc) # Connect the villages via roads
  
  # Add houses to the village with origin (x,y)
  def __add_houses(self, x: int, y: int) -> None:
    for j in range(-SIZE_VILLAGE_Y, SIZE_VILLAGE_Y+1):
      for i in range(-SIZE_VILLAGE_X, SIZE_VILLAGE_X+1):
        if random.uniform(0,1) <= P_HOUSE: # Build house
          if self.on_map(x+i, y+j) and not self.map[y+j][x+i][0] == WATER[0]:
            self.map[y+j][x+i] = HOUSE
  
  # Randomly select which villages are connected with each other
  def __add_roads(self, loc: list) -> None:
    for j in range(len(loc)):
      for i in range(j+1, len(loc)):
        V1, V2 = loc[i], loc[j]
        if random.uniform(0,1) <= P_ROAD and euclidian_dist(V1, V2) <= MAX_DIST:
          self.__connect(V1, V2)  # Connect villages V1 and V2 with road

  # Connect the two given villages
  def __connect(self, start: list, end: list) -> None:
    x, y = start[0], start[1] # Starting point
    while not [x, y] == end:  # Destination not reached yet
      self.map[y][x] = ROAD
      x, y = self.__get_next_pixel(x, y, end)
      if x == -1:  # No pixels left, unable to create road. Road ends here
        break
  
  # Get the next pixel to continue road with, this pixel has shortest distance to end
  def __get_next_pixel(self, x: int, y: int, end: list) -> typing.Tuple[int, int]:
    best_dist = MAX_DIST
    next_x, next_y = -1, -1
    for j in range(-1, 2):
      for i in range(-1, 2):
        if i == 0 and j == 0:  # Skip current pixel
          continue
        if self.on_map(x+i, y+j):
          dist = euclidian_dist([x+i, y+j], end)
          if dist < best_dist:
            best_dist = dist
            next_x, next_y = x+i, y+j
    return next_x, next_y