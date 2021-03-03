import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import math
import typing
import copy

from utility import HSV_to_RGB, euclidian_dist
from settings import *

#initialize blank map
#hue and saturation are set to GRASS, value will be overwritten during relief forming
def init_map(res_X: int, res_Y: int) -> np.ndarray:
  map = np.full((res_Y, res_X, 3), GRASS[0], dtype=int) #contains HSV-values
  for y in range(res_Y):
    for x in range(res_X):
      map[y][x][1] = GRASS[1] #set saturation to 100%
  return map

#return whether the given coordinates are on the map
def on_map(map: np.ndarray, x: int, y: int) -> bool:
  res_X, res_Y = len(map[0]), len(map)
  return 0 <= x < res_X and 0 <= y < res_Y

#increment count of element in list of the pixel's biome
def increment_lst(pixel: np.ndarray, lst: list) -> list:
  for item in lst:
    if item[0][0] == pixel[0]: #biome is based on Hue
      item[1] += 1
      return lst

#return the most frequent biome around (x,y) in a range R
def count_highest_biome(map: np.ndarray, x: int, y: int, R: int) -> typing.Tuple[typing.Tuple[int, int], int]:
  lst = copy.deepcopy(BIOME_LIST)
  for j in range(-R, R+1):
    for i in range(-R, R+1):
      if i == 0 and j == 0:
        continue
      if on_map(map, x+i, y+j):
        count = increment_lst(map[y+j][x+i], lst)
  biome = max(lst, key=lambda x:x[1])
  return biome[0], biome[1]


# RELIEF ======================================================================================
#get the average value of the pixels within a distance of 2
def avg_relief_around(map: np.ndarray, x: int, y: int) -> int:
  val = 0
  count = 0
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


# BIOMES ======================================================================================
#randomly select a biome (excluding GRASS and WATER)
def select_biome() -> typing.Tuple[int, int]:
  R = random.randint(0, N_BIOMES-1)
  if R == 0:
    return SAND
  elif R == 1:
    return SAVANNAH
  elif R == 2:
    return JUNGLE
  elif R == 3:
    return MUSHROOM

