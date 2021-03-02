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
  map = np.full((res_Y, res_X, 3), GRASS, dtype=float) #contains HSV-values
  for y in range(res_Y):
    for x in range(res_X):
      map[y][x][1] = 100.0 #set saturation to 100%
  return map

#return whether the given coordinates are on the board
def on_map(map: np.ndarray, x: int, y: int) -> bool:
  res_X, res_Y = len(map[0]), len(map)
  return 0 <= x < res_X and 0 <= y < res_Y


# RELIEF ======================================================================================
#get the average value of the pixels within a distance of 2
def avg_relief_around(map: np.ndarray, x: int, y: int) -> float:
  val = map[y][x][2]
  count = 1
  for j in range(-2, 3):
    for i in range(-2, 3):
      if on_map(map, x+i, y+j):
        val += map[y+j][x+i][2]
        count += 1
  return val/count 

#add height differences to the map
#the value of every HSV-pixel will represent its height
def add_relief(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)

  #add relief horizontally
  for y in range(res_Y):
    prev = -1
    for x in range(res_X):
      if prev == -1: #first pixel
        map[y][x][2] = random.uniform(0.0, 100.0)
        prev = map[y][x][2]
      else: #generate within certain range from previous pixel (for smoothness)
        lim_min = max(0.0, prev-RELIEF_FACTOR)
        lim_max = min(100, prev+RELIEF_FACTOR)
        map[y][x][2] = random.uniform(lim_min, lim_max)
        prev = map[y][x][2]

  #vertical relief - take average of two neighbouring pixels
  for x in range(res_X):
    for y in range(res_Y):
      if y == 0:
        map[y][x][2] = (map[y][x][2] + map[y+1][x][2])/2
      elif y == res_Y-1:
        map[y][x][2] = (map[y][x][2] + map[y-1][x][2])/2
      else:
        map[y][x][2] = (map[y][x][2] + map[y-1][x][2] + map[y+1][x][2])/3

  #take average of all neighbours within a distance of 2
  for x in range(res_X):
    for y in range(res_Y):
      map[y][x][2] = avg_relief_around(map, x, y)

  return map

#==============================================================================================

# BIOMES ======================================================================================
#randomly select a biome (excluding GRASS and WATER)
def select_biome() -> float:
  R = random.randint(0, N_BIOMES-1)
  if R == 0:
    return SAND
  elif R == 1:
    return ICE
  elif R == 2:
    return JUNGLE
  elif R == 3:
    return MUSHROOM

#add various biomes to the map
def add_biomes(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for y in range(res_Y):
    for x in range(res_X):
      #add biome to map
      if random.randint(0, 2000) <= CHANCE_BIOME:
        biome = select_biome()
        #TODO
  return map

#==============================================================================================

# WATER =======================================================================================
#count the number of non-water pixels around the given pixel
def count_non_water(map: np.ndarray, x: int, y: int) -> int:
  count = 0
  for j in range(-1, 2):
    for i in range(-1, 2):
      if on_map(map, x+i, y+j) and not map[y+j][x+i][0] == WATER:
        count += 1
  return count

#remove the small patches (e.g. 1 block) water
def remove_small_patches(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      if map[y][x][0] == WATER and count_non_water(map, x, y) >= 5:
        map[y][x][0] = GRASS
        map[y][x][2] = WATER_THRESHOLD+1
  return map

#add lakes to map
def add_water(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      if map[y][x][2] <= WATER_THRESHOLD:
        map[y][x][0] = WATER
  return remove_small_patches(map)

#==============================================================================================

# BEACH =======================================================================================
#create beach around one pixel of water (unless there is water already)
def create_beach(map: np.ndarray, x: int, y: int) -> np.ndarray:
  chance_beach = [10, 20, 40, 20, 10] #chance of converting pixel to beach
  for j in range(-2, 3):
    for i in range(-2, 3):
      if on_map(map, x+i, y+j) and not map[y+j][x+i][0] == WATER:
        if random.randint(0, 100) <= chance_beach[j+2]:
          map[y+j][x+i][0] = SAND[0]
          map[y+j][x+i][1] = SAND[1]
  return map

#add beaches surrounding the water
def add_beach(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      if map[y][x][0] == WATER:
        map = create_beach(map, x, y)
  return map
#==============================================================================================

#calls all function which will in turn alter the map
def generate_map(res_X: int, res_Y: int) -> np.ndarray:
  map = init_map(res_X, res_Y)

  map = add_relief(map)
  map = add_biomes(map)
  map = add_water(map) #TODO: connect some lakes with rivers?
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