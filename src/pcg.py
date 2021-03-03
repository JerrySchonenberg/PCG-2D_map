import numpy as np
import matplotlib.pyplot as plt
import random
import typing
import copy

from utility import HSV_to_RGB
from biomes import *

#initialize blank map
#hue and value are set to 0, while saturation is set to 100
def init_map(res_X: int, res_Y: int) -> np.ndarray:
  map = np.full((res_Y, res_X, 3), GRASS[0], dtype=int) #contains HSV-values
  for y in range(res_Y):
    for x in range(res_X):
      map[y][x][1] = GRASS[1] #set saturation to 100%
  return map

#return whether the given coordinates are on the board
def on_map(map: np.ndarray, x: int, y: int) -> bool:
  res_X, res_Y = len(map[0]), len(map)
  return 0 <= x < res_X and 0 <= y < res_Y

#increment count of element in list of the pixel's biome
def increment_lst(pixel: np.ndarray, lst: list) -> list:
  for item in lst:
    if item[0][0] == pixel[0] and item[0][1] == pixel[1]:
      item[1] += 1
      return lst

#return the most frequent biome around (x,y)
def count_highest_biome(map: np.ndarray, x: int, y: int) -> typing.Tuple[typing.Tuple[int, int], int]:
  lst = copy.deepcopy(BIOME_LIST)
  for j in range(-2, 3):
    for i in range(-2, 3):
      if i == 0 and j == 0:
        continue
      if on_map(map, x+i, y+j):
        count = increment_lst(map[y+j][x+i], lst)
  biome = max(lst, key=lambda x:x[1])
  return biome[0], biome[1]


# RELIEF ======================================================================================
#get the average value of the pixels within a distance of 2
def avg_relief_around(map: np.ndarray, x: int, y: int) -> int:
  val = map[y][x][2]
  count = 1
  for j in range(-2, 3):
    for i in range(-2, 3):
      if on_map(map, x+i, y+j):
        val += map[y+j][x+i][2]
        count += 1
  return int(val/count) 

#add height differences to the map
#the value of every HSV-pixel will represent its height
def add_relief(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)

  #add relief horizontally
  for y in range(res_Y):
    prev = -1
    for x in range(res_X):
      if prev == -1: #first pixel
        map[y][x][2] = random.randint(0, 100)
        prev = map[y][x][2]
      else: #generate within certain range from previous pixel (for smoothness)
        lim_min = max(0, prev-RELIEF_FACTOR)
        lim_max = min(100, prev+RELIEF_FACTOR)
        map[y][x][2] = random.randint(lim_min, lim_max)
        prev = map[y][x][2]

  #vertical relief - take average of two neighbouring pixels
  #make the rows more smooth with each other
  for x in range(res_X):
    for y in range(res_Y):
      if y == 0:
        map[y][x][2] = (map[y][x][2] + map[y+1][x][2])/2
      elif y == res_Y-1:
        map[y][x][2] = (map[y][x][2] + map[y-1][x][2])/2
      else:
        map[y][x][2] = (map[y][x][2] + map[y-1][x][2] + map[y+1][x][2])/3

  #take average of all neighbours within a distance of 2
  #tries to remove the horizontal lines
  for x in range(res_X):
    for y in range(res_Y):
      map[y][x][2] = avg_relief_around(map, x, y)

  return map
#==============================================================================================

# BIOMES ======================================================================================
#randomly select a biome (excluding GRASS and WATER)
def select_biome() -> typing.Tuple[int, int]:
  R = random.randint(0, N_BIOMES-1)
  if R == 0:
    return SAND
  elif R == 1:
    return DIRT
  elif R == 2:
    return JUNGLE
  elif R == 3:
    return MUSHROOM