#remove the small patches of biomes
def cleanup_biomes(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for y in range(res_Y):
    for x in range(res_X):
      biome, count = count_highest_biome(map, x, y, 2)
      if count >= 8: #too many pixels of a different biome
        map[y][x][:2] = biome
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
          map[y+j][x+i][:2] = biome
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


# WATER =======================================================================================
#count the number of non-water pixels around the given pixel
def count_non_water(map: np.ndarray, x: int, y: int) -> int:
  count = 0
  for j in range(-1, 2):
    for i in range(-1, 2):
      if j == 0 and i == 0: #skip the given pixel itself
        continue
      if on_map(map, x+i, y+j) and not map[y+j][x+i][0] == WATER[0]:
        count += 1
  return count

#remove the small patches (e.g. 1 block) water
def remove_small_patches(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      #count number of surrounding non-water pixels
      if map[y][x][0] == WATER[0] and count_non_water(map, x, y) >= 5:
        biome, _ = count_highest_biome(map, x, y, 1)
        map[y][x][:2] = biome
        map[y][x][2] = WATER_THRESHOLD+1
  return map

#add lakes to map
def add_water(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      if map[y][x][2] <= WATER_THRESHOLD:
        map[y][x][:2] = WATER
  return remove_small_patches(map)


# BEACH =======================================================================================
#create beach around one pixel of water (unless there is water already)
def create_beach(map: np.ndarray, x: int, y: int) -> np.ndarray:
  for j in range(-2, 3):
    for i in range(-2, 3):
      if on_map(map, x+i, y+j) and not map[y+j][x+i][0] == WATER[0]:
        if random.randint(0, 100) <= CHANCE_BEACH[j+2]:
          map[y+j][x+i][:2] = SAND
  return map

#add beaches surrounding the water
def add_beach(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      if map[y][x][0] == WATER[0]:
        map = create_beach(map, x, y)
  return map


# PLANTS ======================================================================================
#add plants to all biomes (trees, cacti)
def add_plants(map: np.ndarray) -> np.ndarray:
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      if random.randint(0, 100) <= CHANCE_PLANT: #generate plant?
        if map[y][x][0] == WATER[0]: #water -> no plant
          continue
        elif map[y][x][0] == MUSHROOM[0]: #special biome -> plant red mushroom
          if random.randint(0,1) == 0: #brown mushroom
            map[y][x] = BROWN_MUSHROOM
          else: #red mushroom
            map[y][x] = RED_MUSHROOM
        else: #plant tree/cactus
          if map[y][x][0] == SAND[0] and random.randint(0, 100) > CHANCE_CACTI: #chance of cacti is lower, than trees
            continue
          map[y][x] = PLANT
  return map


# VILLAGES + ROADS ============================================================================
#get next pixel to continue road with
def get_next_pixel(map: np.ndarray, x: int, y: int, end: list) -> typing.Tuple[int, int]:
  best_dist = sys.maxsize
  next_x, next_y = -1, -1

  for j in range(-1, 2):
    for i in range(-1, 2):
      if on_map(map, x+i, y+j):
          dist = euclidian_dist([x+i, y+j], end)
          if dist < best_dist:
            best_dist = dist
            next_x, next_y = x+i, y+j
  return next_x, next_y

#connect the two villages via a road, don't go over water
def connect(map: np.ndarray, start: list, end: list) -> np.ndarray:
  x, y = start[0], start[1] #starting point
  while not [x, y] == end: #destination not reached yet
    map[y][x] = ROAD
    x, y = get_next_pixel(map, x, y, end)
    if x == -1: #no pixels left, end the road here
      break
  return map

#connect (some of) the villages with roads
def add_roads(map: np.ndarray, loc: list) -> np.ndarray:
  for i in range(len(loc)):
    for j in range(i+1, len(loc)):
      V1, V2 = loc[i], loc[j]
      if random.randint(0, 100) <= CHANCE_ROAD and euclidian_dist(V1, V2) <= MAX_DIST:
        map = connect(map, V1, V2)
  return map

#add houses to the village with origin (x,y)
def add_houses(map: np.ndarray, x: int, y: int) -> np.ndarray:
  for j in range(-SIZE_VILLAGE_Y, SIZE_VILLAGE_Y+1):
    for i in range(-SIZE_VILLAGE_X, SIZE_VILLAGE_X+1):
      if random.randint(0, 100) <= CHANCE_HOUSE: #build house
        if on_map(map, x+i, y+j) and not map[y+j][x+i][0] == WATER[0]:
          map[y+j][x+i] = HOUSE
  return map

#add villages to the map, only if it is on land
def add_villages(map: np.ndarray) -> typing.Tuple[np.ndarray, list]:
  loc = [] #origin of villages, for creating the roads
  res_X, res_Y = len(map[0]), len(map)
  for x in range(res_X):
    for y in range(res_Y):
      #only create villages in grass biomes
      if map[y][x][0] == GRASS[0] and random.randint(0, 2000) <= CHANCE_VILLAGE:
        map = add_houses(map, x, y)
        loc.append([x,y]) #save location of origin
  return map, loc
#============================================================================================== 

#calls all function which will in turn alter the map
def generate_map(res_X: int, res_Y: int) -> np.ndarray:
  map = init_map(res_X, res_Y)

  map = add_relief(map)          #step 1: relief
  map = add_biomes(map)          #step 2: biomes
  map = add_water(map)           #step 3: water
  map = add_beach(map)           #step 4: beaches
  map = add_plants(map)          #step 5: plants
  map, loc = add_villages(map)   #step 6: villages
  map = add_roads(map, loc)      #step 7: roads

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