#remove the small patches of biomes
def cleanup_biomes(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for y in range(res_Y):
    for x in range(res_X):
      biome, count = count_highest_biome(map, x, y)
      if count >= 3:
        map[y][x][0] = biome[0]
        map[y][x][1] = biome[1]
  return map

#create biome with (x,y) as origin
def create_biome(map: np.ndarray, biome: typing.Tuple[int, int], x: int, y: int) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  rad_X, rad_Y = int(res_X/SIZE_X), int(res_Y/SIZE_Y) #radius in which the biome is generated (1/6 of size)
  
  step = int(50/rad_Y)*2 #stepsize to in/decrease the CHANCE
  CHANCE_BIOME = 0
  for j in range(-rad_Y, rad_Y+1):
    mult = 1 if j < 0 else -1
    CHANCE_BIOME += step * mult #CHANCE highest around origin
    for i in range(-rad_X, rad_X+1):
      if on_map(map, x+i, y+j):
        if random.randint(0, 100) <= CHANCE_BIOME:
          map[y+j][x+i][0] = biome[0]
          map[y+j][x+i][1] = biome[1]
  return map

#add various biomes to the map
def add_biomes(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for y in range(res_Y):
    for x in range(res_X):
      #add biome to map
      if random.randint(0, 2000) <= CHANCE_BIOME:
        biome = select_biome()
        map = create_biome(map, biome, x, y)
  return cleanup_biomes(map)
#==============================================================================================

# WATER =======================================================================================
#count the number of non-water pixels around the given pixel
def count_non_water(map: np.ndarray, x: int, y: int) -> int:
  count = 0
  for j in range(-1, 2):
    for i in range(-1, 2):
      if on_map(map, x+i, y+j) and not map[y+j][x+i][0] == WATER[0]:
        count += 1
  return count

#remove the small patches (e.g. 1 block) water
def remove_small_patches(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      if map[y][x][0] == WATER[0] and count_non_water(map, x, y) >= 5:
        biome, _ = count_highest_biome(map, x, y)
        map[y][x][0] = biome[0]
        map[y][x][1] = biome[1]
        map[y][x][2] = WATER_THRESHOLD+1
  return map

#add lakes to map
def add_water(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      if map[y][x][2] <= WATER_THRESHOLD:
        map[y][x][0] = WATER[0]
        map[y][x][1] = WATER[1]
  return remove_small_patches(map)
#==============================================================================================

# BEACH =======================================================================================
#create beach around one pixel of water (unless there is water already)
def create_beach(map: np.ndarray, x: int, y: int) -> np.ndarray:
  for j in range(-2, 3):
    for i in range(-2, 3):
      if on_map(map, x+i, y+j) and not map[y+j][x+i][0] == WATER[0]:
        if random.randint(0, 100) <= CHANCE_BEACH[j+2]:
          map[y+j][x+i][0] = SAND[0]
          map[y+j][x+i][1] = SAND[1]
  return map

#add beaches surrounding the water
def add_beach(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      if map[y][x][0] == WATER[0]:
        map = create_beach(map, x, y)
  return map
#==============================================================================================

#calls all function which will in turn alter the map
def generate_map(res_X: int, res_Y: int) -> np.ndarray:
  map = init_map(res_X, res_Y)

  map = add_relief(map)
  map = add_biomes(map) #TODO: smoothen the hard edges?
  map = add_water(map)  #TODO: connect some lakes with rivers?
  map = add_beach(map)

  #TODO: houses
  #TODO: roads
  return map

#show generated map with pyplot
def show_map(map: np.ndarray) -> None:
  RGB_map = HSV_to_RGB(map)

  plt.imshow(RGB_map)
  plt.axis("off")
  plt.show()

#start of script
if __name__ == "__main__":
  try:
    res_X = 128  #TODO int(input("Width of to be generated map >> "))
    res_Y = 64   #TODO int(input("Height of to be generated map >> "))

    if res_X <= 0 and res_Y <= 0: #only positive (excl. 0) resolutions
      raise ValueError
  except ValueError:
    print("Error: Invalid input.")
    exit(1)

  show_map(generate_map(res_X, res_Y))